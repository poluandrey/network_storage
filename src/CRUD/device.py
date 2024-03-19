from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.reference_book import Service
from src.core.logger import logger
from src.schemas.device import DeviceBase, DeviceUpdate, DeviceCreate
from src.validators.device import device_create_network_validator


async def devices_get(session: Session, request_id: str, limit: int, offset: int):
    logger.info(f'[{request_id}] start handling')
    devices = session.query(Device).offset(offset).limit(limit)
    devices = [device.to_base_model() for device in devices]
    logger.info(f'[{request_id}] finished handling')
    return devices


async def device_read(device):
    return device.to_base_model()


async def device_update(
        session: Session,
        device_for_update: DeviceUpdate,
        device: Device,
        request_id: str,
) -> DeviceBase:
    logger.info(f'[{request_id}] start handling')
    device.name = device_for_update.name if device_for_update.name else device.name
    device.service_id = device_for_update.service if device_for_update.service else device.service_id
    session.commit()
    session.refresh(device)
    logger.info(f'[{request_id}] finished handling')
    return device.to_base_model()


async def device_create(
        session: Session,
        device: DeviceCreate,
        request_id: str,
):
    device_obj = Device(
        name=device.name
    )

    if device.service:
        service = session.get(Service, device.service)
        if not service:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='service does not exists')

    validate_data = device_create_network_validator(device.interfaces)

    if validate_data.not_exists_interfaces:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'networks does not exists: {validate_data.not_exists_interfaces}'
        )

    if validate_data.invalid_interfaces:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'invalid networks for host: {validate_data.valid_interfaces}'
        )

    device_obj.interfaces = validate_data.valid_interfaces
    device_obj.service = service

    session.add(device_obj)
    session.commit()
    session.refresh(device_obj)

    return device_obj.to_base_model()


async def device_add_network(
        session: Session,
        device: Device,
        request_id: int,
):
    pass
