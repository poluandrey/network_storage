from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
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

    def __str__(self):
        return self.network

    def __repr__(self):
        return f'{self.__class__.__name__}: <{self.network}>'
