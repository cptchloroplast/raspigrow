from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, Depends, Request, Response
from sse_starlette import EventSourceResponse

from ...models.sensor import SensorReading
from ...contexts.sensor import SensorContext, get_sensor_context

router = APIRouter(prefix="/sensor", tags=["sensor"])


@router.get(
    "/stream",
    name="Stream Sensor",
    response_class=Response(media_type="text/event-stream"),
)
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


@router.get("/history", name="Read Sensor History", response_model=List[SensorReading])
async def history(
    start: datetime = datetime.now(timezone.utc) - timedelta(days=1),
    end: datetime = datetime.now(timezone.utc),
    sensor: SensorContext = Depends(get_sensor_context),
):
    history = await sensor.get_history(start, end)
    return history
