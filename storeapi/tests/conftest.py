from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from storeapi.main import app
from storeapi.routers.post import comment_table, post_table


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


def client() -> Generator:
    yield TestClient(app=app, base_url="http:127.0.0.1/8000")


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
