from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.base import Base


class Network(Base):
    __tablename__ = 'network'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('network.id'), nullable=True)
    network = Column(String, unique=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True), onupdate=func.now())

    sub_networks = relationship("Network", back_populates='parent_network')
    parent_network = relationship("Network", remote_side=[id], back_populates='sub_networks')

