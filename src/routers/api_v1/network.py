from typing import List

from fastapi import APIRouter, status

from src.depends import SessionDep
from src.schemas.network import NetworkBase, NetworkRead, NetworkCreate
from src.CRUD import network as network_crud


router = APIRouter()


@router.get('/', response_model=List[NetworkBase])
async def get_networks(session: SessionDep, offset: int = 0, limit: int = 100):
    networks = await network_crud.networks_get(session=session, offset=offset, limit=limit)
    return networks


@router.get(path='/{id}', response_model=NetworkRead)
async def network_read(session: SessionDep, id: int):
    network = await network_crud.network_read(session, id)
    return network


@router.post(path='/', response_model=NetworkBase, status_code=status.HTTP_201_CREATED)
async def network_read(session: SessionDep, network: NetworkCreate):
    network = await network_crud.network_create(session, network)
    return network


@router.delete(path='/{id}', status_code=status.HTTP_200_OK)
async def network_delete(session: SessionDep, id: int):
    await network_crud.network_delete(session, id)
