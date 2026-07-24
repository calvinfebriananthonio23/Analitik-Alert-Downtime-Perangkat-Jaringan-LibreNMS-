import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

url = f"{BASE_URL}/api/v0/alerts"

response = requests.get(url, headers=headers)

data = response.json()

print(data.keys())