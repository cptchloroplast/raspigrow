#include <EspMQTTClient.h>
#include <secrets.h>
#include <arduino-timer.h>
#include <dht.h>

EspMQTTClient client(
  WIFI_SSID,
  WIFI_PASSWORD,
  MQTT_HOSTNAME,  // MQTT Broker server ip
  // "MQTTUsername",   // Can be omitted if not needed
  // "MQTTPassword",   // Can be omitted if not needed
  "TestClient",     // Client name that uniquely identify your device
  1883              // The MQTT port, default to 1883. this line can be omitted
);

auto timer = timer_create_default();

void setup()
{
  Serial.begin(115200);
  initDHT();
  client.enableDebuggingMessages(); // Enable debugging messages sent to serial output
  client.enableHTTPWebUpdater(); // Enable the web updater. User and password default to values of MQTTUsername and MQTTPassword. These can be overridded with enableHTTPWebUpdater("user", "password").
  client.enableOTA(); // Enable OTA (Over The Air) updates. Password defaults to MQTTPassword. Port is the default OTA port. Can be overridden with enableOTA("password", port).
  client.enableLastWillMessage("TestClient/lastwill", "I am going offline");  // You can activate the retain flag by setting the third parameter to true
}

void onConnectionEstablished()
{
  client.subscribe("test", [](const String & payload) {
    Serial.println(payload);
  });
  timer.every(1000, [](void*) -> bool {
    auto reading = readDHT();
    String json = "";
    serializeJson(reading, json);
    client.publish("grow:v1:sensor", json.c_str());
    return true;
  });
}

void loop()
{
  client.loop();
  timer.tick<void>();
}
