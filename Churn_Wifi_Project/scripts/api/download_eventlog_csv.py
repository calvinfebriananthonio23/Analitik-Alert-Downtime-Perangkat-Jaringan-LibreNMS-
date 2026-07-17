import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

url = f"{BASE_URL}/api/v0/logs/eventlog"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    print(data.keys())

    df_eventlog = pd.DataFrame(data["logs"])

    print(f"Jumlah Event : {len(df_eventlog)}")
    print(df_eventlog.head())

    df_eventlog.to_csv("eventlog.csv", index=False)

    print("eventlog.csv berhasil disimpan")
else:
    print(response.text)