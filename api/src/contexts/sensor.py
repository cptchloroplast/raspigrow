from ..models.sensor import SensorReading
from ..contexts.redis import RedisContext, RedisMessage
from ..contexts.sql import SqlContext
from ..models.sensor import sensor_readings
import logging

logger = logging.getLogger(__name__)


class SensorContext:
    sql: SqlContext
    redis: RedisContext

    def __init__(self, sql: SqlContext, redis: RedisContext):
        self.sql = sql
        self.redis = redis

    def start(self):
        self.redis.subscribe("default", self._process_redis_message)

    async def _process_redis_message(self, message: RedisMessage):
        reading = SensorReading(
            timestamp=message.timestamp,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )
        created = await self._persist_sensor_reading(reading)
        logger.info(created.json())

    async def _persist_sensor_reading(self, reading: SensorReading):
        query = sensor_readings.insert().values(
            timestamp=reading.timestamp,
            temperature=reading.temperature,
            humidity=reading.humidity,
        )
        try:
            id = await self.sql.database.execute(query)
        except Exception as ex:
            logger.error(ex)
        reading.id = id
        return reading


def start_sensor_context(sql: SqlContext, redis: RedisContext):
    sensor = SensorContext(sql, redis)
    sensor.start()
    return sensor
