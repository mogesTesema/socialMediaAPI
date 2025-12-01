import sqlalchemy
from argon2 import PasswordHasher
from storeapi.database import user_table, database
import logging

logger = logging.getLogger(__name__)


SECRETE_KEY = "6152bf528fa1f07a8c42b24fda7e82e4"
ALGORITHM = "HS256"
password_hasher = PasswordHasher()


async def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(hashed_password, plain_password)


async def get_user(email: str):
    user_query = sqlalchemy.select(user_table.c.email).where(
        user_table.c.email == email
    )
    user = await database.fetch_one(user_query)
    logger.debug(user_query)

    return user
