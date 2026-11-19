import sys
import os

# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
from pathlib import Path

from dashboard.components.filters import apply_global_filters


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Supply Chain BI Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

CUSTOM_CSS = """
<style>

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

.block-container {
    max-width: 1600px;
    padding: 2rem 2rem 3rem 2rem;
}

[data-testid="stSidebarNav"] {
    display: none;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263449;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #172338, #1E293B);
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

div[data-baseweb="select"] > div {
    background-color: #1E293B;
    border-color: #334155;
}

.stButton > button {
    background-color: #16A34A;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #15803D;
    color: white;
}

.brand-title {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 800;
}

.brand-subtitle {
    color: #94A3B8;
    font-size: 10px;
    letter-spacing: 2px;
}

.section-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 20px;
    margin-bottom: 10px;
}

.dashboard-header {
    background: linear-gradient(110deg, #172338, #1E293B);
    padding: 25px;
    border: 1px solid #334155;
    border-radius: 14px;
    margin-bottom: 25px;
}

.header-tag {
    color: #22C55E;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.header-title {
    color: #F8FAFC;
    font-size: 32px;
    font-weight: 800;
    margin-top: 12px;
    margin-bottom: 8px;
}

.header-description {
    color: #94A3B8;
    font-size: 15px;
    margin: 0;
}

.dashboard-footer {
    color: #64748B;
    font-size: 11px;
    text-align: center;
    padding: 20px;
}

@media screen and (max-width: 768px) {

    .block-container {
        padding: 1rem 0.8rem 2rem 0.8rem;
    }

    .dashboard-header {
        padding: 18px;
    }

    .header-title {
        font-size: 26px;
        line-height: 1.3;
    }

    .header-description {
        font-size: 13px;
        line-height: 1.6;
    }

    [data-testid="stMetric"] {
        padding: 12px;
    }
}

</style>
"""


def render_html(content):
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_data(show_spinner="Loading supply chain dataset...")
def load_dashboard_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    return df


try:
    df = load_dashboard_data()

except Exception as error:

    st.error("Unable to load the supply chain dataset.")
    st.exception(error)
    st.stop()


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

PAGES = [
    "Executive Overview",
    "Delivery Analytics",
    "Regional Analysis",
    "Shipping Analysis",
    "Risk Intelligence",
    "Ad-hoc Analysis",
    "Data Explorer"
]

PAGE_ICONS = {
    "Executive Overview": "📊",
    "Delivery Analytics": "🚚",
    "Regional Analysis": "🌍",
    "Shipping Analysis": "📦",
    "Risk Intelligence": "🧠",
    "Ad-hoc Analysis": "⚙️",
    "Data Explorer": "🔎"
}


