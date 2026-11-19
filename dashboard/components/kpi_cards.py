
"""
Reusable KPI Cards Component
Supply Chain Business Intelligence Dashboard
"""

import streamlit as st


# ==========================================================
# KPI CARD CONFIGURATION
# ==========================================================

KPI_CONFIG = {
    "total_shipments": {
        "label": "TOTAL SHIPMENTS",
        "icon": "📦",
        "color": "#38BDF8",
        "format": "number"
    },

    "valid_deliveries": {
        "label": "VALID DELIVERIES",
        "icon": "🚚",
        "color": "#22C55E",
        "format": "number"
    },

    "late_deliveries": {
        "label": "LATE DELIVERIES",
        "icon": "⚠️",
        "color": "#F87171",
        "format": "number"
    },

    "late_delivery_rate": {
        "label": "LATE DELIVERY RATE",
        "icon": "📉",
        "color": "#F59E0B",
        "format": "percentage"
    },

    "avg_scheduled_days": {
        "label": "AVG. SCHEDULED DAYS",
        "icon": "📅",
        "color": "#A78BFA",
        "format": "decimal"
    }
}


# ==========================================================
# VALUE FORMATTER
# ==========================================================

def format_kpi_value(value, format_type="number"):

    if value is None:
        value = 0

    if format_type == "percentage":
        return f"{value:.2f}%"

    elif format_type == "decimal":
        return f"{value:.2f}"

    return f"{value:,.0f}"


# ==========================================================
# KPI CARD HTML
# ==========================================================

def create_kpi_card(label, value, icon, color):

    return f"""
    <div style="
        background: linear-gradient(
            135deg,
            #172338,
            #1E293B
        );
        border: 1px solid #334155;
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 20px 18px;
        min-height: 125px;
        box-sizing: border-box;
        width: 100%;
    ">

        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">

            <span style="
                color: #94A3B8;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            ">
                {label}
            </span>

            <span style="font-size: 22px;">
                {icon}
            </span>

        </div>

        <div style="
            color: #F8FAFC;
            font-size: 28px;
            font-weight: 800;
            margin-top: 18px;
            letter-spacing: -0.5px;
        ">
            {value}
        </div>

    </div>
    """


# ==========================================================
# DISPLAY KPI CARDS
# ==========================================================

def display_kpi_cards(
    total_shipments,
    valid_deliveries,
    late_deliveries,
    late_delivery_rate,
    avg_scheduled_days
):
    """
    Display five reusable KPI cards.

    Values should be calculated from the currently
    filtered dataframe.
    """

    kpi_values = {
        "total_shipments": total_shipments,
        "valid_deliveries": valid_deliveries,
        "late_deliveries": late_deliveries,
        "late_delivery_rate": late_delivery_rate,
        "avg_scheduled_days": avg_scheduled_days
    }

    columns = st.columns(5)

    for column, (key, config) in zip(
        columns,
        KPI_CONFIG.items()
    ):

        value = format_kpi_value(
            kpi_values[key],
            config["format"]
        )

        card_html = create_kpi_card(
            label=config["label"],
            value=value,
            icon=config["icon"],
            color=config["color"]
        )

        with column:

            if hasattr(st, "html"):
                st.html(card_html)
            else:
                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )


# ==========================================================
# COMPACT KPI DISPLAY
# ==========================================================

def display_compact_kpis(metrics):
    """
    Display custom KPI metrics using a dictionary.

    Example:
    {
        "Total Orders": 1000,
        "Late Shipments": 500
    }
    """

    if not metrics:
        st.info("No KPI metrics available.")
        return

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(
        columns,
        metrics.items()
    ):

        with column:

            st.metric(
                label=label,
                value=f"{value:,}"
                if isinstance(value, (int, float))
                else str(value)
            )
