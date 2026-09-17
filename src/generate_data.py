import pandas as pd
import numpy as np

np.random.seed(42)

n = 8000

warehouses = ["Chennai", "Coimbatore", "Bangalore", "Hyderabad", "Kochi"]
carriers = ["BlueDart", "Delhivery", "DTDC", "Ecom Express", "XpressBees"]
products = ["Electronics", "Clothing", "Grocery", "Furniture", "Pharmacy"]

routes = {
    "Chennai-Coimbatore": 510,
    "Chennai-Bangalore": 350,
    "Bangalore-Hyderabad": 570,
    "Coimbatore-Kochi": 190,
    "Hyderabad-Chennai": 630,
    "Kochi-Bangalore": 550
}

order_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2025-01-01", "2025-12-31"),
        n
    )
)

data = pd.DataFrame({
    "Order_ID": [f"ORD{i:05d}" for i in range(1, n + 1)],
    "Order_Date": order_dates,
    "Warehouse": np.random.choice(warehouses, n),
    "Carrier": np.random.choice(carriers, n),
    "Product_Type": np.random.choice(products, n),
    "Route": np.random.choice(list(routes.keys()), n)
})

# Route distance
data["Route_Distance_KM"] = data["Route"].map(routes)

# Warehouse processing time
warehouse_delay = {
    "Chennai": 1.5,
    "Coimbatore": 2.0,
    "Bangalore": 1.2,
    "Hyderabad": 1.7,
    "Kochi": 1.8
}

data["Processing_Days"] = (
    data["Warehouse"].map(warehouse_delay)
    + np.random.normal(0, 0.5, n)
).clip(0.5, 4).round(1)

# Transit time based on distance
data["Transit_Days"] = (
    data["Route_Distance_KM"] / 300
    + np.random.normal(0, 0.7, n)
).clip(1, 5).round(1)

# Calendar features
data["Day_of_Week"] = data["Order_Date"].dt.day_name()
data["Month"] = data["Order_Date"].dt.month_name()

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Autumn"

data["Season"] = data["Order_Date"].dt.month.map(get_season)

# Carrier reliability
carrier_risk = {
    "BlueDart": 0.4,
    "Delhivery": 0.6,
    "DTDC": 0.5,
    "Ecom Express": 0.7,
    "XpressBees": 0.9
}

# Product handling risk
product_risk = {
    "Electronics": 0.3,
    "Clothing": 0.2,
    "Grocery": 0.8,
    "Furniture": 0.6,
    "Pharmacy": 0.4
}

# Weekend / seasonal effect
day_risk = {
    "Monday": 0.2,
    "Tuesday": 0.3,
    "Wednesday": 0.2,
    "Thursday": 0.3,
    "Friday": 0.8,
    "Saturday": 0.6,
    "Sunday": 0.4
}

season_risk = {
    "Winter": 0.2,
    "Summer": 0.4,
    "Monsoon": 0.8,
    "Autumn": 0.5
}

# Calculate operational risk
risk_score = (
    data["Warehouse"].map(warehouse_delay)
    + data["Carrier"].map(carrier_risk)
    + data["Product_Type"].map(product_risk)
    + data["Day_of_Week"].map(day_risk)
    + data["Season"].map(season_risk)
    + data["Route_Distance_KM"] / 1000
    + np.random.normal(0, 0.6, n)
)

# Convert risk into delay days
data["Delay_Days"] = np.select(
    [
        risk_score < 3.5,
        risk_score < 5,
        risk_score < 6.5
    ],
    [0, 1, 2],
    default=3
)

# Add occasional severe delays
severe_delay = np.random.random(n) < 0.04
data.loc[severe_delay, "Delay_Days"] += np.random.randint(2, 4, severe_delay.sum())

# Delivery dates
data["Promised_Delivery_Date"] = (
    data["Order_Date"]
    + pd.to_timedelta(
        np.ceil(
            data["Processing_Days"] + data["Transit_Days"]
        ),
        unit="D"
    )
)

data["Actual_Delivery_Date"] = (
    data["Promised_Delivery_Date"]
    + pd.to_timedelta(data["Delay_Days"], unit="D")
)

data["Delivery_Status"] = np.where(
    data["Delay_Days"] == 0,
    "On-Time",
    "Delayed"
)

# Risk category
data["Delay_Risk"] = pd.cut(
    data["Delay_Days"],
    bins=[-1, 0, 2, 100],
    labels=["Low", "Medium", "High"]
)

# Save
data.to_csv("data/delivery_data.csv", index=False)

print("========================================")
print("DELIVERY DATASET CREATED SUCCESSFULLY")
print("========================================")
print(f"Total Records : {len(data)}")
print(f"Total Columns : {len(data.columns)}")
print("File          : data/delivery_data.csv")
print("\nDelay Distribution:")
print(data["Delivery_Status"].value_counts())