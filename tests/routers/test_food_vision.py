import io
import zipfile

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
    assert len(payload["predictions"]) == 10
    first = payload["predictions"][0]
    assert "label" in first
    assert "score_percent" in first
    assert isinstance(first["score_percent"], (int, float))


@pytest.mark.anyio
async def test_food_vision_predict_batch(async_client: AsyncClient):
    image_a = Image.new("RGB", (224, 224), color=(160, 70, 60))
    buffer_a = io.BytesIO()
    image_a.save(buffer_a, format="PNG")
    buffer_a.seek(0)

    image_b = Image.new("RGB", (300, 300), color=(60, 110, 130))
    buffer_b = io.BytesIO()
    image_b.save(buffer_b, format="PNG")
    buffer_b.seek(0)

    response = await async_client.post(
        "/food-vision/predict-batch",
        files=[
            ("files", ("image-a.png", buffer_a, "image/png")),
            ("files", ("image-b.png", buffer_b, "image/png")),
        ],
    )

    assert response.status_code == 200
    payload = response.json()

    assert "results" in payload
    assert isinstance(payload["results"], list)
    assert len(payload["results"]) == 2
    first = payload["results"][0]
    assert "filename" in first
    assert "prediction" in first
    assert "label" in first["prediction"]
    assert "score_percent" in first["prediction"]
    assert isinstance(first["prediction"]["score_percent"], (int, float))


@pytest.mark.anyio
async def test_food_vision_predict_zip(async_client: AsyncClient):
    image_a = Image.new("RGB", (224, 224), color=(120, 80, 60))
    buffer_a = io.BytesIO()
    image_a.save(buffer_a, format="PNG")
    buffer_a.seek(0)

    image_b = Image.new("RGB", (224, 224), color=(60, 120, 140))
    buffer_b = io.BytesIO()
    image_b.save(buffer_b, format="PNG")
    buffer_b.seek(0)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
        zip_file.writestr("image-a.png", buffer_a.getvalue())
        zip_file.writestr("nested/image-b.png", buffer_b.getvalue())
    zip_buffer.seek(0)

    response = await async_client.post(
        "/food-vision/predict-zip",
        files={"file": ("images.zip", zip_buffer, "application/zip")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "results" in payload
    assert isinstance(payload["results"], list)
    assert len(payload["results"]) == 2
    first = payload["results"][0]
    assert "filename" in first
    assert "prediction" in first
    assert "label" in first["prediction"]
    assert "score_percent" in first["prediction"]