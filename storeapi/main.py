from storeapi.logging_config import configure_logging
from fastapi import FastAPI, HTTPException, Request
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from contextlib import asynccontextmanager
from storeapi.routers.post import router as post_router
from storeapi.fileuploads.fileuploaderouters import router as upload_router
from storeapi.videochats.videochatrouter import router as videochat_router
from storeapi.routers.user import router as user_router
from storeapi.database import database

# from storeapi.logtail_storage_config import test
import logging

# print(f"logtail test:{test}")
# 1️⃣ Configure logging first
configure_logging()
logger = logging.getLogger("storeapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("📡 Connecting database...")
        await database.connect()
    except Exception as e:
        logger.critical(f"failed connecting to database:{e}")
        logging.shutdown()
        raise

    yield

    try:
        logger.info("🔌 Disconnecting database...")
        await database.disconnect()
    except Exception:
        logger.critical("unable to disconnect database connection")
        logging.shutdown()
        raise


# 2️⃣ Create app AFTER logging is configured
app = FastAPI(debug=False, lifespan=lifespan)

# 3️⃣ Add middleware BEFORE routers
app.add_middleware(CorrelationIdMiddleware)

# 4️⃣ Routers
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(videochat_router)
app.include_router(user_router)


# 5️⃣ Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request: Request, exc: HTTPException):
    logger.error(
        f"HTTPException:-url:{request.url}, method:{request.method}, "
        f"status_code:{exc.status_code}, detail:{exc.detail}"
    )
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def general_exception_handle_logging(request: Request, exc: Exception):
    logger.exception(
        f"Exception:-url:{request.url}, method:{request.method}, unhandled error"
    )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
