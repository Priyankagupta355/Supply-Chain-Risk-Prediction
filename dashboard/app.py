
import streamlit as st
import pandas as pd
from pathlib import Path

from dashboard.components.filters import apply_global_filters
from dashboard.components.kpi_cards import display_kpi_cards


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)


# --------------------------------------------------
# CUSTOM HTML RENDERER
# --------------------------------------------------

def render_html(html):
    try:
        st.html(html)
    except Exception:
        st.markdown(html, unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_dashboard_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_dashboard_data()
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

render_html("""
<style>

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-header {
    background: linear-gradient(120deg, #172338, #1E293B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 25px;
}

.dashboard-header h1 {
    color: #F8FAFC;
    font-size: 30px;
    margin-bottom: 5px;
}

.dashboard-header p {
    color: #94A3B8;
    margin: 0;
}

.section-title {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 700;
    margin: 20px 0 15px 0;
}

@media screen and (max-width: 768px) {

    .block-container {
        padding: 1rem 0.8rem 2rem 0.8rem;
    }

    .dashboard-header {
        padding: 18px;
        margin-bottom: 20px;
    }

    .dashboard-header h1 {
        font-size: 24px;
    }

}

</style>
""")


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        "<h2 style='color:#F8FAFC;'>📦 Supply Chain</h2>",
        unsafe_allow_html=True
    )

    st.caption("Risk Intelligence Platform")

    st.divider()

    selected_page = st.radio(
        "NAVIGATION",
        [
            "Executive Overview",
            "Delivery Analytics",
            "Regional Analysis",
            "Shipping Analysis",
            "Risk Intelligence",
            "Ad-hoc Analysis",
            "Data Explorer"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown(
        """
        <div style="color:#94A3B8; font-size:12px;">
            SUPPLY CHAIN RISK PREDICTION<br>
            Analytics Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

render_html("""
<div class="dashboard-header">
    <h1>Supply Chain Analytics</h1>
    <p>Interactive analytics and delivery risk intelligence platform</p>
</div>
""")


# --------------------------------------------------
# GLOBAL FILTERS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Global Filters</div>',
    unsafe_allow_html=True
)

filtered_df, selected_filters = apply_global_filters(df)


# --------------------------------------------------
# KPI CALCULATION
# --------------------------------------------------

def calculate_kpis(data):

    total = len(data)

    if "Delivery Status" in data.columns:

        status = (
            data["Delivery Status"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        valid_mask = ~status.str.contains("cancel", na=False)

        valid_df = data.loc[valid_mask]

        valid_status = status.loc[valid_mask]

        late = int(
            valid_status.eq("late delivery").sum()
        )

        valid = len(valid_df)

    else:

        valid = total

        if "Late_delivery_risk" in data.columns:
            late = int(
                pd.to_numeric(
                    data["Late_delivery_risk"],
                    errors="coerce"
                ).fillna(0).sum()
            )
        else:
            late = 0

    late_rate = (
        (late / valid) * 100
        if valid > 0
        else 0
    )

    if "Days for shipment (scheduled)" in data.columns:

        avg_scheduled_days = pd.to_numeric(
            data["Days for shipment (scheduled)"],
            errors="coerce"
        ).mean()

    else:
        avg_scheduled_days = 0

    return {
        "total": total,
        "valid": valid,
        "late": late,
        "late_rate": late_rate,
        "avg_scheduled_days": (
            avg_scheduled_days
            if pd.notna(avg_scheduled_days)
            else 0
        )
    }


kpis = calculate_kpis(filtered_df)


# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------

if selected_page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    # Professional KPI Cards
    display_kpi_cards(
        total_shipments=kpis["total"],
        valid_deliveries=kpis["valid"],
        late_deliveries=kpis["late"],
        late_delivery_rate=kpis["late_rate"],
        avg_scheduled_days=kpis["avg_scheduled_days"]
    )

    st.divider()

    st.markdown("### Dataset Preview")

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True
    )


# --------------------------------------------------
# DELIVERY ANALYTICS
# --------------------------------------------------

elif selected_page == "Delivery Analytics":

    st.markdown("## Delivery Analytics")

    if "Delivery Status" in filtered_df.columns:

        delivery_counts = (
            filtered_df["Delivery Status"]
            .value_counts()
        )

        st.bar_chart(delivery_counts)

    else:
        st.warning("Delivery Status column not found.")


# --------------------------------------------------
# REGIONAL ANALYSIS
# --------------------------------------------------

elif selected_page == "Regional Analysis":

    st.markdown("## Regional Analysis")

    if "Order Region" in filtered_df.columns:

        regional_data = (
            filtered_df["Order Region"]
            .value_counts()
        )

        st.bar_chart(regional_data)

    else:
        st.warning("Order Region column not found.")


# --------------------------------------------------
# SHIPPING ANALYSIS
# --------------------------------------------------

elif selected_page == "Shipping Analysis":

    st.markdown("## Shipping Analysis")

    if "Shipping Mode" in filtered_df.columns:

        shipping_data = (
            filtered_df["Shipping Mode"]
            .value_counts()
        )

        st.bar_chart(shipping_data)

    else:
        st.warning("Shipping Mode column not found.")


# --------------------------------------------------
# RISK INTELLIGENCE
# --------------------------------------------------

elif selected_page == "Risk Intelligence":

    st.markdown("## Risk Intelligence")

    st.metric(
        "Late Delivery Rate",
        f"{kpis['late_rate']:.2f}%"
    )

    st.metric(
        "Late Shipments",
        f"{kpis['late']:,}"
    )

    st.info(
        "This section will contain detailed risk patterns "
        "and model insights in upcoming steps."
    )


# --------------------------------------------------
# AD-HOC ANALYSIS
# --------------------------------------------------

elif selected_page == "Ad-hoc Analysis":

    st.markdown("## Ad-hoc Analysis")

    st.info(
        "Custom dimension and metric analysis will be added next."
    )


# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

elif selected_page == "Data Explorer":

    st.markdown("## Data Explorer")

    st.write(
        f"Records available: {len(filtered_df):,}"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_supply_chain_data.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Supply Chain Risk Prediction | Interactive Analytics Platform"
)
