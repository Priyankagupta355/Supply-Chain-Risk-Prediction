
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.title("📦 Supply Chain Overview")

st.markdown(
    "Historical analysis of supply chain delivery "
    "performance and operational risks."
)


# =====================================================
# 2. CUSTOM STYLING
# =====================================================

st.markdown("""
<style>
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


# =====================================================
# 3. DATASET PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)


# =====================================================
# 4. LOAD DATASET
# =====================================================

@st.cache_data
def load_data(path):

    data = pd.read_csv(
        path,
        encoding="latin1"
    )

    return data


try:

    df = load_data(str(DATA_PATH))

    # Remove cancelled shipments for delivery analysis
    df = df[
        df["Delivery Status"] != "Shipping canceled"
    ].copy()

    if df.empty:
        st.warning("No valid shipment records found.")
        st.stop()


    # =================================================
    # 5. CALCULATE KPIs
    # =================================================

    total_shipments = len(df)

    late_shipments = (
        df["Delivery Status"] == "Late delivery"
    ).sum()

    on_time_shipments = (
        df["Delivery Status"] == "Shipping on time"
    ).sum()

    advance_shipments = (
        df["Delivery Status"] == "Advance shipping"
    ).sum()

    late_percentage = (
        late_shipments / total_shipments * 100
    )

    on_time_percentage = (
        on_time_shipments / total_shipments * 100
    )

    advance_percentage = (
        advance_shipments / total_shipments * 100
    )


    # =================================================
    # 6. KPI CARDS
    # =================================================

    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )

    col2.metric(
        "Late Shipments",
        f"{late_shipments:,}"
    )

    col3.metric(
        "Late Delivery Rate",
        f"{late_percentage:.2f}%"
    )

    col4.metric(
        "On-Time Delivery Rate",
        f"{on_time_percentage:.2f}%"
    )

    st.caption(
        f"Advance Shipments: {advance_shipments:,} "
        f"({advance_percentage:.2f}%)"
    )

    st.divider()


    # =================================================
    # 7. DELIVERY STATUS DISTRIBUTION
    # =================================================

    st.subheader("Delivery Status Distribution")

    status_counts = (
        df["Delivery Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Delivery Status",
        "Shipments"
    ]

    fig_status = px.pie(
        status_counts,
        names="Delivery Status",
        values="Shipments",
        hole=0.55,
        title="Shipment Distribution",
        color_discrete_sequence=[
            "#EF553B",
            "#00CC96",
            "#636EFA"
        ]
    )

    fig_status.update_layout(
        template="plotly_dark",
        legend_title="Delivery Status"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

    st.divider()


    # =================================================
    # 8. SHIPPING MODE PERFORMANCE
    # =================================================

    st.subheader("Shipping Mode Performance")

    shipping_analysis = (
        df.groupby("Shipping Mode")
        .agg(
            Total_Shipments=(
                "Delivery Status",
                "count"
            ),

            Late_Shipments=(
                "Delivery Status",
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    shipping_analysis["Late_Delivery_Rate"] = (
        shipping_analysis["Late_Shipments"]
        / shipping_analysis["Total_Shipments"]
        * 100
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_shipping = px.bar(
            shipping_analysis.sort_values(
                "Late_Delivery_Rate",
                ascending=True
            ),

            x="Shipping Mode",
            y="Late_Delivery_Rate",

            title="Late Delivery Rate by Shipping Mode",

            text_auto=".2f",

            color="Late_Delivery_Rate",

            color_continuous_scale="Reds"
        )

        fig_shipping.update_layout(
            template="plotly_dark",
            xaxis_title="Shipping Mode",
            yaxis_title="Late Delivery Rate (%)"
        )

        st.plotly_chart(
            fig_shipping,
            use_container_width=True
        )


    # =================================================
    # 9. REGIONAL DELIVERY RISK
    # =================================================

    with col2:

        regional_analysis = (
            df.groupby("Order Region")
            .agg(
                Total_Shipments=(
                    "Delivery Status",
                    "count"
                ),

                Late_Shipments=(
                    "Delivery Status",
                    lambda x: (x == "Late delivery").sum()
                )
            )
            .reset_index()
        )

        regional_analysis["Late_Delivery_Rate"] = (
            regional_analysis["Late_Shipments"]
            / regional_analysis["Total_Shipments"]
            * 100
        )

        top_regions = regional_analysis.nlargest(
            10,
            "Late_Delivery_Rate"
        )

        fig_region = px.bar(
            top_regions.sort_values(
                "Late_Delivery_Rate",
                ascending=True
            ),

            x="Late_Delivery_Rate",
            y="Order Region",

            orientation="h",

            title="Top 10 Regions by Late Delivery Rate",

            text_auto=".2f",

            color="Late_Delivery_Rate",

            color_continuous_scale="Oranges"
        )

        fig_region.update_layout(
            template="plotly_dark",
            xaxis_title="Late Delivery Rate (%)",
            yaxis_title="Order Region"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    st.divider()


    # =================================================
    # 10. MONTHLY DELIVERY TREND
    # =================================================

    st.subheader("Monthly Delivery Trend")

    date_column = "order date (DateOrders)"

    if date_column in df.columns:

        df[date_column] = pd.to_datetime(
            df[date_column],
            errors="coerce"
        )

        monthly_df = df.dropna(
            subset=[date_column]
        ).copy()

        monthly_df["Month"] = (
            monthly_df[date_column]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        monthly_analysis = (
            monthly_df.groupby("Month")
            .agg(
                Total_Shipments=(
                    "Delivery Status",
                    "count"
                ),

                Late_Shipments=(
                    "Delivery Status",
                    lambda x: (x == "Late delivery").sum()
                )
            )
            .reset_index()
        )

        monthly_analysis["Late_Delivery_Rate"] = (
            monthly_analysis["Late_Shipments"]
            / monthly_analysis["Total_Shipments"]
            * 100
        )

        fig_monthly = px.line(
            monthly_analysis,

            x="Month",
            y="Late_Delivery_Rate",

            markers=True,

            title="Monthly Late Delivery Rate",

            hover_data=[
                "Total_Shipments",
                "Late_Shipments"
            ]
        )

        fig_monthly.update_traces(
            line=dict(width=3)
        )

        fig_monthly.update_layout(
            template="plotly_dark",
            xaxis_title="Month",
            yaxis_title="Late Delivery Rate (%)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    else:

        st.warning(
            f"Date column '{date_column}' not found. "
            "Monthly trend cannot be displayed."
        )

    st.divider()


    # =================================================
    # 11. SHIPPING MODE SUMMARY TABLE
    # =================================================

    st.subheader("Shipping Mode Analysis Table")

    display_shipping = shipping_analysis.copy()

    display_shipping["Late_Delivery_Rate"] = (
        display_shipping["Late_Delivery_Rate"]
        .round(2)
    )

    display_shipping = display_shipping.rename(
        columns={
            "Shipping Mode": "Shipping Mode",
            "Total_Shipments": "Total Shipments",
            "Late_Shipments": "Late Shipments",
            "Late_Delivery_Rate": "Late Delivery Rate (%)"
        }
    )

    st.dataframe(
        display_shipping,
        use_container_width=True,
        hide_index=True
    )


    # =================================================
    # 12. FOOTER
    # =================================================

    st.divider()

    st.caption(
        "Supply Chain Risk Prediction System | "
        "Historical Data Analysis | "
        "Powered by Python, Pandas, Plotly and Streamlit"
    )

    st.caption(
        "Note: Cancelled shipments are excluded from "
        "delivery performance calculations. "
        "Historical associations do not establish causation."
    )


# =====================================================
# 13. ERROR HANDLING
# =====================================================

except FileNotFoundError:

    st.error(
        f"Dataset not found at: {DATA_PATH}"
    )

except KeyError as e:

    st.error(
        f"Required dataset column is missing: {e}"
    )

except Exception as e:

    st.error(
        f"Something went wrong: {e}"
    )
