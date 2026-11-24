import json
from config import ADS_URL
from api_client import submit_data

# Single ad record (Python dictionary sent as JSON)
payload = {
    "shop": "example123.com",
    "channel": "facebook-ads",
    "event_date": "2026-11-22",
    "currency": "AUD",
    "campaign": {
        "id": "001",
        "name": "November Fitness Campaign",
        "status": "ACTIVE"
    },
    "metrics": {
        "spend": 100
    }
}

# Display JSON payload for debugging
print(json.dumps(payload, indent=2))

# Send one POST request using the shared API client
response = submit_data(ADS_URL, payload)

print("HTTP status:", response.status_code)
print("API response:", response.text)