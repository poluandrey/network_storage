from pydantic import BaseModel


class ServiceBase(BaseModel):
    service_name: str

    class Config:
        from_attributes = True


class Service(ServiceBase):
    id: int

    class Config:
        orm_model = True
