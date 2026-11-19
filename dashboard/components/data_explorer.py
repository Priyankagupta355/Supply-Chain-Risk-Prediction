
import streamlit as st
import pandas as pd
from io import BytesIO


def get_excel_file(data):
    """Convert DataFrame into an Excel file in memory."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(
            writer,
            index=False,
            sheet_name="Supply Chain Data"
        )

    output.seek(0)
    return output


def render_data_explorer(df):

    st.markdown("## Dataset Explorer")
    st.caption(
        "Explore, search, sort, analyze and export your supply chain dataset."
    )

    if df is None or df.empty:
        st.warning("No data available to explore.")
        return

    # -----------------------------------
    # 1. DATASET SUMMARY
    # -----------------------------------

    st.markdown("### Dataset Summary")

    total_rows = len(df)
    total_columns = len(df.columns)
    total_missing = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{total_rows:,}")

    with col2:
        st.metric("Total Columns", total_columns)

    with col3:
        st.metric("Missing Values", f"{total_missing:,}")

    with col4:
        st.metric("Duplicate Rows", f"{duplicate_rows:,}")

    st.divider()

    # -----------------------------------
    # 2. COLUMN SELECTION
    # -----------------------------------

    st.markdown("### Select Columns")

    selected_columns = st.multiselect(
        "Choose columns to display",
        options=list(df.columns),
        default=list(df.columns[:10]),
        key="explorer_columns"
    )

    if not selected_columns:
        st.info("Please select at least one column.")
        return

    display_df = df[selected_columns].copy()

    # -----------------------------------
    # 3. GLOBAL SEARCH
    # -----------------------------------

    st.markdown("### Search Dataset")

    search_query = st.text_input(
        "Search across selected columns",
        placeholder="Enter a keyword or value...",
        key="explorer_search"
    )

    if search_query.strip():

        search_mask = display_df.astype(str).apply(
            lambda column: column.str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
        ).any(axis=1)

        display_df = display_df.loc[search_mask]

        st.caption(
            f"Search results: {len(display_df):,} matching records"
        )

    # -----------------------------------
    # 4. SORTING
    # -----------------------------------

    st.markdown("### Sort Records")

    sort_col1, sort_col2 = st.columns(2)

    with sort_col1:
        sort_column = st.selectbox(
            "Sort by column",
            options=selected_columns,
            key="explorer_sort_column"
        )

    with sort_col2:
        sort_order = st.selectbox(
            "Sort order",
            options=["Ascending", "Descending"],
            key="explorer_sort_order"
        )

    if sort_column in display_df.columns:
        display_df = display_df.sort_values(
            by=sort_column,
            ascending=(sort_order == "Ascending"),
            na_position="last"
        )

    # -----------------------------------
    # 5. ROW LIMIT
    # -----------------------------------

    st.markdown("### Display Settings")

    row_limit = st.select_slider(
        "Number of records to display",
        options=[100, 500, 1000, 2500, 5000, 10000],
        value=1000,
        key="explorer_row_limit"
    )

    st.caption(
        f"Showing {min(len(display_df), row_limit):,} of "
        f"{len(display_df):,} matching records"
    )

    preview_df = display_df.head(row_limit)

    st.dataframe(
        preview_df,
        use_container_width=True,
        height=450,
        hide_index=True
    )

    st.divider()

    # -----------------------------------
    # 6. MISSING VALUE ANALYSIS
    # -----------------------------------

    st.markdown("### Missing Value Analysis")

    missing_data = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean().values * 100
        ).round(2)
    })

    missing_data = missing_data.sort_values(
        by="Missing Percentage",
        ascending=False
    )

    missing_data = missing_data[
        missing_data["Missing Values"] > 0
    ]

    if missing_data.empty:
        st.success("No missing values found in the dataset.")
    else:
        missing_col1, missing_col2 = st.columns(2)

        with missing_col1:
            st.metric(
                "Columns With Missing Values",
                len(missing_data)
            )

        with missing_col2:
            st.metric(
                "Total Missing Cells",
                f"{total_missing:,}"
            )

        st.dataframe(
            missing_data,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            missing_data.set_index("Column")[
                "Missing Percentage"
            ],
            height=350
        )

    st.divider()

    # -----------------------------------
    # 7. DATA QUALITY SUMMARY
    # -----------------------------------

    st.markdown("### Data Quality Summary")

    quality_data = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Values": df.notnull().sum().values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        quality_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------------
    # 8. DATA EXPORT
    # -----------------------------------

    st.markdown("### Export Dataset")

    export_col1, export_col2 = st.columns(2)

    with export_col1:
        csv_data = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="supply_chain_explorer.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:
        try:
            excel_data = get_excel_file(display_df)

            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name="supply_chain_explorer.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )

        except ImportError:
            st.warning(
                "Excel export ke liye openpyxl install karo: "
                "pip install openpyxl"
            )
