import subprocess
import uuid
import os

VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

def start_ffmpeg_writer():
    video_id = str(uuid.uuid4())
    output_file = f"{VIDEO_DIR}/{video_id}.mp4"

    process = subprocess.Popen(
        [
            "ffmpeg", "-y",
            "-f", "mpegts", "-i", "-",
            "-vcodec", "libx264", output_file
        ],
        stdin=subprocess.PIPE
    )

    return process, output_file
