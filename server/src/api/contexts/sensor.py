from typing import Callable
from fastapi import FastAPI, Request
from ...models.sensor import SensorReading
from ..contexts.redis import RedisContext, RedisMessage
from .data import DataContext
from ...database import sensor_readings
import logging

logger = logging.getLogger(__name__)


class SensorContext:
    channel = "grow:v1:sensor"
    data: DataContext
    redis: RedisContext
    cancelled = False

    def __init__(self, data: DataContext, redis: RedisContext):
        self.data = data
        self.redis = redis

    def start(self):
        self.redis.subscribe(self.channel, self._process_redis_message, self._canceller)

    def subscribe(self, handler: Callable = None, canceller: Callable = None):
        return self.redis.subscribe(self.channel, handler, canceller)

    async def _canceller(self):
        return self.cancelled

    async def _process_redis_message(self, message: RedisMessage):
        reading = SensorReading.from_message(message)
        logger.info(reading.json())
        await self._persist_sensor_reading(reading)

    async def _persist_sensor_reading(self, reading: SensorReading):
        query = sensor_readings.insert()
        try:
            id: int = await self.data.database.execute(query, reading.dict())
            return id
        except Exception as ex:
            logger.error(ex)
            self.cancelled = True


def start_sensor_context(app: FastAPI, data: DataContext, redis: RedisContext):
    sensor = SensorContext(data, redis)
    sensor.start()
    app.state.sensor = sensor
    return sensor


def get_sensor_context(request: Request):
    sensor: SensorContext = request.app.state.sensor
    return sensor
