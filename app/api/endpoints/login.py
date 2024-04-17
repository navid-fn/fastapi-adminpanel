from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.configs.security import create_access_token
from app.crud.user import authenticate
from app.models.users import Token

router = APIRouter()


@router.post("/login/access-token")
async def login_user(
    session: SessionDep, login_form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db_user = authenticate(session, login_form.username, login_form.password)
    if not db_user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authorization Failed"
        )
    return Token(
        access_token=create_access_token(db_user.id),
    )
