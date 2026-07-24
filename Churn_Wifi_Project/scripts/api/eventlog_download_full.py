import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

all_logs = []

start = 0
limit = 1000

while True:

    print(f"Mengambil data start={start}")

    url = f"{BASE_URL}/api/v0/logs/eventlog?limit={limit}&start={start}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Stop karena status", response.status_code)
        break

    data = response.json()["logs"]

    if len(data) == 0:
        print("Data habis.")
        break

    all_logs.extend(data)

    print("Jumlah didapat :", len(data))

    start += limit

df = pd.DataFrame(all_logs)

print(df.shape)

df.to_csv("eventlog_full.csv", index=False)

print("Selesai")