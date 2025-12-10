"""
Docstring for storeapi.tests.conftest
this is the core pytest configuration file that has many fixtures which going to be used by any test and test suite
in this root folder and subfolders. it register all fixture to fixture index lookup table.
"""

from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from storeapi.main import app
from storeapi.routers.post import comment_dict, post_dict


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app=app)


@pytest.fixture(autouse=False)
async def db() -> AsyncGenerator:
    post_dict.clear()
    comment_dict.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac
