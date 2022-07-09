from datetime import datetime
from operator import and_
from databases import Database
from sqlalchemy import func, select

from ..database import sensor_readings

class SensorData:
  db: Database

  def __init__(self, db: Database):
      self.db = db
  
  async def get_history(self, start: datetime, end: datetime):
        query = (
            select(
                sensor_readings.c.timestamp,
                func.ROUND(func.AVG(sensor_readings.c.temperature), 1).label(
                    "temperature"
                ),
                func.AVG(sensor_readings.c.humidity).label("humidity"),
            )
            .where(
                and_(
                    sensor_readings.c.timestamp > start,
                    sensor_readings.c.timestamp < end,
                )
            )
            .group_by(
                func.HOUR(sensor_readings.c.timestamp),
                func.MINUTE(sensor_readings.c.timestamp),
            )
        )
        result = await self.db.fetch_all(query)
        return result