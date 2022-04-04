import os

from pydantic import BaseSettings

class Settings(BaseSettings):
   TITLE = "Grow"
   REDIS_HOST: str
   class Config:
        env_file = os.path.abspath(".env")
        env_file_encoding = "utf-8"