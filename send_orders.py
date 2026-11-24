#Use Case: Upload orders (customer details, items, totals) from platforms without a native Triple Whale sales platform.
#Example Workflow:
#Identify orders to add from external platforms.
#Send a POST request with Order ID, Customer Details and Transaction Totals.
#Metrics like Order Revenue and AOV update automatically.
# Use case: Upload a single order to Triple Whale

from config import ORDERS_URL
from api_client import submit_data

payload = {
    "shop": "example123.com",
    "order_id": "111",
    "created_at": "2026-11-22T00:00:00Z",
    "currency": "AUD",
    "customer": {
        "id": "111",
        "email": "cust111@example.com"
    },
    "order_revenue": 500
}

response = submit_data(ORDERS_URL, payload)

print("HTTP status:", response.status_code)
print("Response:", response.text)