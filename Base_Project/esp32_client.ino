// esp32_client.ino - minimal WebSocket client for ESP32 (Arduino framework)
// Requires: arduinoWebSockets library
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";
const char* ws_server = "192.168.1.100"; // change to your server IP
const uint16_t ws_port = 8080;
String droneId = "DRONE-01";

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  if(type == WStype_CONNECTED) {
    Serial.println("WS connected");
    // send JOIN_REQ
    StaticJsonDocument<200> doc;
    doc["type"] = "JOIN_REQ";
    doc["id"] = droneId;
    String out; serializeJson(doc, out);
    webSocket.sendTXT(out);
  } else if(type == WStype_TEXT) {
    Serial.printf("Got WS: %s\n", payload);
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  Serial.print("Connecting WiFi");
  while(WiFi.status() != WL_CONNECTED) { delay(300); Serial.print('.'); }
  Serial.println(" connected");

  webSocket.begin(ws_server, ws_port, "/");
  webSocket.onEvent(webSocketEvent);
}

unsigned long lastHb = 0;
void loop() {
  webSocket.loop();
  if (millis() - lastHb > 1000) {
    lastHb = millis();
    // send heartbeat
    StaticJsonDocument<200> doc;
    doc["type"] = "HEARTBEAT";
    doc["id"] = droneId;
    doc["battery"] = random(50,100);
    JsonObject pos = doc.createNestedObject("pos");
    pos["lat"] = 12.34 + random(-100,100)/10000.0;
    pos["lng"] = 77.56 + random(-100,100)/10000.0;
    doc["state"] = "IDLE";
    String out; serializeJson(doc, out);
    webSocket.sendTXT(out);
  }
}
