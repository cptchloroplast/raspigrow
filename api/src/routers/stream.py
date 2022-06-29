from datetime import datetime
from json import dumps
from databases import Database
from fastapi import APIRouter, Depends, Request
from sse_starlette import EventSourceResponse

from ..contexts.sql import get_sql_database
from ..models.sensor import SensorReading
from ..repositories.sensor import create
from ..contexts.redis import RedisContext, get_redis_context

router = APIRouter()


@router.get("/publish")
async def publish(
    channel: str = "default",
    redis: RedisContext = Depends(get_redis_context),
    db: Database = Depends(get_sql_database),
):
    await redis.redis.publish(channel, "Hello world!")
    await create(
        db,
        SensorReading(id=123, timestamp=datetime.now(), humidity=12, temperature=12.3),
    )
    return "ok"


@router.get("/stream")
async def stream(
    request: Request,
    channel: str = "default",
    context: RedisContext = Depends(get_redis_context),
):
    async def get_event():
        subscription = context.subscribe(channel, cancelled=request.is_disconnected)
        async for message in subscription:
            yield dumps(
                {"timestamp": datetime.now(), "event": "message", "data": message},
                default=str,
            )

    return EventSourceResponse(get_event())
