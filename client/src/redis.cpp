#include <ESP8266WiFi.h>
#include <Redis.h>
#include <secrets.h>
#include <redis.h>

WiFiClient client;
Redis *redis = nullptr;

unsigned long prev = 0;
const long interval = 2000;

void initRedis() {
  Serial.println("Starting Redis...");
  if(!client.connect(HOST, PORT)) {
    Serial.println("Error connecting to Redis host");
  }
  redis = new Redis(client);
  Serial.println("Redis started");
}

void publishRedis(char* channel, char* message) {
  unsigned long currentMillis = millis();
  if(currentMillis - prev >= interval) {
    Serial.println("Publish");
    auto listeners = redis->publish(channel, message);
    prev = currentMillis;
  }
}