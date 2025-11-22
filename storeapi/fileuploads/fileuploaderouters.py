from fastapi import APIRouter,File,UploadFile
import os




router = APIRouter()
root_dir = os.path.join(os.getcwd(),"uploadedfiles")

os.makedirs(root_dir,exist_ok=True)



@router.post("/upload")
async def create_file(file:UploadFile=File(...)):

    save_path = os.path.join(root_dir,file.filename)

    with open(save_path,"wb") as buffer:
        buffer.write(await file.read())

    return {"status":"uploaded","filename":file.filename}


@router.post("/upload/multiple")
async def create_multiple_files(files:list[UploadFile]=File(...)):
        
        uploaded_files = []
        for uploaded in files:
            save_path = os.path.join(root_dir,uploaded.filename)

            with open(save_path,"wb") as f:
                f.write(await uploaded.read())

            uploaded_files.append(uploaded.filename)  
        return {"status":"uploaded","uploadef_files":uploaded_files}
