
import streamlit as st
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Supply Chain Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #101820;
        color: #F2F4F8;
    }

    [data-testid="stSidebar"] {
        background-color: #17232E;
    }

    [data-testid="stSidebar"] p {
        color: #E5EAF0;
    }

    h1, h2, h3 {
        color: #F2F4F8;
    }

    div[data-testid="stMetric"] {
        background-color: #1B2B38;
        border: 1px solid #304453;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #B8C7D3;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📦 SupplyChain AI")
    st.caption("Risk Intelligence Platform")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("""
    Select a page from the navigation menu above.
    """)

    st.divider()

    st.markdown("### Project Information")
    st.write("**Model:** XGBoost")
    st.write("**Application:** Risk Prediction")
    st.write("**Dataset:** DataCo Supply Chain")

    st.divider()
    st.caption("Portfolio Project | 2026")

# ---------------- HOME PAGE ----------------
st.title("📦 Supply Chain Intelligence")
st.subheader("Delivery Performance & Risk Analytics")

st.markdown("""
Welcome to the Supply Chain Risk Prediction Platform.

This application analyzes historical shipment data, identifies
delivery risk patterns, and provides machine-learning-based
risk predictions.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Delivery Analytics")
    st.write(
        "Explore delivery performance, shipping modes, "
        "regional trends, and operational patterns."
    )

with col2:
    st.markdown("### 🤖 Risk Intelligence")
    st.write(
        "Predict late delivery risk using the trained "
        "machine learning pipeline."
    )

st.divider()

st.markdown("### Available Modules")

m1, m2, m3, m4 = st.columns(4)

m1.info("📊 Overview")
m2.info("🚚 Delivery Analysis")
m3.info("🤖 Risk Prediction")
m4.info("🔍 Model Insights")

st.caption(
    "Note: This platform uses historical shipment data. "
    "Predictions are model estimates, not guaranteed outcomes."
)
