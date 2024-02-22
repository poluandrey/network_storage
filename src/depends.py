from fastapi import Depends
from typing import Generator, Annotated
from sqlalchemy.orm import Session

from src.database.base import Base


def get_db() -> Generator:
    with Session(Base.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
