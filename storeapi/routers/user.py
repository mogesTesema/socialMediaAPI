from fastapi import APIRouter, HTTPException, status
from storeapi.models.user import User, UserIn
from storeapi.database import user_table, database
from storeapi.security.get_user import (
    get_user,
    get_password_hash,
    verify_password,
    create_access_token,
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    password = await get_password_hash(user.password)
    print("\n" * 5)
    print(
        f"hashed_password:{password} original_password:{user.password} for user:{user}"
    )
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
    access_token = create_access_token(email)

    return {"status": "user registered", "token": access_token}


@router.get("/profile", response_model=User)
async def get_profile(user: UserIn):
    password = user.password
    db_user = await get_user(user.email)
    is_authed = await verify_password(
        plain_password=password, hashed_password=db_user.password
    )
    if is_authed:
        return User(db_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password or email"
        )
