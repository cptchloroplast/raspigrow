from fastapi import APIRouter
from . import sensor

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(sensor.router)
