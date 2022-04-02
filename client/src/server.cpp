#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <dht.h>
#include <server.h>

ESP8266WebServer server(PORT);

void handle() {
  StaticJsonDocument<DHTSIZE> doc = readDHT();
  String json = "";
  serializeJson(doc, json);
  server.send(200, "application/json", json); 
}

void initServer() {
  Serial.println("Starting server...");
  server.on("/", handle);
  server.begin();
  Serial.println("Server started");
}

void handleServer() {
  server.handleClient();
}
