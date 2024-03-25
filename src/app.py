import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.core.config import settings
from src.middleware.middleware import (JWTAuthMiddleware,
                                       RequestLoggerMiddleware)
from src.routers.api_router_v1 import router


sentry_sdk.init(
    dsn='https://06ba225e07693e59ad9a5675dfbdf962@o4506947982065664.ingest.us.sentry.io/4506947984097280',
    enable_tracing=True,
    profiles_sample_rate=1.0,
    traces_sample_rate=1.0,
)


app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthMiddleware())


app.include_router(router, prefix='/api/v1')
