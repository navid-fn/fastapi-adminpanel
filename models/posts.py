from sqlmodel import SQLModel, Field
from typing import Optional


class PostBase(SQLModel):
    title: str
    description: str
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass

class PostGet(PostBase):
    id: int
