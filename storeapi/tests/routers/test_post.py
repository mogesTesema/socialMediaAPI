from httpx import AsyncClient
import pytest


async def create_post(body: str, client: AsyncClient, user_token: str) -> dict:
    response = await client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient, logged_in_token: str):
    body = "Test Post"
    return await create_post(body, async_client, logged_in_token)


async def create_comment(
    body: str, post_id: int, client: AsyncClient, user_token: str
) -> dict:
    response = await client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    return response.json()


async def like_post(post_id: int, async_client: AsyncClient, logged_in_token: str):
    response = await async_client.post(
        "/like",
        json={"body": "I really like this post", "post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response


@pytest.fixture()
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    body = "comment one"
    response = await create_comment(
        body=body,
        post_id=created_post["id"],
        client=async_client,
        user_token=logged_in_token,
    )
    return response


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient, logged_in_token: str):
    body = "Test post"

    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 200
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_like_post(
    async_client: AsyncClient, logged_in_token: str, created_post: dict
):
    liked = await like_post(created_post["id"], async_client, logged_in_token)
    assert liked.status_code == 201


@pytest.mark.anyio
async def test_get_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")
    assert response.status_code == 200
    # assert created_post.items() <= response.json().items()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "sorting,expected_order", [("new", [3, 2, 1]), ("old", [1, 2, 3])]
)
async def test_get_all_post_sorting(
    async_client: AsyncClient, logged_in_token: str, sorting: str, expected_order: list
):
    await create_post("test body", async_client, logged_in_token)
    await create_post("test body", async_client, logged_in_token)
    await create_post("test body", async_client, logged_in_token)
    response = await async_client.get("/posts", params={"sorting": sorting})
    assert response.status_code == 200
    data = response.json()

    post_ids = [post["id"] for post in data]

    assert post_ids == expected_order


@pytest.mark.anyio
async def test_create_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    body = "Test comment"
    response = await async_client.post(
        "/comment",
        json={
            "body": body,
            "post_id": created_post["id"],
        },
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 200

    # assert {
    #     "id": 0,
    #     "body": body,
    #     "post_id": created_post["id"],
    # }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comments")
    assert response.status_code == 200
    # assert created_comment.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")
    assert response.status_code == 200
    # assert response.json() == {"post": created_post, "comment": [created_comment]}
