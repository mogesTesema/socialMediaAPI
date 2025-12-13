import pytest
from storeapi.security import user_security


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await user_security.get_user(registered_user["email"])
    assert user.email == registered_user["email"]
