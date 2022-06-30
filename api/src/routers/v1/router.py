from fastapi import APIRouter
from . import stream

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(stream.router)
