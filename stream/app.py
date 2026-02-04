import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

# -------------------------------------------------
# Streamlit Config
# -------------------------------------------------
st.set_page_config(
    page_title="Customer Spend Prediction – Model Comparison",
    layout="wide"
)

st.title("📊 Customer Spend Prediction (3 Algorithms)")
st.caption("Linear Regression | QSVR | XGBoost")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_retail_data.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['amount'] = df['line_item_amount']
    return df

df = load_data()

# -------------------------------------------------
# Feature Engineering (Customer Level)
# -------------------------------------------------
rfm = df.groupby('customer_id').agg(
    recency=('transaction_date', lambda x: (df['transaction_date'].max() - x.max()).days),
    frequency=('transaction_id', 'count'),
    avg_spend=('amount', 'mean'),
    total_spend=('amount', 'sum')
)

# -------------------------------------------------
# Simulated Future Spend (Supervised Target)
# -------------------------------------------------
np.random.seed(42)
rfm['future_spend'] = (
    rfm['frequency'] *
    rfm['avg_spend'] *
    np.random.uniform(0.08, 0.15, size=len(rfm))
)

rfm['target_log'] = np.log1p(rfm['future_spend'])

# -------------------------------------------------
# Train/Test Split
# -------------------------------------------------
X = rfm[['recency', 'frequency', 'avg_spend']]
y = rfm['target_log']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------------------------
# Sidebar: Algorithm Selection
# -------------------------------------------------
st.sidebar.header("⚙️ Algorithm Selection")

algo = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Linear Regression", "QSVR (Quadratic SVR)", "XGBoost"]
)

# -------------------------------------------------
# Model Definitions
# -------------------------------------------------
if algo == "Linear Regression":
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])
    algo_insight = "Linear Regression provides a simple and interpretable baseline."

elif algo == "QSVR (Quadratic SVR)":
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('model', SVR(kernel='poly', degree=2, C=10, epsilon=0.3))
    ])
    algo_insight = "QSVR captures non-linear relationships using a quadratic kernel."

else:
    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    algo_insight = "XGBoost models complex non-linear patterns using boosted trees."

# -------------------------------------------------
# Train Model
# -------------------------------------------------
model.fit(X_train, y_train)

# -------------------------------------------------
# Customer Selection
# -------------------------------------------------
st.subheader("👤 Select Customer")

selected_customer = st.selectbox(
    "Customer ID",
    rfm.index.tolist()
)

cust = rfm.loc[selected_customer]

recency = cust['recency']
frequency = cust['frequency']
avg_spend = cust['avg_spend']
actual_spend = cust['total_spend']

# -------------------------------------------------
# Customer Profile
# -------------------------------------------------
st.subheader("📌 Customer Profile")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recency (days)", int(recency))
c2.metric("Frequency", int(frequency))
c3.metric("Avg Spend (₹)", round(avg_spend, 2))
c4.metric("Historical Spend (₹)", round(actual_spend, 2))

# -------------------------------------------------
# Forecast (Baseline)
# -------------------------------------------------
forecasted_spend = avg_spend * (frequency / max(rfm['frequency']))

# -------------------------------------------------
# ML Prediction (Safe)
# -------------------------------------------------
log_pred = model.predict([[recency, frequency, avg_spend]])[0]
log_pred = np.clip(log_pred, y.min(), y.max())
predicted_spend = min(np.expm1(log_pred), 100000)

# -------------------------------------------------
# Comparison Graph
# -------------------------------------------------
st.subheader("📊 Actual vs Forecasted vs Predicted")

compare_df = pd.DataFrame({
    "Actual (Historical)": [actual_spend],
    "Forecasted (Baseline)": [forecasted_spend],
    "Predicted (ML)": [predicted_spend]
}).T

st.bar_chart(compare_df)

# -------------------------------------------------
# Business Insight
# -------------------------------------------------
st.subheader("🧠 Business Insight")

if predicted_spend > forecasted_spend * 1.1:
    st.success("📈 Customer likely to **increase spending** → Upsell & premium offers")
elif predicted_spend < forecasted_spend * 0.9:
    st.warning("📉 Customer likely to **reduce spending** → Retention & discounts")
else:
    st.info("➡️ Customer spending likely **stable** → Maintain engagement")

# -------------------------------------------------
# Model Performance
# -------------------------------------------------
st.subheader("📈 Model Performance")

y_pred = model.predict(X_test)

mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))
rmse = np.sqrt(mean_squared_error(np.expm1(y_test), np.expm1(y_pred)))
r2 = r2_score(y_test, y_pred)

m1, m2, m3 = st.columns(3)
m1.metric("MAE", f"₹ {round(mae, 2)}")
m2.metric("RMSE", f"₹ {round(rmse, 2)}")
m3.metric("R²", round(r2, 3))

# -------------------------------------------------
# Algorithm Insight
# -------------------------------------------------
st.subheader("⚙️ Algorithm Insight")
st.info(algo_insight)
