import sqlalchemy
from fastapi import HTTPException, status
from argon2 import PasswordHasher
from storeapi.database import user_table, database
import logging
from jwt import ExpiredSignatureError, PyJWTError
import jwt
import datetime

logger = logging.getLogger(__name__)


SECRETE_KEY = "6152bf528fa1f07a8c42b24fda7e82e4"
ALGORITHM = "HS256"
password_hasher = PasswordHasher()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials"
)


def access_token_expire_minutes() -> int:
    return 30


def create_access_token(email: str):
    logger.debug("creating access token", extra={"email": email})
    expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        minutes=access_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(payload=jwt_data, key=SECRETE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def decrpypt_access_token(access_token: str):
    return jwt.decode(access_token)


async def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(hashed_password, plain_password)


async def get_user(email: str):
    user_query = sqlalchemy.select(user_table).where(user_table.c.email == email)
    user = await database.fetch_one(user_query)
    logger.debug(user_query)

    return user


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticaling user", extra={"email": email})
    user = await get_user(email=email)
    if not user:
        raise credentials_exception
    print("\n" * 10)
    print(f"user_password:{user.password, user.email}")
    print("\n" * 10)
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise credentials_exception

    return user


async def get_current_user(token: str):
    try:
        payload = jwt.decode(jwt=token, key=SECRETE_KEY, algorithms=ALGORITHM)

        email = payload.get("sub")
        if not email:
            raise credentials_exception

    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except PyJWTError as e:
        raise credentials_exception from e

    user = await get_user(email=email)

    if not user:
        raise credentials_exception
    return user
