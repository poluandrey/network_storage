from fastapi import APIRouter

from src.routers.api_v1 import auth, network

router = APIRouter()

router.include_router(network.router, prefix='/networks',)
router.include_router(auth.router, prefix='/auth')
