from fastapi import FastAPI
from contextlib import asynccontextmanager
from storeapi.routers.post import router as post_router
from storeapi.fileuploads.fileuploaderouters import router as upload_router
from storeapi.videochats.videochatrouter import router as videochat_router
from storeapi.database import database
from storeapi.logging_config import configure_logging
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- SETUP (start server) ----
    print("📡 Connecting database...")
    await database.connect()
    configure_logging()
    logger.info("hello loger")

    yield  # ⛔ Pause here — FastAPI runs routes now

    # ---- TEARDOWN (stop server) ----
    print("🔌 Disconnecting database...")
    await database.disconnect()

    
app = FastAPI(debug=True,lifespan=lifespan)
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(videochat_router)