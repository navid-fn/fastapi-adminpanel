from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional, Union


class UserBase(SQLModel):
    username: str = Field(unique=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: str = Field(index=True, unique=True)
    age: Optional[int] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    is_active: bool = True
    is_superuser: bool = False
    password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRegister(SQLModel):
    email: str
    password: str
    username: Union[str, None] = None


class UsersOut(SQLModel):
    email: str
    username: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    age: Union[str, None]
