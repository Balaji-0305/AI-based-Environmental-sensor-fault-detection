import os

import joblib
import pandas as pd
import requests
import streamlit as st

SERVER_DATA_URL = "http://127.0.0.1:5000/data"
MODEL_FILE = "anomaly_model.joblib"

st.set_page_config(page_title="Environmental Sensor Monitor", layout="wide")
st.title("AI-Based Environmental Sensor Fault Detection")
st.caption("DHT22 + ESP32 | Anomaly monitoring | Adaptive sampling")


@st.cache_resource
def load_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    return None


model = load_model()

try:
    response = requests.get(SERVER_DATA_URL, timeout=3)
    response.raise_for_status()
    rows = response.json()
except requests.RequestException:
    rows = []
    st.warning("Cannot reach the data server. Start server.py first.")

if not rows:
    st.info("Waiting for sensor readings from the ESP32.")
    st.stop()

df = pd.DataFrame(rows)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["temperature", "humidity"])

if model is not None:
    df["anomaly"] = model.predict(df[["temperature", "humidity"]]) == -1
else:
    # Fallback range checks are not a substitute for a trained model.
    df["anomaly"] = (
        (df["temperature"] < 0)
        | (df["temperature"] > 50)
        | (df["humidity"] < 0)
        | (df["humidity"] > 100)
    )

latest = df.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{latest['temperature']:.1f} °C")
col2.metric("Humidity", f"{latest['humidity']:.1f} %")
col3.metric("Latest status", "Possible anomaly" if latest["anomaly"] else "Normal")

st.subheader("Sensor readings")
st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])

st.subheader("Anomaly records")
anomalies = df[df["anomaly"]]
if anomalies.empty:
    st.success("No anomalies detected in the available readings.")
else:
    st.warning(f"{len(anomalies)} possible anomalous reading(s) detected.")
    st.dataframe(anomalies.tail(100), use_container_width=True)

st.subheader("Recent data")
st.dataframe(df.tail(100), use_container_width=True)
