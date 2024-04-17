from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import or_, select

import app.crud.user as crud_user
from app.api.deps import IsSuperUser, SessionDep
from app.models.users import (User, UserCreate, UserRegister, UsersOut,
                              UserUpdate)

router = APIRouter()


@router.post("/create", response_model=UsersOut, dependencies=[IsSuperUser])
async def create_user(user: UserCreate, session: SessionDep):
    if session.exec(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    ).first():
        raise HTTPException(status_code=200, detail="repeated email or username")
    return crud_user.create_user(session=session, user_create=user)


@router.get("/", response_model=List[UsersOut], dependencies=[IsSuperUser])
async def read_active_users(session: SessionDep, offset: int = 0, limit: int = 100):
    statement = (
        select(User)
        .where(User.is_active == True)
        .offset(offset)
        .limit(limit)
        .order_by(User.id)
    )
    users = session.exec(statement).all()
    return users


@router.post("/register", response_model=UsersOut, dependencies=[IsSuperUser])
async def register_user(user: UserRegister, session: SessionDep):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=200, detail="This Email is already in used")
    return crud_user.create_user(session=session, user_create=user)


@router.patch(
    "/{user_id}/update",
    response_model=UsersOut,
)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
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


@router.get("/{user_id}/", response_model=UsersOut, dependencies=[IsSuperUser])
def read_single_user(session: SessionDep, user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/user_id/delete")
def delete_user(session: SessionDep, user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    crud_user.delete_user(session, db_user)
