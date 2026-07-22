import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

processed_dir = BASE_DIR / "data" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "dataset_final.csv"
)

print("="*60)
print("DATASET")
print("="*60)

print(df.shape)

print(df.head())

print(df.columns.tolist())

# ANALISIS 1 - TOTAL EVENT & DEVICE

print("\n===== TOTAL EVENT =====")
print(len(df))

print("\n===== TOTAL DEVICE =====")
print(df["device_id"].nunique())

# ANALISIS 2 - JENIS EVENT


print("\n===== JENIS EVENT =====")

print(
    df["type_x"]
    .value_counts()
)

# ANALISIS 3 - SEVERITY

print("\n===== SEVERITY =====")

severity_distribution = (
    df.groupby("severity")
      .size()
      .reset_index(name="Jumlah Event")
      .sort_values("severity")
)

print(severity_distribution)

severity_distribution.to_csv(
    processed_dir / "severity_distribution.csv",
    index=False
)

# ANALISIS 4 - TOP DEVICE

print("\n===== TOP DEVICE =====")

top_device = (
    df.groupby("hostname_y")
      .size()
      .reset_index(name="Jumlah Event")
      .sort_values("Jumlah Event", ascending=False)
)

print(top_device.head(10))

top_device.to_csv(
    processed_dir / "top_device.csv",
    index=False
)

# ANALISIS 5 - TOP HARDWARE

print("\n===== TOP HARDWARE =====")

top_hardware = (
    df.groupby("hardware")
      .size()
      .reset_index(name="Jumlah Event")
      .sort_values("Jumlah Event", ascending=False)
)

print(top_hardware)

top_hardware.to_csv(
    processed_dir / "top_hardware.csv",
    index=False
)

# ANALISIS 6 - TOP OS

print("\n===== TOP OS =====")

top_os = (
    df.groupby("os")
      .size()
      .reset_index(name="Jumlah Event")
      .sort_values("Jumlah Event", ascending=False)
)

print(top_os)

# ANALISIS 7 - EVENT PER JAM

print("\n===== EVENT PER JAM =====")

event_per_jam = (
    df.groupby("Jam")
      .size()
      .reset_index(name="Jumlah Event")
)

print(event_per_jam)

event_per_jam.to_csv(
    processed_dir / "event_per_jam.csv",
    index=False
)

# ANALISIS 8 - EVENT PER HARI

print("\n===== EVENT PER HARI =====")

event_per_hari = (
    df.groupby("Hari")
      .size()
      .reset_index(name="Jumlah Event")
)

print(event_per_hari)

event_per_hari.to_csv(
    processed_dir / "event_per_hari.csv",
    index=False
)

# ANALISIS 9 - TOP MESSAGE

print("\n===== TOP MESSAGE =====")

top_message = (
    df.groupby("message")
      .size()
      .reset_index(name="Jumlah")
      .sort_values("Jumlah", ascending=False)
)

print(top_message.head(20))

top_message.to_csv(
    processed_dir / "top_message.csv",
    index=False
)

print("\n===== NILAI SEVERITY =====")

print(df["severity"].unique())

# Konversi severity menjadi angka
df["severity_score"] = (
    pd.to_numeric(
        df["severity"],
        errors="coerce"
    ).fillna(0)
)

priority = (
    df.groupby("hostname_y")
      .agg(
          Total_Event=("event_id","count"),
          Severity_Score=("severity_score","sum")
      )
)

priority["Priority_Score"] = (
    priority["Total_Event"] +
    priority["Severity_Score"]
)

priority = priority.sort_values(
    "Priority_Score",
    ascending=False
)

print(priority.head(10))

priority.to_csv(
    processed_dir / "priority_maintenance.csv",
    index=True
)
