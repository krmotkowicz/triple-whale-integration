# to send orders 
import requests

url = "https://jsonplaceholder.typicode.com/posts"
payload_test = {
    "title": "Test post",
    "body": "Testing my page",
    "userId": 1,
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "123"
}


#file or json 
#await 


def call_api(url: str, payload: dict, headers: dict):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    return response

print("Sending customers")
cust_resp = call_api(url, payload_test, headers=headers)
print(f"Status: {cust_resp.status_code}")
print(f"Response: {cust_resp.json()}")