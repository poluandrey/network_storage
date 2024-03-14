from typing import Optional

from pydantic import BaseModel


class ServiceBase(BaseModel):
    service_id: int
    service_name: str

    class Config:
        orm_model = True
        from_attributes = True


class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None


class ServiceCreate(BaseModel):
    service_name: str
