# Ethiopia Financial Inclusion Forecasting System
**Client:** Consortium of DFIs, NBE, and Mobile Money Operators  
**Consultancy:** Selam Analytics

## Project Overview
This system tracks and predicts Ethiopia's digital financial transformation (2011–2027). It utilizes a unified schema to model the relationship between market events (e.g., Telebirr launch, M-Pesa entry, Fayda ID) and World Bank Global Findex indicators.

## Core Metrics
* **Access:** Account Ownership Rate (% of adults 15+)
* **Usage:** Digital Payment Adoption Rate (% of adults 15+)

## Repository Structure
- `data/`: Unified schema datasets (Observations, Events, Impact Links).
- `src/`: Core logic for event-impact estimation and time-series modeling.
- `notebooks/`: Exploratory Data Analysis (EDA) and Model Validation.
- `dashboard/`: Streamlit interface for stakeholder visualization.

## Setup Instructions
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run dashboard/app.py`
## 🖥️ How to Run the Dashboard
1. Install dependencies: `pip install streamlit plotly`
2. Launch: `streamlit run dashboard/app.py`
