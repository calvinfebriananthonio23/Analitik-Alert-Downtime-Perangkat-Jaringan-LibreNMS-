import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

# Endpoint yang ingin diuji
test_urls = [
    f"{BASE_URL}/api/v0/alerts",
    f"{BASE_URL}/api/v0/alerts?state=0",
    f"{BASE_URL}/api/v0/alerts?state=1",
    f"{BASE_URL}/api/v0/alerts?state=2",
]

for url in test_urls:

    print("=" * 80)
    print("Testing:", url)

    try:
        response = requests.get(url, headers=headers)

        print("Status Code :", response.status_code)

        if response.status_code == 200:

            data = response.json()

            print("Response Keys :", list(data.keys()))

            if "alerts" in data:

                df = pd.DataFrame(data["alerts"])

                print("Jumlah Alert :", len(df))

                if len(df) > 0:

                    filename = (
                        url.split("alerts")[-1]
                        .replace("?", "_")
                        .replace("=", "_")
                        .replace("&", "_")
                    )

                    if filename == "":
                        filename = "_all"

                    df.to_csv(
                        f"alerts{filename}.csv",
                        index=False
                    )

                    print(
                        f"File berhasil disimpan: alerts{filename}.csv"
                    )

                else:
                    print("Data alert kosong")

            else:
                print(data)

        else:
            print("Response:")
            print(response.text)

    except Exception as e:
        print("ERROR:", e)