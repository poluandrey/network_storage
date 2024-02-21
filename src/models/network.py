from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.database.base import Base


class Network(Base):
    __tablename__ = 'network'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    network = Column(String, unique=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True), onupdate=func.now())


