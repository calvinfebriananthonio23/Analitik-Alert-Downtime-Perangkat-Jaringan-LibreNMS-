import requests

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

for start in [0,1000,2000,3000]:

    url = f"{BASE_URL}/api/v0/logs/eventlog?limit=1000&start={start}"

    response = requests.get(url, headers=headers)

    print("="*50)
    print("start =", start)
    print("status =", response.status_code)

    if response.status_code == 200:

        data = response.json()

        print("jumlah =", len(data["logs"]))

        if len(data["logs"]) > 0:
            print("event pertama =", data["logs"][0]["event_id"])
            print("event terakhir =", data["logs"][-1]["event_id"])