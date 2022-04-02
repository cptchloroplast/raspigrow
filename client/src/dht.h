#include <ArduinoJson.h>

#define DHTTYPE DHT11
#define DHTPIN  2
#define DHTSIZE JSON_OBJECT_SIZE(2)

void initDHT();
StaticJsonDocument<DHTSIZE> readDHT();