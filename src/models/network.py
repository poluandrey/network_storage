from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from src.database.base import Base


class Network(Base):
    __tablename__ = 'network'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('network.id'), nullable=True)
    network = Column(String, unique=True)
    comment = Column(String(length=120), nullable=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True), onupdate=func.now())

    sub_networks = relationship(
        "Network",
        remote_side=[parent_id],
        back_populates='parent_network',
        passive_deletes=True
    )
    parent_network = relationship(
        "Network",
        remote_side=[id],
        passive_deletes=True,
        back_populates='sub_networks'
    )
    device: Mapped['Device'] = relationship(secondary='network_interface', back_populates='interfaces')

    def __str__(self) -> str:
        return self.network

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: <{self.network}>'
