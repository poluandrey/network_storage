from fastapi import APIRouter

from src.routers.api_v1 import auth, network, reference_book, device

router = APIRouter()

router.include_router(network.router, prefix='/networks',)
router.include_router(auth.router, prefix='/auth')
router.include_router(reference_book.router, prefix='/ref_book')
router.include_router(device.router, prefix='/device')
