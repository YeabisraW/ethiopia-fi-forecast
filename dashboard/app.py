import streamlit as st
import pandas as pd
import plotly.express as px
import os
import logging
from typing import Tuple, Optional

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Ethiopia FI Forecast Dashboard",
    page_icon="🇪🇹",
    layout="wide"
)

# --- DATA LOGIC (Separated from UI) ---
@st.cache_data
def load_and_validate_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Loads and validates the historical and forecast datasets.
    Provides basic error handling for missing files and schema mismatches.
    """
    hist_path = 'data/processed/unified_inclusion_data.csv'
    fore_path = 'data/processed/long_term_forecast.csv'
    
    try:
        # Check existence
        if not os.path.exists(hist_path) or not os.path.exists(fore_path):
            logger.error("Data files missing at designated paths.")
            return None, None
        
        hist = pd.read_csv(hist_path)
        fore = pd.read_csv(fore_path)
        
        # Schema validation (Reviewer Comment 3)
        required_hist = {'indicator_code', 'value_numeric', 'fiscal_year'}
        if not required_hist.issubset(hist.columns):
            st.error("Historical data schema mismatch. Please check unified_inclusion_data.csv")
            return None, None
            
        return hist, fore
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.exception("Data loading failed.")
        return None, None

df_hist, df_fore = load_and_validate_data()

# --- SIDEBAR ---
st.sidebar.title("GMF Consortium")
st.sidebar.image("https://flagcdn.com/w320/et.png", width=100)
page = st.sidebar.radio("Navigation", ["Overview", "Historical Trends", "Forecasts & Scenarios", "Analytical Deep Dive"])

# --- SHARED UI LOGIC ---
if df_hist is None or df_fore is None:
    st.error("🚨 **System Error:** Could not initialize data. Ensure the preprocessing scripts have been run.")
    st.stop()

# --- PAGE 1: OVERVIEW ---
if page == "Overview":
    st.title("🇪🇹 Financial Inclusion Overview")
    st.markdown("### National Summary (2011 - 2024)")
    
    col1, col2, col3, col4 = st.columns(4)
    latest_data = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP'].iloc[-1]
    latest_val = latest_data['value_numeric']
    
    col1.metric("Current Inclusion", f"{latest_val}%", "2021 Baseline")
    col2.metric("2027 Target", "70.0%", "-25.1% Gap")
    col3.metric("Usage Shift", "Structural", "Post-2021")
    col4.metric("Model Confidence", "LSTM-High")

    st.markdown("---")
    st.image("reports/figures/event_timeline.png", caption="Historical Milestone Timeline")

# --- PAGE 2: HISTORICAL TRENDS ---
elif page == "Historical Trends":
    st.title("📈 Historical Trend Analysis")
    indicator = st.selectbox("Select Indicator:", df_hist['indicator_code'].unique())
    filtered_df = df_hist[df_hist['indicator_code'] == indicator].sort_values('fiscal_year')
    
    fig = px.line(filtered_df, x='fiscal_year', y='value_numeric', markers=True, title=f"Evolution of {indicator}")
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 4: ANALYTICAL DEEP DIVE (NEW - Comment 2) ---
elif page == "Analytical Deep Dive":
    st.title("🧠 Research Insights & Data Limitations")
    
    st.subheader("1. The 2021-2024 'Digital Slowdown'")
    st.write("""
    While account registration surged with Telebirr, our analysis shows a **slowdown in banking penetration growth rates** from 2022 onwards. 
    This suggests that the 'Access' pillar is hitting a saturation point in urban areas, shifting the national priority to the 'Usage' pillar.
    """)
    
    st.subheader("2. Usage vs. Access Gap")
    st.info("**Key Finding:** There is a estimated 15-20% gap between 'Registered' mobile money accounts and 'Active' (90-day) users.")
    
    st.subheader("3. Data Limitations")
    st.warning("""
    - **Temporal Coverage:** Indicators like 'Account Ownership' rely on Findex surveys which occur every 3 years, leading to interpolation requirements.
    - **Source Variability:** Merging NBE and World Bank data requires careful handling of fiscal vs. calendar years.
    """)

# --- PAGE 3: FORECASTS ---
elif page == "Forecasts & Scenarios":
    st.title("🔮 2027 Projections")
    st.sidebar.markdown("---")
    growth_boost = st.sidebar.slider("Policy Impact Boost (%)", 0, 25, 5)
    
    df_fore['Optimistic_Scenario'] = df_fore['Forecasted_Inclusion'] + growth_boost
    fig_fore = px.line(df_fore, x='Year', y=['Forecasted_Inclusion', 'Optimistic_Scenario'], 
                       title="Baseline vs. Policy Intervention Scenario")
    fig_fore.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="70% Target")
    st.plotly_chart(fig_fore, use_container_width=True)
    
    # Download Button
    st.download_button("📥 Download Results", df_fore.to_csv(index=False), "forecast.csv", "text/csv")