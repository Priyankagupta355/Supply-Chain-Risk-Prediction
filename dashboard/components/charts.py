
import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# CHART THEME
# --------------------------------------------------

CHART_TEMPLATE = "plotly_dark"

CHART_COLORS = [
    "#16A34A",
    "#3B82F6",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#06B6D4",
    "#EC4899"
]


def apply_chart_layout(fig, title, height=380):

    fig.update_layout(
        title={
            "text": title,
            "font": {
                "size": 18,
                "color": "#F8FAFC"
            }
        },
        template=CHART_TEMPLATE,
        height=height,
        paper_bgcolor="#0B1120",
        plot_bgcolor="#111827",
        font={
            "color": "#E5E7EB",
            "family": "Arial"
        },
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=35
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig


# --------------------------------------------------
# DELIVERY STATUS DONUT CHART
# --------------------------------------------------

def delivery_status_chart(df):

    if "Delivery Status" not in df.columns:
        st.warning("Delivery Status column not found.")
        return

    chart_data = (
        df["Delivery Status"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    chart_data.columns = [
        "Delivery Status",
        "Shipments"
    ]

    fig = px.pie(
        chart_data,
        names="Delivery Status",
        values="Shipments",
        hole=0.55,
        color_discrete_sequence=CHART_COLORS
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Shipments: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Delivery Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# MONTHLY DELIVERY TREND
# --------------------------------------------------

def monthly_delivery_trend(df):

    date_column = "shipping date (DateOrders)"

    if date_column not in df.columns:
        st.warning("Shipping date column not found.")
        return

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    data = data.dropna(
        subset=[date_column]
    )

    if data.empty:
        st.info("No valid dates available.")
        return

    data["Month"] = (
        data[date_column]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_data = (
        data.groupby("Month")
        .size()
        .reset_index(name="Shipments")
    )

    fig = px.line(
        monthly_data,
        x="Month",
        y="Shipments",
        markers=True,
        color_discrete_sequence=["#16A34A"]
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Shipments: %{y:,}"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Monthly Shipment Trend",
        height=400
    )

    fig.update_xaxes(
        tickangle=-45,
        title="Month"
    )

    fig.update_yaxes(
        title="Total Shipments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# REGIONAL SHIPMENT PERFORMANCE
# --------------------------------------------------

def regional_shipment_chart(df):

    required_columns = [
        "Order Region",
        "Delivery Status"
    ]

    if not all(
        column in df.columns
        for column in required_columns
    ):
        st.warning("Required regional columns not found.")
        return

    data = df.copy()

    data["Delivery Status"] = (
        data["Delivery Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    data = data[
        ~data["Delivery Status"].str.contains(
            "cancel",
            na=False
        )
    ]

    if data.empty:
        st.info("No valid shipment records available.")
        return

    regional_data = (
        data.groupby("Order Region")
        .size()
        .reset_index(name="Shipments")
        .sort_values(
            "Shipments",
            ascending=True
        )
    )

    fig = px.bar(
        regional_data,
        x="Shipments",
        y="Order Region",
        orientation="h",
        color="Shipments",
        color_continuous_scale=[
            "#14532D",
            "#16A34A",
            "#4ADE80"
        ]
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Shipments: %{x:,}"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Regional Shipment Performance",
        height=550
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        title="Total Shipments"
    )

    fig.update_yaxes(
        title="Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# SHIPPING MODE DISTRIBUTION
# --------------------------------------------------

def shipping_mode_chart(df):

    if "Shipping Mode" not in df.columns:
        st.warning("Shipping Mode column not found.")
        return

    chart_data = (
        df["Shipping Mode"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    chart_data.columns = [
        "Shipping Mode",
        "Shipments"
    ]

    fig = px.bar(
        chart_data,
        x="Shipping Mode",
        y="Shipments",
        color="Shipping Mode",
        color_discrete_sequence=CHART_COLORS
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Shipments: %{y:,}"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Shipping Mode Distribution"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# LATE DELIVERY BY REGION
# --------------------------------------------------

def regional_late_delivery_chart(df):

    required_columns = [
        "Order Region",
        "Delivery Status"
    ]

    if not all(
        column in df.columns
        for column in required_columns
    ):
        st.warning("Required columns not found.")
        return

    data = df.copy()

    data["Delivery Status"] = (
        data["Delivery Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    data = data[
        ~data["Delivery Status"].str.contains(
            "cancel",
            na=False
        )
    ]

    if data.empty:
        st.info("No valid shipment records available.")
        return

    data["Is Late"] = (
        data["Delivery Status"] == "late delivery"
    ).astype(int)

    regional_data = (
        data.groupby("Order Region")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum")
        )
        .reset_index()
    )

    regional_data["Late_Rate"] = (
        regional_data["Late_Shipments"]
        / regional_data["Total_Shipments"]
        * 100
    )

    regional_data = regional_data.sort_values(
        "Late_Rate",
        ascending=False
    )

    fig = px.bar(
        regional_data,
        x="Order Region",
        y="Late_Rate",
        color="Late_Rate",
        color_continuous_scale=[
            "#14532D",
            "#F59E0B",
            "#EF4444"
        ],
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Late Rate: %{y:.2f}%<br>"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Late Delivery Rate by Region",
        height=450
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        tickangle=-45,
        title="Region"
    )

    fig.update_yaxes(
        title="Late Delivery Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
