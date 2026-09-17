import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load dataset
data = pd.read_csv("data/delivery_data.csv")

# Features
feature_columns = [
    "Warehouse",
    "Carrier",
    "Product_Type",
    "Route",
    "Processing_Days",
    "Transit_Days",
    "Route_Distance_KM",
    "Day_of_Week",
    "Season"
]

X = pd.get_dummies(data[feature_columns], drop_first=True)

y = (data["Delay_Days"] > 0).astype(int)

# Train model
model = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)

model.fit(X, y)

# Save feature names
feature_names = X.columns

print("Model trained successfully!")
print(f"Training Records: {len(X)}")
print(f"Features Used: {len(feature_names)}")