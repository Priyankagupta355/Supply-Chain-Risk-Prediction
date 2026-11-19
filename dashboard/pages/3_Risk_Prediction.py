
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from pathlib import Path


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.title("🤖 AI-Powered Delivery Risk Prediction")

st.caption(
    "Predict the probability of late delivery using "
    "the trained XGBoost machine learning pipeline."
)


# =====================================================
# 2. PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "best_model.pkl"

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)


# =====================================================
# 3. MODEL AND INPUT DATA LOADING
# =====================================================

@st.cache_resource
def load_model(path):
    return joblib.load(path)


@st.cache_data
def load_input_options(path):

    columns = [
        "Shipping Mode",
        "Customer Segment",
        "Market",
        "Order Region",
        "Department Name",
        "Category Name",
        "Days for shipment (scheduled)",
        "Order Item Quantity",
        "Order Item Discount",
        "Order Item Discount Rate",
        "Order Item Product Price"
    ]

    return pd.read_csv(
        path,
        encoding="latin1",
        usecols=columns
    )


try:

    model = load_model(str(MODEL_PATH))
    options_df = load_input_options(str(DATA_PATH))

    st.success("Trained ML model loaded successfully!")

except FileNotFoundError as e:

    st.error(f"Required file not found: {e}")
    st.stop()

except Exception as e:

    st.error(f"Model or dataset loading failed: {e}")
    st.stop()


# =====================================================
# 4. MODEL INFORMATION
# =====================================================

st.subheader("Model Information")

col1, col2, col3 = st.columns(3)

col1.metric("Algorithm", "XGBoost")
col2.metric("Risk Threshold", "0.40")
col3.metric("Prediction Type", "Binary Classification")

st.info(
    "Enter shipment details below. The model will estimate "
    "whether the shipment is likely to be delivered late."
)

st.divider()


# =====================================================
# 5. INPUT FORM
# =====================================================

st.subheader("Shipment Details")

with st.form("risk_prediction_form"):

    col1, col2 = st.columns(2)

    # ---------------- CATEGORICAL INPUTS ----------------

    with col1:

        shipping_mode = st.selectbox(
            "Shipping Mode",
            sorted(
                options_df["Shipping Mode"]
                .dropna()
                .unique()
            )
        )

        customer_segment = st.selectbox(
            "Customer Segment",
            sorted(
                options_df["Customer Segment"]
                .dropna()
                .unique()
            )
        )

        market = st.selectbox(
            "Market",
            sorted(
                options_df["Market"]
                .dropna()
                .unique()
            )
        )

        order_region = st.selectbox(
            "Order Region",
            sorted(
                options_df["Order Region"]
                .dropna()
                .unique()
            )
        )

        department = st.selectbox(
            "Department",
            sorted(
                options_df["Department Name"]
                .dropna()
                .unique()
            )
        )

    with col2:

        category = st.selectbox(
            "Product Category",
            sorted(
                options_df["Category Name"]
                .dropna()
                .unique()
            )
        )

        scheduled_days = st.selectbox(
            "Scheduled Shipping Days",
            sorted(
                options_df[
                    "Days for shipment (scheduled)"
                ]
                .dropna()
                .unique()
                .tolist()
            )
        )

        quantity = st.number_input(
            "Order Item Quantity",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        discount = st.number_input(
            "Order Item Discount",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

        discount_rate = st.number_input(
            "Order Item Discount Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            format="%.4f"
        )

        product_price = st.number_input(
            "Order Item Product Price",
            min_value=0.0,
            value=50.0,
            step=5.0
        )

    predict_button = st.form_submit_button(
        "Predict Delivery Risk",
        use_container_width=True
    )


# =====================================================
# 6. PREDICTION
# =====================================================

if predict_button:

    input_data = pd.DataFrame([{

        "Shipping Mode": shipping_mode,

        "Days for shipment (scheduled)": scheduled_days,

        "Customer Segment": customer_segment,

        "Market": market,

        "Order Region": order_region,

        "Department Name": department,

        "Category Name": category,

        "Order Item Quantity": quantity,

        "Order Item Discount": discount,

        "Order Item Discount Rate": discount_rate,

        "Order Item Product Price": product_price

    }])

    try:

        # Predict probability of late delivery
        probabilities = model.predict_proba(input_data)

        # Identify the probability column for class 1
        classes = list(model.classes_)

        late_class_index = classes.index(1)

        risk_probability = probabilities[
            0, late_class_index
        ]

        risk_percentage = risk_probability * 100

        # Project's selected validation threshold
        threshold = 0.40

        prediction = int(
            risk_probability >= threshold
        )

        st.divider()

        st.subheader("Prediction Results")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Late Delivery Risk",
                f"{risk_percentage:.2f}%"
            )

            st.progress(
                float(risk_probability)
            )

        with col2:

            if prediction == 1:

                st.error(
                    "⚠️ HIGH RISK: Late delivery predicted"
                )

                st.write(
                    "The model's estimated late-delivery "
                    "probability is at or above the "
                    "selected 40% threshold."
                )

            else:

                st.success(
                    "LOWER RISK: Late delivery not predicted"
                )

                st.write(
                    "The model's estimated late-delivery "
                    "probability is below the selected "
                    "40% threshold."
                )

        st.divider()

        # ---------------- RECOMMENDATIONS ----------------

        st.subheader("Operational Recommendations")

        if prediction == 1:

            st.warning(
                "Consider reviewing this shipment before dispatch."
            )

            st.write(
                "- Monitor shipment progress regularly."
            )

            st.write(
                "- Review the selected shipping mode."
            )

            st.write(
                "- Check regional logistics capacity."
            )

            st.write(
                "- Consider proactive customer communication."
            )

        else:

            st.info(
                "Continue standard shipment monitoring."
            )

            st.write(
                "- Maintain the planned dispatch schedule."
            )

            st.write(
                "- Track delivery progress."
            )

            st.write(
                "- Review any changes in logistics conditions."
            )

        # ---------------- INPUT SUMMARY ----------------

        with st.expander("View Submitted Shipment Details"):

            st.dataframe(
                input_data,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )


# =====================================================
# 7. MODEL LIMITATIONS
# =====================================================

st.divider()

with st.expander("About This Prediction Model"):

    st.write(
        "This application uses a trained XGBoost classification "
        "pipeline to estimate late-delivery risk."
    )

    st.write(
        "The selected classification threshold is 0.40, "
        "based on the project's validation analysis."
    )

    st.write(
        "The model was evaluated using grouped train, "
        "validation and test splits."
    )

    st.write(
        "Test ROC-AUC: 73.92%"
    )

    st.write(
        "Test Recall: 76.46%"
    )

    st.write(
        "These predictions are estimates based on historical "
        "data and should not be treated as guaranteed outcomes."
    )


st.caption(
    "Supply Chain Risk Prediction System | "
    "AI Risk Prediction Module"
)
