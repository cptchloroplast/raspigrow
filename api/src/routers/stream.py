from redis import Redis
from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse

from ..redis import get_redis, subscribe

router = APIRouter()

@router.get("/publish")
async def get(channel: str = "default", redis: Redis = Depends(get_redis)):
    await redis.publish(channel, "Hello world!")
    return "ok"


@router.get("/stream")
async def stream(channel: str = "default", redis: Redis = Depends(get_redis)):
    return EventSourceResponse(subscribe(channel, redis))


