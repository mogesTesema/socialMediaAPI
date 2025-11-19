from fastapi import APIRouter
from storeapi.models.post import UserPost,UserPostIn


router = APIRouter()


"installing Linux as professional"
post_table = {}


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


@router.get("/posts", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
