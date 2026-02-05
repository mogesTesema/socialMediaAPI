from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    BackgroundTasks,
    Response,
    status,
    Depends,
)
from foodapp.models.user import (
    UserIn,
    Token,
    User,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from foodapp.db.database import (
    user_table,
    db_connection,
    refreshtoken_table,
    password_reset_table,
)
from foodapp.integrations.email.verify_email import (
    send_verfication_email,
    send_password_reset_email,
)
from foodapp.security.user_security import (
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_subject_token_type,
    create_confirm_token,
    create_refresh_token,
    refresh_token_rotation,
    verify_password,
    create_password_reset_token,
    store_password_reset_token,
    validate_password_reset_token,
)
from foodapp.core.config import config
from urllib.parse import urlparse

import logging
import uuid
from typing import Annotated

logger = logging.getLogger(__name__)

router = APIRouter()
database = db_connection()

@router.post("/register", status_code=201)
async def register(
    user: UserIn, background_task: BackgroundTasks, request: Request, response: Response
):
    email = user.email
    user_exist = await get_user(email)
    logger.debug("registering user")
    if user_exist:
        logger.debug("user already exist in database")
        raise HTTPException(
            status_code=409,
            detail="user already exist,conflict with exsisting info",
        )
    else:
        hashed_password = await get_password_hash(user.password)
        user_query = user_table.insert().values(email=email, password=hashed_password)
        logger.debug(user_query)

        try:
            await database.execute(user_query)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"database crash:{e}")
    access_token = create_access_token(email)
    confirm_token = create_confirm_token(email)
    refresh_id = str(uuid.uuid4())
    refresh_token = create_refresh_token(email=email, jti=refresh_id)
    hashed_refresh_token = await get_password_hash(refresh_token)

    refresh_query = refreshtoken_table.insert().values(
        jti=refresh_id, user_email=user.email, hashed_token=hashed_refresh_token
    )
    try:
        await database.execute(refresh_query)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server Error,unable to sotre refresh token to databse:{e}",
        )

    verify_url = request.url_for("confirm_email", token=confirm_token)
    background_task.add_task(
        send_verfication_email,
        to=user.email,
        token=confirm_token,
        verify_url=verify_url,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=60 * 60 * 24 * 30,
        path="/auth/refresh",
        secure=True,
        httponly=True,
        samesite="strict",
    )

    return {
        "status": "user registered. please confirm your email",
        "access token:": access_token,
    }


@router.post("/login")
async def login(user: UserIn, response: Response):
    user_exist = await get_user(user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user don't exist,incorrect passowrd or email",
        )
    if not await verify_password(user.password, user_exist.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="incorrect password or email"
        )
    access_token = create_access_token(user_exist.email)
    # confirm_token = create_confirm_token(email)
    refresh_id = str(uuid.uuid4())
    refresh_token = create_refresh_token(email=user_exist.email, jti=refresh_id)
    hashed_refresh_token = await get_password_hash(refresh_token)

    refresh_query = (
        refreshtoken_table.update()
        .values(jti=refresh_id, hashed_token=hashed_refresh_token)
        .where(refreshtoken_table.c.user_email == user_exist.email)
    )
    try:
        await database.execute(refresh_query)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server Error,unable to sotre refresh token to databse:{e}",
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=60 * 60 * 24 * 30,
        path="/auth/refresh",
        secure=True,
        httponly=True,
        samesite="strict",
    )

    return {"status": "seccussfully login", "access token": access_token}


@router.post("/token")
async def get_profile(user: UserIn):
    user = await authenticate_user(email=user.email, password=user.password)
    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/myemail")
async def get_email(token: Token):
    user = await get_current_user(token.token)

    return user


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_token_type(token, "confirmation")

    confirm_query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )
    logger.debug(confirm_query)

    await database.execute(confirm_query)

    return {"detail": "user has been confirmed"}


@router.post("/auth/refresh")
async def refresh_token(
    reqeust: Request, response: Response, refresh_token: str | None = None
):
    refresh_token = reqeust.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="there is no refresh token, please login agian to get new one",
        )

    refresh_token_detail = await refresh_token_rotation(refresh_token)  # noqa
    new_access_token = refresh_token_detail["new_access_token"]
    new_refresh_token = refresh_token_detail["new_refresh_token"]

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        max_age=60 * 60 * 24 * 30,
        path="/auth/refresh",
        secure=True,
        httponly=True,
        samesite="strict",
    )

    return {"status": "secessfully refreshed", "access token": new_access_token}


@router.delete("/delete")
async def delete_account(current_user: Annotated[User, Depends(get_current_user)]):
    # first delete user's refresh token
    logger.debug(f"DELETTING user:{current_user}")
    if not current_user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="please confirm your email before trying to delete account",
        )
    delete_refresh_query = refreshtoken_table.delete().where(
        refreshtoken_table.c.user_email == current_user.email
    )
    logger.debug(delete_refresh_query)

    try:
        await database.execute(delete_refresh_query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to delete user's refresh token:{e}",
        )

    delete_user_query = user_table.delete().where(
        user_table.c.email == current_user.email
    )

    logger.debug(delete_user_query)

    try:
        await database.execute(delete_user_query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to delete user:{e}",
        )

    return {"status": "seccussfully deleted"}


@router.post("/password/forgot")
async def forgot_password(
    payload: PasswordResetRequest,
    background_task: BackgroundTasks,
    request: Request,
):
    user = await get_user(payload.email)
    if not user:
        return {"status": "if the email exists, a reset link has been sent"}

    reset_id = str(uuid.uuid4())
    reset_token = create_password_reset_token(email=payload.email, jti=reset_id)
    await store_password_reset_token(payload.email, reset_token, reset_id)

    frontend_base = config.FRONTEND_BASE_URL
    if not frontend_base:
        allowlist = [
            origin.strip()
            for origin in (config.FRONTEND_BASE_URLS or "").split(",")
            if origin.strip()
        ]
        requested_base = request.headers.get("X-Frontend-Base-Url")
        if requested_base and allowlist:
            parsed = urlparse(requested_base)
            normalized = f"{parsed.scheme}://{parsed.netloc}"
            if normalized in allowlist:
                frontend_base = normalized

    frontend_base = frontend_base or "http://localhost:5173"
    reset_url = f"{frontend_base.rstrip('/')}/auth/reset?token={reset_token}"
    background_task.add_task(
        send_password_reset_email,
        to=payload.email,
        reset_url=reset_url,
    )

    return {"status": "if the email exists, a reset link has been sent"}


@router.post("/password/reset")
async def reset_password(payload: PasswordResetConfirm):
    email, reset_id = await validate_password_reset_token(payload.token)

    hashed_password = await get_password_hash(payload.new_password)
    update_password_query = (
        user_table.update().where(user_table.c.email == email).values(
            password=hashed_password
        )
    )
    await database.execute(update_password_query)

    delete_reset_query = password_reset_table.delete().where(
        password_reset_table.c.jti == reset_id,
        password_reset_table.c.user_email == email,
    )
    await database.execute(delete_reset_query)

    delete_refresh_query = refreshtoken_table.delete().where(
        refreshtoken_table.c.user_email == email
    )
    await database.execute(delete_refresh_query)

    return {"status": "password reset successfully"}
