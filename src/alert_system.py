"""
Alert Generation System
Sends notifications for pipeline failures and anomalies
"""
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import requests
import logging

logger = logging.getLogger(__name__)

class AlertSystem:
    """Generate and send alerts for pipeline issues"""
    
    def __init__(self, config_path="config/alerts_config.json"):
        self.config = self._load_config(config_path)
        self.alerts_log = []
    
    def _load_config(self, config_path):
        """Load alert configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "email": {"enabled": False},
                "slack": {"enabled": False},
                "thresholds": {
                    "quality_score_min": 0.5,
                    "blur_rate_max": 0.1,
                    "missing_values_max": 0.05,
                    "duplicate_rate_max": 0.02
                }
            }
    
    def check_data_quality_thresholds(self, metrics: Dict) -> List[str]:
        """Check if metrics violate thresholds"""
        violations = []
        thresholds = self.config["thresholds"]
        
        if metrics.get("avg_quality_score", 1.0) < thresholds["quality_score_min"]:
            violations.append(f"Quality score {metrics['avg_quality_score']:.3f} below threshold")
        
        if metrics.get("blur_rate", 0) > thresholds["blur_rate_max"]:
            violations.append(f"Blur rate {metrics['blur_rate']:.3f} exceeds threshold")
        
        return violations
    
    def alert_pipeline_failure(self, stage: str, error: str):
        """Alert on pipeline failure"""
        self.alerts_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "pipeline_failure",
            "stage": stage,
            "error": error
        })
        print(f"ALERT: Pipeline failure in {stage}: {error}")
    
    def alert_data_quality_issues(self, violations: List[str]):
        """Alert on data quality issues"""
        self.alerts_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "data_quality",
            "violations": violations
        })
        print(f"ALERT: {len(violations)} data quality violations detected")

if __name__ == "__main__":
    alert_system = AlertSystem()
    metrics = {"avg_quality_score": 0.45, "blur_rate": 0.15}
    violations = alert_system.check_data_quality_thresholds(metrics)
    if violations:
        alert_system.alert_data_quality_issues(violations)
    print("✓ Alert system operational")
