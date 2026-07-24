import pandas as pd

eventlog = pd.read_csv("eventlog.csv")

print(eventlog["message"].head(20))