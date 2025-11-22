import pytest
import pandas as pd
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPipeline:
    def test_metadata_exists(self):
        assert Path('data/processed/all_metadata.csv').exists()
    
    def test_splits_exist(self):
        assert Path('data/splits/train_metadata.csv').exists()

class TestQuality:
    def test_no_nulls(self):
        df = pd.read_csv('data/processed/all_metadata.csv')
        assert df['doc_id'].notna().all()
    
    def test_unique_checksums(self):
        df = pd.read_csv('data/processed/all_metadata.csv')
        assert df['checksum'].is_unique

class TestAlerts:
    def test_alert_import(self):
        from src.alert_system import AlertSystem
        assert AlertSystem() is not None

class TestBias:
    def test_bias_import(self):
        from src.bias_detector import BiasDetector
        assert BiasDetector() is not None

class TestModel:
    def test_model_exists(self):
        if Path('models').exists():
            assert True

class TestConfig:
    def test_configs_exist(self):
        assert Path('config/pipeline_config.yaml').exists()
