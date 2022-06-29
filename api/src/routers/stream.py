from datetime import datetime
from json import dumps
from fastapi import APIRouter, Depends, Request, Response
from sse_starlette import EventSourceResponse

from ..contexts.redis import RedisContext, get_redis_context

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("/", response_class=Response(media_type="text/event-stream"))
async def stream(
    request: Request,
    context: RedisContext = Depends(get_redis_context),
):
    """
    Stream sensor data from the API via [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), published at 2 second intervals.
    """

    async def get_event():
        subscription = context.subscribe("default", cancelled=request.is_disconnected)
        async for message in subscription:
            yield dumps(
                {"timestamp": datetime.now(), "event": "message", "data": message},
                default=str,
            )

    return EventSourceResponse(get_event())
