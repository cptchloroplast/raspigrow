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
    SQL_HOSTNAME = "localhost"
    SQL_DATABASE = "grow"
    SQL_USERNAME = "root"
    SQL_PASSWORD = "password"

    # MQTT
    MQTT_HOSTNAME = "localhost"

    @property
    def SQL_URL(self):
        return self._get_base_sql_url("pymysql")

    @property
    def SQL_URL_ASYNC(self):
        return self._get_base_sql_url("aiomysql")

    def _get_base_sql_url(self, driver: str):
        return f"mysql+{driver}://{self.SQL_USERNAME}:{self.SQL_PASSWORD}@{self.SQL_HOSTNAME}/{self.SQL_DATABASE}"

    class Config:
        env_file = join(dirname(abspath(__file__)), "../.env")
        env_file_encoding = "utf-8"

    @classmethod
    def depends(cls):
        return cls()
