import os
import requests

URL = "https://jsonplaceholder.typicode.com/posts". #ORDERS 
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": os.getenv("TRIPLE_WHALE_KEY_API")                          # env var set up in Profile/Settings/Codespaces
}


def call_api(payload: dict):
    response = requests.post(URL, json=payload, timeout=10)
    response.raise_for_status()

    return response
