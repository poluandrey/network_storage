from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")
AuthRequiredDep = Annotated[str, Depends(oauth2_scheme)]

# async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         username: str = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return True
