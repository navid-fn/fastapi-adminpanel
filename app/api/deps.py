from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.configs.security import ALGORITHM
from app.configs.settings import settings
from app.db.into_db import get_session
from app.models.users import TokenPayload, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except Exception as e:
        raise credentials_exception
    user = session.get(User, token_data.sub)
    if not user:
        raise user_not_found_exception
    return user


CurrenctUser = Annotated[User, Depends(get_current_user)]


def get_current_super_user(user: CurrenctUser):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user.is_superuser:
        raise credentials_exception
    return user


IsSuperUser = Depends(get_current_super_user)
