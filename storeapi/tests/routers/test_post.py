# async def create_post(body:str,async_client:AsyncClient)->dict:
#     response = await async_client.post("/post",json={"body":body})
#     return response.json()


# @pytest.fixture()
# async def created_post(async_client:AsyncClient):
#     return await create_post("Test Post",async_client)


# async def test_create_post(async_client:AsyncClient):
#     body = "Test Post"
#     response = await async_client.post(
#         "/post",
#         json={"body":body}
#         )
#     assert response.status_code == 201
#     assert {"id":0,"body":body}.items() <= response.json().items()


from httpx import AsyncClient
import pytest


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    body = "Test Post"
    return await create_post(body, async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test post"

    response = await async_client.post("/post", json={"body": body})
    assert response.status_code == 201
    assert {"id": 0, "body": body}.items() <= response.json().items()
