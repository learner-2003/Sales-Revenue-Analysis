import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

.kpi-title {
    font-size:18px;
    color:gray;
}

.kpi-value {
    font-size:32px;
    font-weight:bold;
    color:#0068c9;
}
</style>
""", unsafe_allow_html=True)

FILE_PATH = r"C:/SalesDashboard/sales_data(1).csv"

try:
    df = pd.read_csv(FILE_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
except FileNotFoundError:
    st.error(f"CSV file not found: {FILE_PATH}")
    st.stop()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

st.title("Sales & Revenue Analysis Dashboard")
st.markdown("Real-Time Business Intelligence Dashboard")

st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

channel = st.sidebar.multiselect(
    "Sales Channel",
    df["SalesChannel"].unique(),
    default=df["SalesChannel"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["SalesChannel"].isin(channel))
]

total_revenue = filtered_df["FinalRevenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["OrderID"].nunique()
total_qty = filtered_df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Revenue", f"₹{total_revenue:,.0f}")

with c2:
    st.metric("Profit", f"₹{total_profit:,.0f}")

with c3:
    st.metric("Orders", f"{total_orders}")

with c4:
    st.metric("Quantity Sold", f"{total_qty}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    revenue_trend = (
        filtered_df.groupby("Date")["FinalRevenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        revenue_trend,
        x="Date",
        y="FinalRevenue",
        title="Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    monthly_profit = (
        filtered_df.groupby("Date")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.area(
        monthly_profit,
        x="Date",
        y="Profit",
        title="Profit Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    top_products = (
        filtered_df.groupby("Product")["FinalRevenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top_products,
        x="Product",
        y="FinalRevenue",
        title="Top 10 Products"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    region_sales = (
        filtered_df.groupby("Region")["FinalRevenue"]
        .sum()
        .reset_index()
    )

    fig4 = px.pie(
        region_sales,
        names="Region",
        values="FinalRevenue",
        hole=0.5,
        title="Revenue by Region"
    )

    st.plotly_chart(fig4, use_container_width=True)

category_sales = (
    filtered_df.groupby("Category")["FinalRevenue"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    category_sales,
    x="Category",
    y="FinalRevenue",
    color="Category",
    title="Category Performance"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("AI Business Insights")

if not top_products.empty and not region_sales.empty:

    best_product = top_products.iloc[0]["Product"]

    best_region = region_sales.sort_values(
        by="FinalRevenue",
        ascending=False
    ).iloc[0]["Region"]

    st.success(
        f"Highest revenue generating product: {best_product}"
    )

    st.info(
        f"Best performing region: {best_region}"
    )

    st.warning(
        "Focus marketing on low-performing regions to improve sales."
    )

else:
    st.warning("No data available for selected filters.")

st.subheader("Sales Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown(
    "Developed by Arun | Sales & Revenue Analysis Dashboard"
)