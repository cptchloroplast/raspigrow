#include <EspMQTTClient.h>
#include <secrets.h>
#include <arduino-timer.h>
#include <dht.h>

EspMQTTClient client(
  WIFI_SSID,
  WIFI_PASSWORD,
  MQTT_HOSTNAME,
  "grow",
  1883
);

auto timer = timer_create_default();

void setup()
{
  Serial.begin(115200);
  initDHT();
  client.enableDebuggingMessages();
  client.enableOTA();
  client.enableLastWillMessage("grow/v1/sensor/lastwill", "I am going offline");
}

void onConnectionEstablished()
{
  timer.every(1000, [](void*) -> bool {
    auto reading = readDHT();
    String json = "";
    serializeJson(reading, json);
    client.publish("grow/v1/sensor", json.c_str());
    return true;
  });
}

void loop()
{
  client.loop();
  timer.tick<void>();
}
