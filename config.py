import os
from pydantic import SecretStr

# API configuration constants
BASE_URL = "https://api.triplewhale.com/api/v2/data-in"
ORDERS_URL = f"{BASE_URL}/orders"
ADS_URL = f"{BASE_URL}/ads"
TIMEOUT = 20

# Retrieve and mask the API key   # env var set up in Profile/Settings/Codespaces
raw_key = os.getenv("TRIPLE_WHALE_API_KEY")

if not raw_key:
    raise RuntimeError("API key not found")

API_KEY = SecretStr(raw_key)