from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.database.base import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(length=120), unique=True)

    devices = relationship('Device', back_populates='service')
