
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Common chart layout
def _apply_layout(fig, title, height=420):
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=height,
        margin=dict(l=30, r=30, t=65, b=30),
        title_x=0.02,
        legend_title_text=""
    )
    return fig


# 1. Delivery Status Donut Chart
def delivery_status_chart(
    df,
    status_col="Delivery Status"
):
    if status_col not in df.columns:
        raise ValueError(f"Column '{status_col}' not found.")

    status_counts = (
        df[status_col]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Delivery Status",
        "Count"
    ]

    fig = px.pie(
        status_counts,
        names="Delivery Status",
        values="Count",
        hole=0.55,
        title="Delivery Status Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return _apply_layout(fig, "Delivery Status Distribution")


# 2. Shipping Mode Late Delivery Chart
def shipping_mode_chart(
    df,
    mode_col="Shipping Mode",
    status_col="Delivery Status"
):
    required = [mode_col, status_col]

    if not all(col in df.columns for col in required):
        raise ValueError("Required shipping mode columns not found.")

    valid_df = df[
        df[status_col] != "Shipping canceled"
    ].copy()

    summary = (
        valid_df.groupby(mode_col)
        .agg(
            Total_Shipments=(status_col, "count"),
            Late_Shipments=(
                status_col,
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    summary["Late_Delivery_Percentage"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    fig = px.bar(
        summary,
        x=mode_col,
        y="Late_Delivery_Percentage",
        text="Late_Delivery_Percentage",
        title="Late Delivery Rate by Shipping Mode",
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_yaxes(title="Late Delivery (%)")

    return _apply_layout(
        fig,
        "Late Delivery Rate by Shipping Mode"
    )


# 3. Regional Late Delivery Chart
def regional_delivery_chart(
    df,
    region_col="Order Region",
    status_col="Delivery Status",
    top_n=10
):
    required = [region_col, status_col]

    if not all(col in df.columns for col in required):
        raise ValueError("Required regional columns not found.")

    valid_df = df[
        df[status_col] != "Shipping canceled"
    ].copy()

    summary = (
        valid_df.groupby(region_col)
        .agg(
            Total_Shipments=(status_col, "count"),
            Late_Shipments=(
                status_col,
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    summary["Late_Delivery_Percentage"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    summary = (
        summary.sort_values(
            "Late_Delivery_Percentage",
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        summary,
        x="Late_Delivery_Percentage",
        y=region_col,
        orientation="h",
        text="Late_Delivery_Percentage",
        title=f"Top {top_n} Regions by Late Delivery Rate",
        hover_data=[
            "Total_Shipments",
            "Late_Shipments"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(title="Late Delivery (%)")

    return _apply_layout(
        fig,
        f"Top {top_n} Regions by Late Delivery Rate",
        height=500
    )


# 4. Monthly Delivery Trend Chart
def monthly_delivery_trend(
    df,
    date_col="order date (DateOrders)",
    status_col="Delivery Status"
):
    required = [date_col, status_col]

    if not all(col in df.columns for col in required):
        raise ValueError("Required date or status columns not found.")

    trend_df = df.copy()

    trend_df[date_col] = pd.to_datetime(
        trend_df[date_col],
        errors="coerce"
    )

    trend_df = trend_df.dropna(subset=[date_col])

    trend_df = trend_df[
        trend_df[status_col] != "Shipping canceled"
    ].copy()

    trend_df["Month"] = (
        trend_df[date_col]
        .dt.to_period("M")
        .astype(str)
    )

    summary = (
        trend_df.groupby("Month")
        .agg(
            Total_Shipments=(status_col, "count"),
            Late_Shipments=(
                status_col,
                lambda x: (x == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    summary["Late_Delivery_Percentage"] = (
        summary["Late_Shipments"]
        / summary["Total_Shipments"]
        * 100
    )

    fig = px.line(
        summary,
        x="Month",
        y="Late_Delivery_Percentage",
        markers=True,
        title="Monthly Late Delivery Trend"
    )

    fig.update_yaxes(title="Late Delivery (%)")
    fig.update_xaxes(title="Month")

    return _apply_layout(
        fig,
        "Monthly Late Delivery Trend"
    )


# 5. Feature Importance Chart
def feature_importance_chart(
    importance_df,
    feature_col="Feature",
    importance_col="Importance",
    top_n=10
):
    required = [feature_col, importance_col]

    if not all(col in importance_df.columns for col in required):
        raise ValueError("Feature importance columns not found.")

    plot_df = (
        importance_df
        .sort_values(importance_col, ascending=False)
        .head(top_n)
        .sort_values(importance_col, ascending=True)
    )

    fig = px.bar(
        plot_df,
        x=importance_col,
        y=feature_col,
        orientation="h",
        title="Top Feature Importance"
    )

    fig.update_xaxes(title="Importance")
    fig.update_yaxes(title="Feature")

    return _apply_layout(
        fig,
        "Top Feature Importance",
        height=500
    )


# 6. Confusion Matrix Heatmap
def confusion_matrix_chart(
    matrix,
    labels=("Not Late", "Late")
):
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=list(labels),
            y=list(labels),
            colorscale="Blues",
            text=matrix,
            texttemplate="%{text}",
            textfont={"size": 16},
            hovertemplate=(
                "Actual: %{y}<br>"
                "Predicted: %{x}<br>"
                "Count: %{z}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Label",
        yaxis_title="Actual Label",
        template="plotly_dark",
        height=450,
        title_x=0.02
    )

    return fig
