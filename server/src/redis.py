from datetime import datetime, timezone
from json import loads
from typing import Any, Dict
from pydantic import BaseModel


class RedisMessage(BaseModel):
    timestamp: datetime
    channel: str
    data: dict

    class Config:
        orm_mode = True

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]):
      return cls(
                timestamp=datetime.now(timezone.utc),
                channel=raw.get("channel"),
                data=loads(raw.get("data")),
            )
