from pydantic import BaseModel


class UserPostIn(BaseModel):
    body:str

class UserPost(UserPostIn):
    id:int

class CommentIn(BaseModel):
    body:str
    post_id:int

class Comment(CommentIn):
    id:int

class UserPostWithComments(BaseModel):
    post: UserPost
    comment:list[Comment]


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