import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "dashboard_dataset.csv",
    low_memory=False
)

print("="*60)
print("DISTRIBUSI SEVERITY")
print("="*60)

print(df["severity"].value_counts().sort_index())

print("\n")
print("="*60)
print("CONTOH MESSAGE SETIAP SEVERITY")
print("="*60)

for s in sorted(df["severity"].dropna().unique()):
    print(f"\n===== Severity {s} =====")

    contoh = (
        df[df["severity"] == s][["message"]]
        .drop_duplicates()
        .head(10)
    )

    print(contoh)
    
print("\n")
print("="*60)
print("TYPE vs SEVERITY")
print("="*60)

print(
    pd.crosstab(
        df["type_x"],
        df["severity"]
    )
)

print("\n")
print("="*60)
print("EVENT YANG MENGANDUNG KATA KRITIS")
print("="*60)

critical = df[
    df["message"].str.contains(
        "down|fail|critical|temperature|reboot|error",
        case=False,
        na=False
    )
]

print(
    critical[
        ["message", "severity"]
    ].drop_duplicates()
)

for s in sorted(df["severity"].dropna().unique()):
    print("\n" + "="*60)
    print(f"SEVERITY {s}")
    print("="*60)

    print(
        df[df["severity"] == s][["message"]]
        .drop_duplicates()
        .head(20)
        .to_string(index=False)
    )

print(df["severity"].value_counts().sort_index())