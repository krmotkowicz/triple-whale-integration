import json
import requests

from config import ADS_URL
from api_client import submit_data

# Load advertising records from JSON file
with open("files/ads_bulk.json", "r", encoding="utf-8") as file:
    payload = json.load(file)

# Validate payload structure
if not isinstance(payload, list):
    raise ValueError("Expected a JSON array of ads")

successful_ads = []
failed_ads = []

# Submit each advertising record
for ad in payload:
    campaign_id = ad["campaign"]["id"]

    try:
        response = submit_data(ADS_URL, ad)
        successful_ads.append(campaign_id)

        print(f"Campaign {campaign_id}: {response.status_code}")

    except requests.HTTPError as error:
        failed_ads.append(campaign_id)

        print(f"Campaign {campaign_id} failed: {error}")

        if error.response.status_code == 400:
            continue

        break

    except requests.RequestException:
        print(f"Campaign {campaign_id}: submission outcome unknown")
        break

# Execution summary
print("Successful ads:", successful_ads)
print("Failed ads:", failed_ads)