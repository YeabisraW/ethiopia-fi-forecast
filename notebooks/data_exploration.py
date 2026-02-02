import pandas as pd
import os

# Define paths
raw_data_path = 'data/raw/ethiopia_fi_unified_data.csv'

def enrich_and_check(path):
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return
    
    # 1. Load Data
    df = pd.read_csv(path)
    
    # 2. Enrichment: Define new rows for 2024-2025 milestones
    # This addresses the project requirement to "Enrich the dataset"
    new_rows = [
        {'record_type': 'event', 'indicator': 'Fayda Digital ID Mandatory', 'observation_date': '2024-06-01', 'source_name': 'NBE', 'notes': 'Boosts Access by simplifying KYC'},
        {'record_type': 'event', 'indicator': 'EthSwitch P2P Interop', 'observation_date': '2025-10-01', 'source_name': 'EthSwitch', 'notes': 'Boosts Usage by allowing cross-app transfers'},
        {'record_type': 'observation', 'indicator': 'Safaricom 4G Population Coverage', 'value_numeric': 55.0, 'observation_date': '2025-01-01', 'source_name': 'Safaricom FY25', 'notes': 'Infrastructure enabler'}
    ]
    
    # 3. Append only if not already added (to avoid duplicates)
    if 'Fayda Digital ID Mandatory' not in df['indicator'].values:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        df.to_csv(path, index=False)
        print("--- Enrichment Complete: 3 new records added ---")
    else:
        print("--- Enrichment Skipped: Records already exist ---")

    # 4. Final Overview
    print("\n--- Updated Dataset Overview ---")
    print(f"Total Records: {len(df)}")
    print("\n--- Record Type Distribution ---")
    print(df['record_type'].value_counts())
    
    return df

if __name__ == "__main__":
    df = enrich_and_check(raw_data_path)