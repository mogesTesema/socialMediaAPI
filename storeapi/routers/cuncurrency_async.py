from fastapi import APIRouter
import time
import asyncio

test_router = APIRouter()


@test_router.get("/test1")
async def test_one():
    print("test_one endpoint started process")
    time.sleep(10)
    print("test_one endpoint finished process")


@test_router.get("/test2")
async def test_two():
    print("test_two endpoint started process")
    await asyncio.sleep(10)
    print("test_two endpoint finished process")


@test_router.get("/test3")
def test_three():
    print("test_three endpoint started process")
    time.sleep(10)
    print("test_three endpoint finished process")
