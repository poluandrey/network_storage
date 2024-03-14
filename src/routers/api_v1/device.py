from typing import List

from fastapi import APIRouter, Depends

from src.core.auth import oauth2_scheme
from src.schemas.device import DeviceBase
from src.depends import get_params, get_request_id, SessionDep

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)],
    tags=['device'],
)


@router.get('/', response_model=List[DeviceBase])
async def get_devices(
        session=SessionDep,
        request_id=Depends(get_request_id),
        params=Depends(get_params),
):
    pass
