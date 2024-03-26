from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.device import Device
from src.models.reference_book import Service
from src.core.logger import logger
from src.schemas.device import DeviceBase, DeviceUpdate, DeviceCreate, DeviceInterface
from src.validators.device import NetworkInterfaceValidator


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
    service = None
    device_obj = Device(
        name=device.name
    )

    if device.service:
        service = session.get(Service, device.service)
        if not service:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='service does not exists')

    network_validator = NetworkInterfaceValidator()
    network_validator.validate(session=session, networks_id=device.interfaces)
    network_validator.raise_error()

    validated_data = network_validator.data.valid_interfaces

    device_obj.interfaces = validated_data
    device_obj.service = service

    session.add(device_obj)
    session.commit()
    session.refresh(device_obj)

    return device_obj.to_base_model()


async def device_add_networks(
        session: Session,
        device: Device,
        networks_id: DeviceInterface,
) -> DeviceBase:

    validator = NetworkInterfaceValidator()
    validator.validate(session=session, networks_id=networks_id.networks_id)
    validator.raise_error()
    validated_data = validator.data.valid_interfaces

    device.interfaces.extend(validated_data)
    session.commit()
    return device.to_base_model()
