from typing import List

from fastapi import APIRouter, Depends, status

from src.depends import get_params, get_request_id, SessionDep, GetServiceOr404Dep
from src.schemas.reference_book import ServiceBase, Service
from src.CRUD import reference_book
from src.core.auth import oauth2_scheme

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)],
)

service_router = APIRouter(
    prefix='/service'
)


@service_router.get('/', response_model=List[Service], tags=['service'])
async def get_services(
        session: SessionDep,
        params=Depends(get_params),
        request_id=Depends(get_request_id),
):
    services = await reference_book.services_get(session=session, request_id=request_id, **params)
    return services


@service_router.get(path='/{id}', response_model=Service, tags=['service'])
async def read_service(
        service=GetServiceOr404Dep
):
    return service


@service_router.post(path='/', response_model=Service, tags=['service'], status_code=status.HTTP_201_CREATED)
async def create_service(
        session: SessionDep,
        service: ServiceBase,
        request_id=Depends(get_request_id),
):
    service = await reference_book.service_create(session, request_id, service)
    return service


@service_router.put(path='/{id}', tags=['service'], response_model=Service)
async def update_service(
        service_for_update: ServiceBase,
        session: SessionDep,
        service=GetServiceOr404Dep,
        request_id=Depends(get_request_id)
):
    service = await reference_book.service_update(session, request_id=request_id, service=service, service_for_update=service_for_update)
    return service


@service_router.delete(path='/{id}', tags=['service'], status_code=status.HTTP_200_OK)
async def delete_service(session: SessionDep, service_for_delete=GetServiceOr404Dep, request_id=Depends(get_request_id)):
    await reference_book.service_delete(session, service=service_for_delete, request_id=request_id)
    return

router.include_router(service_router)
