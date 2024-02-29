from fastapi import Depends, HTTPException, status
from typing import Generator, Annotated
from sqlalchemy.orm import Session

from src.database.base import Base
from src.models.network import Network


def get_db() -> Generator:
    # with Session(Base.engine) as session:
    #     yield session
    yield Base.db_session


SessionDep = Annotated[Session, Depends(get_db)]


class GetNetworkOr404:

    async def __call__(self, id: int, session: SessionDep):
        network = session.get(Network, id)
        if not network:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='network does not exists')

        return network


GetNetworkOr404Dep = Depends(GetNetworkOr404())
