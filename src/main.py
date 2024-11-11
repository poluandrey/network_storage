from fastapi import FastAPI
from fastapi import APIRouter

router = APIRouter()


@router.get("/networks")
async def get_items():
    return [{"network_id": 1, "name": "LANCK", "ip": "89.31.240.234"}]


app = FastAPI()
app.include_router(router)

