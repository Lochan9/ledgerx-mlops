"""
Baseline Model Training
Simple document classifier as proof-of-concept
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import json
from pathlib import Path
from datetime import datetime
import mlflow
import mlflow.sklearn

class BaselineModelTrainer:
    """Train baseline ML model on document metadata"""
    
    def __init__(self, model_dir="models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        self.scaler = StandardScaler()
        self.model = None
        
    def load_data(self):
        """Load train/val/test data"""
        train_df = pd.read_csv('data/splits/train_metadata.csv')
        val_df = pd.read_csv('data/splits/val_metadata.csv')
        test_df = pd.read_csv('data/splits/test_metadata.csv')
        
        return train_df, val_df, test_df
    
    def prepare_features(self, df):
        """Extract features from metadata"""
        features = df[[
            'file_size_bytes',
            'image_width',
            'image_height',
            'quality_score',
            'has_blur'
        ]].copy()
        
        # Convert boolean to int
        features['has_blur'] = features['has_blur'].astype(int)
        
        # Create derived features
        features['aspect_ratio'] = features['image_width'] / features['image_height']
        features['pixel_count'] = features['image_width'] * features['image_height']
        features['size_per_pixel'] = features['file_size_bytes'] / features['pixel_count']
        
        return features
    
    def create_labels(self, df):
        """Create classification labels (high/medium/low quality)"""
        # Use quality_score to create 3 classes
        labels = pd.cut(df['quality_score'], 
                       bins=3, 
                       labels=['low', 'medium', 'high'])
        return labels
    
    def train(self):
        """Train baseline model"""
        print("Loading data...")
        train_df, val_df, test_df = self.load_data()
        
        # Prepare features
        print("Preparing features...")
        X_train = self.prepare_features(train_df)
        X_val = self.prepare_features(val_df)
        X_test = self.prepare_features(test_df)
        
        # Create labels
        y_train = self.create_labels(train_df)
        y_val = self.create_labels(val_df)
        y_test = self.create_labels(test_df)
        
        # Scale features
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        # MLflow tracking
        mlflow.set_experiment("ledgerx_baseline")
        
        with mlflow.start_run(run_name="baseline_rf"):
            # Train
            self.model.fit(X_train_scaled, y_train)
            
            # Predict
            train_pred = self.model.predict(X_train_scaled)
            val_pred = self.model.predict(X_val_scaled)
            test_pred = self.model.predict(X_test_scaled)
            
            # Metrics
            train_acc = accuracy_score(y_train, train_pred)
            val_acc = accuracy_score(y_val, val_pred)
            test_acc = accuracy_score(y_test, test_pred)
            
            train_f1 = f1_score(y_train, train_pred, average='weighted')
            val_f1 = f1_score(y_val, val_pred, average='weighted')
            test_f1 = f1_score(y_test, test_pred, average='weighted')
            
            # Log metrics
            mlflow.log_param("model_type", "RandomForest")
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 10)
            
            mlflow.log_metric("train_accuracy", train_acc)
            mlflow.log_metric("val_accuracy", val_acc)
            mlflow.log_metric("test_accuracy", test_acc)
            
            mlflow.log_metric("train_f1", train_f1)
            mlflow.log_metric("val_f1", val_f1)
            mlflow.log_metric("test_f1", test_f1)
            
            # Log model
            mlflow.sklearn.log_model(self.model, "model")
            
            print("\n" + "="*70)
            print("MODEL TRAINING RESULTS")
            print("="*70)
            print(f"Train Accuracy: {train_acc:.4f} | F1: {train_f1:.4f}")
            print(f"Val Accuracy:   {val_acc:.4f} | F1: {val_f1:.4f}")
            print(f"Test Accuracy:  {test_acc:.4f} | F1: {test_f1:.4f}")
            
            print("\nTest Set Classification Report:")
            print(classification_report(y_test, test_pred))
            
            # Save model
            model_path = self.model_dir / 'baseline_model.pkl'
            scaler_path = self.model_dir / 'scaler.pkl'
            
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            
            # Save metadata
            metadata = {
                "model_type": "RandomForestClassifier",
                "trained_date": datetime.now().isoformat(),
                "train_samples": len(train_df),
                "val_samples": len(val_df),
                "test_samples": len(test_df),
                "features": list(X_train.columns),
                "classes": ["low", "medium", "high"],
                "metrics": {
                    "train_accuracy": float(train_acc),
                    "val_accuracy": float(val_acc),
                    "test_accuracy": float(test_acc),
                    "train_f1": float(train_f1),
                    "val_f1": float(val_f1),
                    "test_f1": float(test_f1)
                }
            }
            
            with open(self.model_dir / 'model_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"\n✓ Model saved: {model_path}")
            print(f"✓ Scaler saved: {scaler_path}")
            print(f"✓ Metadata saved: {self.model_dir / 'model_metadata.json'}")
            print("="*70)
            
            return metadata

if __name__ == "__main__":
    trainer = BaselineModelTrainer()
    trainer.train()
