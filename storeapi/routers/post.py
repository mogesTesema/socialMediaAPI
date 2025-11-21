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
    """
    this post endpoint is going to insert posts into database from clients post request
    """
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
    """
    this endpoint is ganna insert comment into database
    """
    return unique_comment


@router.get("/posts", response_model=list[UserPost])
async def get_posts():
    """
    this endpoint gonna retrive data from database and then send those retrieved data back to client
    """
    return list(post_table.values())


@router.get("/post/{post_id}/comment",response_model=list[Comment])
def get_comments_on_post(post_id:int):
    """
    this endpoing ganna finter commant based on this post_id and then send back to the client
    """
    return [
        comment for comment in  comment_table.values() if comment["post_id"]==post_id
    ]

@router.get("/post/{post_id}",response_model=UserPostWithComments)
async def get_post_with_comments(post_id:int):
    post = find_post(post_id=post_id)
    """
    this endpoint is unique, it combines post and comment property that leads to foreigh relation between those tables
    """
    if not post:
        raise HTTPException(status_code=404,detail="comment not found")
    
    return {
        "post":post,
        "comment": get_comments_on_post(post_id)
    }