from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.core.config import settings
from src.routers.api_router_v1 import router
from src.middleware.middleware import RequestLoggerMiddleware, JWTAuthMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthMiddleware())

app.include_router(router, prefix='/api/v1')
