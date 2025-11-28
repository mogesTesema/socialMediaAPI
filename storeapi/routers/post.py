from fastapi import APIRouter,HTTPException
from storeapi.models.post import (UserPost,
                                  UserPostIn,
                                  Comment,
                                  CommentIn,
                                  UserPostWithComments)
from storeapi.database import database,post_table,comment_table
from sqlalchemy import select
import logging
                                            






router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def root():
    return {"message": "well come!"}




async def find_post(post_id:int):
    logger.info(f"Finding post with id {post_id}")
    query = select(post_table.c.id).where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query=query)




@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    """
    this post endpoint is going to insert posts into database from clients post request
    """
    logger.info(f"creating user post with details: {post}")
    data = post.model_dump()
    query = post_table.insert().values(data)
    logger.debug(query)
    try:   
        post_id = await database.execute(query=query)
    except Exception:
        logger.error("can't execute database query:{query}")
        raise HTTPException(status_code=500,detail="internal server error due to database crash")
    new_post = {**data, "id": post_id}
    return new_post




@router.post("/comment",response_model=Comment)
async def comment_post(comment:CommentIn):
    """
    this endpoint is ganna insert comment into database
    """
    logger.info(f"creating comment with details:{comment}")
    post= await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404,detail="post doesn't exist")
    comment = comment.model_dump()
    query = comment_table.insert().values(comment)
    logger.debug(query)
    try:
        comment_id = await database.execute(query)
    except Exception as e:
        logger.error(f"fail to execute database query:{query},error_message:{e}")
        raise HTTPException(status_code=500,detail=f"internal server error, database crash\n{str(e)}")

    unique_comment = {**comment,"id":comment_id}
    return unique_comment





@router.get("/post/{post_id}",response_model=UserPost)
async def get_post(post_id:int):
    logger.info("geting user post with id {post_id}")
    query = post_table.select().where(post_table.c.id==post_id)
    logger.debug(query)
    post_content = await database.fetch_one(query)
    if post_content:
        return UserPost(**post_content)
    else:
        raise HTTPException(status_code=404,detail=f"post with post_id:{post_id} doesn't exist")

 


@router.get("/posts",response_model=list[UserPost])
async def get_posts():
    """
    this endpoint gonna retrive data from database and then send those retrieved data back to client
    """
    logger.info("getting all posts up to 50 recent posts")
    query = post_table.select()
    logger.debug(query)
    logger.debug(query)
    try:
        all_posts = await database.fetch_all(query=query)
    except Exception:
        raise HTTPException(status_code=500,detail="insternal server crash")
    return all_posts
    




@router.get("/post/{post_id}/comments",response_model=UserPostWithComments)
async def get_post_with_comments(post_id:int):
    """
    this endpoint is unique, it combines post and comment property that leads to foreign relation between those tables
    """
    query = comment_table.select().where(comment_table.c.post_id==post_id)
    logger.debug(query)
    try:
        all_comments = await database.fetch_all(query)
        
    except Exception:
        raise HTTPException(status_code=404)
    try:
        post_detail = await database.fetch_one(post_table.select().where(post_table.c.id==post_id))
    except Exception:
        raise HTTPException(status_code=500,detail="inernal server error due to database crash when fetching post_text")
    if not post_detail:
        raise HTTPException(status_code=404, detail="Post not found")
    all_comments = [Comment(**c) for c in all_comments]

    return {
        "post":UserPost(**post_detail),
        "comment": all_comments
    }





@router.delete("/post/{post_id}")
async def delete_post(post_id:int):
    logger.info(f"Deleting post with id {post_id}")
    post = await find_post(post_id)
    if not post:
        logger.error(f"Post with post id {post_id} don't exist in the database")
        raise HTTPException(status_code=404, detail="Post not found")

    query = post_table.delete().where(post_table.c.id==post_id)
    logger.debug(query)
    await database.execute(query)
    return {"status": "deleted"}






@router.put("/comment")
async def update_comment(comment:Comment):
    comment_id = comment.id
    query = comment_table.update().values(comment.model_dump(exclude="id")).where(comment_table.c.id==comment_id)
    try:
        await database.execute(query)
    except Exception:
        raise HTTPException(status_code=404,detail=f"comment with comment_id:{comment_id} don't exist")
    return {"status":"comment updated","id":comment_id}
