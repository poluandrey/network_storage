from typing import List

from fastapi import APIRouter, Depends

from src.depends import get_db, get_params, get_request_id, SessionDep
from src.schemas.reference_book import ServiceBase, ServiceUpdate
from src.core.auth import oauth2_scheme

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)],
)


@router.get('/', response_model=List[ServiceBase], tags=['service'])
async def get_services(
        session=SessionDep,
        params=Depends(get_params),
        request_id=Depends(get_request_id),
):
    pass


@router.get(path='/{id}', response_model=ServiceBase, tags=['service'])
async def read_service(
        id: int,
        session=SessionDep,
        params=Depends(get_params),
        request_id=Depends(get_request_id),
):
    pass


@router.post(path='/', response_model=ServiceBase, tags=['service'])
async def create_service(
        session=SessionDep,
        request_id=Depends(get_request_id),
):
    pass


@router.patch(path='/{id}', tags=['service'])
async def update_service(
        id: int,
        service: ServiceUpdate,
        session=SessionDep,
):
    pass
