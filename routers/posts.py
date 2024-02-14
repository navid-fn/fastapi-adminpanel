from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_posts():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_my_posts():
    return {"username": "fakecurrentuser"}


@router.get("/{post_id}")
async def read_user(post_id: str):
    return {"username": post_id}