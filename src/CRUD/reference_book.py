from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.logger import logger
from src.models.reference_book import Service
from src.schemas.reference_book import ServiceBase


async def services_get(session: Session, request_id: str, offset: int = 0, limit: int = 100):
    logger.info(f'[{request_id}] start handling')
    services = session.query(Service).offset(offset).limit(limit)
    logger.info(f'[{request_id}] finish handling')
    return services


async def service_create(session: Session, request_id: str, service: ServiceBase):
    logger.info(f'[{request_id}] start handling')
    logger.info(f'[{request_id}] create service: {service.json()}')

    if session.query(Service).filter(Service.service_name == service.service_name).first():
        logger.warning(f'[{request_id}] service already exists')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='service already exists')

    service_obj = Service(**service.model_dump())
    session.add(service_obj)
    session.commit()
    session.refresh(service_obj)
    logger.info(f'[{request_id}] finish handling')
    return service_obj


async def service_update(session: Session, request_id: str, service: Service, service_for_update: ServiceBase):
    logger.info(f'[{request_id}] start handling')
    service.service_name = service_for_update.service_name
    session.commit()
    session.refresh(service)
    logger.info(f'[{request_id}] finish handling')
    return service


async def service_delete(session, service: Service, request_id):
    logger.info(f'[{request_id}] start handling')
    if service.devices:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Device with {service.service_name} service exists'
        )

    session.delete(service)
    logger.info(f'[{request_id}] finish handling')
    return
