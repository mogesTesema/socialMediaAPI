from fastapi import FastAPI
from storeapi.routers.post import router as post_router

app = FastAPI(debug=True)
app.include_router(post_router)
