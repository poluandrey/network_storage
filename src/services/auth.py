from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from src.core.config import settings
from src.models.user import User


def authenticate_user(session: Session, username: str, password: str):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user does not exists')

    if not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect password')

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
