from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.mqtt import Message


class SensorReading(BaseModel):
    id: Optional[int]
    timestamp: datetime
    topic: Optional[str]
    temperature: float
    humidity: int

    class Config:
        orm_mode = True

    @classmethod
    def from_message(cls, message: Message):
        return cls(
            timestamp=message.timestamp,
            topic=message.topic,
            temperature=message.data.get("temperature"),
            humidity=message.data.get("humidity"),
        )
