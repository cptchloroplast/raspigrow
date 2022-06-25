import os

from pydantic import BaseSettings

class Settings(BaseSettings):
   TITLE = "Grow"
   REDIS_HOST: str
   DATABASE_URL: str
   DATABASE_INIT = False
   class Config:
      env_file = os.path.abspath(".env")
      env_file_encoding = "utf-8"