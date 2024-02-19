from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.users import UserCreate, UserRegister, UsersOut, User
from db.into_db import get_session
from sqlmodel import select, Session, or_
from security import get_password_hash

router = APIRouter()

 
@router.post("/create", response_model=UsersOut)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    ).first():
        raise HTTPException(status_code=200, detail="repeated email or username")
    user.password = get_password_hash(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


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
    user.password = get_password_hash(user.password)
    user.username = user.email
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

