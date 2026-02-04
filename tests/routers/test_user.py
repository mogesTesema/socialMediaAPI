from httpx import AsyncClient
import pytest
from foodapp.utils.formatted_printer import print_better
from fastapi import Request


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


@pytest.mark.anyio
async def test_confirm_user(async_client: AsyncClient, mocker):
    spy = mocker.spy(Request, "url_for")
    await register_user(async_client, "test@example.com", "2121341s")
    confirmation_url = str(spy.spy_return)
    print_better(obj="confirmation url of spy", message=confirmation_url)
    response = await async_client.get(confirmation_url)

    assert "user has been confirmed" in response.json()["detail"]


@pytest.mark.anyio
async def test_confirm_user_invalid_token(async_client: AsyncClient):
    response = await async_client.get("confirm/invalid-token")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_confirm_user_expired_token(async_client: AsyncClient, mocker):
    mocker.patch(
        "foodapp.security.user_security.confirm_token_expire_minutes", return_value=-1
    )
    spy = mocker.spy(Request, "url_for")
    await register_user(async_client, "test@example.com", "2121341s")
    confirmation_url = str(spy.spy_return)
    print_better(obj="confirmation url of spy", message=confirmation_url)
    response = await async_client.get(confirmation_url)

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/token", json={"email": "test@token.com", "password": "token123"}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_user_not_confirmed(
    async_client: AsyncClient, registered_user: dict
):
    response = await async_client.post(
        "/token",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 401
    assert "email is not confirmed" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user_exists(async_client: AsyncClient, confirmed_user: dict):
    response = await async_client.post(
        "/token",
        json={
            "email": confirmed_user["email"],
            "password": confirmed_user["password"],
        },
    )
    assert response.status_code == 200
