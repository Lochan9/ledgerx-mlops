import pytest
from pathlib import Path

def test_config_exists():
    assert Path('config/pipeline_config.yaml').exists()

def test_metadata_exists():
    assert Path('data/processed/all_metadata.csv').exists()
    assert Path('data/splits/train_metadata.csv').exists()

def test_data_card_exists():
    assert Path('data/processed/DATA_CARD.json').exists()

if __name__ == "__main__":
    test_config_exists()
    test_metadata_exists()
    test_data_card_exists()
    print("All tests passed!")
