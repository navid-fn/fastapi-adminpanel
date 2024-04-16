from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.crud import post as post_crud
from app.db.into_db import get_session
from app.models.posts import Post, PostCreate, PostGet
from app.models.users import User

router = APIRouter()


@router.get("/", response_model=List[PostGet])
def get_posts(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    statement = select(Post).offset(offset).limit(limit)
    posts = session.exec(statement).all()
    return posts


@router.post("/create", response_model=PostGet)
def create_post(post_create: PostCreate, session: Session = Depends(get_session)):
    owner = session.get(User, post_create.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="ownder is not exists.")
    return post_crud.create_post(session, post_create)


@router.get("/{post_id}", response_model=PostGet)
def get_single_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not exists.")
    return post
