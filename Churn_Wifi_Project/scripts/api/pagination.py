import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

all_alerts = []

start = 0
limit = 1000

while True:

    url = f"{BASE_URL}/api/v0/alerts?limit={limit}&start={start}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    data = response.json()

    alerts = data.get("alerts", [])

    if len(alerts) == 0:
        break

    all_alerts.extend(alerts)

    print(f"Start={start} | Data={len(alerts)}")

    start += limit

df = pd.DataFrame(all_alerts)

print("Total Alert :", len(df))

df.to_csv("alerts.csv", index=False)

print("alerts.csv berhasil disimpan.")