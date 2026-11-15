import requests

URL = "https://jsonplaceholder.typicode.com/posts"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "123"
}


def call_api(payload: dict):
    response = requests.post(URL, json=payload, timeout=10)
    response.raise_for_status()

    return response
