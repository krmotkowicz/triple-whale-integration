import json
import requests

from config import ORDERS_URL
from api_client import submit_data

with open("files/orders_bulk.json", "r", encoding="utf-8") as file:
    payload = json.load(file)

if not isinstance(payload, list):
    raise ValueError("Expected a JSON array of orders")

successful_orders = []
failed_orders = []

for order in payload:
    order_id = order["order_id"]

    try:
        response = submit_data(ORDERS_URL, order)
        successful_orders.append(order_id)

        print(f"Order {order_id}: {response.status_code}")

    except requests.HTTPError as error:
        failed_orders.append(order_id)

        print(f"Order {order_id} failed: {error}")

        if error.response.status_code == 400:
            continue

        break

    except requests.RequestException:
        print(f"Order {order_id}: submission outcome unknown")
        break

print("Successful orders:", successful_orders)
print("Failed orders:", failed_orders)