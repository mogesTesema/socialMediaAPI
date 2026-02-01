import io

import pytest
from PIL import Image
from httpx import AsyncClient


@pytest.mark.anyio
async def test_food_vision_predict(async_client: AsyncClient):
    image = Image.new("RGB", (244, 244), color=(160, 70, 60))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = await async_client.post(
        "/food-vision/predict",
        files={"file": ("steak.png", buffer, "image/png")},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["filename"] == "steak.png"
    assert "predictions" in payload
    assert isinstance(payload["predictions"], list)
    assert len(payload["predictions"]) > 0
    first = payload["predictions"][0]
    assert "label" in first
    assert "score" in first
    assert isinstance(first["score"], float)