from datetime import datetime
from json import dumps
from fastapi import APIRouter, Depends, Request
from sse_starlette import EventSourceResponse


from ..contexts.redis import RedisContext, get_redis_context

router = APIRouter()

@router.get("/publish")
async def get(channel: str = "default", context: RedisContext = Depends(get_redis_context)):
    await context.redis.publish(channel, "Hello world!")
    return "ok"

@router.get("/stream")
async def stream(request: Request, channel: str = "default", context: RedisContext = Depends(get_redis_context)):
    async def get_event():
        subscription = context.subscribe(channel, cancelled=request.is_disconnected)
        async for message in subscription:
            yield dumps({ 
                "timestamp": datetime.now(), 
                "event": "message", 
                "data": message 
            }, default=str)
    return EventSourceResponse(get_event())


