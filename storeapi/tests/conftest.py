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
import os

os.environ["ENV_STATE"] = "test"  # hacking the env configuration durring testing

from storeapi.main import app
from storeapi.database import database


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
