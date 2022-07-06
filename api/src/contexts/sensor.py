from datetime import datetime
from typing import Callable
from fastapi import FastAPI, Request
from sqlalchemy import and_
from ..models.sensor import SensorReading
from ..contexts.redis import RedisContext, RedisMessage
from ..contexts.sql import SqlContext
from ..models.sensor import sensor_readings
import logging

logger = logging.getLogger(__name__)


class SensorContext:
    channel = "grow:v1:sensor"
    sql: SqlContext
    redis: RedisContext

    def __init__(self, sql: SqlContext, redis: RedisContext):
        self.sql = sql
        self.redis = redis

    def start(self):
        self.redis.subscribe(self.channel, self._process_redis_message)

    def subscribe(self, handler: Callable = None, canceller: Callable = None):
        return self.redis.subscribe(self.channel, handler, canceller)

    async def get_history(self, start: datetime, end: datetime):
        query = sensor_readings.select().where(
            and_(sensor_readings.c.timestamp > start, sensor_readings.c.timestamp < end)
        )
        result = await self.sql.database.fetch_all(query)
        return result

    async def _process_redis_message(self, message: RedisMessage):
        reading = SensorReading(
            timestamp=message.timestamp,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )
        logger.info(reading.json())
        await self._persist_sensor_reading(reading)

    async def _persist_sensor_reading(self, reading: SensorReading):
        query = sensor_readings.insert()
        try:
            id: int = await self.sql.database.execute(query, reading.dict())
            return id
        except Exception as ex:
            logger.error(ex)


def start_sensor_context(app: FastAPI, sql: SqlContext, redis: RedisContext):
    sensor = SensorContext(sql, redis)
    sensor.start()
    app.state.sensor = sensor
    return sensor


def get_sensor_context(request: Request):
    sensor: SensorContext = request.app.state.sensor
    return sensor
