from fastapi import APIRouter,HTTPException
from storeapi.models.post import (UserPost,UserPostIn,Comment,CommentIn,UserPostWithComments)


router = APIRouter()

post_table = {}
comment_table = {}
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
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404,detail=f"post with {comment.post_id} doen't exist")
    comment = comment.model_dump()
    id = len(comment_table)
    unique_comment = {**comment,"comment_id":id}
    comment_table[id] = unique_comment
    return unique_comment

@router.get("/comments",response_model=list[UserPostWithComments])
async def get_comments(post_id:int):
    pass




@router.get("/posts", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())


@router.get("post/{post_id}/comment",response_model=list[Comment])
async def get_comments_on_post(post_id:int):
    return [
        comment for comment in  comment_table.values() if comment["post_id"]==post_id
    ]