with st.sidebar:

    render_html("""
    <div style="padding: 10px 0 20px 0;">
        <div style="font-size: 38px;">📦</div>
        <div class="brand-title">SUPPLY CHAIN</div>
        <div class="brand-subtitle">BUSINESS INTELLIGENCE</div>
    </div>
    """)

    st.divider()

    render_html(
        '<div class="section-label">MAIN MENU</div>'
    )

    selected_page = st.radio(
        "Navigation",
        options=PAGES,
        format_func=lambda page: (
            PAGE_ICONS[page] + "   " + page
        ),
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.divider()

    render_html(
        '<div class="section-label">PROJECT INFORMATION</div>'
    )

    st.caption("Supply Chain Risk Prediction")
    st.caption("Machine Learning + Business Analytics")

    st.divider()

    st.caption("VERSION 2.0")
    st.caption("DARK BI ANALYTICS")


# ==========================================================
# MAIN HEADER
# ==========================================================

render_html("""
<div class="dashboard-header">

    <div class="header-tag">
        BUSINESS INTELLIGENCE PLATFORM
    </div>

    <div class="header-title">
        Supply Chain Analytics
    </div>

    <p class="header-description">
        Monitor delivery performance, analyze operations
        and identify shipment risks.
    </p>

</div>
""")


# ==========================================================
# GLOBAL FILTERS
# ==========================================================

st.markdown("## Dashboard Filters")

filtered_df, selected_filters = apply_global_filters(df)


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

def calculate_kpis(data):

    total_records = len(data)

    if total_records == 0:
        return {
            "total": 0,
            "valid": 0,
            "late": 0,
            "late_rate": 0,
            "non_late_rate": 0,
            "avg_scheduled_days": 0
        }

    valid_df = data.copy()

    if "Delivery Status" in valid_df.columns:

        status = (
            valid_df["Delivery Status"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        valid_df = valid_df[
            ~status.str.contains("cancel", na=False)
        ]

        late_count = int(
            status.loc[valid_df.index]
            .str.contains("late delivery", na=False)
            .sum()
        )

    elif "Late_delivery_risk" in valid_df.columns:

        late_count = int(
            (valid_df["Late_delivery_risk"] == 1).sum()
        )

    else:
        late_count = 0

    valid_records = len(valid_df)

    late_rate = (
        (late_count / valid_records) * 100
        if valid_records > 0 else 0
    )

    non_late_rate = 100 - late_rate

    scheduled_column = "Days for shipment (scheduled)"

    if scheduled_column in data.columns:

        avg_days = pd.to_numeric(
            data[scheduled_column],
            errors="coerce"
        ).mean()

        avg_days = (
            float(avg_days)
            if pd.notna(avg_days) else 0
        )

    else:
        avg_days = 0

    return {
        "total": total_records,
        "valid": valid_records,
        "late": late_count,
        "late_rate": late_rate,
        "non_late_rate": non_late_rate,
        "avg_scheduled_days": avg_days
    }


kpis = calculate_kpis(filtered_df)


# ==========================================================
# EXECUTIVE OVERVIEW
# ==========================================================

if selected_page == "Executive Overview":

    st.markdown("## Executive Overview")

    st.caption(
        "Key performance indicators based on selected filters."
    )

    if filtered_df.empty:

        st.warning(
            "No records found for the selected filters. "
            "Please adjust your filters."
        )

    else:

        kpi_columns = st.columns(5)

        with kpi_columns[0]:
            st.metric(
                "Total Records",
                f"{kpis['total']:,}"
            )

        with kpi_columns[1]:
            st.metric(
                "Valid Deliveries",
                f"{kpis['valid']:,}"
            )

        with kpi_columns[2]:
            st.metric(
                "Late Deliveries",
                f"{kpis['late']:,}"
            )

        with kpi_columns[3]:
            st.metric(
                "Late Delivery Rate",
                f"{kpis['late_rate']:.2f}%"
            )

        with kpi_columns[4]:
            st.metric(
                "Avg. Scheduled Days",
                f"{kpis['avg_scheduled_days']:.2f}"
            )

        st.divider()

        st.markdown("### Delivery Performance")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.metric(
                "Non-Late Delivery Rate",
                f"{kpis['non_late_rate']:.2f}%"
            )

        with chart_col2:

            st.metric(
                "Filtered Records",
                f"{len(filtered_df):,}",
                delta=f"{len(filtered_df) - len(df):,} vs total dataset"
            )

        st.markdown("### Filtered Dataset Preview")

        st.dataframe(
            filtered_df.head(10),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# OTHER ANALYTICS PAGES
# ==========================================================

elif selected_page == "Delivery Analytics":

    st.title("🚚 Delivery Analytics")

    st.write(
        "Explore delivery status and performance "
        "using the global filters."
    )

    st.metric("Filtered Records", f"{len(filtered_df):,}")

    if "Delivery Status" in filtered_df.columns:

        st.bar_chart(
            filtered_df["Delivery Status"]
            .value_counts()
        )


elif selected_page == "Regional Analysis":

    st.title("🌍 Regional Analysis")

    if "Order Region" in filtered_df.columns:

        regional_data = (
            filtered_df["Order Region"]
            .value_counts()
            .head(15)
        )

        st.bar_chart(regional_data)

    else:
        st.warning("Order Region column not found.")


elif selected_page == "Shipping Analysis":

    st.title("📦 Shipping Analysis")

    if "Shipping Mode" in filtered_df.columns:

        shipping_data = (
            filtered_df["Shipping Mode"]
            .value_counts()
        )

        st.bar_chart(shipping_data)

    else:
        st.warning("Shipping Mode column not found.")


elif selected_page == "Risk Intelligence":

    st.title("🧠 Risk Intelligence")

    st.metric(
        "Late Delivery Rate",
        f"{kpis['late_rate']:.2f}%"
    )

    st.metric(
        "Late Deliveries",
        f"{kpis['late']:,}"
    )

    st.caption(
        "Risk metrics describe historical filtered records. "
        "They are not live shipment predictions."
    )


elif selected_page == "Ad-hoc Analysis":

    st.title("⚙️ Ad-hoc Analysis")

    st.write(
        "Dynamic chart builder will be implemented "
        "in the next step."
    )

    st.metric("Available Records", f"{len(filtered_df):,}")


elif selected_page == "Data Explorer":

    st.title("🔎 Data Explorer")

    st.write(
        "Explore the records returned by your global filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data (CSV)",
        data=csv_data,
        file_name="filtered_supply_chain_data.csv",
        mime="text/csv"
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

render_html("""
<div class="dashboard-footer">
    SUPPLY CHAIN BI PLATFORM
    <br>
    HISTORICAL DATA ANALYTICS
    <br><br>
    Powered by Python, Streamlit, Plotly and XGBoost
</div>
""")
