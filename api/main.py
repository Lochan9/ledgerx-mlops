"""
FastAPI Inference Service
Serves trained model predictions
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Initialize FastAPI
app = FastAPI(
    title="LedgerX Document Quality Prediction API",
    description="Predicts document quality class (low/medium/high) from metadata",
    version="1.0.0"
)

# Load model and scaler
MODEL_DIR = Path("models")
model = joblib.load(MODEL_DIR / "baseline_model.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")

with open(MODEL_DIR / "model_metadata.json") as f:
    model_metadata = json.load(f)

# Request model
class DocumentMetadata(BaseModel):
    file_size_bytes: int
    image_width: int
    image_height: int
    quality_score: float
    has_blur: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_size_bytes": 45000,
                "image_width": 800,
                "image_height": 1000,
                "quality_score": 0.65,
                "has_blur": False
            }
        }

# Response model
class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: dict
    timestamp: str
    model_version: str

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LedgerX Inference API",
        "version": "1.0.0",
        "model_type": model_metadata["model_type"],
        "trained_date": model_metadata["trained_date"]
    }

@app.get("/health")
def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info")
def model_info():
    """Get model metadata"""
    return model_metadata

@app.post("/predict", response_model=PredictionResponse)
def predict(data: DocumentMetadata):
    """Predict document quality class"""
    try:
        # Prepare features
        features = np.array([[
            data.file_size_bytes,
            data.image_width,
            data.image_height,
            data.quality_score,
            int(data.has_blur),
            data.image_width / data.image_height,
            data.image_width * data.image_height,
            data.file_size_bytes / (data.image_width * data.image_height)
        ]])
        
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        classes = model.classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        confidence = float(max(probabilities))
        
        return PredictionResponse(
            predicted_class=str(prediction),
            confidence=confidence,
            probabilities=prob_dict,
            timestamp=datetime.now().isoformat(),
            model_version="1.0.0"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
