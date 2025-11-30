from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

# Load the trained model
try:
    model = joblib.load('housing_model.joblib')
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Warning: Model not found. Run training script first.")
    model = None

app = FastAPI(
    title="Housing Price Prediction API",
    description="ML-powered API for predicting housing prices",
    version="1.0.0"
)

# Pydantic models
class HouseFeatures(BaseModel):
    square_feet: int = Field(..., gt=0, description="Square footage")
    bedrooms: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=10, description="Number of bathrooms")
    age_years: int = Field(..., ge=0, le=100, description="Age of the house")
    distance_to_city: float = Field(..., gt=0, description="Distance to city center (km)")

class PredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: dict
    model_version: str
    predicted_at: str

class BatchPredictionRequest(BaseModel):
    houses: List[HouseFeatures]

@app.get("/")
def read_root():
    return {
        "message": "Housing Price Prediction API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Check if model is loaded and ready"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
def predict_price(house: HouseFeatures):
    """Predict price for a single house"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert to DataFrame
    input_df = pd.DataFrame([house.dict()])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    # Calculate confidence interval (simplified)
    std_error = prediction * 0.1  # Assume 10% error
    confidence_interval = {
        "lower": float(prediction - 1.96 * std_error),
        "upper": float(prediction + 1.96 * std_error)
    }
    
    return PredictionResponse(
        predicted_price=float(prediction),
        confidence_interval=confidence_interval,
        model_version="v1.0.0",
        predicted_at=datetime.now().isoformat()
    )

@app.post("/predict/batch")
def predict_batch(request: BatchPredictionRequest):
    """Predict prices for multiple houses"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert to DataFrame
    input_df = pd.DataFrame([h.dict() for h in request.houses])
    
    # Make predictions
    predictions = model.predict(input_df)
    
    return {
        "predictions": [float(p) for p in predictions],
        "count": len(predictions),
        "model_version": "v1.0.0"
    }

@app.get("/model/info")
def get_model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model.named_steps['regressor']).__name__,
        "features": list(model.feature_names_in_),
        "version": "v1.0.0",
        "training_date": "2024-01-01"  # Would come from metadata
    }
