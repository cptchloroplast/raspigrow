#include <DHT.h>
#include <ArduinoJson.h>
#include <dht.h>
#include <math.h>

DHT dht(DHTPIN, DHTTYPE);
StaticJsonDocument<DHTSIZE> doc;

unsigned long previous = 0;
const long interval = 2000;

void initDHT() {
  Serial.println("Starting DHT sensor...");
  dht.begin();
  Serial.println("DHT sensor started");
}

StaticJsonDocument<DHTSIZE> readDHT() {
  unsigned long current = millis();
  if(current - previous >= interval) {
    doc["temperature"] = roundf(dht.readTemperature() * 100) / 100.0;
    doc["humidity"] = dht.readHumidity();
    previous = current;
  }
  return doc;
}
