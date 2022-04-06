from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse

from ..redis import RedisContext, get_redis_context, listener

router = APIRouter()

@router.get("/publish")
async def get(channel: str = "default", context: RedisContext = Depends(get_redis_context)):
    await context.redis.publish(channel, "Hello world!")
    return "ok"

def handler(message: dict):
    return {"event": "message", "data": message}

@router.get("/stream")
async def stream(channel: str = "default", context: RedisContext = Depends(get_redis_context)):
    return EventSourceResponse(listener(context.pubsub))


