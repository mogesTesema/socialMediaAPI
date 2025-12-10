from fastapi import APIRouter, HTTPException, Depends, status
from storeapi.models.user import User
from storeapi.security.user_security import get_current_user, is_confirmed
from storeapi.utilits.formatted_printer import print_better as better_print  # noqa
from storeapi.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    PostLikeIn,
    PostLike,
    UserPostWithLike,
    UserPostWithComments,
)
from storeapi.database import database, post_table, comment_table, like_table
from sqlalchemy import select
import sqlalchemy
import logging
from typing import Annotated
from enum import Enum


router = APIRouter()

logger = logging.getLogger(__name__)
comment_dict = {}
post_dict = {}

select_liked_post = (
    sqlalchemy.select(post_table, sqlalchemy.func.count(like_table.c.id).label("likes"))
    .select_from(post_table.outerjoin(like_table))
    .group_by(post_table.c.id)
)


@router.get("/")
async def root():
    return {"message": "well come!"}


async def find_post(post_id: int):
    logger.info(f"Finding post with id {post_id}")
    query = select(post_table.c.id).where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query=query)


@router.post("/post", status_code=status.HTTP_201_CREATED)
async def mock_post(body: UserPostIn):
    index = len(post_dict)
    post_dict[str(index)] = body.body
    return {"id": index, "body": body.body}


@router.post("/posts", response_model=UserPost)
async def create_post(
    post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]
):
    """
    this post endpoint is going to insert posts into database from clients post request
    """
    logger.info(f"creating user post with details: {post}")
    # noqa
    if not await is_confirmed(current_user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="your email is not confirmed, please check your spam folder and confirm your email.",
        )
    data = {**post.model_dump(), "user_id": current_user.id}
    logger.debug(data)
    query = post_table.insert().values(data)
    logger.debug(query)
    try:
        post_id = await database.execute(query=query)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error due to database crash"
        )
    new_post = {**data, "id": post_id}
    return new_post


@router.post("/comment", response_model=Comment)
async def comment_post(
    comment: CommentIn, current_user: Annotated[User, Depends(get_current_user)]
):
    """
    this endpoint is ganna insert comment into database
    """
    logger.info(f"creating comment with details:{comment}")
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post doesn't exist")
    comment = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(comment)
    logger.debug(query)
    try:
        comment_id = await database.execute(query)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"internal server error, database crash\n{str(e)}"
        )

    unique_comment = {**comment, "id": comment_id}
    return unique_comment


@router.get("/post/{post_id}", response_model=UserPost)
async def get_post(post_id: int):
    logger.info("geting user post with id {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    post_content = await database.fetch_one(query)
    if post_content:
        return UserPost(**post_content)
    else:
        raise HTTPException(
            status_code=404, detail=f"post with post_id:{post_id} doesn't exist"
        )


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    most_liked = "likes"


@router.get("/posts", response_model=list[UserPostWithLike])
async def get_posts(sorting: PostSorting = PostSorting.new):
    """
    this endpoint gonna retrive data from database and then send those retrieved data back to client
    """
    logger.info("getting all posts up to 50 recent posts")
    if sorting == PostSorting.new:
        query = select_liked_post.order_by(sqlalchemy.desc(post_table.c.id))

    elif sorting == PostSorting.old:
        query = select_liked_post.order_by(sqlalchemy.asc(post_table.c.id))

    else:
        query = select_liked_post.order_by(sqlalchemy.desc("likes"))
    logger.debug(query)
    logger.debug(query)
    try:
        all_posts = await database.fetch_all(query=query)
    except Exception:
        raise HTTPException(status_code=500, detail="insternal server crash")
    return all_posts


@router.get("/post/{post_id}/comments", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    """
    this endpoint is unique, it combines post and comment property that leads to foreign relation between those tables
    """
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    logger.debug(query)

    try:
        all_comments = await database.fetch_all(query)

    except Exception:
        raise HTTPException(status_code=404)

    post_query = select_liked_post.where(post_table.c.id == post_id)
    try:
        post_detail = await database.fetch_one(post_query)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="intrnal server error due to database crash when fetching post_text",
        )
    if not post_detail:
        raise HTTPException(status_code=404, detail="Post not found")
    all_comments = [Comment(**c) for c in all_comments]
    post_detail = {
        "id": post_id,
        "user_id": post_detail.user_id,
        "body": post_detail.body,
        "likes": 0,
    }

    return {"post": post_detail, "comment": all_comments}


@router.delete("/post/{post_id}")
async def delete_post(post_id: int):
    logger.info(f"Deleting post with id {post_id}")
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    query = post_table.delete().where(post_table.c.id == post_id)
    logger.debug(query)
    await database.execute(query)
    return {"status": "deleted"}


@router.put("/comment")
async def update_comment(comment: Comment):
    comment_id = comment.id
    query = (
        comment_table.update()
        .values(comment.model_dump(exclude="id"))
        .where(comment_table.c.id == comment_id)
    )
    try:
        await database.execute(query)
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"comment with comment_id:{comment_id} don't exist"
        )
    return {"status": "comment updated", "id": comment_id}


@router.post("/like", status_code=status.HTTP_201_CREATED, response_model=PostLike)
async def like_post(
    postlike: PostLikeIn, liker: Annotated[User, Depends(get_current_user)]
):
    logger.debug("Liking post")
    post = await find_post(postlike.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    data = {**postlike.model_dump(), "user_id": liker.id}
    like_query = like_table.insert().values(data)
    logger.debug(like_query)

    result = await database.execute(like_query)

    return {"id": result, "post_id": postlike.post_id, "user_id": liker.id}
