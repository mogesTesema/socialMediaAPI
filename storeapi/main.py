from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from contextlib import asynccontextmanager
from storeapi.routers.post import router as post_router
from storeapi.fileuploads.fileuploaderouters import router as upload_router
from storeapi.videochats.videochatrouter import router as videochat_router
from storeapi.database import database
from storeapi.logging_config import configure_logging
import logging



configure_logging() # configuring logging before system start up
logger = logging.getLogger("storeapi")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- SETUP (start server) ----
    try:
        logger.info("📡 Connecting database...")
        await database.connect()
    except Exception as e:
        logger.critical(f"failed connecting to database:{e}")
        # for handler in logger.handlers:
        #     handler.flush()
        logging.shutdown()
        raise

    yield  # ⛔ Pause here — FastAPI runs routes now

    # ---- TEARDOWN (stop server) ----
    try:
        logger.info("system shutdown,🔌 Disconnecting database...")
        await database.disconnect()
    except Exception:
        logger.critical("unable to disconnect database connection:{e}")
        # for handler in logger.handlers:
        #     handler.flush()
        logging.shutdown()
        raise

    

    
app = FastAPI(debug=False,lifespan=lifespan)
app.include_router(post_router)
app.include_router(upload_router)
app.include_router(videochat_router)

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request:Request, exc:HTTPException):
    logger.error(f"HTTPException:-url:{request.url}, method:{request.method}, status_code: {exc.status_code}, detail:{exc.detail}")
    return await http_exception_handler(request=request,exc=exc)

@app.exception_handler(Exception)
async def general_exception_handle_logging(request:Request,exc:Exception):
    logger.exception(f"Exception:= url:{request.url}, method:{request.method}, exception:something goes wrong")
    return JSONResponse(status_code=500,content={"detail":"Internal Server Error New Yederesebign"})