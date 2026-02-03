import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from storeapi.videochats.videostore import start_ffmpeg_writer

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/stream")
async def video_stream(ws: WebSocket):
    await ws.accept()

    ffmpeg_proc, output_path = start_ffmpeg_writer()

    try:
        while True:
            chunk = await ws.receive_bytes()
            ffmpeg_proc.stdin.write(chunk)
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("video stream error")
    finally:
        if ffmpeg_proc.stdin:
            ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()
        if ws.client_state.name != "DISCONNECTED":
            await ws.close()
