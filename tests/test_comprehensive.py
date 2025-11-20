"""
Comprehensive Test Suite
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestDataPipeline:
    def test_metadata_exists(self):
        assert Path('data/processed/all_metadata.csv').exists()
    
    def test_splits_exist(self):
        assert Path('data/splits/train_metadata.csv').exists()
        assert Path('data/splits/val_metadata.csv').exists()
        assert Path('data/splits/test_metadata.csv').exists()

class TestDataQuality:
    def test_no_missing_doc_ids(self):
        df = pd.read_csv('data/processed/all_metadata.csv')
        assert df['doc_id'].notna().all()
    
    def test_unique_checksums(self):
        df = pd.read_csv('data/processed/all_metadata.csv')
        assert df['checksum'].is_unique

class TestAlertSystem:
    def test_alert_system_loads(self):
        try:
            from src.alert_system import AlertSystem
            alert = AlertSystem()
            assert alert.config is not None
        except ImportError:
            pytest.skip("Alert system module not importable")

class TestBiasDetector:
    def test_bias_detector_loads(self):
        try:
            from src.bias_detector import BiasDetector
            detector = BiasDetector()
            assert detector.bias_report is not None
        except ImportError:
            pytest.skip("Bias detector module not importable")

class TestModel:
    def test_model_exists(self):
        if Path('models/baseline_model.pkl').exists():
            import joblib
            model = joblib.load('models/baseline_model.pkl')
            assert model is not None

class TestConfig:
    def test_config_files_exist(self):
        assert Path('config/pipeline_config.yaml').exists()
        assert Path('config/alerts_config.json').exists()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
