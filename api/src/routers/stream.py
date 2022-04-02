from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from sse_starlette import EventSourceResponse

from ..sensors import subscribe

router = APIRouter()

@router.get("/publish")
async def get(channel: str = "default", redis: Redis = Depends(depends_redis)):
    await redis.publish(channel=channel, message="Hello world!")
    return "ok"


@router.get("/stream")
async def stream(channel: str = "default", redis: Redis = Depends(depends_redis)):
    return EventSourceResponse(subscribe(channel, redis))


