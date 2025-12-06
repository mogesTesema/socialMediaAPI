import logging
import tempfile
import aiofiles
from anyio import to_thread
from fastapi import APIRouter, HTTPException, UploadFile, status
from storeapi.libs.b2 import b2_upload_file


logger = logging.getLogger(__name__)

router = APIRouter()

CHUNK_SIZE = 1024 * 1024


@router.post("/b2upload")
async def upload_file(file: UploadFile, status_code=status.HTTP_201_CREATED):
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            filename = temp_file.name
            logger.info(f"saving uploaded file temporarlly to {filename}")

            async with aiofiles.open(filename, "wb") as f:
                # chunk = await file.read(CHUNK_SIZE)
                # while chunk:
                #     await f.write(chunk)
                #     chunk = await file.read(CHUNK_SIZE)
                while chunk := await file.read(CHUNK_SIZE):
                    await f.write(chunk)

            file_url = await to_thread.run_sync(b2_upload_file, filename, file.filename)
            logger.info(f"file is successfully uploaded. it url is:{file_url}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"there is an error durring file uploadding.\nERROR:{e}",
        )
    return {"detail": f"successfully uploaded {file.filename}", "file_url": file_url}
