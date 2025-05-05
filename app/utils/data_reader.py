# app/utils/data_reader.py
import gspread
import os

# Updated path (project root, not app folder)
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  # Go up 3 levels from app/utils
    "pestdt-e9f8a81c8a68.json"
)

def get_latest_sensor_data():
    try:
        # Rest of your code...

        # Authenticate with Google Sheets
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_PATH)
        
        # Open your Google Sheet by ID (from sheet URL)
        sheet = gc.open_by_key("1fXL0wIxqeHEehuy_NoCpjVjjcvnJNnJk9xULSdZjbKo")  # Replace with your sheet ID
        
        # Select worksheet (use correct sheet name/index)
        worksheet = sheet.worksheet("SensorData")  # Change to your sheet name
        
        # Get all records
        records = worksheet.get_all_records()
        
        if not records:
            return None
            
        # Get latest row (assuming data is appended chronologically)
        latest_row = records[-1]
        
        # Convert categorical values to numeric
        ir = 1 if str(latest_row.get("IR", "")).lower() == "detected" else 0
        pir = 1 if str(latest_row.get("PIR", "")).lower() == "active" else 0
        
        # Prepare feature vector (adjust column names as per your sheet)
        features = [
            float(latest_row["Temperature"]),
            float(latest_row["Humidity"]),
            float(latest_row["Moisture"]),
            float(latest_row["Gas"]),
            ir,
            pir,
            float(latest_row["Vibration"])
        ]
        return features
        
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return None
