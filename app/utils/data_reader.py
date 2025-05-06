import gspread
from google.oauth2 import service_account
import os
import datetime
import json
import traceback

# Debug: Print working directory
print("Working directory:", os.getcwd())

# Path to service account JSON file
SERVICE_ACCOUNT_PATH = "pestdt-08dc67f86eeb.json"
print("Looking for service account at:", SERVICE_ACCOUNT_PATH)

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_latest_sensor_data():
    try:
        print("Current UTC time:", datetime.datetime.utcnow())

        if not os.path.exists(SERVICE_ACCOUNT_PATH):
            print(f"ERROR: Service account file not found at {SERVICE_ACCOUNT_PATH}")
            print("Files in current directory:", os.listdir(os.getcwd()))
            return None

        # Load and verify service account file
        with open(SERVICE_ACCOUNT_PATH, 'r') as f:
            sa_content = json.load(f)
            print(f"Service account email: {sa_content.get('client_email')}")

        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_PATH,
            scopes=SCOPES
        )

        # Authorize gspread client
        gc = gspread.authorize(credentials)

        # Open the spreadsheet by ID
        sheet = gc.open_by_key("1fXL0wIxqeHEehuy_NoCpjVjjcvnJNnJk9xULSdZjbKo")

        # Access the worksheet
        worksheet = sheet.worksheet("SensorData")  # Change name if needed

        # Fetch all data
        records = worksheet.get_all_records()
        if not records:
            print("No records found in the sheet.")
            return None

        latest_row = records[-1]
        print("Latest row data:", latest_row)

        # Normalize and extract values
        def find_key(possible_keys):
            return next((k for k in latest_row if k.lower().strip() in possible_keys), None)

        temp_key = find_key(["temperature"])
        humidity_key = find_key(["humidity"])
        moisture_key = find_key(["moisture"])
        gas_key = find_key(["gas", "gas'"])
        ir_key = find_key(["ir", "ir'"])
        pir_key = find_key(["pir", "pir'"])
        vibration_key = find_key(["vibration"])

        ir = 1 if str(latest_row.get(ir_key, "")).strip().lower() == "detected" else 0
        pir = 1 if str(latest_row.get(pir_key, "")).strip().lower() == "active" else 0

        features = [
            float(latest_row.get(temp_key, 0)),
            float(latest_row.get(humidity_key, 0)),
            float(latest_row.get(moisture_key, 0)),
            float(latest_row.get(gas_key, 0)),
            ir,
            pir,
            float(latest_row.get(vibration_key, 0))
        ]

        print("Processed features:", features)
        return features

    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        traceback.print_exc()
        return None
