from fastapi_plugins import RedisSettings
import os

class Settings(RedisSettings):
   class Config:
        env_file = os.path.abspath(".env")
        env_file_encoding = "utf-8"