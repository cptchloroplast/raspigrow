from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..contexts.redis import RedisMessage


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
