import os
import pandas as pd

def test_data_files_exist():
    """Ensure essential data files are present in the repo."""
    assert os.path.exists('data/processed/unified_inclusion_data.csv')
    assert os.path.exists('data/processed/long_term_forecast.csv')

def test_indicator_logic():
    """Check if the unified data contains the primary target indicator."""
    df = pd.read_csv('data/processed/unified_inclusion_data.csv')
    assert 'ACC_OWNERSHIP' in df['indicator_code'].values