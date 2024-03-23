from typing import List

from fastapi import APIRouter, Depends, status

from src.core.auth import oauth2_scheme
from src.CRUD import network as network_crud
from src.depends import (GetNetworkOr404Dep, SessionDep, get_db, get_params,
                         get_request_id)
from src.models.network import Network
from src.schemas.network import (NetworkBase, NetworkCreate, NetworkRead,
                                 NetworkSplit)

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)],
    tags=['network']
)


@router.get('/', response_model=List[NetworkBase | None], )
async def get_networks(
        session=Depends(get_db),
        params=Depends(get_params),
        request_id=Depends(get_request_id),
) -> List[NetworkBase | None]:
    networks = await network_crud.networks_get(session=session, request_id=request_id, **params)
    return networks


@router.get(path='/{id}', response_model=NetworkRead)
async def network_read(
        request_id=Depends(get_request_id),
        network: Network = GetNetworkOr404Dep,
) -> NetworkRead:
    network = await network_crud.network_read(network, request_id)
    return network


@router.post(
    path='/',
    response_model=NetworkBase,
    status_code=status.HTTP_201_CREATED
)
async def network_create(
        session: SessionDep,
        network: NetworkCreate,
        request_id=Depends(get_request_id)
) -> NetworkBase:
    network = await network_crud.network_create(session, network, request_id)
    return network


@router.delete(path='/{id}', status_code=status.HTTP_200_OK)
async def network_delete(
        session: SessionDep,
        network: Network = GetNetworkOr404Dep,
        request_id=Depends(get_request_id)
) -> None:
    await network_crud.network_delete(session, network, request_id)


@router.post(path='/{id}/split/by_host', response_model=NetworkSplit)
async def network_split_by_host(
        session: SessionDep,
        network: Network = GetNetworkOr404Dep,
        request_id=Depends(get_request_id)
) -> List[NetworkBase | None]:
    networks = await network_crud.network_split_by_host(session, network, request_id)
    return networks


@router.post(path='/{id}/split', response_model=NetworkSplit)
async def network_split(
        session: SessionDep,
        network_prefix: int,
        network: Network = GetNetworkOr404Dep,
        request_id=Depends(get_request_id),
) -> List[NetworkBase | None]:
    networks = await network_crud.network_split(session, network, network_prefix, request_id)
    return networks
