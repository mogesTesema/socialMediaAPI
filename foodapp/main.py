from foodapp.core.logging_config import configure_logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from contextlib import asynccontextmanager
from foodapp.routers.post import router as post_router
from foodapp.routers.fileuploads import router as upload_router
from foodapp.routers.upload import router as b2_upload_router
from foodapp.routers.videochats import router as videochat_router
from foodapp.routers.user import router as user_router
from foodapp.routers.concurrency_async import test_router
from foodapp.db.database import db_connection, init_db
from foodapp.routers.food_vision import router as food_vision_router
import sentry_sdk
from foodapp.core.config import SecurityKeys, config

import logging
secret_key = SecurityKeys()

from fastapi.staticfiles import StaticFiles
import os

# 1️⃣ Configure logging first
configure_logging()
logger = logging.getLogger("foodapp")
sentry_sdk.init(
    dsn= secret_key.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=bool(secret_key.SENTRY_SEND_DEFAULT_PII))


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        logger.info(" Connecting database...")
        init_db()
        database = db_connection()
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

cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if config.CORS_ORIGINS:
    cors_origins.extend(
        [origin.strip() for origin in config.CORS_ORIGINS.split(",") if origin.strip()]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

# Mount static files
static_dir = os.path.join(os.getcwd(), "uploadedfiles")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 4️⃣ Routers
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(videochat_router)
app.include_router(user_router)
app.include_router(test_router)
app.include_router(b2_upload_router)
app.include_router(food_vision_router)


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
