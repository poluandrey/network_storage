from fastapi import APIRouter

from src.depends import SessionDep


router = APIRouter()


@router.get('/')
async def networks(session: SessionDep, skip: int = 0, limit: int = 0):
    pass
