# AI-Based Environmental Sensor Fault Detection

An IoT starter project that reads environmental data from a DHT22 sensor connected to an ESP32, sends readings to a Flask server, and displays readings and possible anomalies in a Streamlit dashboard.

## Project files

- `esp32_sensor.ino` — ESP32 firmware for reading DHT22 temperature and humidity and posting readings over Wi-Fi.
- `server.py` — Flask API that receives readings and exposes recent records.
- `train_model.py` — trains a baseline Isolation Forest anomaly detector.
- `dashboard.py` — Streamlit dashboard for sensor readings and anomaly flags.
- `requirements.txt` — Python dependencies.

## Run the Python application

Use Python 3.10 or newer.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Train the baseline model:
   ```bash
   python train_model.py
   ```
3. Start the data server in one terminal:
   ```bash
   python server.py
   ```
4. Start the dashboard in another terminal:
   ```bash
   streamlit run dashboard.py
   ```

## Hardware setup

1. Install ESP32 board support and the DHT sensor library in Arduino IDE.
2. Connect the DHT22 data pin to ESP32 GPIO 4, plus power and ground.
3. In `esp32_sensor.ino`, set `WIFI_SSID`, `WIFI_PASSWORD`, and `SERVER_URL`.
4. Set `SERVER_URL` to the computer's LAN IP, for example `http://192.168.1.10:5000/ingest`.
5. Connect the ESP32 and computer to the same network. Allow port 5000 through the computer firewall if required.
6. Upload the sketch to the ESP32.

## Train using real data

Create `sensor_data.csv` with numeric columns named `temperature` and `humidity`, then run `python train_model.py` again.

## Notes

This is a starter/demo implementation. Isolation Forest is an unsupervised baseline, not a validated fault diagnosis system. Test it with real sensor readings and labelled fault examples before relying on alerts. The sample model uses synthetic data when `sensor_data.csv` is not present.
