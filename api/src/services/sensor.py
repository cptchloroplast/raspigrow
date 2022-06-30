from datetime import datetime
from ..models.sensor import SensorReading
from ..contexts.redis import RedisContext
from ..contexts.sql import SqlContext
from ..repositories import sensor


def log_reading(sql: SqlContext, redis: RedisContext):
    db = sql.database

    async def log(message):
        reading = SensorReading(
            timestamp=message["timestamp"],
            temperature=message["data"]["temperature"],
            humidity=message["data"]["humidity"],
        )
        created = await sensor.create(
            db,
            reading,
        )
        print(created.json())

    redis.subscribe("default", log)
