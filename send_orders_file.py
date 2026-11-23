import os
import json
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

# Read all orders from JSON
with open("files/orders_bulk.json", "r",encoding="utf-8") as file:
    payload = json.load(file)

if not isinstance(payload, list):
    raise ValueError("Expected a JSON array of orders")

print("Total orders to send:", len(payload))

# Send every order
for order in payload:
    order_id = order["order_id"]
    print("Sending order:", order_id)

    try:
        response = requests.post(
            url,
            json=order,
            headers=headers,
            timeout=20
        )
    except requests.RequestException as error:
        print("Request failed:", error)
        break

    print("HTTP status:", response.status_code)
    print("Response:", response.text)

    if not response.ok:
        print("Stopping after failed order:", order_id)
        break
else:
    print("All orders submitted successfully")
