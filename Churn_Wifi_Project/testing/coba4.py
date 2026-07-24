import pandas as pd

eventlog = pd.read_csv("eventlog.csv")

print(eventlog["type"].value_counts())
print(eventlog["severity"].value_counts())

eventlog["datetime"] = pd.to_datetime(eventlog["datetime"])

print(eventlog["datetime"].min())
print(eventlog["datetime"].max())