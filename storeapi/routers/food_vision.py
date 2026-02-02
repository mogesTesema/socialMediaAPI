import logging

from fastapi import APIRouter, HTTPException, UploadFile, File, status

from storeapi.food_vision_model.food_prediction import predict_food, predict_food_batch
from storeapi.food_vision_model.preprocessing import decode_zip_images

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

        predictions = predict_food(contents, labels=CLASS_NAMES, top_k=None)
        return {
            "filename": file.filename,
            "predictions": [
                {
                    "label": label,
                    "score_percent": round(score * 100.0, 2),
                }
                for label, score in predictions
            ],
        }
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("food vision prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"prediction failed: {exc}",
        )


@router.post("/predict-batch", status_code=status.HTTP_200_OK)
async def predict_food_vision_batch(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="files are required"
        )

    if len(files) > 32:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="maximum 32 images allowed per batch",
        )

    try:
        images = []
        for upload in files:
            contents = await upload.read()
            if not contents:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"uploaded file is empty: {upload.filename}",
                )

            images.append(contents)

        predictions = predict_food_batch(images, labels=CLASS_NAMES, top_k=1)
        results = []
        for upload, pred in zip(files, predictions):
            label, score = pred[0]
            results.append(
                {
                    "filename": upload.filename,
                    "prediction": {
                        "label": label,
                        "score_percent": round(score * 100.0, 2),
                    },
                }
            )

        return {"results": results}
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("food vision batch prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"batch prediction failed: {exc}",
        )


@router.post("/predict-zip", status_code=status.HTTP_200_OK)
async def predict_food_vision_zip(file: UploadFile = File(...)):
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

        names, images = decode_zip_images(contents, max_images=32)

        predictions = predict_food_batch(images, labels=CLASS_NAMES, top_k=1)
        results = []
        for name, pred in zip(names, predictions):
            label, score = pred[0]
            results.append(
                {
                    "filename": name,
                    "prediction": {
                        "label": label,
                        "score_percent": round(score * 100.0, 2),
                    },
                }
            )

        return {"results": results}
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("food vision zip prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"zip prediction failed: {exc}",
        )