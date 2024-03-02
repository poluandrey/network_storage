from fastapi import FastAPI

from src.core.config import settings
from src.routers.api_router_v1 import router

app = FastAPI(
    title=settings.PROJECT_NAME,
)


app.include_router(router, prefix='/api/v1')
