import pytest
from storeapi.security import user_security


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
