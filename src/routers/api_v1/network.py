from typing import List, Annotated

from fastapi import APIRouter, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from src.depends import SessionDep, GetNetworkOr404Dep, get_db, get_params
from src.models.network import Network
from src.schemas.network import NetworkBase, NetworkRead, NetworkCreate
from src.CRUD import network as network_crud
from src.auth import AuthRequiredDep, oauth2_scheme, verify_token


router = APIRouter(
  dependencies=[Depends(oauth2_scheme)]
         )


@router.get('/', response_model=List[NetworkBase | None],)
async def get_networks(request: Request, session=Depends(get_db), params=Depends(get_params), token=Depends(verify_token)) -> List[NetworkBase | None]:
    print(request.headers)
    networks = await network_crud.networks_get(session=session, **params)
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
