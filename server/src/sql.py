from datetime import datetime, timezone
from databases import Database
from sqlalchemy import Column, Float, Integer, MetaData, String, Table
from sqlalchemy.types import TypeDecorator, DateTime

from src.settings import Settings


class Timestamp(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)


class DatabaseFactory:
    @staticmethod
    def create(settings: Settings):
        return Database(settings.DATABASE_URL_ASYNC)


metadata = MetaData()


sensor_readings = Table(
    "sensor_readings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", Timestamp, nullable=False),
    Column("channel", String(32), nullable=False),
    Column("temperature", Float, nullable=False),
    Column("humidity", Integer, nullable=False),
)
