#Use Case: Upload orders (customer details, items, totals) from platforms without a native Triple Whale sales platform.
#Example Workflow:
#Identify orders to add from external platforms.
#Send a POST request with Order ID, Customer Details, Product ID, and Transaction Totals.
#Metrics like Order Revenue and AOV update automatically.


import os
import requests

url = "https://api.triplewhale.com/api/v2/data-in/orders"

api_key = os.getenv("TRIPLE_WHALE_API_KEY")
if not api_key:
    raise RuntimeError("TRIPLE_WHALE_API_KEY not found")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": api_key
}

payload = {
  "shop": "example123.com",
  "order_id": "001",
  "created_at": "2026-11-16T00:00:00Z",
  "currency": "AUD",
  "customer": {
    "id": "001",
    "email": "cust1@example.com"
  },
  "order_revenue": 500
}

response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=20
)

print("HTTP status:", response.status_code)
print("Response:", response.text)
