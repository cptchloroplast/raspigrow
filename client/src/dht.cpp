#include <DHT.h>
#include <ArduinoJson.h>
#include <dht.h>

DHT dht(DHTPIN, DHTTYPE);
StaticJsonDocument<DHTSIZE> doc;

unsigned long previousMillis = 0;
const long interval = 2000;

void initDHT() {
  Serial.println("Starting DHT sensor...");
  dht.begin();
  Serial.println("DHT sensor started");
}

StaticJsonDocument<DHTSIZE> readDHT() {
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) {
    doc["temperature"] = dht.readTemperature();
    doc["humidity"] = dht.readHumidity();
    previousMillis = currentMillis;
  }
  return doc;
}
