from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.depends import SessionDep
from src.schemas.auth import Token
from src.services.auth import authenticate_user, create_access_token

router = APIRouter()


@router.post('/')
def token(request: Request, session: SessionDep, form_data=Depends(OAuth2PasswordRequestForm)):
    user = authenticate_user(session, username=form_data.username, password=form_data.password)
    token = create_access_token(data={'sub': user.username})

    return Token(access_token=token, token_type='bearer')
