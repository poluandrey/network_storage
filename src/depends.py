from fastapi import Depends
from typing import Generator, Annotated
from sqlalchemy.orm import Session

from src.database.engine import engine


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
