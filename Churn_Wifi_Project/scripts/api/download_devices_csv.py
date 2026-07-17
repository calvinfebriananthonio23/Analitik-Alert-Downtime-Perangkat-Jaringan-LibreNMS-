import requests
import pandas as pd

BASE_URL = "http://10.246.7.42:8000"
API_TOKEN = "******************"

url = f"{BASE_URL}/api/v0/devices"

headers = {
    "X-Auth-Token": API_TOKEN,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

data = response.json()

# Cek isi data
print(data.keys())

# Membuat DataFrame
df_devices = pd.DataFrame(data['devices'])

# Menampilkan 5 baris pertama
print(df_devices.head())

# Menyimpan ke CSV
df_devices.to_csv("devices.csv", index=False)

print("devices.csv berhasil disimpan!")