Import("env")
import os

secrets = ("REDIS_HOSTNAME", "WIFI_SSID", "WIFI_PASSWORD", "MQTT_HOSTNAME")

cppdefines = [(x, env.StringifyMacro(os.getenv(x, x))) for x in secrets]

env.Prepend(CPPDEFINES=cppdefines)