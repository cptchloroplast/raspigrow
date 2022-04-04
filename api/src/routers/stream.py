from redis import Redis
from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse

from .. import redis
from ..sensors import subscribe

router = APIRouter()

@router.get("/publish")
async def get(channel: str = "default", redis: Redis = Depends(redis.get)):
    await redis.publish(channel, "Hello world!")
    return "ok"


@router.get("/stream")
async def stream(channel: str = "default", redis: Redis = Depends(redis.get)):
    return EventSourceResponse(subscribe(channel, redis))


