import io
import logging

from fastapi import APIRouter, HTTPException, UploadFile, status
from PIL import Image

from storeapi.food_vision_model.food_prediction import predict_food

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/food-vision", tags=["food-vision"])

CLASS_NAMES = [
    "chicken_curry",
    "chicken_wings",
    "fried_rice",
    "grilled_salmon",
    "hamburger",
    "ice_cream",
    "pizza",
    "ramen",
    "steak",
    "sushi",
]


@router.post("/predict", status_code=status.HTTP_200_OK)
async def predict_food_vision(file: UploadFile):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="file is required"
        )

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="uploaded file is empty",
            )

        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"invalid image file: {exc}",
            )

        # Preprocess to 224x224x3, keep 0-255 range (no rescaling).
        image = image.resize((224, 224))

        predictions = predict_food(image, labels=CLASS_NAMES, top_k=3)
        return {
            "filename": file.filename,
            "predictions": [
                {"label": label, "score": score} for label, score in predictions
            ],
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("food vision prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"prediction failed: {exc}",
        )