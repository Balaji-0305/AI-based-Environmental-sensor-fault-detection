from flask import Flask, request, jsonify
from datetime import datetime
from collections import deque
import threading

app = Flask(__name__)
records = deque(maxlen=5000)
lock = threading.Lock()


@app.post("/ingest")
def ingest():
    payload = request.get_json(silent=True) or {}
    try:
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature": float(payload["temperature"]),
            "humidity": float(payload["humidity"]),
        }
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "temperature and humidity must be numeric"}), 400

    with lock:
        records.append(row)
    return jsonify({"status": "ok"}), 200


@app.get("/data")
def data():
    with lock:
        return jsonify(list(records))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
