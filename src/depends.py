from typing import Annotated, Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.core.logger import logger
from src.database.base import Base
from src.models.network import Network


def get_request_id(request: Request) -> str:
    return request.state.request_id


def get_db() -> Generator:
    yield Base.db_session


SessionDep = Annotated[Session, Depends(get_db)]


class GetNetworkOr404:

    async def __call__(self, id: int, session: SessionDep, request_id=Depends(get_request_id)):
        logger.info(f'[{request_id}] start getting network with id: {id}')
        network = session.get(Network, id)
        if not network:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='network does not exists')

        return network


GetNetworkOr404Dep = Depends(GetNetworkOr404())


def get_params(offset: int = 0, limit: int = 100):
    return {'offset': offset, 'limit': limit}
