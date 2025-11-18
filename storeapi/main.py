from fastapi import FastAPI
from pydantic import BaseModel

import os

app = FastAPI(debug=True)

class UserPostIn(BaseModel):
    body: str
path = os.listdir("/")

class UserPost(UserPostIn):
    id: int

"installing Linux as professional"
post_table = {}


@app.get("/")
async def root():
    return {"message": "well come!"}


@app.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    x = data
    print(" data object",data)
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@app.get("/posts", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
