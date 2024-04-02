from typing import List
from models.posts import Post, PostGet, PostCreate
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select
from db.into_db import get_session
from models.users import User

router = APIRouter()


@router.get("/", response_model=List[PostGet])
def get_posts(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    statement = select(Post).offset(offset).limit(limit)
    posts = session.exec(statement).all()
    return posts


@router.post("/create", response_model=PostGet)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    owner = session.get(User, post.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="ownder is not exists.")
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/{post_id}", response_model=PostGet)
def get_single_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not exists.")
    return post
