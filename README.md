# 🚚 Delivery Delay & Operations Analytics

## 📌 Project Overview
Delivery Delay & Operations Analytics is a data analytics and machine learning project that analyzes delivery performance and identifies the major factors behind delayed orders.

The system helps organizations understand operational bottlenecks across warehouses, carriers, routes, products, days, and seasons.

## 🎯 Objectives
- Analyze delivery performance
- Identify major delay patterns
- Find operational delay hotspots
- Compare warehouse and carrier performance
- Predict delivery delay risk
- Provide data-driven operational recommendations

## 🛠️ Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit
- Matplotlib
- Git & GitHub

## 📊 Key Features
- 8,000 delivery records
- Interactive dashboard
- Warehouse, carrier and product filters
- Delivery performance KPIs
- Delay analysis charts
- Operational hotspot analysis
- Decision Tree delay prediction
- Delay risk probability
- Filtered CSV download

## 🤖 Machine Learning
A Decision Tree Classifier is used to predict whether an order may experience a delivery delay based on operational and transportation conditions.

## 📁 Project Structure

```text
Delivery_Delay_Analytics/
├── .streamlit/
│   └── config.toml
├── data/
│   └── delivery_data.csv
├── notebooks/
├── src/
│   ├── generate_data.py
│   ├── check_data.py
│   ├── analysis.py
│   └── prediction.py
├── app.py
└── README.md