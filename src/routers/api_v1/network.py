from typing import List

from fastapi import APIRouter, status

from src.depends import SessionDep, GetNetworkOr404Dep
from src.models.network import Network
from src.schemas.network import NetworkBase, NetworkRead, NetworkCreate
from src.CRUD import network as network_crud


router = APIRouter()


@router.get('/', response_model=List[NetworkBase | None])
async def get_networks(session: SessionDep, offset: int = 0, limit: int = 100) -> List[NetworkBase | None]:
    networks = await network_crud.networks_get(session=session, offset=offset, limit=limit)
    return networks


@router.get(path='/{id}', response_model=NetworkRead)
async def network_read(network: Network = GetNetworkOr404Dep) -> NetworkRead:
    network = await network_crud.network_read(network)
    return network


@router.post(path='/', response_model=NetworkBase, status_code=status.HTTP_201_CREATED)
async def network_create(session: SessionDep, network: NetworkCreate) -> NetworkBase:
    network = await network_crud.network_create(session, network)
    return network


@router.delete(path='/{id}', status_code=status.HTTP_200_OK)
async def network_delete(session: SessionDep, network: Network = GetNetworkOr404Dep) -> None:
    await network_crud.network_delete(session, network)


@router.post(path='/{id}/split/by_host', response_model=List[NetworkBase | None])
async def network_split_by_host(session: SessionDep, network: Network = GetNetworkOr404Dep) -> List[NetworkBase | None]:
    networks = await network_crud.network_split_by_host(session, network)
    return networks


@router.post(path='/{id}/split', response_model=List[NetworkBase | None])
async def network_split(
        session: SessionDep,
        network_prefix: int,
        network: Network = GetNetworkOr404Dep,
) -> List[NetworkBase | None]:
    networks = await network_crud.network_split(session, network, network_prefix)
    return networks
