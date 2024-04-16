from typing import Any

from pydantic import EmailStr
from sqlmodel import Session, select

from app.configs.security import get_password_hash, verify_password
from app.models.users import User, UserCreate, UserRegister, UserUpdate


def get_user_by_email(session: Session, email: EmailStr) -> Any:
    user = select(User).where(User.email == email)
    return session.exec(user).first()


def create_user(session: Session, user_create: UserCreate | UserRegister) -> User:
    db_obj = User.model_validate(
        user_create, update={"password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> Any:
    user = session.get(User, user_id)
    if not user:
        return None
    user_data = user_update.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["password"] = hashed_password

    user.sqlmodel_update(user_data, update=extra_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(session: Session, username: str, password: str):
    db_user = get_user_by_email(session, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user
