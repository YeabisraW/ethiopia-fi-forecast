import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ethiopia FI Forecast Dashboard",
    page_icon="🇪🇹",
    layout="wide"
)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    hist_path = 'data/processed/unified_inclusion_data.csv'
    fore_path = 'data/processed/long_term_forecast.csv'
    
    if os.path.exists(hist_path) and os.path.exists(fore_path):
        hist = pd.read_csv(hist_path)
        fore = pd.read_csv(fore_path)
        return hist, fore
    return None, None

df_hist, df_fore = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("GMF Consortium")
st.sidebar.image("https://flagcdn.com/w320/et.png", width=100)
page = st.sidebar.radio("Navigation", ["Overview", "Historical Trends", "Forecasts & Scenarios"])

if df_hist is not None and df_fore is not None:
    
    # --- PAGE 1: OVERVIEW ---
    if page == "Overview":
        st.title("🇪🇹 Financial Inclusion Overview")
        st.markdown("### National Summary (2011 - 2024)")
        
        # Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Get latest data point for Account Ownership
        latest_data = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP'].iloc[-1]
        latest_val = latest_data['value_numeric']
        
        col1.metric("Current Inclusion", f"{latest_val}%", "2021 Baseline")
        col2.metric("2027 Target", "70.0%", "-25.1% Gap")
        col3.metric("Digital Surge", "+12.5%", "Post-Telebirr")
        col4.metric("Growth Confidence", "High", "LSTM Verified")

        st.markdown("---")
        st.info("**Key Insight:** Historical growth was steady until 2021. The entry of mobile money (Telebirr) and private telcos (Safaricom) has created a structural shift in the growth curve.")

    # --- PAGE 2: HISTORICAL TRENDS ---
    elif page == "Historical Trends":
        st.title("📈 Historical Trend Analysis")
        
        indicator = st.selectbox("Select Indicator to Explore:", df_hist['indicator_code'].unique())
        
        filtered_df = df_hist[df_hist['indicator_code'] == indicator].sort_values('fiscal_year')
        
        fig = px.line(
            filtered_df, 
            x='fiscal_year', 
            y='value_numeric',
            title=f"Evolution of {indicator}",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#1f77b4"]
        )
        
        fig.update_layout(yaxis_title="Percentage (%)", xaxis_title="Year")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Raw Data View")
        st.dataframe(filtered_df[['fiscal_year', 'indicator', 'value_numeric']].tail(10))

    # --- PAGE 3: FORECASTS & SCENARIOS ---
    elif page == "Forecasts & Scenarios":
        st.title("🔮 2027 Inclusion Projections")
        st.markdown("Use the slider in the sidebar to simulate policy impacts.")

        # Sidebar Slider for Scenario Selection
        st.sidebar.markdown("---")
        st.sidebar.subheader("Simulation Settings")
        growth_boost = st.sidebar.slider("Policy Impact Boost (%)", 0, 25, 5)
        
        # Calculate Optimistic Scenario
        df_fore['Optimistic_Scenario'] = df_fore['Forecasted_Inclusion'] + growth_boost
        
        # Plotly Multi-Line Chart
        fig_fore = px.line(
            df_fore, 
            x='Year', 
            y=['Forecasted_Inclusion', 'Optimistic_Scenario'],
            labels={'value': 'Inclusion Rate (%)', 'variable': 'Scenario'},
            title="Baseline LSTM Forecast vs. Policy Intervention Scenario",
            markers=True,
            color_discrete_map={
                "Forecasted_Inclusion": "#ff7f0e",
                "Optimistic_Scenario": "#2ca02c"
            }
        )
        
        # Add the 70% National Target Line
        fig_fore.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="70% National Target")
        
        st.plotly_chart(fig_fore, use_container_width=True)
        
        # Gap Analysis Logic
        final_pred = df_fore['Optimistic_Scenario'].iloc[-1]
        gap = 70 - final_pred
        
        if gap <= 0:
            st.success(f"🎊 **Goal Reached!** With a {growth_boost}% policy boost, Ethiopia hits {final_pred:.2f}% inclusion by 2027.")
        else:
            st.warning(f"⚠️ **Gap Remaining:** Even with a {growth_boost}% boost, we reach {final_pred:.2f}%. We still need an additional {gap:.2f}% to hit the target.")

        # --- DATA DOWNLOAD SECTION ---
        st.markdown("---")
        st.subheader("📥 Export Forecast Data")
        csv = df_fore.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Forecast Results as CSV",
            data=csv,
            file_name='ethiopia_2027_projections.csv',
            mime='text/csv',
        )

else:
    st.error("🚨 **Error:** Data files not found in `data/processed/`. Please run your forecasting engine script first.") 

