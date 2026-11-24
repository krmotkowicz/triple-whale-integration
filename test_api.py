#Test to chech if Python can read the 3Whale API key 
import os

api_key = os.getenv("TRIPLE_WHALE_API_KEY")

if api_key:
    print("API key found successfully")
else:
    print("API key not found")




