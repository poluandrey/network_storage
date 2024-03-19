from typing import List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from src.database.base import Base
from src.schemas.device import DeviceBase


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, unique=True, index=True, primary_key=True)
    name = Column(String(length=120), nullable=False)
    service_id = Column(ForeignKey('service.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True), server_onupdate=func.now())

    interfaces: Mapped[List['Network']] = relationship(secondary='network_interface', back_populates='device')
    service = relationship('Service', back_populates='devices')

    def to_base_model(self):
        return DeviceBase(
            id=self.id,
            name=self.name,
            service=self.service.service_name if self.service else None,
            interfaces=self.interfaces,
            create_at=self.created_at,
            last_update=self.last_update,
        )


class NetworkInterface(Base):
    __tablename__ = 'network_interface'

    id = Column(Integer, unique=True, primary_key=True, index=True)
    device_id = Column(ForeignKey('device.id'),)
    ip_addresses = Column(ForeignKey('network.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True), server_onupdate=func.now())
