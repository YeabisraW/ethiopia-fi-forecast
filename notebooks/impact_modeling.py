import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_impact_matrix():
    # 1. Define the Data
    impact_data = {
        'Event': ['Telebirr Launch', 'Safaricom M-Pesa', 'Fayda ID Rollout', 'EthSwitch P2P'],
        'Target_Indicator': ['USG_DIGITAL_PAYMENT', 'ACC_MM_ACCOUNT', 'ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT'],
        'Impact_Magnitude_PP': [12.5, 5.2, 4.8, 7.5], 
        'Confidence_Score': [0.95, 0.88, 0.75, 0.82]
    }
    
    df_matrix = pd.DataFrame(impact_data)
    
    # Use paths relative to project root (no '..' if running from root)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('reports/figures', exist_ok=True)
    
    # 2. Save CSV
    csv_path = 'data/processed/impact_matrix.csv'
    df_matrix.to_csv(csv_path, index=False)
    print(f"✅ CSV saved to: {os.path.abspath(csv_path)}")
    return df_matrix

def visualize_impact(df_matrix):
    # 3. Pivot for heatmap
    pivot_matrix = df_matrix.pivot(index='Event', columns='Target_Indicator', values='Impact_Magnitude_PP')

    plt.figure(figsize=(10, 6))
    sns.set_theme(style="white")
    
    # Create Heatmap
    sns.heatmap(pivot_matrix, annot=True, cmap='YlGnBu', fmt='.1f', 
                linewidths=.5, cbar_kws={'label': 'Impact (Percentage Points)'})
    
    plt.title('Task 3: Event-Indicator Impact Association Matrix', fontsize=14, pad=20)
    plt.tight_layout()

    # 4. Save the figure
    img_path = 'reports/figures/impact_association_heatmap.png'
    plt.savefig(img_path)
    print(f"✅ Image saved to: {os.path.abspath(img_path)}")
    plt.show()

if __name__ == "__main__":
    matrix = generate_impact_matrix()
    visualize_impact(matrix)