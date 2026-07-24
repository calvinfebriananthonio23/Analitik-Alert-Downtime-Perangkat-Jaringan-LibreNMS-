import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

devices = pd.read_csv(BASE_DIR / "data" / "raw" / "devices.csv")
eventlog = pd.read_csv(BASE_DIR / "data" / "raw" / "eventlog_full.csv")

print("="*50)
print("DEVICES")
print(devices.shape)

print("="*50)
print("EVENTLOG")
print(eventlog.shape)

print("\n===== DEVICES =====")
print(devices.info())

print("\nMissing Value")
print(devices.isnull().sum())

print("\nDuplicate")
print(devices.duplicated().sum())

print("\nKolom")
print(devices.columns.tolist())


print("\n\n===== EVENTLOG =====")
print(eventlog.info())

print("\nMissing Value")
print(eventlog.isnull().sum())

print("\nDuplicate")
print(eventlog.duplicated().sum())

print("\nKolom")
print(eventlog.columns.tolist())

# KONVERSI DATETIME

eventlog["datetime"] = pd.to_datetime(eventlog["datetime"])

print(eventlog["datetime"].head())

# FEATURE ENGINEERING

eventlog["Tanggal"] = eventlog["datetime"].dt.date
eventlog["Jam"] = eventlog["datetime"].dt.hour
eventlog["Hari"] = eventlog["datetime"].dt.day_name()
eventlog["Bulan"] = eventlog["datetime"].dt.month_name()
eventlog["Tahun"] = eventlog["datetime"].dt.year

print(eventlog.head())

# MERGE DATASET

df = eventlog.merge(
    devices,
    on="device_id",
    how="left"
)

print(df.shape)
print(df.head())

print(df.columns.tolist())

# SIMPAN DATASET FINAL

df.to_csv(
    BASE_DIR / "data" / "processed" / "dataset_final.csv",
    index=False
)

print("dataset_final.csv berhasil dibuat")

dashboard_df = df[
    [
        "device_id",
        "hostname_y",
        "datetime",
        "Jam",
        "Hari",
        "type_x",
        "severity",
        "hardware",
        "message",
        "os"
    ]
]

dashboard_df.to_csv(
    BASE_DIR / "data" / "processed" / "dashboard_dataset.csv",
    index=False
)