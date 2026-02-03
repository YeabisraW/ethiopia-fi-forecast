import matplotlib.pyplot as plt
import pandas as pd

# Data for the timeline
events = [
    {"year": 2011, "event": "National FI Strategy I"},
    {"year": 2017, "event": "NFI Strategy II Launched"},
    {"year": 2020, "event": "New Banking Proclamation"},
    {"year": 2021, "event": "Telebirr Launch (Digital Pivot)"},
    {"year": 2022, "event": "Safaricom Ethiopia Entry"},
    {"year": 2023, "event": "M-Pesa Ethiopia Launch"}
]

df_events = pd.DataFrame(events)

plt.figure(figsize=(10, 4))
plt.scatter(df_events['year'], [1]*len(df_events), color='darkgreen', s=100)
plt.axhline(y=1, color='gray', linestyle='--', zorder=0)

for i, row in df_events.iterrows():
    plt.annotate(row['event'], (row['year'], 1.02), rotation=45, ha='left', fontsize=9)

plt.title("Key Financial Inclusion Milestones in Ethiopia", pad=40)
plt.yticks([])
plt.xlabel("Year")
plt.xlim(2010, 2025)
plt.tight_layout()
plt.savefig('reports/figures/event_timeline.png')
plt.show()