from fastapi import APIRouter, HTTPException, Request
from storeapi.models.user import UserIn, Token
from storeapi.database import user_table, database
from storeapi.email.verify_email import send_verfication_email
from storeapi.utilits.formatted_printer import print_better
from storeapi.security.user_security import (
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_subject_token_type,
    create_confirm_token,
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn, request: Request):
    email = user.email
    user_exist = await get_user(email)
    if user_exist:
        raise HTTPException(
            status_code=409, detail="user already exist,conflict with exsisting info"
        )

    hashed_password = await get_password_hash(user.password)
    user_query = user_table.insert().values(email=email, password=hashed_password)
    try:
        await database.execute(user_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database crash:{e}")
    logger.debug(user_query)
    access_token = create_access_token(email)
    confirm_token = create_confirm_token(user.email)
    verify_url = request.url_for("confirm_email", token=confirm_token)
    sending_email = await send_verfication_email(
        to=user.email, token=confirm_token, verify_url=verify_url
    )
    print_better(obj="email confirmation response", message=sending_email)
    logger.debug(sending_email)
    return {
        "status": "user registered. please confirm your email",
        "token:": access_token,
    }


@router.get("/token")
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
