from fastapi import APIRouter, File, UploadFile, HTTPException, status
import os


router = APIRouter()
root_dir = os.path.join(os.getcwd(), "uploadedfiles")

os.makedirs(root_dir, exist_ok=True)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.post("/upload")
async def create_file(file: UploadFile = File(...)):
    safe_name = os.path.basename(file.filename or "")
    if not safe_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid filename",
        )
    save_path = os.path.join(root_dir, safe_name)

    with open(save_path, "wb") as buffer:
        contents = await file.read()
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="file too large",
            )
        buffer.write(contents)

    return {"status": "uploaded", "filename": safe_name}


@router.post("/upload/multiple")
async def create_multiple_files(files: list[UploadFile] = File(...)):
    uploaded_files = []
    for uploaded in files:
        safe_name = os.path.basename(uploaded.filename or "")
        if not safe_name:
            continue
        save_path = os.path.join(root_dir, safe_name)

        with open(save_path, "wb") as f:
            contents = await uploaded.read()
            if len(contents) > MAX_UPLOAD_BYTES:
                continue
            f.write(contents)

        uploaded_files.append(safe_name)
    return {"status": "uploaded", "uploadef_files": uploaded_files}
