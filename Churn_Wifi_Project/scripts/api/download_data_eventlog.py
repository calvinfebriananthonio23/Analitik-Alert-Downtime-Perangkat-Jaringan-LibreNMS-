import requests

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

endpoints = [
    "/api/v0/logs/eventlog",
    "/api/v0/eventlog",
    "/api/v0/logs",
    "/api/v0/events",
    "/api/v0/eventlogs",
]

for ep in endpoints:
    url = BASE_URL + ep

    try:
        response = requests.get(url, headers=headers)

        print("="*60)
        print("Endpoint :", ep)
        print("Status   :", response.status_code)
        print("Response :", response.text[:200])

    except Exception as e:
        print(ep, e)