import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_FILE = "sensor_data.csv"
MODEL_FILE = "anomaly_model.joblib"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    X = df[["temperature", "humidity"]].dropna()
else:
    rng = np.random.default_rng(42)
    X = pd.DataFrame({
        "temperature": rng.normal(27, 2.5, 1000),
        "humidity": np.clip(rng.normal(60, 8, 1000), 20, 95),
    })

model = make_pipeline(
    StandardScaler(),
    IsolationForest(n_estimators=150, contamination=0.05, random_state=42),
)
model.fit(X)
joblib.dump(model, MODEL_FILE)
print(f"Saved {MODEL_FILE}; trained on {len(X)} samples.")
