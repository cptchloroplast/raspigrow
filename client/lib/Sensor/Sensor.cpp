#include <DHT.h>
#include <ArduinoJson.h>
#include <Sensor.h>
#include <math.h>

DHT dht(DHTPIN, DHTTYPE);

void initSensor() {
  Serial.println("Starting DHT sensor...");
  dht.begin();
  Serial.println("DHT sensor started");
}

StaticJsonDocument<DHTSIZE> readSensor() {
  StaticJsonDocument<DHTSIZE> doc;
  doc["Temperature"] = roundf(dht.readTemperature() * 100) / 100.0;
  doc["Humidity"] = dht.readHumidity();
  return doc;
}
