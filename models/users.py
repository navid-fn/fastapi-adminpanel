from pydantic import EmailStr, BaseModel, validator
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

    @validator("phone_number")
    def validate_phonen_umber(cls, v: str):
        if not v.startswith("09"):
            raise ValueError("number must start with 09")
        if not v.isdigit():
            raise ValueError("Phone number must contain numbers")
        return v


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    email: EmailStr


class UserRegister(SQLModel):
    email: EmailStr
    password: str
    username: Union[str, None] = None


class UsersOut(SQLModel):
    email: str
    username: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    age: Union[int, None]
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str
