
import streamlit as st
from pathlib import Path

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Supply Chain BI Platform",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ==========================================================
# CUSTOM CSS
# ==========================================================

CUSTOM_CSS = """
<style>

/* Main application */

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

.block-container {
    max-width: 1600px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide automatic Streamlit page navigation */

[data-testid="stSidebarNav"] {
    display: none;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263449;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Typography */

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

/* KPI cards */

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #172338,
        #1E293B
    );
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

/* Select boxes */

div[data-baseweb="select"] > div {
    background-color: #1E293B;
    border-color: #334155;
}

/* Input fields */

input, textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

/* Buttons */

.stButton > button {
    background-color: #16A34A;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}

.stButton > button:hover {
    background-color: #15803D;
    color: white;
    border: none;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

/* Dividers */

hr {
    border-color: #334155;
}

/* Sidebar branding */

.brand-title {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 800;
    margin-top: 8px;
}

.brand-subtitle {
    color: #94A3B8;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 5px;
}

.section-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Dashboard header */

.dashboard-header {
    background: linear-gradient(
        110deg,
        #172338,
        #1E293B
    );
    padding: 28px;
    border: 1px solid #334155;
    border-radius: 14px;
    margin-bottom: 25px;
}

.header-tag {
    color: #22C55E;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.header-title {
    color: #F8FAFC;
    font-size: 32px;
    font-weight: 800;
    margin-top: 12px;
    margin-bottom: 8px;
}

.header-description {
    color: #94A3B8;
    font-size: 15px;
    margin: 0;
}

/* Footer */

.dashboard-footer {
    color: #64748B;
    font-size: 11px;
    text-align: center;
    padding: 20px;
}

/* ======================================================
   RESPONSIVE DASHBOARD DESIGN
   ====================================================== */

@media screen and (max-width: 768px) {

    .block-container {
        padding: 1rem 0.8rem 2rem 0.8rem;
    }

    .dashboard-header {
        padding: 18px;
        margin-bottom: 20px;
    }

    .header-title {
        font-size: 26px !important;
        line-height: 1.3;
    }

    .header-description {
        font-size: 13px;
        line-height: 1.6;
    }

    h1 {
        font-size: 25px !important;
    }

    h2 {
        font-size: 21px !important;
    }

    h3 {
        font-size: 18px !important;
    }

    [data-testid="stMetric"] {
        padding: 12px;
    }
}

</style>
"""


# ==========================================================
# HTML RENDERING FUNCTION
# ==========================================================

def render_html(html_content):

    if hasattr(st, "html"):
        st.html(html_content)

    else:
        st.markdown(
            html_content,
            unsafe_allow_html=True
        )


st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

PAGES = [
    "Executive Overview",
    "Delivery Analytics",
    "Regional Analysis",
    "Shipping Analysis",
    "Risk Intelligence",
    "Ad-hoc Analysis",
    "Data Explorer"
]

PAGE_ICONS = {
    "Executive Overview": "📊",
    "Delivery Analytics": "🚚",
    "Regional Analysis": "🌍",
    "Shipping Analysis": "📦",
    "Risk Intelligence": "🧠",
    "Ad-hoc Analysis": "⚙️",
    "Data Explorer": "🔎"
}


with st.sidebar:

    # Branding

    render_html("""
    <div style="padding: 10px 0 20px 0;">

        <div style="font-size: 38px;">📦</div>

        <div class="brand-title">
            SUPPLY CHAIN
        </div>

        <div class="brand-subtitle">
            BUSINESS INTELLIGENCE
        </div>

    </div>
    """)

    st.divider()

    render_html("""
    <div class="section-label">
        MAIN MENU
    </div>
    """)

    selected_page = st.radio(
        "Navigation",
        options=PAGES,
        format_func=lambda page: (
            PAGE_ICONS[page] + "   " + page
        ),
        label_visibility="collapsed",
        key="main_navigation"
    )

    st.divider()

    render_html("""
    <div class="section-label">
        PROJECT INFORMATION
    </div>
    """)

    st.caption("Supply Chain Risk Prediction")
    st.caption("Machine Learning + Business Analytics")

    st.divider()

    render_html("""
    <div style="
        font-size:11px;
        color:#64748B;
        line-height:1.8;
    ">
        VERSION 2.0<br>
        POWER BI STYLE ANALYTICS<br>
        DARK PROFESSIONAL THEME
    </div>
    """)


# ==========================================================
# MAIN DASHBOARD HEADER
# ==========================================================

render_html("""
<div class="dashboard-header">

    <div class="header-tag">
        BUSINESS INTELLIGENCE PLATFORM
    </div>

    <div class="header-title">
        Supply Chain Analytics
    </div>

    <p class="header-description">
        Monitor delivery performance, analyze operations
        and identify shipment risks.
    </p>

</div>
""")


# ==========================================================
# PAGE ROUTING
# ==========================================================

st.session_state["selected_page"] = selected_page


if selected_page == "Executive Overview":

    st.title("📊 Executive Overview")

    st.info(
        "Executive overview analytics will be implemented next."
    )


elif selected_page == "Delivery Analytics":

    st.title("🚚 Delivery Analytics")

    st.info(
        "Delivery performance analysis will be implemented next."
    )


elif selected_page == "Regional Analysis":

    st.title("🌍 Regional Analysis")

    st.info(
        "Regional performance analysis will be implemented next."
    )


elif selected_page == "Shipping Analysis":

    st.title("📦 Shipping Analysis")

    st.info(
        "Shipping analytics will be implemented next."
    )


elif selected_page == "Risk Intelligence":

    st.title("🧠 Risk Intelligence")

    st.info(
        "Machine learning risk analytics will be implemented next."
    )


elif selected_page == "Ad-hoc Analysis":

    st.title("⚙️ Ad-hoc Analysis")

    st.info(
        "Dynamic chart builder will be implemented next."
    )


elif selected_page == "Data Explorer":

    st.title("🔎 Data Explorer")

    st.info(
        "Interactive data exploration will be implemented next."
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

render_html("""
<div class="dashboard-footer">

    SUPPLY CHAIN BI PLATFORM
    <br>
    HISTORICAL DATA ANALYTICS
    <br><br>
    Powered by Python, Streamlit, Plotly and XGBoost

</div>
""")
