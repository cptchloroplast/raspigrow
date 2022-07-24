Import("env")
import os

secrets = ("REDIS_HOSTNAME", "WIFI_SSID", "WIFI_PASSWORD")

cppdefines = [(x, env.StringifyMacro(os.getenv(x, x))) for x in secrets]

env.Prepend(CPPDEFINES=cppdefines)