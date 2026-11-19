
import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# CUSTOM ANALYSIS BUILDER
# --------------------------------------------------

def render_adhoc_analysis(df):

    st.markdown("### Build Your Own Analysis")

    st.caption(
        "Select dimensions, metrics and chart type to create "
        "your own supply chain analysis."
    )

    if df.empty:
        st.warning("No data available for analysis.")
        return

    # --------------------------------------------------
    # AVAILABLE COLUMNS
    # --------------------------------------------------

    categorical_columns = [
        col for col in df.columns
        if (
            df[col].dtype == "object"
            or isinstance(df[col].dtype, pd.CategoricalDtype)
        )
    ]

    numerical_columns = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    if not categorical_columns:
        st.warning("No categorical columns available.")
        return

    if not numerical_columns:
        st.warning("No numerical columns available.")
        return

    # --------------------------------------------------
    # ANALYSIS SETTINGS
    # --------------------------------------------------

    st.markdown("#### Analysis Configuration")

    col1, col2 = st.columns(2)

    with col1:

        dimension = st.selectbox(
            "Select Dimension (X-axis)",
            categorical_columns,
            key="adhoc_dimension"
        )

        metric = st.selectbox(
            "Select Metric (Y-axis)",
            [
                "Shipment Count",
                "Sum",
                "Average",
                "Maximum",
                "Minimum"
            ],
            key="adhoc_metric"
        )

    with col2:

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Scatter Chart"
            ],
            key="adhoc_chart_type"
        )

        sort_order = st.selectbox(
            "Sort Results",
            [
                "Descending",
                "Ascending"
            ],
            key="adhoc_sort"
        )

    # --------------------------------------------------
    # NUMERIC COLUMN SELECTION
    # --------------------------------------------------

    numeric_column = None

    if metric != "Shipment Count":

        numeric_column = st.selectbox(
            "Select Numerical Column",
            numerical_columns,
            key="adhoc_numeric_column"
        )

    # --------------------------------------------------
    # OPTIONAL RECORD LIMIT
    # --------------------------------------------------

    top_n = st.slider(
        "Number of categories to display",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
        key="adhoc_top_n"
    )

    # --------------------------------------------------
    # GENERATE ANALYSIS
    # --------------------------------------------------

    if st.button(
        "Generate Analysis",
        type="primary",
        use_container_width=True
    ):

        try:

            working_df = df.copy()

            if metric == "Shipment Count":

                result = (
                    working_df
                    .groupby(dimension, dropna=False)
                    .size()
                    .reset_index(name="Value")
                )

            else:

                working_df[numeric_column] = pd.to_numeric(
                    working_df[numeric_column],
                    errors="coerce"
                )

                grouped = working_df.groupby(
                    dimension,
                    dropna=False
                )[numeric_column]

                if metric == "Sum":
                    result = grouped.sum().reset_index(
                        name="Value"
                    )

                elif metric == "Average":
                    result = grouped.mean().reset_index(
                        name="Value"
                    )

                elif metric == "Maximum":
                    result = grouped.max().reset_index(
                        name="Value"
                    )

                else:
                    result = grouped.min().reset_index(
                        name="Value"
                    )

            result[dimension] = (
                result[dimension]
                .astype(str)
                .replace("nan", "Unknown")
            )

            result = result.dropna(
                subset=["Value"]
            )

            ascending = sort_order == "Ascending"

            result = result.sort_values(
                "Value",
                ascending=ascending
            )

            result = result.head(top_n)

            if result.empty:
                st.warning("No results found for this analysis.")
                return

            # Save result in session state
            st.session_state["adhoc_result"] = result
            st.session_state["adhoc_dimension"] = dimension
            st.session_state["adhoc_metric"] = metric
            st.session_state["adhoc_chart_type"] = chart_type

        except Exception as error:

            st.error(
                f"Unable to generate analysis: {error}"
            )

    # --------------------------------------------------
    # DISPLAY GENERATED ANALYSIS
    # --------------------------------------------------

    if "adhoc_result" in st.session_state:

        result = st.session_state["adhoc_result"]

        dimension = st.session_state["adhoc_dimension"]
        metric = st.session_state["adhoc_metric"]
        chart_type = st.session_state["adhoc_chart_type"]

        st.divider()

        st.markdown("### Generated Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Categories",
            len(result)
        )

        col2.metric(
            "Highest Value",
            f"{result['Value'].max():,.2f}"
        )

        col3.metric(
            "Lowest Value",
            f"{result['Value'].min():,.2f}"
        )

        # Chart creation
        if chart_type == "Bar Chart":

            fig = px.bar(
                result,
                x=dimension,
                y="Value",
                color="Value",
                color_continuous_scale="Greens",
                text="Value"
            )

            fig.update_traces(
                texttemplate="%{text:,.2f}",
                textposition="outside"
            )

        elif chart_type == "Line Chart":

            fig = px.line(
                result,
                x=dimension,
                y="Value",
                markers=True
            )

        elif chart_type == "Pie Chart":

            fig = px.pie(
                result,
                names=dimension,
                values="Value",
                hole=0.45
            )

        else:

            fig = px.scatter(
                result,
                x=dimension,
                y="Value",
                size="Value",
                color="Value"
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B1120",
            plot_bgcolor="#111827",
            font_color="#E5E7EB",
            height=450,
            title=f"{metric} by {dimension}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Results table
        st.markdown("### Analysis Data")

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        # CSV export
        csv_data = result.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Analysis CSV",
            data=csv_data,
            file_name="custom_supply_chain_analysis.csv",
            mime="text/csv",
            use_container_width=True
        )
