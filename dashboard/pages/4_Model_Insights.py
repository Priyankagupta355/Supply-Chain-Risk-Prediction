
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import joblib

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.title("Model Insights")
st.markdown(
    "Understand model performance, prediction quality, "
    "and the factors influencing delivery risk."
)

st.markdown("---")

# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


model = load_model()

if model is not None:
    st.success("Trained XGBoost model loaded successfully.")
else:
    st.warning(
        "Model file not found. Please check models/best_model.pkl."
    )

# --------------------------------------------------
# MODEL PERFORMANCE METRICS
# --------------------------------------------------

st.subheader("1. Model Performance")

st.caption("Evaluation on the grouped test dataset")

metrics = [
    ("Accuracy", "64.61%"),
    ("Precision", "66.82%"),
    ("Recall", "76.46%"),
    ("F1 Score", "71.32%"),
    ("ROC-AUC", "73.92%"),
]

cols = st.columns(5)

for col, (label, value) in zip(cols, metrics):
    with col:
        st.metric(label, value)

st.info(
    "The model identifies approximately 76.46% of actual late "
    "deliveries in the test dataset. However, false positives "
    "remain an important limitation."
)

st.markdown("---")

# --------------------------------------------------
# CONFUSION MATRIX
# --------------------------------------------------

st.subheader("2. Confusion Matrix")

confusion_matrix = [
    [7062, 7488],
    [4642, 15080]
]

fig_cm = go.Figure(
    data=go.Heatmap(
        z=confusion_matrix,
        x=["Predicted On-Time", "Predicted Late"],
        y=["Actual On-Time", "Actual Late"],
        text=confusion_matrix,
        texttemplate="%{text}",
        colorscale="Blues",
        showscale=True
    )
)

fig_cm.update_layout(
    title="Confusion Matrix - Test Dataset",
    xaxis_title="Predicted Class",
    yaxis_title="Actual Class",
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig_cm, use_container_width=True)

st.markdown("""
**Understanding the results:**

- True Negative (7,062): Correctly predicted on-time deliveries.
- False Positive (7,488): On-time deliveries predicted as late.
- False Negative (4,642): Late deliveries predicted as on-time.
- True Positive (15,080): Correctly predicted late deliveries.
""")

st.markdown("---")

# --------------------------------------------------
# FEATURE IMPORTANCE - SHAP
# --------------------------------------------------

st.subheader("3. SHAP Feature Importance")

st.write(
    "SHAP values help explain which features influence "
    "the model's predictions."
)

shap_data = pd.DataFrame({
    "Feature": [
        "Shipping Mode - First Class",
        "Scheduled Shipping Days",
        "Shipping Mode - Second Class",
        "Shipping Mode - Standard Class",
        "Order Item Discount",
        "Order Item Discount Rate",
        "Order Item Product Price"
    ],
    "Mean Absolute SHAP": [
        1.201627,
        0.806508,
        0.121909,
        0.046020,
        0.030616,
        0.017347,
        0.014632
    ]
})

shap_data = shap_data.sort_values(
    "Mean Absolute SHAP",
    ascending=True
)

fig_shap = px.bar(
    shap_data,
    x="Mean Absolute SHAP",
    y="Feature",
    orientation="h",
    title="Top Features Influencing Model Predictions",
    color="Mean Absolute SHAP",
    color_continuous_scale="Blues",
    template="plotly_dark"
)

fig_shap.update_layout(height=500)

st.plotly_chart(fig_shap, use_container_width=True)

st.caption(
    "SHAP importance was calculated using a sample of 1,000 records. "
    "Values represent average absolute SHAP contributions."
)

st.warning(
    "Feature importance indicates model associations, not proof "
    "that a feature directly causes delivery delays."
)

st.markdown("---")

# --------------------------------------------------
# MODEL THRESHOLD ANALYSIS
# --------------------------------------------------

st.subheader("4. Prediction Threshold Analysis")

threshold = 0.40

col1, col2 = st.columns(2)

with col1:
    st.metric("Selected Classification Threshold", "0.40")

with col2:
    st.metric("Test Recall", "76.46%")

st.write(
    "The model classifies a shipment as HIGH RISK when its "
    "predicted late-delivery probability is 40% or higher."
)

st.progress(threshold)

st.markdown("""
**Threshold interpretation:**

- Probability below 40%: Lower Risk
- Probability equal to or above 40%: High Risk

A lower threshold can help identify more potentially late
shipments, but may also increase false-positive predictions.
""")

st.markdown("---")

# --------------------------------------------------
# MODEL SUMMARY
# --------------------------------------------------

st.subheader("5. Overall Model Assessment")

summary = pd.DataFrame({
    "Evaluation Area": [
        "Algorithm",
        "Data Splitting",
        "Threshold",
        "Accuracy",
        "Recall",
        "ROC-AUC",
        "Main Influencing Features",
        "Model Status"
    ],
    "Result": [
        "XGBoost Classifier",
        "Group-based Train/Validation/Test Split",
        "0.40",
        "64.61%",
        "76.46%",
        "73.92%",
        "Shipping Mode and Scheduled Shipping Days",
        "Requires Further Improvement"
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.subheader("6. Key Findings")

st.markdown("""
1. The model achieved a test ROC-AUC of 73.92%.
2. Recall of 76.46% indicates that the model detects a majority
   of actual late deliveries.
3. Shipping Mode - First Class has the highest SHAP importance.
4. Scheduled shipping days are another major factor influencing
   model predictions.
5. False positives are still high, so the model needs further
   optimization before real-world deployment.
""")

st.success("Model Insights Dashboard Loaded!")
