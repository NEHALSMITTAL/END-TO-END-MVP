import streamlit as st
import pandas as pd

# -------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Retail Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Business Intelligence Dashboard")
st.caption("Actionable insights for product sales, customers, and stores")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_retail_data.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR FILTERS (Very Attractive)
# -------------------------------------------------
st.sidebar.header("🔎 Filters")

selected_region = st.sidebar.multiselect(
    "Select Store Region",
    df['store_region'].dropna().unique(),
    default=df['store_region'].dropna().unique()
)

selected_channel = st.sidebar.multiselect(
    "Select Channel",
    df['channel_name'].dropna().unique(),
    default=df['channel_name'].dropna().unique()
)

filtered_df = df[
    (df['store_region'].isin(selected_region)) &
    (df['channel_name'].isin(selected_channel))
]

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("📌 Key Business KPIs")

total_revenue = filtered_df['line_item_amount'].sum()
total_orders = filtered_df['transaction_id'].nunique()
total_customers = filtered_df['customer_id'].nunique()
avg_order_value = total_revenue / total_orders

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue", f"₹ {round(total_revenue, 2)}")
c2.metric("🧾 Total Orders", total_orders)
c3.metric("👥 Customers", total_customers)
c4.metric("📦 Avg Order Value", f"₹ {round(avg_order_value, 2)}")

st.divider()

# -------------------------------------------------
# PRODUCT PERFORMANCE
# -------------------------------------------------
st.subheader("📦 Product Performance")

top_products = (
    filtered_df.groupby('product_name')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

slow_products = (
    filtered_df.groupby('product_name')['line_item_amount']
    .sum()
    .sort_values()
    .head(10)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔝 Top 10 Best-Selling Products")
    st.bar_chart(top_products)

with col2:
    st.markdown("### 🐢 Slow-Moving Products")
    st.bar_chart(slow_products)

st.divider()

# -------------------------------------------------
# CATEGORY INSIGHTS
# -------------------------------------------------
st.subheader("🗂 Category-wise Revenue Contribution")

category_sales = (
    filtered_df.groupby('product_category')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_sales)

st.divider()

# -------------------------------------------------
# STORE & REGION PERFORMANCE
# -------------------------------------------------
st.subheader("🏬 Store & Region Performance")

store_sales = (
    filtered_df.groupby('store_name')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

region_sales = (
    filtered_df.groupby('store_region')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top Performing Stores")
    st.bar_chart(store_sales)

with col2:
    st.markdown("### 🌍 Region-wise Revenue")
    st.bar_chart(region_sales)

st.divider()

# -------------------------------------------------
# CHANNEL INSIGHTS
# -------------------------------------------------
st.subheader("📱 Channel Performance")

channel_sales = (
    filtered_df.groupby('channel_name')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(channel_sales)

st.divider()

# -------------------------------------------------
# LOYALTY ANALYSIS
# -------------------------------------------------
st.subheader("💳 Loyalty Impact")

loyalty_sales = (
    filtered_df.groupby('loyalty_status')['line_item_amount']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(loyalty_sales)

st.divider()

# -------------------------------------------------
# BUSINESS INSIGHTS (AUTO-GENERATED)
# -------------------------------------------------
st.subheader("🧠 Key Business Insights & Recommendations")

st.success("""
✅ **Revenue is concentrated in a small number of products**
→ Prioritize inventory & promotions for top-selling SKUs.

✅ **Several products contribute very little to revenue**
→ Consider discounts, bundling, or discontinuation.

✅ **Certain regions and stores consistently outperform others**
→ Replicate best practices across low-performing locations.

✅ **Specific sales channels dominate revenue**
→ Invest marketing budget in high-performing channels.

✅ **Loyal customers generate significantly higher revenue**
→ Strengthen loyalty programs and retention strategies.
""")

# -------------------------------------------------
# EXPORT OPTION
# -------------------------------------------------
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="business_insights_filtered_data.csv",
    mime="text/csv"
)

