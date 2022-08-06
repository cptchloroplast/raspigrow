from os.path import abspath, dirname, join
from pydantic import BaseSettings


class Settings(BaseSettings):
    # OpenAPI
    OPENAPI_TITLE = "Grow"
    OPENAPI_DESCRIPTION = "Greenhouse Automation Ssoftware"
    OPENAPI_VERSION = "development"
    OPENAPI_CONTACT_NAME = "Okkema Labs"
    OPENAPI_CONTACT_URL = "https://okkema.org"
    OPENAPI_CONTACT_EMAIL = "correos@okkema.org"
    OPENAPI_LICENSE_NAME = "MIT"
    OPENAPI_LICENSE_URL = "https://github.com/okkema/grow/blob/main/LICENSE"

    # Auth
    AUTH_USERNAME = "guest"
    AUTH_PASSWORD = "guest"

    # Redis
    REDIS_HOSTNAME = "localhost"

    # SQL
    DATABASE_USERNAME = "root"
    DATABASE_PASSWORD = "password"
    DATABASE_HOSTNAME = "localhost"
    DATABASE_DATABASE = "grow"
    DATABASE_INIT = False

    # MQTT
    MQTT_HOSTNAME = "localhost"

    @property
    def DATABASE_URL(self):
        return self._get_base_database_url("pymysql")

    @property
    def DATABASE_URL_ASYNC(self):
        return self._get_base_database_url("aiomysql")

    def _get_base_database_url(self, driver: str):
        return f"mysql+{driver}://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}/{self.DATABASE_DATABASE}"

    class Config:
        env_file = join(dirname(abspath(__file__)), "../.env")
        env_file_encoding = "utf-8"

    @classmethod
    def depends(cls):
        return cls()
