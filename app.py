import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Delivery Operations Analytics",
    page_icon="🚚",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fa;
    color: #1f2937;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Chart area spacing */
[data-testid="stPlotlyChart"] {
    background-color: #eef2f7;
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 10px;
}
/* Remove black top area */
header[data-testid="stHeader"] {
    background-color: #f5f7fa !important;
    box-shadow: none !important;
}

[data-testid="stDecoration"] {
    display: none;
}

/* Main text */
h1, h2, h3, h4, p, label {
    color: #1f2937 !important;
}

h1 {
    font-size: 2.3rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    font-weight: 650 !important;
}

/* KPI Cards */
[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #d9dee7;
    border-radius: 14px;
    padding: 20px;
    min-height: 100px;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #d9dee7;
}

[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

/* Select boxes */
[data-baseweb="select"] {
    border-radius: 8px;
}

/* Multiselect boxes */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #d9dee7 !important;
    border-radius: 8px !important;
}

/* Selected filter tags */
[data-baseweb="tag"] {
    background-color: #ffd6dc !important;
    color: #1f2937 !important;
}

/* Text inside multiselect */
[data-baseweb="select"] input {
    color: #1f2937 !important;
}

/* Dropdown menu */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

[data-baseweb="menu"] {
    background-color: #ffffff !important;
}

[role="option"] {
    background-color: #ffffff !important;
    color: #1f2937 !important;
}

[role="option"]:hover {
    background-color: #f1f5f9 !important;
}
/* FORCE SIDEBAR FILTER BOXES TO LIGHT MODE */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #1f2937 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #1f2937 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #1f2937 !important;
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #fce7f3 !important;
    color: #1f2937 !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #1f2937 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

data = pd.read_csv("data/delivery_data.csv")


# =========================================================
# TITLE
# =========================================================

st.title("🚚 Delivery Delay & Operations Analytics")

st.markdown(
    "**Operational Performance Dashboard**"
)

st.caption(
    "Monitor delivery performance, identify bottlenecks, "
    "and analyze the factors contributing to delivery delays."
)

st.divider()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")

warehouse = st.sidebar.multiselect(
    "Warehouse",
    sorted(data["Warehouse"].unique()),
    default=sorted(data["Warehouse"].unique())
)

carrier = st.sidebar.multiselect(
    "Carrier",
    sorted(data["Carrier"].unique()),
    default=sorted(data["Carrier"].unique())
)

product = st.sidebar.multiselect(
    "Product Type",
    sorted(data["Product_Type"].unique()),
    default=sorted(data["Product_Type"].unique())
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_data = data[
    data["Warehouse"].isin(warehouse)
    & data["Carrier"].isin(carrier)
    & data["Product_Type"].isin(product)
]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_orders = len(filtered_data)

delayed_orders = (
    filtered_data["Delivery_Status"] == "Delayed"
).sum()

on_time_percentage = (
    filtered_data["Delivery_Status"].eq("On-Time").mean() * 100
    if total_orders > 0 else 0
)

average_delay = (
    filtered_data["Delay_Days"].mean()
    if total_orders > 0 else 0
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "⚠️ Delayed Orders",
    f"{delayed_orders:,}"
)

col3.metric(
    "✅ On-Time %",
    f"{on_time_percentage:.2f}%"
)

col4.metric(
    "⏱️ Avg Delay",
    f"{average_delay:.2f} days"
)


st.divider()

st.subheader("📥 Export Filtered Data")

csv_data = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="filtered_delivery_data.csv",
    mime="text/csv"
)

st.divider()


# =========================================================
# DELIVERY STATUS + WAREHOUSE
# =========================================================

col1, col2 = st.columns(2)


# ---------- DELIVERY STATUS ----------

