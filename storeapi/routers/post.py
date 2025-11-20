from fastapi import APIRouter
from storeapi.models.post import (UserPost,UserPostIn,Comment,CommentIn,UserPostWithComments)


router = APIRouter()

post_table = {}
comments = {}
def find_post(post_id:int):
    return post_table.get(post_id)


@router.get("/")
async def root():
    return {"message": "well come!"}


@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    x:str = data
    print(x)
    print(" data object",data)
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post

@router.post("/comment",response_model=Comment)
async def comment_post(comment:CommentIn):
    comment = comment.model_dump()
    id = len(comments)
    unique_comment = {**comment,"comment_id":id}
    comments[id] = unique_comment
    return unique_comment

@router.get("/comments",response_model=list[UserPostWithComments])
async def get_comments(post_id:int):
    pass




@router.get("/posts", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
