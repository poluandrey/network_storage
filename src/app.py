from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.auth import BasicAuthBackend
from src.core.config import settings
from src.routers.api_router_v1 import router
from src.middleware.middleware import RequestLoggerMiddleware, SetCurrentUserMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    middleware=[Middleware(AuthenticationMiddleware, backend=BasicAuthBackend)]
)

# middlewares = [RequestLoggerMiddleware, SetCurrentUserMiddleware]
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(SetCurrentUserMiddleware)
app.include_router(router, prefix='/api/v1')
