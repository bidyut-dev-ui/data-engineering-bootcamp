# Week 20: Mini-Project 5 - Predictive Service

**Goal**: Build an end-to-end ML service that trains a model, serves predictions via FastAPI, and runs in Docker.

## Scenario
You've built a great ML model. Now you need to deploy it so others can use it. This project combines everything: training, serialization, API development, and containerization.

## Concepts Covered
1. **End-to-End ML Pipeline**: From data to deployment
2. **Model Serving**: Exposing ML models via REST API
3. **Input Validation**: Using Pydantic for type safety
4. **Batch Predictions**: Handling multiple requests efficiently
5. **Model Versioning**: Tracking model versions in production
6. **Containerization**: Packaging ML services with Docker
7. **API Design**: RESTful patterns for ML services

## Structure
- `train_model.py`: Train and save the model
- `app/main.py`: FastAPI application serving predictions
- `housing_model.joblib`: Trained model file
- `Dockerfile`: Container image definition
- `docker-compose.yml`: Service orchestration
- `requirements.txt`: Python dependencies

## Instructions

### 1. Setup
```bash
cd projects/16_predictive_service
source ../00_setup_and_refresher/venv/bin/activate
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python train_model.py
```

**Expected Output**:
- Training progress
- Train/Test R² scores
- Saved model: `housing_model.joblib`

### 3. Run the API Locally
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs`

### 4. Test the Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "square_feet": 2000,
    "bedrooms": 3,
    "bathrooms": 2,
    "age_years": 10,
    "distance_to_city": 5
  }'
```

**Expected Output**:
```json
{
  "predicted_price": 425000.50,
  "confidence_interval": {
    "lower": 382500.45,
    "upper": 467500.55
  },
  "model_version": "v1.0.0",
  "predicted_at": "2024-01-01T12:00:00"
}
```

#### Batch Prediction
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "houses": [
      {"square_feet": 1500, "bedrooms": 2, "bathrooms": 1, "age_years": 20, "distance_to_city": 10},
      {"square_feet": 2500, "bedrooms": 4, "bathrooms": 3, "age_years": 5, "distance_to_city": 3}
    ]
  }'
```

#### Model Info
```bash
curl http://localhost:8000/model/info
```

### 5. Run with Docker
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`

### 6. Cleanup
```bash
docker compose down
```

## Homework / Challenge

### Challenge 1: Add Model Monitoring
Create `app/monitoring.py`:
1. Track prediction requests (count, latency)
2. Log predictions to a file
3. Add `/metrics` endpoint showing statistics

### Challenge 2: A/B Testing
Modify the service:
1. Train two different models (RandomForest vs GradientBoosting)
2. Save both models
3. Add `model_version` parameter to `/predict`
4. Route requests to different models

### Challenge 3: Model Retraining
Create `retrain.py`:
1. Load new data
2. Retrain the model
3. Compare with current model
4. Auto-deploy if better (update joblib file)
5. Add versioning (v1.0.0 → v1.1.0)

### Challenge 4: Integration Test
Create `tests/test_api.py`:
1. Use `pytest` and `httpx`
2. Test all endpoints
3. Test input validation (invalid data should return 422)
4. Test edge cases (very large/small values)

## Expected Learning Outcomes
- ✅ Build complete ML service from scratch
- ✅ Serve ML models via REST API
- ✅ Handle input validation and errors
- ✅ Containerize ML applications
- ✅ Understand production ML considerations
- ✅ Integrate ML with previous projects (data warehouse, ETL)

## Production Considerations
1. **Model Versioning**: Use semantic versioning (v1.0.0)
2. **Monitoring**: Track predictions, errors, latency
3. **Scaling**: Use multiple workers (gunicorn)
4. **Caching**: Cache predictions for identical inputs
5. **Security**: Add API key authentication
6. **Logging**: Structured logging for debugging
7. **Testing**: Unit tests, integration tests, load tests
