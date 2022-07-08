from datetime import datetime, timezone
from sqlalchemy.types import TypeDecorator, DateTime

class TimeStamp(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime, dialect):
        return value.astimezone(timezone.utc)