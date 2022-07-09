from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, Table

from ..contexts.redis import RedisMessage
from ..utils.timestamp import TimeStamp
from ..contexts.sql import metadata


class SensorReading(BaseModel):
    id: Optional[int]
    timestamp: datetime
    temperature: float
    humidity: int

    class Config:
        orm_mode = True

    @classmethod
    def from_message(cls, message: RedisMessage):
      return cls(
            timestamp=message.timestamp,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )


sensor_readings = Table(
    "sensor_readings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", TimeStamp, nullable=False),
    Column("temperature", Float, nullable=False),
    Column("humidity", Integer, nullable=False),
)
