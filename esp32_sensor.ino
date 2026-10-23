#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 4
#define DHTTYPE DHT22

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* SERVER_URL = "http://YOUR_COMPUTER_IP:5000/ingest";

DHT dht(DHTPIN, DHTTYPE);
unsigned long lastSample = 0;
unsigned long sampleIntervalMs = 5000;

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected");
}

void loop() {
  if (millis() - lastSample < sampleIntervalMs) {
    return;
  }
  lastSample = millis();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT22 read failed");
    sampleIntervalMs = 2000;
    return;
  }

  Serial.printf("Temperature: %.2f C, Humidity: %.2f %%\n",
                temperature, humidity);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    String payload = "{\"temperature\":" + String(temperature, 2) +
                     ",\"humidity\":" + String(humidity, 2) + "}";
    int status = http.POST(payload);
    Serial.printf("Server response: %d\n", status);
    http.end();
  }

  // Adjust sampling interval based on change between readings.
  static float previousTemperature = NAN;
  static float previousHumidity = NAN;
  if (!isnan(previousTemperature) && !isnan(previousHumidity)) {
    float change = abs(temperature - previousTemperature) +
                   abs(humidity - previousHumidity) / 10.0;
    sampleIntervalMs = (change < 0.5) ? 10000 : 3000;
  }
  previousTemperature = temperature;
  previousHumidity = humidity;
}
