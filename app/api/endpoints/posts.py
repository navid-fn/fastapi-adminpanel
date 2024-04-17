from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud import post as post_crud
from app.models.posts import Post, PostCreate, PostGet, PostUpdate
from app.models.users import User

router = APIRouter()


@router.get("/", response_model=List[PostGet])
def get_posts(session: SessionDep, offset: int = 0, limit: int = 100):
    statement = select(Post).offset(offset).limit(limit)
    posts = session.exec(statement).all()
    return posts


@router.post("/create", response_model=PostGet)
def create_post(session: SessionDep, post_create: PostCreate):
    owner = session.get(User, post_create.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="ownder is not exists.")
    return post_crud.create_post(session, post_create)


@router.get("/{post_id}", response_model=PostGet)
def get_single_post(session: SessionDep, post_id: int):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not exists.")
    return post


@router.patch("/{post_id}/update", response_model=PostGet)
def update_post(session: SessionDep, post_id: int, post_data: PostUpdate):
    db_post = post_crud.update_post(session, post_id, post_data)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return db_post


@router.delete("/post_id/delete")
def delete_post(session: SessionDep, post_id: int):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    post_crud.delete_post(session, db_post)
    return {"detail": "success"}
