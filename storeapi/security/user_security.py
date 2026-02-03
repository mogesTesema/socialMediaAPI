import sqlalchemy
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from storeapi.database import user_table, db_connection, refreshtoken_table
from storeapi.config import get_secrets
import logging
import jwt
from jwt import ExpiredSignatureError, PyJWTError
import datetime
from typing import Annotated, Literal

logger = logging.getLogger(__name__)
secret_keys = get_secrets()
database = db_connection()

SECRET_KEY = secret_keys.SECRET_KEY
ALGORITHM = secret_keys.ALGORITHM
REFRESH_TOKEN_SECRET_KEY = secret_keys.REFRESH_TOKEN_SECRET_KEY
REFRESH_TOKEN_ALGORITHM = secret_keys.REFRESH_TOKEN_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hasher = PasswordHasher()


def create_credentials_exception(
    detail: str, status_code=status.HTTP_401_UNAUTHORIZED
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=detail,
    )


def access_token_expire_minutes() -> int:
    return 30


def confirm_token_expire_minutes() -> int:
    return 15


def refresh_token_expire_days() -> int:
    return 30


def create_access_token(email: str):
    logger.debug("creating access token", extra={"email": email})
    expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        minutes=access_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(payload=jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_confirm_token(email: str):
    logger.debug(f"create confirmation token for user:{email}")
    confirm_expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        minutes=confirm_token_expire_minutes()
    )

    jwt_confirm_data = {"sub": email, "exp": confirm_expire, "type": "confirmation"}

    encoded_confirm_token = jwt.encode(
        payload=jwt_confirm_data, key=SECRET_KEY, algorithm=ALGORITHM
    )

    return encoded_confirm_token


def create_refresh_token(email: str, jti: str):
    expire_date = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        days=refresh_token_expire_days()
    )
    refresh_payload = {"sub": email, "jti": jti, "exp": expire_date, "type": "refresh"}

    refresh_token = jwt.encode(
        payload=refresh_payload,
        key=REFRESH_TOKEN_SECRET_KEY,
        algorithm=REFRESH_TOKEN_ALGORITHM,
    )
    return refresh_token


def validate_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=REFRESH_TOKEN_SECRET_KEY,
            algorithms=[REFRESH_TOKEN_ALGORITHM],
        )
    except ExpiredSignatureError as e:
        raise create_credentials_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token expired",
        ) from e
    except PyJWTError as e:
        raise create_credentials_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid refresh token",
        ) from e

    if payload.get("type") != "refresh":
        raise create_credentials_exception(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="wrong refresh token type",
        )
    return payload


def get_subject_token_type(token: str, type: Literal["access", "confirmation"]) -> str:
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except PyJWTError as e:
        raise create_credentials_exception(detail="invalid token") from e

    email = payload.get("sub")
    token_type = payload.get("type")
    if token_type != type or token_type is None:
        raise create_credentials_exception(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"token has incorrect type, expected: {type}",
        )
    if not email:
        raise create_credentials_exception(detail="Token is missing 'sub' field")

    return email


def decrypt_access_token(access_token: str):
    return jwt.decode(access_token, key=SECRET_KEY, algorithms=[ALGORITHM])


async def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except Exception:
        return False


async def get_user(email: str):
    user_query = sqlalchemy.select(user_table).where(user_table.c.email == email)
    user = await database.fetch_one(user_query)
    logger.debug(user_query)

    return user


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticaling user", extra={"email": email})
    user = await get_user(email=email)

    if not user:
        raise create_credentials_exception(detail="invalid email or password")
    if not await verify_password(
        plain_password=password, hashed_password=user.password
    ):
        raise create_credentials_exception("invalid email or password")

    if not user.confirmed:
        raise create_credentials_exception(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="email is not confirmed"
        )

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.debug("Getting Current user with access token")
    email = get_subject_token_type(token=token, type="access")
    user = await get_user(email=email)

    if not user:
        raise create_credentials_exception(
            detail="user not found for this token",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return user


async def is_confirmed(email: str) -> bool:
    user = await get_user(email)
    return user.confirmed == True #noqa


async def refresh_token_rotation(refresh_token: str):
    logger.debug("token rotation excutting")
    try:
        refresh_payload = jwt.decode(
            jwt=refresh_token,
            key=REFRESH_TOKEN_SECRET_KEY,
            algorithms=[REFRESH_TOKEN_ALGORITHM],
        )

    except ExpiredSignatureError as e:
        raise create_credentials_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"your refresh token has been expired please login using password and email:{e}",
        )
    except PyJWTError:
        raise create_credentials_exception(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong refresh token"
        )

    type = refresh_payload["type"]
    if type != "refresh":
        raise create_credentials_exception(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"wrong refresh token type:{type}",
        )
    refresh_id = refresh_payload["jti"]

    jti_query = sqlalchemy.select(refreshtoken_table).where(
        refreshtoken_table.c.jti == refresh_id
    )
    logger.debug(jti_query)

    token_content = await database.fetch_one(jti_query)
    if not token_content:
        raise create_credentials_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="refresh token no longer in database,please login again",
        )
    try:
        hashed_token = token_content.hashed_token
        user_email = token_content.user_email
    except Exception as e:
        raise create_credentials_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"refreshtoken_table object error: {e}",
        )

    if not await verify_password(refresh_token, hashed_token):
        raise create_credentials_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="wrong refresh token,please use correct token or login with your email and password",
        )

    new_access_token = create_access_token(email=user_email)
    new_refresh_token = create_refresh_token(email=user_email, jti=refresh_id)
    new_hashed_token = await get_password_hash(new_refresh_token)

    update_token_query = (
        sqlalchemy.update(refreshtoken_table)
        .where(refreshtoken_table.c.jti == refresh_id)
        .values(hashed_token=new_hashed_token)
    )
    logger.debug(update_token_query)
    try:
        await database.execute(update_token_query)

    except Exception as e:
        raise create_credentials_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to update refresh token table in database:{e}",
        )

    return {
        "new_access_token": new_access_token,
        "new_refresh_token": new_refresh_token,
    }
