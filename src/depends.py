from fastapi import Depends, HTTPException, status
from typing import Generator, Annotated
from sqlalchemy.orm import Session

from src.database.base import Base


def get_db() -> Generator:
    # with Session(Base.engine) as session:
    #     yield session
    yield Base.db_session


SessionDep = Annotated[Session, Depends(get_db)]


def get_obj_or_raise_error(session: SessionDep, id: int, model):
    obj = session.get(model, id)

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object not found')
    return obj


GetObjectDep = Annotated[Base, Depends(get_obj_or_raise_error)]
