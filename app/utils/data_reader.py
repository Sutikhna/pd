import pandas as pd
import os

EXCEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sensor_data.xlsx")

def get_latest_sensor_data():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="SensorData")
        # Drop rows with missing values in required columns
        df = df.dropna(subset=["Temperature'", "Humidity'", "Moisture'", "Gas'", "IR'", "PIR'", "Vibration'"])
        if df.empty:
            return None

        # Get the latest row
        latest_row = df.iloc[-1]

        # Preprocess IR: 'Detected'->1, else 0
        ir = 1 if str(latest_row["IR'"]).strip().lower() == "detected" else 0

        # Preprocess PIR: 'Active'->1, else 0
        pir = 1 if str(latest_row["PIR'"]).strip().lower() == "active" else 0

        # Prepare feature vector in order: Temperature, Humidity, Moisture, Gas, IR, PIR, Vibration
        features = [
            float(latest_row["Temperature'"]),
            float(latest_row["Humidity'"]),
            float(latest_row["Moisture'"]),
            float(latest_row["Gas'"]),
            ir,
            pir,
            float(latest_row["Vibration'"])
        ]
        return features
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None
