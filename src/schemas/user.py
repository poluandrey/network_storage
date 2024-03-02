from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    username: str
    is_active: bool
    last_login: datetime | None = None
