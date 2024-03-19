from typing import List

from fastapi import APIRouter, Depends

from src.core.auth import oauth2_scheme
from src.schemas.device import DeviceBase, DeviceUpdate, DeviceCreate
from src.depends import get_params, get_request_id, SessionDep, GetDeviceOr404Dep
from src.CRUD import device as device_crud

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)],
    tags=['device'],
)


@router.get('/', response_model=List[DeviceBase])
async def get_devices(
        session: SessionDep,
        request_id=Depends(get_request_id),
        params=Depends(get_params),
):
    devices = await device_crud.devices_get(session=session, request_id=request_id, **params)
    return devices


@router.get('/{id}', response_model=DeviceBase)
async def read_device(
        device=GetDeviceOr404Dep,
):
    device = await device_crud.device_read(device=device)
    return device


@router.put('/{id}', response_model=DeviceBase)
async def update_device(
        session: SessionDep,
        device_for_update: DeviceUpdate,
        request_id=Depends(get_request_id),
        device=GetDeviceOr404Dep,

):
    device = await device_crud.device_update(device_for_update=device_for_update, session=session, device=device,
                                             request_id=request_id)
    return device


@router.post('/', response_model=DeviceBase)
async def create_device(
        session: SessionDep,
        device: DeviceCreate,
        request_id=Depends(get_request_id),
):
    device = await device_crud.device_create(session=session, device=device, request_id=request_id)
    return device
