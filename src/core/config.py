from pathlib import Path

from pydantic import PostgresDsn, computed_field, Extra
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    LOGGER_CONFIG: str = f'{BASE_DIR}/logging.conf'

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str: #ignore
        return str(PostgresDsn.build(
            scheme='postgresql+psycopg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))

    class Config:
        case_sensitive = True
        env_file = f'{BASE_DIR}/.env'
        extra = Extra.allow


settings = Settings()
