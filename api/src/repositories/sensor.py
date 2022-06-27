from databases import Database

from ..models.sensor import SensorReading, readings


async def create(db: Database, reading: SensorReading):
    query = readings.insert().values(
        timestamp=reading.timestamp,
        temperature=reading.temperature,
        humidity=reading.humidity,
    )
    id = await db.execute(query)
    reading.id = id
    return reading
