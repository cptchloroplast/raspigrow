from datetime import datetime
from ..models.sensor import SensorReading
from ..contexts.redis import RedisContext
from ..contexts.sql import SqlContext
from ..repositories import sensor


def log_reading(sql: SqlContext, redis: RedisContext):
    db = sql.database

    async def log(message):
        await sensor.create(
            db,
            SensorReading(
                timestamp=datetime.utcnow(),
                temperature=message["data"]["temperature"],
                humidity=message["data"]["humidity"],
            ),
        )

    redis.subscribe("default", log)
