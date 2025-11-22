import json
import logging
from datetime import datetime
from typing import List, Dict
from pathlib import Path

class AlertSystem:
    def __init__(self):
        self.config = {
            "thresholds": {
                "quality_score_min": 0.5,
                "blur_rate_max": 0.1,
                "missing_values_max": 0.05
            }
        }
        self.alerts_log = []
    
    def check_thresholds(self, metrics: Dict) -> List[str]:
        violations = []
        if metrics.get("avg_quality_score", 1.0) < self.config["thresholds"]["quality_score_min"]:
            violations.append("Quality score below threshold")
        if metrics.get("blur_rate", 0) > self.config["thresholds"]["blur_rate_max"]:
            violations.append("Blur rate exceeds threshold")
        return violations
    
    def alert_failure(self, stage: str, error: str):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": "failure",
            "stage": stage,
            "error": error
        }
        self.alerts_log.append(alert)
        print(f"ALERT: {stage} failed - {error}")
    
    def save_log(self, path="logs/alerts.json"):
        Path(path).parent.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.alerts_log, f, indent=2)
