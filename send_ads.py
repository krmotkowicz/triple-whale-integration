
import os
import requests

# Triple Whale Ads Data-In endpoint
url = "https://api.triplewhale.com/api/v2/data-in/ads"

# Read API key from Codespaces secret
api_key = os.getenv("TRIPLE_WHALE_API_KEY")

if not api_key:
    raise ValueError("Missing TRIPLE_WHALE_API_KEY")

headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

# Single ad record (Python dictionary sent as JSON)
payload = {
    "shop": "example123.com",
    "channel": "facebook-ads",
    "event_date": "2026-11-16",
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

# Send one POST request
import json

print(json.dumps(payload, indent=2))

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=20
)

print("HTTP status:", response.status_code)
print("API response:", response.text)
