
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Delivery Analysis",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Delivery Performance Analysis")
st.caption("Explore historical delivery patterns and operational performance.")

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #1B2B38;
    border: 1px solid #304453;
    padding: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path, encoding="latin1")

try:
    df = load_data(str(DATA_PATH))

    # =================================================
    # FILTERS
    # =================================================

    st.sidebar.header("Delivery Analysis Filters")

    shipping_modes = sorted(df["Shipping Mode"].dropna().unique())
    selected_modes = st.sidebar.multiselect(
        "Shipping Mode",
        shipping_modes,
        default=shipping_modes
    )

    regions = sorted(df["Order Region"].dropna().unique())
    selected_regions = st.sidebar.multiselect(
        "Order Region",
        regions,
        default=regions
    )

    segments = sorted(df["Customer Segment"].dropna().unique())
    selected_segments = st.sidebar.multiselect(
        "Customer Segment",
        segments,
        default=segments
    )

    filtered_df = df[
        df["Shipping Mode"].isin(selected_modes)
        & df["Order Region"].isin(selected_regions)
        & df["Customer Segment"].isin(selected_segments)
    ].copy()

    # Cancelled shipments excluded from delivery KPIs
    analysis_df = filtered_df[
        filtered_df["Delivery Status"] != "Shipping canceled"
    ].copy()

    if analysis_df.empty:
        st.warning("No records found for the selected filters.")
        st.stop()

    # =================================================
    # KPI METRICS
    # =================================================

    total = len(analysis_df)

    late = (
        analysis_df["Delivery Status"] == "Late delivery"
    ).sum()

    on_time = (
        analysis_df["Delivery Status"] == "Shipping on time"
    ).sum()

    advance = (
        analysis_df["Delivery Status"] == "Advance shipping"
    ).sum()

    late_rate = late / total * 100

    st.subheader("Delivery Performance KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Shipments", f"{total:,}")
    c2.metric("Late Shipments", f"{late:,}")
    c3.metric("Late Delivery Rate", f"{late_rate:.2f}%")
    c4.metric("Advance Shipments", f"{advance:,}")

    st.divider()

    # =================================================
    # DELIVERY STATUS DISTRIBUTION
    # =================================================

    st.subheader("1. Delivery Status Distribution")

    status_data = (
        analysis_df["Delivery Status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = ["Delivery Status", "Count"]

    fig_status = px.pie(
        status_data,
        names="Delivery Status",
        values="Count",
        hole=0.5,
        title="Shipment Status Breakdown",
        color_discrete_sequence=[
            "#EF553B", "#00CC96", "#636EFA"
        ]
    )

    fig_status.update_layout(template="plotly_dark")

    st.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # =================================================
    # SHIPPING MODE ANALYSIS
    # =================================================

    st.subheader("2. Shipping Mode Performance")

    shipping_data = (
        analysis_df.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Delivery Status", "count"),
            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    shipping_data["Late_Rate"] = (
        shipping_data["Late_Shipments"]
        / shipping_data["Total_Shipments"] * 100
    )

    col1, col2 = st.columns(2)

    with col1:
        fig_shipping = px.bar(
            shipping_data,
            x="Shipping Mode",
            y="Late_Rate",
            text_auto=".2f",
            color="Late_Rate",
            title="Late Delivery Rate by Shipping Mode",
            color_continuous_scale="Reds"
        )

        fig_shipping.update_layout(
            template="plotly_dark",
            yaxis_title="Late Delivery Rate (%)"
        )

        st.plotly_chart(fig_shipping, use_container_width=True)

    with col2:
        fig_shipping_volume = px.bar(
            shipping_data,
            x="Shipping Mode",
            y="Total_Shipments",
            color="Shipping Mode",
            title="Shipment Volume by Shipping Mode"
        )

        fig_shipping_volume.update_layout(
            template="plotly_dark",
            showlegend=False
        )

        st.plotly_chart(
            fig_shipping_volume,
            use_container_width=True
        )

    st.divider()

    # =================================================
    # REGION ANALYSIS
    # =================================================

    st.subheader("3. Region-wise Delivery Performance")

    region_data = (
        analysis_df.groupby("Order Region")
        .agg(
            Total_Shipments=("Delivery Status", "count"),
            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    region_data["Late_Rate"] = (
        region_data["Late_Shipments"]
        / region_data["Total_Shipments"] * 100
    )

    region_data = region_data.sort_values(
        "Late_Rate",
        ascending=False
    )

    fig_region = px.bar(
        region_data.head(15).sort_values("Late_Rate"),
        x="Late_Rate",
        y="Order Region",
        orientation="h",
        color="Late_Rate",
        text_auto=".2f",
        title="Top 15 Regions by Late Delivery Rate",
        color_continuous_scale="Oranges"
    )

    fig_region.update_layout(
        template="plotly_dark",
        xaxis_title="Late Delivery Rate (%)"
    )

    st.plotly_chart(fig_region, use_container_width=True)

    st.divider()

    # =================================================
    # CUSTOMER SEGMENT ANALYSIS
    # =================================================

    st.subheader("4. Customer Segment Analysis")

    segment_data = (
        analysis_df.groupby("Customer Segment")
        .agg(
            Total_Shipments=("Delivery Status", "count"),
            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    segment_data["Late_Rate"] = (
        segment_data["Late_Shipments"]
        / segment_data["Total_Shipments"] * 100
    )

    fig_segment = px.bar(
        segment_data,
        x="Customer Segment",
        y="Late_Rate",
        color="Customer Segment",
        text_auto=".2f",
        title="Late Delivery Rate by Customer Segment"
    )

    fig_segment.update_layout(
        template="plotly_dark",
        yaxis_title="Late Delivery Rate (%)",
        showlegend=False
    )

    st.plotly_chart(fig_segment, use_container_width=True)

    st.divider()

    # =================================================
    # DEPARTMENT ANALYSIS
    # =================================================

    st.subheader("5. Department-wise Delivery Performance")

    department_data = (
        analysis_df.groupby("Department Name")
        .agg(
            Total_Shipments=("Delivery Status", "count"),
            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    department_data["Late_Rate"] = (
        department_data["Late_Shipments"]
        / department_data["Total_Shipments"] * 100
    )

    department_data = department_data.sort_values(
        "Late_Rate",
        ascending=False
    )

    fig_department = px.bar(
        department_data,
        x="Late_Rate",
        y="Department Name",
        orientation="h",
        color="Late_Rate",
        text_auto=".2f",
        title="Department-wise Late Delivery Rate",
        color_continuous_scale="Reds"
    )

    fig_department.update_layout(
        template="plotly_dark",
        xaxis_title="Late Delivery Rate (%)"
    )

    st.plotly_chart(
        fig_department,
        use_container_width=True
    )

    st.divider()

    # =================================================
    # SCHEDULED SHIPPING DAYS
    # =================================================

    st.subheader("6. Scheduled Shipping Days Analysis")

    scheduled_data = (
        analysis_df.groupby("Days for shipment (scheduled)")
        .agg(
            Total_Shipments=("Delivery Status", "count"),
            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    scheduled_data["Late_Rate"] = (
        scheduled_data["Late_Shipments"]
        / scheduled_data["Total_Shipments"] * 100
    )

    fig_days = px.bar(
        scheduled_data.sort_values(
            "Days for shipment (scheduled)"
        ),
        x="Days for shipment (scheduled)",
        y="Late_Rate",
        text_auto=".2f",
        title="Late Delivery Rate by Scheduled Shipping Days",
        color="Late_Rate",
        color_continuous_scale="Oranges"
    )

    fig_days.update_layout(
        template="plotly_dark",
        xaxis_title="Scheduled Shipping Days",
        yaxis_title="Late Delivery Rate (%)"
    )

    st.plotly_chart(fig_days, use_container_width=True)

    st.divider()

    # =================================================
    # DETAILED DATA TABLE
    # =================================================

    st.subheader("7. Detailed Shipping Analysis")

    st.dataframe(
        shipping_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Delivery Analysis CSV",
        data=analysis_df.to_csv(index=False).encode("utf-8"),
        file_name="delivery_analysis.csv",
        mime="text/csv"
    )

    # =================================================
    # FOOTER
    # =================================================

    st.divider()

    st.caption(
        "Supply Chain Risk Prediction System | "
        "Delivery Analysis | Historical Dataset"
    )

    st.caption(
        "Cancelled shipments are excluded from delivery "
        "performance calculations. Observed associations "
        "do not establish causation."
    )

except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")

except KeyError as e:
    st.error(f"Required dataset column missing: {e}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
