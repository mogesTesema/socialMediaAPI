"""
This module is dedicated to test methods in user_security under security package
"""

import pytest
from foodapp.security import user_security
import jwt


def test_access_token_expire_minutes():
    assert user_security.access_token_expire_minutes() == 30


def test_confirm_token_expire_date():
    assert user_security.confirm_token_expire_minutes() == 15


def test_create_access_token():
    token = user_security.create_access_token("test@createtoken.com")
    assert {"sub": "test@createtoken.com", "type": "access"}.items() <= jwt.decode(
        token, key=user_security.SECRET_KEY, algorithms=[user_security.ALGORITHM]
    ).items()


def test_create_confirm_token():
    token = user_security.create_confirm_token("test@createtoken.com")
    assert {
        "sub": "test@createtoken.com",
        "type": "confirmation",
    }.items() <= jwt.decode(
        token, key=user_security.SECRET_KEY, algorithms=[user_security.ALGORITHM]
    ).items()


def test_subject_for_token_type_valid_confirmation():
    email = "test@example.com"
    token = user_security.create_confirm_token(email)
    assert email == user_security.get_subject_token_type(token, "confirmation")


def test_subject_for_token_type_valid_access():
    email = "test@example.com"
    token = user_security.create_access_token(email)
    assert email == user_security.get_subject_token_type(token, "access")


def test_get_subject_for_token_type_expired(mocker):
    mocker.patch(
        "foodapp.security.user_security.access_token_expire_minutes", return_value=-1
    )
    email = "test@example.com"
    token = user_security.create_access_token(email)
    with pytest.raises(user_security.HTTPException) as exe_info:
        user_security.get_subject_token_type(token, "access")

    assert "Token has expired" <= exe_info.value.detail


def test_get_subject_for_token_type_invalid_token():
    token = "invalid token sgwotiworehiw"
    with pytest.raises(user_security.HTTPException) as exc_info:
        user_security.get_subject_token_type(token, "access")

    assert "invalid token" <= exc_info.value.detail


def test_get_subject_for_token_type_missing_sub():
    email = "test@example.com"
    token = user_security.create_access_token(email)

    payload = jwt.decode(
        token,
        key=user_security.SECRET_KEY,
        algorithms=[user_security.ALGORITHM],
    )
    del payload["sub"]

    token = jwt.encode(payload, user_security.SECRET_KEY, user_security.ALGORITHM)
    with pytest.raises(user_security.HTTPException) as exc_info:
        user_security.get_subject_token_type(token, "access")
    assert "Token is missing 'sub' field" <= exc_info.value.detail


def test_get_subject_for_token_type_wrong_type():
    email = "test@example.com"
    token = user_security.create_confirm_token(email)
    with pytest.raises(user_security.HTTPException) as exc_info:
        user_security.get_subject_token_type(token, "access")
    assert "token has incorrect type, expected: access" == exc_info.value.detail


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


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = user_security.create_access_token(registered_user["email"])
    user = await user_security.get_current_user(token)

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(user_security.HTTPException):
        await user_security.get_current_user("wrongtoken:wiewoieowiejwr")


@pytest.mark.anyio
async def get_current_user_wrong_token_type(registered_user: dict):
    token = user_security.create_confirm_token(registered_user["email"])
    with pytest.raises(user_security.HTTPException):
        await user_security.get_current_user(token)
