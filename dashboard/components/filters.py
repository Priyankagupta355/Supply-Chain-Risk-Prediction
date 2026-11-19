
"""
Global interactive filters for Supply Chain BI Dashboard.

Provides date, region, shipping mode, market and
customer segment filters.
"""

import streamlit as st
import pandas as pd


# ==========================================================
# FILTER CONFIGURATION
# ==========================================================

DATE_COLUMN = "shipping date (DateOrders)"

FILTER_COLUMNS = {
    "Order Region": "Order Region",
    "Shipping Mode": "Shipping Mode",
    "Market": "Market",
    "Customer Segment": "Customer Segment",
}


# ==========================================================
# GET FILTER OPTIONS
# ==========================================================

def get_filter_options(df, column):
    """Get unique non-null values for a filter column."""

    if column not in df.columns:
        return []

    return sorted(
        df[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


# ==========================================================
# APPLY GLOBAL FILTERS
# ==========================================================

def apply_global_filters(df):
    """
    Display interactive global filters and return
    the filtered dataframe along with selected filters.
    """

    if df is None or df.empty:
        st.warning("No dataset available for filtering.")
        return df.copy() if df is not None else pd.DataFrame(), {}

    filtered_df = df.copy()

    selected_filters = {}

    st.markdown("### 🔎 Global Filters")

    st.caption(
        "Use the filters below to explore supply chain data."
    )

    # ------------------------------------------------------
    # DATE PREPARATION
    # ------------------------------------------------------

    if DATE_COLUMN in filtered_df.columns:

        dates = pd.to_datetime(
            filtered_df[DATE_COLUMN],
            errors="coerce"
        )

        valid_dates = dates.dropna()

        if not valid_dates.empty:

            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            # --------------------------------------------------
            # FILTER LAYOUT
            # --------------------------------------------------

            filter_columns = st.columns([1.5, 1, 1, 1, 1])

            with filter_columns[0]:

                selected_dates = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="global_date_filter"
                )

            if isinstance(selected_dates, (tuple, list)):

                if len(selected_dates) == 2:

                    start_date, end_date = selected_dates

                    date_mask = (
                        dates.dt.date.ge(start_date)
                        & dates.dt.date.le(end_date)
                    )

                    filtered_df = filtered_df.loc[
                        date_mask.fillna(False)
                    ].copy()

                    selected_filters["Date Range"] = (
                        start_date,
                        end_date
                    )

                elif len(selected_dates) == 1:

                    selected_date = selected_dates[0]

                    date_mask = (
                        dates.dt.date == selected_date
                    )

                    filtered_df = filtered_df.loc[
                        date_mask.fillna(False)
                    ].copy()

                    selected_filters["Date Range"] = selected_date

            else:
                selected_filters["Date Range"] = selected_dates

            selected_filters["Date Range"] = (
                selected_dates
            )

        else:
            filter_columns = st.columns(4)

    else:
        filter_columns = st.columns(4)

        with filter_columns[0]:
            st.caption("Date column unavailable")

    # ------------------------------------------------------
    # CATEGORICAL FILTERS
    # ------------------------------------------------------

    available_filter_columns = list(FILTER_COLUMNS.items())

    for index, (label, column) in enumerate(
        available_filter_columns
    ):

        if column not in filtered_df.columns:
            continue

        options = get_filter_options(df, column)

        if not options:
            continue

        # First categorical filter goes in second column
        position = index + 1

        with filter_columns[position]:

            selected_value = st.selectbox(
                label,
                options=["All"] + options,
                index=0,
                key=f"global_filter_{index}"
            )

        selected_filters[label] = selected_value

        if selected_value != "All":

            filtered_df = filtered_df[
                filtered_df[column]
                .astype(str)
                == selected_value
            ].copy()

    # ------------------------------------------------------
    # FILTER SUMMARY
    # ------------------------------------------------------

    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:

        st.caption(
            f"Showing {len(filtered_df):,} records "
            f"out of {len(df):,} total records."
        )

    with col2:

        if st.button(
            "Reset Filters",
            key="reset_global_filters",
            use_container_width=True
        ):

            for key in [
                "global_date_filter",
                "global_filter_0",
                "global_filter_1",
                "global_filter_2",
                "global_filter_3",
            ]:

                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    return filtered_df, selected_filters
