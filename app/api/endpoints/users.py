from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.users import UserCreate, UserRegister, UserUpdate, UsersOut, User
from db.into_db import get_session
from sqlmodel import select, Session, or_
import crud.user as crud_user

router = APIRouter()


@router.post("/create", response_model=UsersOut)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    ).first():
        raise HTTPException(status_code=200, detail="repeated email or username")
    return crud_user.create_user(session=session, user_create=user)


@router.get("/", response_model=List[UsersOut])
async def read_active_users(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    statement = select(User).where(User.is_active == True).offset(offset).limit(limit)
    users = session.exec(statement).all()
    return users


@router.post("/register", response_model=UsersOut)
async def register_user(user: UserRegister, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=200, detail="This Email is already in used")
    return crud_user.create_user(session=session, user_create=user)


@router.post("/{user_id}/update", response_model=UsersOut)
async def update_user(
    user_id: int, user: UserUpdate, session: Session = Depends(get_session)
):

    if session.exec(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    ).first():
        raise HTTPException(status_code=200, detail="repeated email or username")
    user_obj = crud_user.update_user(user_id=user_id, user_update=user, session=session)
    if not user_obj:
        raise HTTPException(status_code=404, detail="No user Found")
    return user_obj
