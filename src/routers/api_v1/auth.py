from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.depends import SessionDep
from src.auth import authenticate_user, create_access_token
from src.schemas.auth import Token

router = APIRouter()


@router.post('/')
def token(session: SessionDep, form_data=Depends(OAuth2PasswordRequestForm)):
    user = authenticate_user(session, username=form_data.username, password=form_data.password)
    token = create_access_token(data={'sub': user.username})
    return Token(token=token, token_type='bearer')
