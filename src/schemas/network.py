from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic import networks


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
    network: networks.IPv4Network
    parent_id: int | None
    comment: str | None = None
