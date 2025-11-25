from fastapi import APIRouter, WebSocket
from storeapi.videochats.videostore import start_ffmpeg_writer

router = APIRouter()

@router.websocket("/ws/stream")
async def video_stream(ws: WebSocket):
    await ws.accept()

    ffmpeg_proc, output_path = start_ffmpeg_writer()

    try:
        while True:
            chunk = await ws.receive_bytes()
            ffmpeg_proc.stdin.write(chunk)

    except Exception:
        ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()

        await ws.close()

    return {"saved_to": output_path}
