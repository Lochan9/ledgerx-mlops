import pandas as pd
import numpy as np
import json
from pathlib import Path

class BiasDetector:
    def __init__(self):
        self.report = {"biases": []}
    
    def check_size_bias(self, df):
        corr = df[['file_size_bytes', 'quality_score']].corr().iloc[0, 1]
        biased = abs(corr) > 0.7
        return {"type": "size_bias", "detected": bool(biased), "correlation": float(corr)}
    
    def check_format_bias(self, df):
        means = df.groupby('file_format')['quality_score'].mean()
        diff = means.max() - means.min()
        biased = diff > 0.3
        return {"type": "format_bias", "detected": bool(biased), "difference": float(diff)}
    
    def analyze(self, csv_path):
        df = pd.read_csv(csv_path)
        
        size_bias = self.check_size_bias(df)
        format_bias = self.check_format_bias(df)
        
        self.report["biases"] = [size_bias, format_bias]
        self.report["total_biases"] = sum(1 for b in self.report["biases"] if b["detected"])
        
        Path("reports").mkdir(exist_ok=True)
        with open('reports/bias_report.json', 'w') as f:
            json.dump(self.report, f, indent=2)
        
        print(f"Bias analysis complete: {self.report['total_biases']} biases detected")
        return self.report
