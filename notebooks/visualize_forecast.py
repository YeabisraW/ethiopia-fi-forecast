import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
historical = pd.read_csv('data/processed/unified_inclusion_data.csv')
historical = historical[historical['indicator_code'] == 'ACC_OWNERSHIP']
forecast = pd.read_csv('data/processed/long_term_forecast.csv')

# 2. Plotting
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Plot Historical
sns.lineplot(data=historical, x='fiscal_year', y='value_numeric', 
             label='Historical (Actual)', marker='o', color='#1f77b4', linewidth=2.5)

# Plot Forecast
sns.lineplot(data=forecast, x='Year', y='Forecasted_Inclusion', 
             label='LSTM Baseline Forecast', linestyle='--', marker='s', color='#ff7f0e', linewidth=2.5)

# Add Target Line
plt.axhline(y=70, color='r', linestyle=':', label='2027 National Target (70%)')

plt.title('Ethiopia Financial Inclusion: Historical Trend vs. 2027 Projection', fontsize=15)
plt.ylabel('Inclusion Rate (%)')
plt.xlabel('Year')
plt.legend()
plt.ylim(0, 80)

# Save
plt.savefig('reports/figures/long_term_forecast_plot.png')
print("✅ Forecast visualization saved to reports/figures/long_term_forecast_plot.png")
plt.show()