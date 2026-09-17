import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("data/delivery_data.csv")

# On-time percentage
on_time_percentage = (
    (data["Delivery_Status"] == "On-Time").mean() * 100
)

print("\n===== DELIVERY PERFORMANCE =====")
print(f"Total Orders       : {len(data)}")
print(f"Delayed Orders     : {(data['Delivery_Status'] == 'Delayed').sum()}")
print(f"On-Time Percentage : {on_time_percentage:.2f}%")
print(f"Average Delay      : {data['Delay_Days'].mean():.2f} days")

# Warehouse analysis
warehouse_analysis = data.groupby("Warehouse").agg(
    Total_Orders=("Order_ID", "count"),
    Avg_Delay=("Delay_Days", "mean"),
    On_Time_Rate=("Delivery_Status",
                  lambda x: (x == "On-Time").mean() * 100)
).sort_values("Avg_Delay", ascending=False)

print("\n===== WAREHOUSE ANALYSIS =====")
print(warehouse_analysis)

# Carrier analysis
carrier_analysis = data.groupby("Carrier").agg(
    Total_Orders=("Order_ID", "count"),
    Avg_Delay=("Delay_Days", "mean"),
    On_Time_Rate=("Delivery_Status",
                  lambda x: (x == "On-Time").mean() * 100)
).sort_values("Avg_Delay", ascending=False)

print("\n===== CARRIER ANALYSIS =====")
print(carrier_analysis)

# Route analysis
route_analysis = data.groupby("Route").agg(
    Total_Orders=("Order_ID", "count"),
    Avg_Delay=("Delay_Days", "mean"),
    On_Time_Rate=("Delivery_Status",
                  lambda x: (x == "On-Time").mean() * 100)
).sort_values("Avg_Delay", ascending=False)

print("\n===== ROUTE ANALYSIS =====")
print(route_analysis)

# Product analysis
product_analysis = data.groupby("Product_Type").agg(
    Total_Orders=("Order_ID", "count"),
    Avg_Delay=("Delay_Days", "mean"),
    On_Time_Rate=("Delivery_Status",
                  lambda x: (x == "On-Time").mean() * 100)
).sort_values("Avg_Delay", ascending=False)

print("\n===== PRODUCT ANALYSIS =====")
print(product_analysis)

# Delay by day
day_analysis = data.groupby("Day_of_Week")["Delay_Days"].mean().sort_values(
    ascending=False
)

print("\n===== DELAY BY DAY =====")
print(day_analysis)

# Delay by season
season_analysis = data.groupby("Season")["Delay_Days"].mean().sort_values(
    ascending=False
)

print("\n===== DELAY BY SEASON =====")
print(season_analysis)

# Simple delay distribution chart
plt.figure(figsize=(8, 5))
data["Delay_Days"].value_counts().sort_index().plot(kind="bar")

plt.title("Delivery Delay Distribution")
plt.xlabel("Delay Days")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()