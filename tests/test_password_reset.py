import uuid

import pytest
from httpx import AsyncClient

from foodapp.db.database import db_connection, password_reset_table, refreshtoken_table
from foodapp.security.user_security import (
    create_password_reset_token,
    store_password_reset_token,
)


database = db_connection()


@pytest.mark.anyio
async def test_forgot_password_creates_reset_token(confirmed_user: dict, async_client: AsyncClient):
    response = await async_client.post(
        "/password/forgot",
        json={"email": confirmed_user["email"]},
    )

    assert response.status_code == 200

    token_query = password_reset_table.select().where(
        password_reset_table.c.user_email == confirmed_user["email"]
    )
    token_record = await database.fetch_one(token_query)
    assert token_record is not None


@pytest.mark.anyio
async def test_forgot_password_unknown_email_no_token(async_client: AsyncClient):
    response = await async_client.post(
        "/password/forgot",
        json={"email": "unknown@example.com"},
    )

    assert response.status_code == 200

    token_query = password_reset_table.select().where(
        password_reset_table.c.user_email == "unknown@example.com"
    )
    token_record = await database.fetch_one(token_query)
    assert token_record is None


@pytest.mark.anyio
async def test_reset_password_updates_password_and_revokes_tokens(
    confirmed_user: dict, async_client: AsyncClient
):
    reset_id = str(uuid.uuid4())
    reset_token = create_password_reset_token(
        email=confirmed_user["email"], jti=reset_id
    )
    await store_password_reset_token(confirmed_user["email"], reset_token, reset_id)

    response = await async_client.post(
        "/password/reset",
        json={"token": reset_token, "new_password": "newpass123"},
    )

    assert response.status_code == 200

    token_query = password_reset_table.select().where(
        password_reset_table.c.user_email == confirmed_user["email"]
    )
    token_record = await database.fetch_one(token_query)
    assert token_record is None

    refresh_query = refreshtoken_table.select().where(
        refreshtoken_table.c.user_email == confirmed_user["email"]
    )
    refresh_record = await database.fetch_one(refresh_query)
    assert refresh_record is None

    login_response = await async_client.post(
        "/token",
        json={
            "email": confirmed_user["email"],
            "password": "newpass123",
        },
    )
    assert login_response.status_code == 200
    assert login_response.json().get("access_token")
