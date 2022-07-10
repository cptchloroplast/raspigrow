from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.redis import RedisMessage


class SensorReading(BaseModel):
    id: Optional[int]
    timestamp: datetime
    channel: Optional[str]
    temperature: float
    humidity: int

    class Config:
        orm_mode = True

    @classmethod
    def from_message(cls, message: RedisMessage):
        return cls(
            timestamp=message.timestamp,
            channel=message.channel,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )
