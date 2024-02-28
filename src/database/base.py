from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from src.core.config import settings


class Base(DeclarativeBase):
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    db_session = scoped_session(sessionmaker(bind=engine, autoflush=False,))
    query = db_session.query_property()
