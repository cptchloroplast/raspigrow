import logging
from datetime import datetime
from ..models.sensor import SensorReading
from ..contexts.redis import RedisContext, RedisMessage
from ..contexts.sql import SqlContext
from ..repositories import sensor


logger = logging.getLogger(__name__)


def log_reading(sql: SqlContext, redis: RedisContext):
    db = sql.database

    async def log(message: RedisMessage):
        reading = SensorReading(
            timestamp=message.timestamp,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )
        created = await sensor.create(
            db,
            reading,
        )
        logger.info(created.json())

    redis.subscribe("default", log)
