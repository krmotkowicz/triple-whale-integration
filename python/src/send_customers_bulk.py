from call_whale_api import call_api

payload_test = {
    "title": "Test post",
    "body": "Testing my page",
    "userId": 1,
}


print("Sending customers")
cust_resp = call_api(payload_test)

print(f"Status: {cust_resp.status_code}")
print(f"Response: {cust_resp.json()}")