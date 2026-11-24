import requests
from config import API_KEY, TIMEOUT

def get_headers():
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": API_KEY.get_secret_value()
    }

def submit_data(url, payload):
    response = requests.post(
        url,
        headers=get_headers(),
        json=payload,
        timeout=TIMEOUT
    )

    response.raise_for_status()
    return response