import requests
from datetime import datetime

url = "https://web-production-190fc.up.railway.app/api/alerts"

data = {
    "alert": "Manual test alert via Python script",
    "alert_location": [40.7128, -74.0060, 0.0],
    "timestamp": 'jffjyt465',
    "alert_type": "manual_test",
    "score": 0.85,
    "drone_id": "python_test_drone"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "PythonScript/1.0"
}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)