import pytest
from storeapi.email.verify_email import send_verfication_email


@pytest.mark.anyio
async def test_verify_email(mock_httpx_client):
    await send_verfication_email(
        "mosoi@gmail.com", "insowqt9qu8er82", "/confirm/wweiweioweiw"
    )
    mock_httpx_client.post.assert_called()


# @pytest.mark.anyio
# async def test_send_verify_email_api_error(mock_httpx_client):
#     mock_httpx_client.return_value = httpx.Response(
#         status_code=500, content="", request=httpx.Request("POST", "//")
#     )


#     with pytest.raises(HTTPException) as exc_mock:
#         await send_verfication_email(
#             "mosoi@gmail.com", "insowqt9qu8er82", "/confirm/wweiweioweiw"
#         )
#     assert exc_mock.status_code == 500
