import logging

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.concurrency import run_in_threadpool

from foodapp.integrations.vision.food_prediction import predict_food, predict_food_batch
from foodapp.integrations.vision.preprocessing import decode_zip_images

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/food-vision", tags=["food-vision"])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}
ALLOWED_ZIP_TYPES = {"application/zip", "application/x-zip-compressed"}

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
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported image type",
        )

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="uploaded file is empty",
            )
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="uploaded file is too large",
            )

        predictions = await run_in_threadpool(
            predict_food, contents, labels=CLASS_NAMES, top_k=None
        )
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
            if upload.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"unsupported image type: {upload.filename}",
                )
            contents = await upload.read()
            if not contents:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"uploaded file is empty: {upload.filename}",
                )
            if len(contents) > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"uploaded file is too large: {upload.filename}",
                )

            images.append(contents)

        predictions = await run_in_threadpool(
            predict_food_batch, images, labels=CLASS_NAMES, top_k=1
        )
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
    if file.content_type not in ALLOWED_ZIP_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported zip type",
        )

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="uploaded file is empty",
            )
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="uploaded file is too large",
            )

        names, images = decode_zip_images(contents, max_images=32)

        predictions = await run_in_threadpool(
            predict_food_batch, images, labels=CLASS_NAMES, top_k=1
        )
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