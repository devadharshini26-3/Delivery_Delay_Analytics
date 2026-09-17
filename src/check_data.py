import pandas as pd

data = pd.read_csv("data/delivery_data.csv")

print("\n--- DATASET SHAPE ---")
print(data.shape)

print("\n--- FIRST 5 RECORDS ---")
print(data.head())

print("\n--- COLUMN NAMES ---")
print(data.columns.tolist())

print("\n--- MISSING VALUES ---")
print(data.isnull().sum())

print("\n--- DELIVERY STATUS ---")
print(data["Delivery_Status"].value_counts())

print("\n--- DELAY SUMMARY ---")
print(data["Delay_Days"].describe())