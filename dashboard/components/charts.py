
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


# --------------------------------------------------
# DELIVERY PERFORMANCE BREAKDOWN
# --------------------------------------------------

def delivery_performance_chart(df):

    if "Delivery Status" not in df.columns:
        st.warning("Delivery Status column not found.")
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
        st.info("No valid delivery records available.")
        return

    performance = (
        data["Delivery Status"]
        .value_counts()
        .reset_index()
    )

    performance.columns = [
        "Delivery Status",
        "Shipments"
    ]

    fig = px.bar(
        performance,
        x="Delivery Status",
        y="Shipments",
        color="Delivery Status",
        color_discrete_sequence=CHART_COLORS,
        text="Shipments"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Shipments: %{y:,}"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Delivery Performance Breakdown",
        height=420
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# MONTHLY LATE DELIVERY RATE
# --------------------------------------------------

def monthly_late_delivery_chart(df):

    date_column = "shipping date (DateOrders)"

    required_columns = [
        date_column,
        "Delivery Status"
    ]

    if not all(
        column in df.columns
        for column in required_columns
    ):
        st.warning("Required delivery columns not found.")
        return

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    data["Delivery Status"] = (
        data["Delivery Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    data = data.dropna(
        subset=[date_column]
    )

    data = data[
        ~data["Delivery Status"].str.contains(
            "cancel",
            na=False
        )
    ]

    if data.empty:
        st.info("No valid delivery records available.")
        return

    data["Month"] = (
        data[date_column]
        .dt.to_period("M")
        .astype(str)
    )

    data["Is Late"] = (
        data["Delivery Status"] == "late delivery"
    ).astype(int)

    monthly_data = (
        data.groupby("Month")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum")
        )
        .reset_index()
    )

    monthly_data["Late_Rate"] = (
        monthly_data["Late_Shipments"]
        / monthly_data["Total_Shipments"]
        * 100
    )

    fig = px.line(
        monthly_data,
        x="Month",
        y="Late_Rate",
        markers=True,
        color_discrete_sequence=["#EF4444"],
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Late Rate: %{y:.2f}%<br>"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Monthly Late Delivery Rate",
        height=420
    )

    fig.update_xaxes(
        title="Month",
        tickangle=-45
    )

    fig.update_yaxes(
        title="Late Delivery Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# SHIPPING MODE DELIVERY PERFORMANCE
# --------------------------------------------------

def shipping_mode_performance_chart(df):

    required_columns = [
        "Shipping Mode",
        "Delivery Status"
    ]

    if not all(
        column in df.columns
        for column in required_columns
    ):
        st.warning("Required shipping columns not found.")
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

    shipping_data = (
        data.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum")
        )
        .reset_index()
    )

    shipping_data["Late_Rate"] = (
        shipping_data["Late_Shipments"]
        / shipping_data["Total_Shipments"]
        * 100
    )

    shipping_data = shipping_data.sort_values(
        "Late_Rate",
        ascending=False
    )

    fig = px.bar(
        shipping_data,
        x="Shipping Mode",
        y="Late_Rate",
        color="Late_Rate",
        color_continuous_scale=[
            "#16A34A",
            "#F59E0B",
            "#EF4444"
        ],
        text="Late_Rate",
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Late Rate: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        "Late Delivery Rate by Shipping Mode",
        height=420
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_yaxes(
        title="Late Delivery Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# TOP 10 HIGH-RISK REGIONS
# --------------------------------------------------

def top_high_risk_regions_chart(df):

    required_columns = [
        "Order Region",
        "Delivery Status"
    ]

    if not all(col in df.columns for col in required_columns):
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
            "cancel", na=False
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

    top_regions = (
        regional_data
        .sort_values("Late_Rate", ascending=False)
        .head(10)
        .sort_values("Late_Rate", ascending=True)
    )

    fig = px.bar(
        top_regions,
        x="Late_Rate",
        y="Order Region",
        orientation="h",
        color="Late_Rate",
        color_continuous_scale=[
            "#F59E0B",
            "#EF4444"
        ],
        text="Late_Rate",
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig = apply_chart_layout(
        fig,
        "Top 10 High-Risk Regions",
        height=500
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        title="Late Delivery Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# REGIONAL DELIVERY STATUS COMPARISON
# --------------------------------------------------

def regional_delivery_comparison_chart(df):

    required_columns = [
        "Order Region",
        "Delivery Status"
    ]

    if not all(col in df.columns for col in required_columns):
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
            "cancel", na=False
        )
    ]

    if data.empty:
        st.info("No valid shipment records available.")
        return

    regional_data = (
        data.groupby(
            ["Order Region", "Delivery Status"]
        )
        .size()
        .reset_index(name="Shipments")
    )

    regional_data["Delivery Status"] = (
        regional_data["Delivery Status"]
        .str.title()
    )

    fig = px.bar(
        regional_data,
        x="Order Region",
        y="Shipments",
        color="Delivery Status",
        barmode="group",
        color_discrete_sequence=CHART_COLORS
    )

    fig = apply_chart_layout(
        fig,
        "Regional Delivery Status Comparison",
        height=500
    )

    fig.update_xaxes(
        title="Region",
        tickangle=-45
    )

    fig.update_yaxes(
        title="Number of Shipments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# REGIONAL KPI SUMMARY
# --------------------------------------------------

def regional_summary_table(df):

    required_columns = [
        "Order Region",
        "Delivery Status"
    ]

    if not all(col in df.columns for col in required_columns):
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
            "cancel", na=False
        )
    ]

    if data.empty:
        st.info("No valid shipment records available.")
        return

    data["Is Late"] = (
        data["Delivery Status"] == "late delivery"
    ).astype(int)

    summary = (
        data.groupby("Order Region")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum")
        )
        .reset_index()
    )

    summary["On_Time_or_Advance"] = (
        summary["Total_Shipments"]
        - summary["Late_Shipments"]
    )

    summary["Late_Rate"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary = summary.sort_values(
        "Late_Rate",
        ascending=False
    )

    summary["Late_Rate"] = (
        summary["Late_Rate"].round(2)
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# SHIPPING MODE SHIPMENT VOLUME
# --------------------------------------------------

def shipping_volume_chart(df):

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
        "Total Shipments"
    ]

    fig = px.bar(
        chart_data,
        x="Shipping Mode",
        y="Total Shipments",
        color="Total Shipments",
        color_continuous_scale=["#14532D", "#16A34A"],
        text="Total Shipments"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig = apply_chart_layout(
        fig,
        "Shipment Volume by Shipping Mode"
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# SHIPPING MODE LATE DELIVERY RATE
# --------------------------------------------------

def shipping_late_rate_chart(df):

    required = ["Shipping Mode", "Delivery Status"]

    if not all(col in df.columns for col in required):
        st.warning("Required shipping columns not found.")
        return

    data = df.copy()

    data["Delivery Status"] = (
        data["Delivery Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    data = data[
        ~data["Delivery Status"].str.contains("cancel", na=False)
    ]

    if data.empty:
        st.info("No valid shipments available.")
        return

    data["Is Late"] = (
        data["Delivery Status"] == "late delivery"
    ).astype(int)

    summary = (
        data.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum")
        )
        .reset_index()
    )

    summary["Late_Rate"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary = summary.sort_values(
        "Late_Rate",
        ascending=False
    )

    fig = px.bar(
        summary,
        x="Shipping Mode",
        y="Late_Rate",
        color="Late_Rate",
        color_continuous_scale=[
            "#16A34A",
            "#F59E0B",
            "#EF4444"
        ],
        text="Late_Rate",
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig = apply_chart_layout(
        fig,
        "Late Delivery Rate by Shipping Mode"
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_yaxes(
        title="Late Delivery Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# SCHEDULED SHIPPING DAYS ANALYSIS
# --------------------------------------------------

def scheduled_days_chart(df):

    column = "Days for shipment (scheduled)"

    if column not in df.columns:
        st.warning("Scheduled shipping days column not found.")
        return

    data = df.copy()

    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )

    data = data.dropna(subset=[column])

    if data.empty:
        st.info("No scheduled shipping data available.")
        return

    summary = (
        data.groupby(column)
        .size()
        .reset_index(name="Total Shipments")
    )

    summary[column] = summary[column].astype(str)

    fig = px.bar(
        summary,
        x=column,
        y="Total Shipments",
        color="Total Shipments",
        color_continuous_scale=["#1E3A8A", "#3B82F6"],
        text="Total Shipments"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig = apply_chart_layout(
        fig,
        "Shipments by Scheduled Delivery Days"
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        title="Scheduled Days"
    )

    fig.update_yaxes(
        title="Number of Shipments"
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# SHIPPING MODE PERFORMANCE SUMMARY
# --------------------------------------------------

def shipping_performance_table(df):

    required = [
        "Shipping Mode",
        "Delivery Status",
        "Days for shipment (scheduled)"
    ]

    if not all(col in df.columns for col in required):
        st.warning("Required shipping columns not found.")
        return

    data = df.copy()

    data["Delivery Status"] = (
        data["Delivery Status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    data = data[
        ~data["Delivery Status"].str.contains("cancel", na=False)
    ]

    data["Is Late"] = (
        data["Delivery Status"] == "late delivery"
    ).astype(int)

    summary = (
        data.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Is Late", "count"),
            Late_Shipments=("Is Late", "sum"),
            Avg_Scheduled_Days=(
                "Days for shipment (scheduled)",
                "mean"
            )
        )
        .reset_index()
    )

    summary["Late_Rate"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary["Late_Rate"] = summary["Late_Rate"].round(2)

    summary["Avg_Scheduled_Days"] = (
        summary["Avg_Scheduled_Days"].round(2)
    )

    summary = summary.sort_values(
        "Late_Rate",
        ascending=False
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    
# --------------------------------------------------
# PREPARE RISK DATA
# --------------------------------------------------

def prepare_risk_data(df):

    required_columns = ["Late_delivery_risk"]

    if not all(col in df.columns for col in required_columns):
        return None

    data = df.copy()

    data["Late_delivery_risk"] = pd.to_numeric(
        data["Late_delivery_risk"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Late_delivery_risk"]
    )

    data = data[
        data["Late_delivery_risk"].isin([0, 1])
    ]

    data["Risk Level"] = data["Late_delivery_risk"].map({
        0: "Low Risk",
        1: "High Risk"
    })

    return data


# --------------------------------------------------
# HIGH RISK VS LOW RISK DISTRIBUTION
# --------------------------------------------------

def risk_distribution_chart(df):

    data = prepare_risk_data(df)

    if data is None or data.empty:
        st.warning("Risk data is not available.")
        return

    risk_summary = (
        data["Risk Level"]
        .value_counts()
        .reset_index()
    )

    risk_summary.columns = [
        "Risk Level",
        "Shipments"
    ]

    fig = px.pie(
        risk_summary,
        names="Risk Level",
        values="Shipments",
        hole=0.55,
        color="Risk Level",
        color_discrete_map={
            "High Risk": "#EF4444",
            "Low Risk": "#16A34A"
        }
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
        "High-Risk vs Low-Risk Shipments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# RISK BY SHIPPING MODE
# --------------------------------------------------

def risk_by_shipping_mode_chart(df):

    data = prepare_risk_data(df)

    if data is None or data.empty:
        st.warning("Risk data is not available.")
        return

    if "Shipping Mode" not in data.columns:
        st.warning("Shipping Mode column not found.")
        return

    summary = (
        data.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Late_delivery_risk", "count"),
            High_Risk_Shipments=("Late_delivery_risk", "sum")
        )
        .reset_index()
    )

    summary["Risk_Rate"] = (
        summary["High_Risk_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary = summary.sort_values(
        "Risk_Rate",
        ascending=False
    )

    fig = px.bar(
        summary,
        x="Shipping Mode",
        y="Risk_Rate",
        color="Risk_Rate",
        color_continuous_scale=[
            "#16A34A",
            "#F59E0B",
            "#EF4444"
        ],
        text="Risk_Rate",
        hover_data=[
            "Total_Shipments",
            "High_Risk_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig = apply_chart_layout(
        fig,
        "Historical Risk Rate by Shipping Mode"
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_yaxes(
        title="High-Risk Shipment Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# RISK BY REGION
# --------------------------------------------------

def risk_by_region_chart(df):

    data = prepare_risk_data(df)

    if data is None or data.empty:
        st.warning("Risk data is not available.")
        return

    if "Order Region" not in data.columns:
        st.warning("Order Region column not found.")
        return

    summary = (
        data.groupby("Order Region")
        .agg(
            Total_Shipments=("Late_delivery_risk", "count"),
            High_Risk_Shipments=("Late_delivery_risk", "sum")
        )
        .reset_index()
    )

    summary["Risk_Rate"] = (
        summary["High_Risk_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary = summary.sort_values(
        "Risk_Rate",
        ascending=True
    )

    fig = px.bar(
        summary,
        x="Risk_Rate",
        y="Order Region",
        orientation="h",
        color="Risk_Rate",
        color_continuous_scale=[
            "#16A34A",
            "#F59E0B",
            "#EF4444"
        ],
        hover_data=[
            "Total_Shipments",
            "High_Risk_Shipments"
        ]
    )

    fig = apply_chart_layout(
        fig,
        "Historical Risk Rate by Region",
        height=550
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    fig.update_xaxes(
        title="High-Risk Shipment Rate (%)",
        ticksuffix="%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# HIGH RISK SHIPMENT DETAILS
# --------------------------------------------------

def high_risk_shipment_table(df):

    data = prepare_risk_data(df)

    if data is None or data.empty:
        st.warning("Risk data is not available.")
        return

    high_risk = data[
        data["Late_delivery_risk"] == 1
    ].copy()

    display_columns = [
        "Order Id",
        "Shipping Mode",
        "Order Region",
        "Market",
        "Customer Segment",
        "Days for shipment (scheduled)",
        "Late_delivery_risk"
    ]

    available_columns = [
        col for col in display_columns
        if col in high_risk.columns
    ]

    if not available_columns:
        st.warning("No shipment detail columns available.")
        return

    st.write(
        f"High-risk shipments found: {len(high_risk):,}"
    )

    st.dataframe(
        high_risk[available_columns].head(100),
        use_container_width=True,
        hide_index=True
    )

    csv_data = high_risk[available_columns].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download High-Risk Shipments",
        data=csv_data,
        file_name="high_risk_shipments.csv",
        mime="text/csv"
    )




