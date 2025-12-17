from pydantic import BaseModel
from typing import Optional


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int
    user_id: int = None
    image_url: Optional[str] = None


class UserPostWithLike(UserPost):
    likes: int

    class config:
        orm_model: True


class CommentIn(BaseModel):
    body: str
    post_id: int
    user_id: int = None


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPostWithLike
    comment: list[Comment]


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    user_id: int
    id: int

    """
    user_post has:-
        body: string
        post_id: int,unique for every single post
    user_comment has:-
        body:string
        post_id:int match with anyone of already posted on user_post,relation
        comment_id:int,unique for every single comment

    user_post_with_comments:-
        here we gonna to filter the post and then retrieve comments on this post: retrieve all comment where post_id is given post id

    """
