from datetime import datetime, timezone
from json import loads
from paho.mqtt.client import MQTTMessage
from asyncio_mqtt import Client
from pydantic import BaseModel

from src.settings import Settings


class Message(BaseModel):
    timestamp: datetime
    topic: str
    data: dict

    class Config:
        orm_mode = True

    @classmethod
    def from_raw(cls, message: MQTTMessage):
        return cls(
            timestamp=datetime.now(timezone.utc),
            topic=message.topic,
            data=loads(message.payload),
        )


class ClientFactory:
    @staticmethod
    def create(settings: Settings):
        return Client(settings.MQTT_HOSTNAME)
