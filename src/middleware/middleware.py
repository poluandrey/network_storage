import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.core.logger import logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """append request_id to request.state"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_uuid = str(uuid.uuid4())
        request.state.request_id = request_uuid
        url = request.url
        query_params = request.query_params
        logger.info(
            f'[{request_uuid}] request url: {url} query params: {query_params} user: {None} headers: {request.headers}'
        )
        response = await call_next(request)
        return response


class SetCurrentUserMiddleware(BaseHTTPMiddleware):
    """decode Authorization token and srt current_user param for request"""
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = request.headers.get('Authorization')
        print(request.user)
        response = await call_next(request)
        return response
