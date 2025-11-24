from fastapi import APIRouter,HTTPException,File, UploadFile,WebSocketException
from storeapi.videochats.videostore import store_video_file

router = APIRouter()

@router.post("/video")
async def upload_video(file:UploadFile=File(...)):
    try:
        await store_video_file(file,file.filename)
    except HTTPException:
        raise HTTPException()
    except Exception:
        raise WebSocketException(code=1,reason="unknown error during uploaded video file storing")
# ws = WebSocket(scope=None,receive=None,send=None)