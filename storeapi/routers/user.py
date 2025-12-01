from fastapi import APIRouter, HTTPException
from storeapi.models.user import User, UserIn
from storeapi.database import user_table, database
from storeapi.security.get_user import get_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn, response_model=User):
    password = user.password
    email = user.email
    user_exist = await get_user(email)
    if user_exist:
        raise HTTPException(
            status_code=409, detail="user already exist,conflict with esisting info"
        )
    user_query = user_table.insert().values(email=email, password=password)
    try:
        await database.execute(user_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database crash:{e}")
    logger.debug(user_query)

    return {"status": "user registered"}