with col1:

    status_count = filtered_data["Delivery_Status"].value_counts()

    fig = px.pie(
        values=status_count.values,
        names=status_count.index,
        title="Delivery Status"
    )

    fig.update_layout(
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------- WAREHOUSE ----------

with col2:

    warehouse_data = (
        filtered_data.groupby("Warehouse")["Delay_Days"]
        .mean()
        .reset_index()
        .sort_values("Delay_Days", ascending=False)
    )

    fig = px.bar(
        warehouse_data,
        x="Warehouse",
        y="Delay_Days",
        title="Average Delay by Warehouse",
        text_auto=".2f"
    )

    fig.update_layout(
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# CARRIER + ROUTE
# =========================================================

col1, col2 = st.columns(2)


# ---------- CARRIER ----------

with col1:

    carrier_data = (
        filtered_data.groupby("Carrier")["Delay_Days"]
        .mean()
        .reset_index()
        .sort_values("Delay_Days", ascending=False)
    )

    fig = px.bar(
        carrier_data,
        x="Carrier",
        y="Delay_Days",
        title="Average Delay by Carrier",
        text_auto=".2f"
    )

    fig.update_layout(
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------- ROUTE ----------

with col2:

    route_data = (
        filtered_data.groupby("Route")["Delay_Days"]
        .mean()
        .reset_index()
        .sort_values("Delay_Days", ascending=False)
    )

    fig = px.bar(
        route_data,
        x="Route",
        y="Delay_Days",
        title="Route Delay Hotspots",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_tickangle=-35,
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# PRODUCT + DAY
# =========================================================

col1, col2 = st.columns(2)


# ---------- PRODUCT ----------

with col1:

    product_data = (
        filtered_data.groupby("Product_Type")["Delay_Days"]
        .mean()
        .reset_index()
        .sort_values("Delay_Days", ascending=False)
    )

    fig = px.bar(
        product_data,
        x="Product_Type",
        y="Delay_Days",
        title="Average Delay by Product Type",
        text_auto=".2f"
    )

    fig.update_layout(
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------- DAY ----------

with col2:

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_data = (
        filtered_data.groupby("Day_of_Week")["Delay_Days"]
        .mean()
        .reindex(day_order)
        .reset_index()
    )

    fig = px.line(
        day_data,
        x="Day_of_Week",
        y="Delay_Days",
        markers=True,
        title="Average Delay by Day"
    )

    fig.update_layout(
        paper_bgcolor="#eef2f7",
        plot_bgcolor="#eef2f7",
        font=dict(color="#1f2937"),
        title_font=dict(color="#1f2937")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# SEASON ANALYSIS
# =========================================================

season_data = (
    filtered_data.groupby("Season")["Delay_Days"]
    .mean()
    .reset_index()
)

fig = px.bar(
    season_data,
    x="Season",
    y="Delay_Days",
    title="Average Delay by Season",
    text_auto=".2f"
)

fig.update_layout(
    paper_bgcolor="#eef2f7",
    plot_bgcolor="#eef2f7",
    font=dict(color="#1f2937"),
    title_font=dict(color="#1f2937")
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# OPERATIONAL HOTSPOTS
# =========================================================

st.subheader("🔥 Operational Delay Hotspots")

hotspots = (
    filtered_data.groupby(
        ["Warehouse", "Carrier", "Route"]
    )
    .agg(
        Orders=("Order_ID", "count"),
        Average_Delay=("Delay_Days", "mean")
    )
    .reset_index()
    .sort_values(
        "Average_Delay",
        ascending=False
    )
    .head(10)
)

hotspots["Average_Delay"] = (
    hotspots["Average_Delay"].round(2)
)

st.dataframe(
    hotspots,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# OPERATIONAL RECOMMENDATIONS
# =========================================================

st.subheader("💡 Operational Recommendations")

if total_orders > 0:

    worst_warehouse = warehouse_data.iloc[0]["Warehouse"]
    worst_carrier = carrier_data.iloc[0]["Carrier"]
    worst_route = route_data.iloc[0]["Route"]

    st.info(
        f"""
        **Priority Areas**

        🏭 **Warehouse:** Review processing performance at **{worst_warehouse}**.

        🚚 **Carrier:** Monitor delivery performance of **{worst_carrier}**.

        🛣️ **Route:** Investigate **{worst_route}** for transportation bottlenecks.

        📊 **Action:** Use the hotspot table above to prioritize high-delay combinations.
        """
    )


# =========================================================
# MACHINE LEARNING – DELAY PREDICTION
# =========================================================

st.divider()

st.subheader("🤖 Delivery Delay Risk Prediction")

st.caption(
    "Enter the order and transportation details below to estimate "
    "the likelihood of a delivery delay."
)


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


X = pd.get_dummies(
    data[feature_columns],
    drop_first=True
)

y = (
    data["Delay_Days"] > 0
).astype(int)


model = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)

model.fit(X, y)


# =========================================================
# PREDICTION INPUTS
# =========================================================

col1, col2, col3 = st.columns(3)


# ---------- COLUMN 1 ----------

with col1:

    p_warehouse = st.selectbox(
        "Warehouse",
        sorted(data["Warehouse"].unique()),
        key="prediction_warehouse"
    )

    p_carrier = st.selectbox(
        "Carrier",
        sorted(data["Carrier"].unique()),
        key="prediction_carrier"
    )

    p_product = st.selectbox(
        "Product Type",
        sorted(data["Product_Type"].unique()),
        key="prediction_product"
    )


# ---------- COLUMN 2 ----------

with col2:

    p_route = st.selectbox(
        "Route",
        sorted(data["Route"].unique()),
        key="prediction_route"
    )

    p_processing = st.number_input(
        "Processing Days",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.5
    )

    p_transit = st.number_input(
        "Transit Days",
        min_value=1.0,
        max_value=7.0,
        value=3.0,
        step=0.5
    )


# ---------- COLUMN 3 ----------

with col3:

    p_day = st.selectbox(
        "Day of Week",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ],
        key="prediction_day"
    )

    p_season = st.selectbox(
        "Season",
        [
            "Winter",
            "Summer",
            "Monsoon",
            "Autumn"
        ],
        key="prediction_season"
    )

    p_distance = st.number_input(
        "Route Distance (KM)",
        min_value=50.0,
        max_value=1000.0,
        value=300.0,
        step=10.0
    )


# =========================================================
# PREDICT BUTTON
# =========================================================

if st.button("🔮 Predict Delay Risk"):

    input_data = pd.DataFrame([{
        "Warehouse": p_warehouse,
        "Carrier": p_carrier,
        "Product_Type": p_product,
        "Route": p_route,
        "Processing_Days": p_processing,
        "Transit_Days": p_transit,
        "Route_Distance_KM": p_distance,
        "Day_of_Week": p_day,
        "Season": p_season
    }])

    input_encoded = pd.get_dummies(input_data)

    input_encoded = input_encoded.reindex(
        columns=X.columns,
        fill_value=0
    )

    prediction = model.predict(input_encoded)[0]

    probability = model.predict_proba(input_encoded)[0][1] * 100

    if prediction == 1:

        st.warning(
            "⚠️ High Risk: This order is predicted to have a delivery delay."
        )

        st.metric(
            "Delay Risk Probability",
            f"{probability:.1f}%"
        )

    else:

        st.success(
            "✅ Low Risk: This order is predicted to be delivered on time."
        )

        st.metric(
            "Delay Risk Probability",
            f"{probability:.1f}%"
        )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Delivery Delay & Operations Analytics | "
    "Python • Pandas • Plotly • Scikit-learn • Streamlit"
)