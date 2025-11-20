"""
Bias Detection and Mitigation
"""
import pandas as pd
import numpy as np
from scipy import stats
import json

class BiasDetector:
    def __init__(self):
        self.bias_report = {"biases_detected": [], "mitigation_applied": []}
    
    def check_size_bias(self, df):
        """Check file size bias"""
        corr = df[['file_size_bytes', 'quality_score']].corr().iloc[0, 1]
        bias_detected = bool(abs(corr) > 0.7)  # Convert to Python bool
        return {"bias_detected": bias_detected, "correlation": float(corr)}
    
    def check_format_bias(self, df):
        """Check format bias"""
        format_quality = df.groupby('file_format')['quality_score'].mean()
        mean_diff = format_quality.max() - format_quality.min()
        bias_detected = bool(mean_diff > 0.3)  # Convert to Python bool
        return {"bias_detected": bias_detected, "mean_difference": float(mean_diff)}
    
    def run_full_bias_analysis(self, metadata_path):
        print("Running bias analysis...")
        df = pd.read_csv(metadata_path)
        
        size_bias = self.check_size_bias(df)
        format_bias = self.check_format_bias(df)
        
        print(f"Size bias detected: {size_bias['bias_detected']}")
        print(f"Format bias detected: {format_bias['bias_detected']}")
        
        self.bias_report["summary"] = {
            "size_bias": size_bias,
            "format_bias": format_bias
        }
        
        with open('reports/bias_analysis_report.json', 'w') as f:
            json.dump(self.bias_report, f, indent=2)
        
        print("✓ Bias analysis complete")
        return self.bias_report

if __name__ == "__main__":
    detector = BiasDetector()
    detector.run_full_bias_analysis('data/processed/all_metadata.csv')
