from fastapi import FastAPI
from contextlib import asynccontextmanager
from storeapi.routers.post import router as post_router
from storeapi.fileuploads.fileuploaderouters import router as upload_router
from storeapi.videochats.videochatrouter import router as videochat_router
from storeapi.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

    
app = FastAPI(debug=True,lifespan=lifespan)
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(videochat_router)