import os
import pandas as pd

def test_processed_file_exists():
    """Check if the cleaned CSV exists."""
    assert os.path.exists("data/processed/sroie_cleaned.csv"), "Processed file missing!"

def test_splits_exist():
    """Check if train/val/test splits exist."""
    for f in ["train.csv", "val.csv", "test.csv"]:
        assert os.path.exists(f"data/splits/{f}"), f"{f} not found!"

def test_data_not_empty():
    """Ensure processed dataset has data."""
    df = pd.read_csv("data/processed/sroie_cleaned.csv")
    assert len(df) > 0, "Processed CSV is empty!"
