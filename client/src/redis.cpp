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
  while(!client.connect(HOST, REDIS_PORT)) {
    delay(2000);
    Serial.println(".");
  }
  redis = new Redis(client);
  Serial.println("Redis started");
}

void publishRedis(char* channel, const char* message) {
  unsigned long current = millis();
  if(current - prev >= interval) {
    auto listeners = redis->publish(channel, message);
    prev = current;
  }
}