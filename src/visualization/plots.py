
"""
Reusable visualization functions for Supply Chain Risk Prediction.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def delivery_distribution_chart(df: pd.DataFrame):
    """Visualize delivery status distribution."""

    counts = df["Delivery Status"].value_counts().reset_index()
    counts.columns = ["Delivery Status", "Count"]

    fig = px.pie(
        counts,
        names="Delivery Status",
        values="Count",
        hole=0.55,
        title="Delivery Status Distribution"
    )

    fig.update_layout(template="plotly_dark")
    return fig


def shipping_mode_risk_chart(df: pd.DataFrame):
    """Compare late delivery percentage across shipping modes."""

    summary = (
        df.groupby("Shipping Mode")
        .agg(
            Total_Shipments=("Target", "count"),
            Late_Shipments=("Target", "sum")
        )
        .reset_index()
    )

    summary["Late_Delivery_Percentage"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"] * 100
    )

    fig = px.bar(
        summary.sort_values(
            "Late_Delivery_Percentage",
            ascending=False
        ),
        x="Shipping Mode",
        y="Late_Delivery_Percentage",
        text="Late_Delivery_Percentage",
        title="Late Delivery Rate by Shipping Mode"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis_title="Late Delivery (%)"
    )

    return fig


def regional_delivery_chart(df: pd.DataFrame):
    """Visualize late delivery percentage by region."""

    summary = (
        df.groupby("Order Region")
        .agg(
            Total_Shipments=("Target", "count"),
            Late_Shipments=("Target", "sum")
        )
        .reset_index()
    )

    summary["Late_Delivery_Percentage"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"] * 100
    )

    summary = summary.sort_values(
        "Late_Delivery_Percentage",
        ascending=False
    )

    fig = px.bar(
        summary,
        x="Late_Delivery_Percentage",
        y="Order Region",
        orientation="h",
        title="Late Delivery Rate by Region"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Late Delivery (%)",
        yaxis_title="Order Region"
    )

    return fig


def monthly_delivery_trend(df: pd.DataFrame):
    """Visualize monthly late delivery trends."""

    if "shipping date (DateOrders)" not in df.columns:
        raise ValueError("Shipping date column is missing.")

    data = df.copy()

    data["Shipping_Date"] = pd.to_datetime(
        data["shipping date (DateOrders)"],
        errors="coerce"
    )

    data = data.dropna(subset=["Shipping_Date"])

    data["Month"] = (
        data["Shipping_Date"].dt.to_period("M").astype(str)
    )

    summary = (
        data.groupby("Month")["Target"]
        .mean()
        .mul(100)
        .reset_index(name="Late_Delivery_Percentage")
    )

    fig = px.line(
        summary,
        x="Month",
        y="Late_Delivery_Percentage",
        markers=True,
        title="Monthly Late Delivery Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis_title="Late Delivery (%)"
    )

    return fig


def feature_importance_chart(
    importance_df: pd.DataFrame,
    feature_column: str = "Feature",
    importance_column: str = "Importance"
):
    """Visualize feature importance values."""

    required = [feature_column, importance_column]

    if not all(column in importance_df.columns for column in required):
        raise ValueError("Required feature importance columns are missing.")

    data = importance_df.sort_values(
        importance_column,
        ascending=True
    )

    fig = px.bar(
        data,
        x=importance_column,
        y=feature_column,
        orientation="h",
        title="Model Feature Importance"
    )

    fig.update_layout(template="plotly_dark")
    return fig


def confusion_matrix_chart(matrix):
    """Create a confusion matrix heatmap."""

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=["Predicted Not Late", "Predicted Late"],
            y=["Actual Not Late", "Actual Late"],
            text=matrix,
            texttemplate="%{text}",
            colorscale="Blues"
        )
    )

    fig.update_layout(
        title="Confusion Matrix",
        template="plotly_dark",
        xaxis_title="Predicted Label",
        yaxis_title="Actual Label"
    )

    return fig
