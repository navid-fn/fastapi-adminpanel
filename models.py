from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    age: Optional[int] = None
    phone_number: str
    password: str


class Post(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    owner_id : Optional[int] = Field(default=None, foreign_key="user.id")
