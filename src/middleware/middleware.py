import uuid

from fastapi import HTTPException, status
from jose import jwt, JWTError
from starlette.authentication import AuthenticationBackend, UnauthenticatedUser, AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.core.config import settings
from src.core.logger import logger
from src.depends import get_db
from src.models.user import User


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """append request_id to request.state"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_uuid = str(uuid.uuid4())
        request.state.request_id = request_uuid
        url = request.url
        query_params = request.query_params
        if isinstance(request.user, UnauthenticatedUser):
            username = 'anonim'
        else:
            username = request.user.username
        logger.info(
            f'[{request_uuid}] request url: {url} query params: {query_params} user: {username} headers: {request.headers}'
        )
        response = await call_next(request)
        return response


class JWTAuthMiddleware(AuthenticationBackend):
    """decode Authorization token and srt current_user param for request"""

    async def authenticate(
        self,
        request: Request,
    ) -> Response:
        if 'authorization' not in request.headers:
            return

        token = request.headers.get('Authorization').split(' ')[-1]
        session = next(get_db())
        try:
            auth = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except JWTError:
            raise AuthenticationError('invalid token')

        username: str = auth.get('sub')
        user = session.query(User).filter(User.username == username).first()

        return auth, user
