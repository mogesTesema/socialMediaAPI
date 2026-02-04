"""
Docstring for foodapp.tests.conftest
this is the core pytest configuration file that has many fixtures which going to be used by any test and test suite
in this root folder and subfolders. it register all fixture to fixture index lookup table.
fixture is the magical that abstract all boring stuff in testing.
Testing software using testing tools like pytest is pretty hands because use define how it test the software
with given data and flow, it will test automatically. Just we have to write single command after creating test suites and test cases.
this nature of testing tool like pytest is incredable great!

"""

from typing import AsyncGenerator, Generator

import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport, Request, Response
from foodapp.utils.formatted_printer import print_better

import os

os.environ["ENV_STATE"] = "test"  # hacking the env configuration durring testing

from foodapp.main import app
from foodapp.db.database import db_connection, user_table, init_db

database = db_connection()
async def _clear_db() -> None:
    url = str(database.url)
    if "sqlite" in url:
        await database.execute("PRAGMA foreign_keys=OFF;")
        await database.execute("DELETE FROM comments;")
        await database.execute("DELETE FROM likes;")
        await database.execute("DELETE FROM posts;")
        await database.execute("DELETE FROM refreshtokens;")
        await database.execute("DELETE FROM password_reset_tokens;")
        await database.execute("DELETE FROM users;")
        seq_exists = await database.fetch_val(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';"
        )
        if seq_exists:
            await database.execute("DELETE FROM sqlite_sequence;")
        await database.execute("PRAGMA foreign_keys=ON;")
    else:
        await database.execute(
            "TRUNCATE TABLE comments, likes, posts, refreshtokens, password_reset_tokens, users RESTART IDENTITY CASCADE;"
        )


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app=app)


@pytest.fixture(autouse=True)
async def db(anyio_backend) -> AsyncGenerator:
    await database.connect()
    init_db()
    await _clear_db()
    yield
    await _clear_db()
    await database.disconnect()


@pytest.fixture()
async def async_client() -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.com", "password": "1234"}
    response = await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    print_better(obj="registered_user", message=response.json())
    return {**user_details, "id": user.id}


@pytest.fixture()
async def confirmed_user(registered_user: dict):
    confirm_query = (
        user_table.update()
        .values(confirmed=True)
        .where(user_table.c.email == registered_user["email"])
    )
    await database.execute(confirm_query)

    return registered_user


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, confirmed_user: dict) -> str:
    response = await async_client.post(
        "/token",
        json={
            "email": confirmed_user["email"],
            "password": confirmed_user["password"],
        },
    )

    return response.json().get("access_token")


@pytest.fixture(autouse=True)
def mock_httpx_client(mocker):
    mocked_client = mocker.patch("foodapp.integrations.email.verify_email.httpx.AsyncClient")
    mocked_async_client = Mock()
    response = Response(
        status_code=200, json={"message": "email sent"}, request=Request("POST", "//")
    )
    mocked_async_client.post = AsyncMock(return_value=response)
    mocked_client.return_value.__aenter__.return_value = mocked_async_client

    return mocked_async_client



@pytest.fixture(autouse=True)
def mock_logtail(mocker):
    mocker.patch("logtail.handler.LogtailHandler.__init__", return_value=None)
