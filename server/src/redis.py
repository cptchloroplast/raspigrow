from datetime import datetime
from pydantic import BaseModel


class RedisMessage(BaseModel):
    timestamp: datetime
    channel: str
    data: dict

    class Config:
        orm_mode = True
