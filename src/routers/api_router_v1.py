from fastapi import APIRouter

from src.routers.api_v1 import network


router = APIRouter()

router.include_router(network.router, prefix='/networks')
