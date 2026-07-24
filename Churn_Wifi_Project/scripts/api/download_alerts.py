import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

url = f"{BASE_URL}/api/v0/alerts"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    print(data.keys())

    df_alerts = pd.DataFrame(data["alerts"])

    print(df_alerts.head())

    df_alerts.to_csv("alerts.csv", index=False)

    print("alerts.csv berhasil disimpan")
else:
    print(response.status_code)
    print(response.text)