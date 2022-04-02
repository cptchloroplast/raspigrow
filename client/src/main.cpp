#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <dht.h>
#include <server.h>
#include <wifi.h>
#include <redis.h>
 
void setup(void)
{
  Serial.begin(115200);
  Serial.println("Okkema Labs - Grow Seed");
  Serial.println("Running setup...");
  initDHT();
  initWifi();
  initServer();
  initRedis();
  Serial.println("Setup completed");
}
 
void loop()
{
  publishRedis("default", "test");
  handleServer();
} 
