from httpx import AsyncClient
import pytest
from storeapi.utilits.formatted_printer import print_better


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/register", json={"email": email, "password": password}
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(
        async_client=async_client, email="test@gmail.com", password="test1234"
    )
    # print_better("test_register_response", message=response.json())

    assert response.status_code == 201

    assert "user registered" in response.json()["status"]


@pytest.mark.anyio
async def test_register_user_exists(async_client: AsyncClient, registered_user: dict):
    response = await register_user(
        async_client, registered_user["email"], registered_user["password"]
    )

    assert response.status_code == 409
    print_better("user exist test", response.json())
    assert "already exist" in response.json()["detail"]
