import pandas as pd

eventlog = pd.read_csv("eventlog.csv")

print(eventlog.shape)
print(eventlog.columns.tolist())
print(eventlog.head(10))