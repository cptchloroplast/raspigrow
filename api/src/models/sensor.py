from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Integer, Table

class SensorReading(BaseModel):
  id: Optional[int]
  timestamp: datetime
  temperature: float
  humidity: int

  class Config:
    orm_mode = True

from ..contexts.sql import metadata


readings = Table("sensor_readings", metadata,
  Column("id", Integer, primary_key=True),
  Column("timestamp", DateTime),
  Column("temperature", Float),
  Column("humidity", Integer)
)