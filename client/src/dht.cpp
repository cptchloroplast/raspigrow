#include <DHT.h>
#include <ArduinoJson.h>
#include <dht.h>
#include <math.h>

DHT dht(DHTPIN, DHTTYPE);

void initDHT() {
  Serial.println("Starting DHT sensor...");
  dht.begin();
  Serial.println("DHT sensor started");
}

StaticJsonDocument<DHTSIZE> readDHT() {
  StaticJsonDocument<DHTSIZE> doc;
  doc["temperature"] = roundf(dht.readTemperature() * 100) / 100.0;
  doc["humidity"] = dht.readHumidity();
  return doc;
}
