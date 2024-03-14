from typing import List

from pydantic import BaseModel
from datetime import datetime

from src.schemas.network import NetworkBase
from src.schemas.reference_book import ServiceBase


class DeviceBase(BaseModel):
    id: int
    name: str
    service: ServiceBase | None = None
    interfaces: List[NetworkBase | None] = []
    created_ad: datetime
    last_update: datetime

    class Config:
        orm_model = True
        from_attributes = True
