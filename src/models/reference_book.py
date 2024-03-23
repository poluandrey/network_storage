from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.database.base import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(length=120), unique=True)

    devices = relationship('Device', back_populates='service')

    def __str__(self) -> str:
        return self.service_name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: <{self.service_name}>'
