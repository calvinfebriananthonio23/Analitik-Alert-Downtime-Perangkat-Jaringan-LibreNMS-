import pandas as pd

devices = pd.read_csv("devices.csv")

print(devices.shape)
print(devices.columns.tolist())