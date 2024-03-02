from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt

from src.models.user import User
from src.schemas.auth import Token
from src.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


AuthRequiredDep = Annotated[str, Depends(oauth2_scheme)]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str):
    user = session.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user does not exists')

    if not verify_password(password, user.userpassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect password')

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': settings.ACCESS_TOKEN_EXPIRE_MINUTES})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt




