from fastapi import APIRouter,HTTPException
from storeapi.models.post import (UserPost,
                                  UserPostIn,
                                  Comment,
                                  CommentIn,
                                  UserPostWithComments,)

from storeapi.models.data.databaseAPI import (create_post as db_create_post,
                                              create_comment,
                                              get_post_comments,
                                              get_post as db_get_post,
                                              get_all_posts)


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
    """
    this post endpoint is going to insert posts into database from clients post request
    """
    data = post.model_dump()
    post_text = post.body
    try:   
        post_id = await db_create_post(post_text=post_text)
    except Exception:
        raise HTTPException(status_code=500,detail="internal server error due to database crash")
    new_post = {**data, "id": post_id}
    return new_post

@router.post("/comment",response_model=Comment)
async def comment_post(comment:CommentIn):
    """
    this endpoint is ganna insert comment into database
    """
    post_id = comment.post_id
    comment_text = comment.body
    comment = comment.model_dump()
    try:
        comment_id = await create_comment(post_id=post_id,comment_text=comment_text)
    except HTTPException:
        raise HTTPException(status_code=404,detail=f"post with {post_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"internal server error, database crash\n{e}")

    unique_comment = {**comment,"comment_id":comment_id}
    return unique_comment


@router.get("/post/{post_id}",response_model=UserPost)
async def get_post(post_id:int):
    post_text = await db_get_post(post_id=post_id)
    return {"body":post_text,"id":post_id}


@router.get("/posts",response_model=list[UserPost])
async def get_posts():
    """
    this endpoint gonna retrive data from database and then send those retrieved data back to client
    """
    try:
        all_posts = await get_all_posts()
    except Exception:
        raise HTTPException(status_code=500,detail="insternal server crash")
    filtered_all_posts = []
    for post_id,post_text in all_posts:
        filtered_all_posts.append({"id":post_id,"body":post_text})
    return filtered_all_posts
    




@router.get("/post/{post_id}/comments",response_model=UserPostWithComments)
async def get_post_with_comments(post_id:int):
    """
    this endpoint is unique, it combines post and comment property that leads to foreign relation between those tables
    """
    try:
        all_comments = await get_post_comments(post_id=post_id)
        print(all_comments)
        
    except Exception:
        raise HTTPException(status_code=404)
    try:
        post_detail = await get_post(post_id=post_id)
    except Exception:
        raise HTTPException(status_code=500,detail="inernal server error due to database crash when fetching post_text")
    comment_lists = []
    for comment_id,comment_text in all_comments:
        comment_dict = {"body":comment_text,"comment_id":comment_id,"post_id":post_id}
        comment_lists.append(comment_dict)

    return {
        "post":post_detail,
        "comment": comment_lists
    }
