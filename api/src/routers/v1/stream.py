from fastapi import APIRouter, Depends, Request, Response
from sse_starlette import EventSourceResponse

from ...contexts.sensor import SensorContext, get_sensor_context

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("/", response_class=Response(media_type="text/event-stream"))
async def stream(
    request: Request,
    sensor: SensorContext = Depends(get_sensor_context),
):
    """
    Stream sensor data from the API via [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), published at 2 second intervals.

    The data is JSON formatted with the following structure:
    ```
    {
        "timestamp": date-time,
        "channel": string,
        "data": {
            "temperature": float,
            "humidity": integer
        }
    }
    ```
    Note on units:
    - `timestamp` is UTC
    - `temperature` is celcius (C)
    - `humidity` is percent relative humidity (%RH)
    """

    async def get_event():
        async for message in sensor.subscribe(canceller=request.is_disconnected):
            yield message.json()

    return EventSourceResponse(get_event())
