from typing import Any, Generic, Type, TypeVar
from fastapi import Depends
from sqlmodel import Session
from db.into_db import get_session


ModelType = TypeVar("ModelType", bound=Any)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def filter_by_id(id: int, db: Session = Depends(get_session)):
        pass
