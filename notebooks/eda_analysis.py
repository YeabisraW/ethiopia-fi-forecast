import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")

# Load data
df = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')

# Filter for the two main indicators
indicators = ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']
plot_data = df[df['indicator_code'].isin(indicators)].copy()
plot_data['observation_date'] = pd.to_datetime(plot_data['observation_date'])

# Visualization
plt.figure(figsize=(10, 6))
sns.lineplot(data=plot_data, x='observation_date', y='value_numeric', hue='indicator', marker='o', linewidth=2.5)

plt.title('Ethiopia: Financial Access vs. Digital Payment Usage', fontsize=14)
plt.ylabel('Percentage of Adults (%)', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.ylim(0, 100)
plt.legend(title='Indicator', labels=['Account Ownership', 'Digital Payments'])

# Save figure
plt.savefig('reports/figures/access_vs_usage_trend.png')
plt.show()
# Get events from your enriched data
events = df[df['record_type'] == 'event']

# Add vertical lines for each event
for _, row in events.iterrows():
    plt.axvline(pd.to_datetime(row['observation_date']), color='red', linestyle='--', alpha=0.3)
    plt.text(pd.to_datetime(row['observation_date']), 5, row['indicator'], rotation=90, color='red', fontsize=8)