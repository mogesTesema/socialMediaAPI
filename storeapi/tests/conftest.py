"""
Docstring for storeapi.tests.conftest
this is the core pytest configuration file that has many fixtures which going to be used by any test and test suite
in this root folder and subfolders. it register all fixture to fixture index lookup table.
fixture is the magical that abstract all boring stuff in testing.
Testing software using testing tools like pytest is pretty hands because use define how it test the software
with given data and flow, it will test automatically. Just we have to write single command after creating test suites and test cases.
this nature of testing tool like pytest is incredable great!

"""

from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from storeapi.utilits.formatted_printer import print_better
import os

os.environ["ENV_STATE"] = "test"  # hacking the env configuration durring testing

from storeapi.main import app
from storeapi.database import database, user_table


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app=app)


@pytest.fixture(autouse=True)
async def db(anyio_backend) -> AsyncGenerator:
    await database.connect()
    yield
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
