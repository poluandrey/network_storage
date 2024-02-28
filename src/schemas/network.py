from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import IPv4Network
from typing import List


class NetworkBase(BaseModel):
    id: int
    network: str
    parent_id: int | None = None
    comment: str | None = None
    create_at: datetime
    last_update: datetime | None = None

    class Config:
        orm_model = True
        from_attributes = True


class NetworkRead(BaseModel):
    id: int
    network: str
    create_at: datetime
    last_update: datetime | None = None
    parent_network: NetworkBase | None = None
    sub_networks: List[NetworkBase | None]


class NetworkCreate(BaseModel):
    network: IPv4Network
    parent_id: int | None
    comment: str | None = None
