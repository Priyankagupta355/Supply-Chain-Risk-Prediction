
import streamlit as st
import pandas as pd
from pathlib import Path

from dashboard.components.filters import apply_global_filters
from dashboard.components.kpi_cards import display_kpi_cards

from dashboard.components.charts import (
    delivery_status_chart,
    monthly_delivery_trend,
    regional_shipment_chart,
    shipping_mode_chart,
    regional_late_delivery_chart,
    delivery_performance_chart,
    monthly_late_delivery_chart,
    shipping_mode_performance_chart,
    top_high_risk_regions_chart,
    regional_delivery_comparison_chart,
    regional_summary_table
)


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
# HTML RENDERER
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

.chart-container {
    background: #111827;
    border: 1px solid #263449;
    border-radius: 12px;
    padding: 12px;
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

    st.caption("SUPPLY CHAIN RISK PREDICTION")


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

        valid_mask = ~status.str.contains(
            "cancel",
            na=False
        )

        valid_status = status.loc[valid_mask]

        late = int(
            valid_status.eq("late delivery").sum()
        )

        valid = len(valid_status)

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

    # KPI CARDS
    display_kpi_cards(
        total_shipments=kpis["total"],
        valid_deliveries=kpis["valid"],
        late_deliveries=kpis["late"],
        late_delivery_rate=kpis["late_rate"],
        avg_scheduled_days=kpis["avg_scheduled_days"]
    )

    st.divider()

    # ROW 1: DELIVERY STATUS + MONTHLY TREND

    st.markdown("### Delivery Performance")

    col1, col2 = st.columns(2)

    with col1:
        delivery_status_chart(filtered_df)

    with col2:
        monthly_delivery_trend(filtered_df)

    st.divider()

    # ROW 2: REGIONAL + SHIPPING MODE

    st.markdown("### Shipment Distribution")

    col3, col4 = st.columns(2)

    with col3:
        regional_shipment_chart(filtered_df)

    with col4:
        shipping_mode_chart(filtered_df)

    st.divider()

    # ROW 3: LATE DELIVERY REGIONAL ANALYSIS

    st.markdown("### Risk Performance")

    regional_late_delivery_chart(filtered_df)

    st.divider()

    # DATA PREVIEW

    st.markdown("### Recent Dataset Records")

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True
    )


# --------------------------------------------------
# DELIVERY ANALYTICS
# --------------------------------------------------


elif selected_page == "Regional Analysis":

    st.markdown("## Regional Analysis")

    st.caption(
        "Explore shipment distribution and delivery risks across regions."
    )

    st.markdown("### Regional Shipment Volume")

    regional_shipment_chart(filtered_df)

    st.divider()

    st.markdown("### Regional Late Delivery Risk")

    regional_late_delivery_chart(filtered_df)

    st.divider()

    st.markdown("### Top 10 High-Risk Regions")

    top_high_risk_regions_chart(filtered_df)

    st.divider()

    st.markdown("### Regional Delivery Comparison")

    regional_delivery_comparison_chart(filtered_df)

    st.divider()

    st.markdown("### Regional Performance Summary")

    regional_summary_table(filtered_df)

# --------------------------------------------------
# REGIONAL ANALYSIS
# --------------------------------------------------

elif selected_page == "Regional Analysis":

    st.markdown("## Regional Analysis")

    regional_shipment_chart(filtered_df)

    regional_late_delivery_chart(filtered_df)


# --------------------------------------------------
# SHIPPING ANALYSIS
# --------------------------------------------------

elif selected_page == "Shipping Analysis":

    st.markdown("## Shipping Analysis")

    shipping_mode_chart(filtered_df)


# --------------------------------------------------
# RISK INTELLIGENCE
# --------------------------------------------------

elif selected_page == "Risk Intelligence":

    st.markdown("## Risk Intelligence")

    display_kpi_cards(
        total_shipments=kpis["total"],
        valid_deliveries=kpis["valid"],
        late_deliveries=kpis["late"],
        late_delivery_rate=kpis["late_rate"],
        avg_scheduled_days=kpis["avg_scheduled_days"]
    )

    regional_late_delivery_chart(filtered_df)


# --------------------------------------------------
# AD-HOC ANALYSIS
# --------------------------------------------------

elif selected_page == "Ad-hoc Analysis":

    st.markdown("## Ad-hoc Analysis")

    st.info(
        "Custom dimension and metric analysis will be added in the next step."
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

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

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
