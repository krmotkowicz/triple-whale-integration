import json
from call_whale_api import call_api

# Pick payload_1 or payload_2
payload_1 = {
    "title": "Test post",
    "body": "Testing my page",
    "userId": 1,
}

with open("./python/src/customers_bulk.json", "r", encoding="utf-8") as file:
    payload_2 = json.load(file)



print("Sending customers")
cust_resp = call_api(payload_2)

print(f"Status: {cust_resp.status_code}")
print(f"Response: {cust_resp.json()}")