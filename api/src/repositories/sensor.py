import logging
from databases import Database

from ..models.sensor import SensorReading, readings

logger = logging.getLogger(__name__)


async def create(db: Database, reading: SensorReading):
    query = readings.insert().values(
        timestamp=reading.timestamp,
        temperature=reading.temperature,
        humidity=reading.humidity,
    )
    try:
        id = await db.execute(query)
    except Exception as ex:
        logger.error(ex)
    reading.id = id
    return reading
