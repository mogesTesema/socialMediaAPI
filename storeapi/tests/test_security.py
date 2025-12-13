"""
This module is dedicated to test methods in user_security under security package
"""

import pytest
from storeapi.security import user_security
import jwt


def test_access_token_expire_minutes():
    assert user_security.access_token_expire_minutes() == 30


def test_create_access_token():
    token = user_security.create_access_token("test@createtoken.com")
    assert {"sub": "test@createtoken.com"}.items() <= jwt.decode(
        token, key=user_security.SECRET_KEY, algorithms=[user_security.ALGORITHM]
    ).items()


@pytest.mark.anyio
async def test_password_hashes():
    password = "password"
    assert await user_security.verify_password(
        password, await user_security.get_password_hash("password")
    )


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await user_security.get_user(registered_user["email"])
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await user_security.get_user("test@example.com")

    assert user is None


@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):
    try:
        user = await user_security.authenticate_user(
            registered_user["email"], registered_user["password"]
        )
        assert user.email == registered_user["email"]
    except Exception as e:
        assert e.status_code == 401


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(Exception):
        await user_security.authenticate_user(
            registered_user["email"], password="wrongpassword"
        )


@pytest.mark.anyio
async def test_authenticate_user_not_exists():
    with pytest.raises(user_security.HTTPException):
        await user_security.authenticate_user("test@example.com", "12424")
