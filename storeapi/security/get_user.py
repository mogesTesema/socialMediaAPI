import sqlalchemy
from storeapi.database import user_table, database


async def get_user(email: str):
    user_query = sqlalchemy.select(user_table.c.email).where(
        user_table.c.email == email
    )
    user = await database.fetch_one(user_query)

    return user
