import os


video_root_dir = "uploaded-videos"
root_dir = os.path.join(os.getcwd(),video_root_dir)
os.makedirs(root_dir,exist_ok=True)

async def store_video_file(video_file,video_filename:str):
    video_store_dir = os.path.join(root_dir,video_filename)

    with open(video_store_dir,"wb") as video_buffer:
        video_buffer.write(await video_file.read())