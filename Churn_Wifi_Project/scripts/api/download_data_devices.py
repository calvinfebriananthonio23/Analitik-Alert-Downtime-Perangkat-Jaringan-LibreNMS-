import requests

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

url = f"{BASE_URL}/api/v0/devices"

headers = {
    "X-Auth-Token": API_TOKEN
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Response:")
print(response.text)