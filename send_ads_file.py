
import os
import json
import requests

url = "https://api.triplewhale.com/api/v2/data-in/ads"

api_key = os.getenv("TRIPLE_WHALE_API_KEY")

if not api_key:
    raise ValueError("Missing TRIPLE_WHALE_API_KEY")

headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

# Read ads from JSON file
with open("files/ads_bulk.json", "r",encoding="utf-8") as file:
    ads = json.load(file)

print(f"Loaded {len(ads)} ad records")

# Send each ad separately
for ad in ads:
    campaign_id = ad["campaign"]["id"]

    response = requests.post(
        url,
        headers=headers,
        json=ad,
        timeout=20
    )

    print(f"\nCampaign: {campaign_id}")
    print("HTTP status:", response.status_code)
    print("Response:", response.text)
