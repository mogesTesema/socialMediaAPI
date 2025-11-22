from fastapi import FastAPI
from storeapi.routers.post import router as post_router
from storeapi.fileuploads.fileuploaderouters import router as upload_router

app = FastAPI(debug=True)
app.include_router(post_router)
app.include_router(upload_router)