from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    username: str = Field(unique=True)
    first_name: Optional[str]
    last_name: Optional[str]
    email: str = Field(index=True, unique=True)
    age: Optional[int] = None
    phone_number: Optional[str]
    password: str
    is_active: bool
    is_superuser: bool


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
