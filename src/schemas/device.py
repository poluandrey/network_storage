from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from src.schemas.network import NetworkBase
from src.schemas.reference_book import ServiceBase


class DeviceBase(BaseModel):
    id: int
    name: str
    service: Optional[str] = None
    interfaces: List[NetworkBase | None] = []
    created_at: datetime = None
    last_update: Optional[datetime] = None

    class Config:
        orm_model = True
        from_attributes = True


class DeviceUpdate(BaseModel):
    name: str


class DeviceCreate(BaseModel):
    name: str
    service: Optional[int] = None
    interfaces: List[Optional[int]]

