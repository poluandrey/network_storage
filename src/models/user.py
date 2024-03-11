from sqlalchemy import Column, String, DateTime, Boolean, Integer
from src.database.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=20), unique=True, nullable=False)
    userpassword = Column(String(length=120), nullable=False)
    is_active = Column(Boolean)
    last_login = Column(DateTime(timezone=True))


    def get_password_hash(self):
        pass

