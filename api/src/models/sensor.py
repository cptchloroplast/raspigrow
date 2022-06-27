from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Integer, Table

from ..contexts.sql import metadata

class SensorReading(BaseModel):
  id: int
  timestamp: datetime
  temperature: float
  humidity: int

  class Config:
    orm_mode = True

readings = Table("sensor_readings", metadata,
  Column("id", Integer, primary_key=True),
  Column("timestamp", DateTime),
  Column("temperature", Float),
  Column("humidity", Integer)
)