from datetime import datetime, timezone
from sqlalchemy import Column, Float, Integer, MetaData, Table
from sqlalchemy.types import TypeDecorator, DateTime


class Timestamp(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)


metadata = MetaData()


sensor_readings = Table(
    "sensor_readings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", Timestamp, nullable=False),
    Column("temperature", Float, nullable=False),
    Column("humidity", Integer, nullable=False),
)
