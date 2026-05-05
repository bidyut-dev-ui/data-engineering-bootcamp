# GOTCHAS & BEST PRACTICES: Predictive Service (Week 20)

This document outlines common pitfalls, best practices, and implementation tips for building production-ready ML prediction services.

## 🚨 Critical Gotchas (Common Mistakes)

### 1. **Model Serialization Incompatibility**
**Problem**: Models trained with one version of scikit-learn may fail to load with another version.
```python
# ❌ DON'T: Assume model compatibility across versions
joblib.dump(model, 'model.joblib')
# Later, with updated sklearn: joblib.load('model.joblib') may fail

# ✅ DO: Pin dependencies and include version metadata
import sklearn
metadata = {
    'sklearn_version': sklearn.__version__,
    'python_version': sys.version,
    'training_date': datetime.now().isoformat()
}
joblib.dump({'model': model, 'metadata': metadata}, 'model.joblib')
```

### 2. **Input Data Drift**
**Problem**: Production data distribution differs from training data, causing poor predictions.
```python
# ❌ DON'T: Blindly trust model with unseen data distributions
prediction = model.predict(features)  # May produce nonsense

# ✅ DO: Monitor input distributions and detect drift
from scipy import stats
# Calculate KL divergence between training and production distributions
drift_score = stats.entropy(train_dist, prod_dist)
if drift_score > threshold:
    trigger_retraining_alert()
```

### 3. **Memory Leaks in Long-Running Services**
**Problem**: ML models and data processing can accumulate memory over time.
```python
# ❌ DON'T: Keep large objects in global scope indefinitely
global_model = joblib.load('large_model.joblib')  # 2GB in memory forever

# ✅ DO: Use lazy loading and cleanup
class ModelManager:
    def __init__(self):
        self._model = None
    
    @property
    def model(self):
        if self._model is None:
            self._model = joblib.load('large_model.joblib')
        return self._model
    
    def cleanup(self):
        del self._model
        self._model = None
        gc.collect()
```

### 4. **Missing Input Validation**
**Problem**: API accepts invalid values causing model errors or incorrect predictions.
```python
# ❌ DON'T: Trust client input
@app.post("/predict")
def predict(features: dict):
    # features could be {"square_feet": -1000, "bedrooms": 999}
    return model.predict([features])

# ✅ DO: Use Pydantic with strict validation
from pydantic import BaseModel, Field, validator

class HouseFeatures(BaseModel):
    square_feet: int = Field(..., gt=0, le=10000)
    bedrooms: int = Field(..., ge=1, le=10)
    
    @validator('square_feet')
    def validate_square_feet_per_bedroom(cls, v, values):
        if 'bedrooms' in values and v / values['bedrooms'] < 200:
            raise ValueError('Minimum 200 sqft per bedroom')
        return v
```

### 5. **Ignoring Prediction Confidence**
**Problem**: Returning point estimates without uncertainty measures.
```python
# ❌ DON'T: Return only point estimates
prediction = model.predict([features])[0]
return {"price": prediction}

# ✅ DO: Include confidence intervals or uncertainty
from sklearn.ensemble import RandomForestRegressor

class UncertaintyAwareModel:
    def predict_with_uncertainty(self, X):
        # Use tree variance for uncertainty estimation
        predictions = []
        for tree in model.estimators_:
            predictions.append(tree.predict(X))
        
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return {
            'prediction': mean_pred[0],
            'std_dev': std_pred[0],
            'confidence_interval': (
                mean_pred[0] - 1.96 * std_pred[0],
                mean_pred[0] + 1.96 * std_pred[0]
            )
        }
```

## 🏆 Best Practices

### 1. **Model Versioning Strategy**
```python
# Semantic versioning for models
MODEL_REGISTRY = {
    'v1.0.0': {
        'path': 'models/v1.0.0/housing_model.joblib',
        'trained_date': '2024-01-01',
        'performance': {'r2': 0.85, 'mae': 25000},
        'features': ['square_feet', 'bedrooms', 'bathrooms']
    },
    'v1.1.0': {
        'path': 'models/v1.1.0/housing_model.joblib',
        'trained_date': '2024-02-01',
        'performance': {'r2': 0.88, 'mae': 22000},
        'features': ['square_feet', 'bedrooms', 'bathrooms', 'location_score']
    }
}

# Include version in API responses
@app.post("/predict")
def predict(features: HouseFeatures):
    prediction = model.predict([features.dict()])[0]
    return {
        'prediction': prediction,
        'model_version': 'v1.1.0',
        'model_timestamp': '2024-02-01T12:00:00Z'
    }
```

### 2. **Batch Prediction Optimization**
```python
# ❌ INEFFICIENT: Loop through single predictions
def predict_batch_naive(houses):
    predictions = []
    for house in houses:
        pred = model.predict([house])[0]
        predictions.append(pred)
    return predictions

# ✅ EFFICIENT: Vectorized batch prediction
def predict_batch_optimized(houses):
    # Convert list of dicts to 2D array
    X = np.array([[h['square_feet'], h['bedrooms'], h['bathrooms']] 
                  for h in houses])
    return model.predict(X).tolist()

# Performance comparison (1000 houses):
# Naive: ~500ms
# Optimized: ~50ms (10x faster)
```

### 3. **Error Handling and Resilience**
```python
from fastapi import HTTPException
from tenacity import retry, stop_after_attempt, wait_exponential

class PredictionService:
    def __init__(self):
        self.circuit_open = False
        self.failure_count = 0
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def predict_with_retry(self, features):
        try:
            if self.circuit_open:
                raise CircuitBreakerOpenError("Circuit breaker is open")
            
            return self._predict(features)
        except ModelError as e:
            self.failure_count += 1
            if self.failure_count > 5:
                self.circuit_open = True
                schedule_circuit_reset()
            raise HTTPException(status_code=503, detail=str(e))
    
    def _predict(self, features):
        # Actual prediction logic
        pass
```

### 4. **Monitoring and Observability**
```python
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
PREDICTION_REQUESTS = Counter('prediction_requests_total', 'Total prediction requests')
PREDICTION_ERRORS = Counter('prediction_errors_total', 'Total prediction errors')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
MODEL_VERSION_USAGE = Gauge('model_version_usage', 'Active model version', ['version'])

@app.post("/predict")
@PREDICTION_LATENCY.time()
def predict(features: HouseFeatures):
    PREDICTION_REQUESTS.inc()
    MODEL_VERSION_USAGE.labels(version='v1.1.0').inc()
    
    try:
        start_time = time.time()
        prediction = model.predict([features.dict()])[0]
        latency = time.time() - start_time
        
        # Log structured data
        logger.info("Prediction completed", extra={
            'prediction_id': str(uuid.uuid4()),
            'model_version': 'v1.1.0',
            'latency_ms': latency * 1000,
            'features': features.dict()
        })
        
        return {"prediction": prediction}
    except Exception as e:
        PREDICTION_ERRORS.inc()
        logger.error("Prediction failed", extra={'error': str(e)})
        raise HTTPException(status_code=500, detail="Prediction failed")
```

### 5. **Containerization Best Practices**
```dockerfile
# Multi-stage Dockerfile for ML services
# Stage 1: Builder
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app

# Copy only necessary files
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
COPY models/ ./models/

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Environment variables
ENV PATH=/root/.local/bin:$PATH \
    MODEL_PATH=/app/models/housing_model.joblib \
    LOG_LEVEL=INFO

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Implementation Patterns

### 1. **Feature Store Integration**
```python
class FeatureStore:
    def __init__(self):
        self.cache = {}
    
    def get_features(self, house_id: str) -> Dict:
        # Check cache first
        if house_id in self.cache:
            return self.cache[house_id]
        
        # Fetch from feature store
        features = self._fetch_from_store(house_id)
        
        # Enrich with derived features
        features['price_per_sqft'] = features.get('price', 0) / max(1, features.get('square_feet', 1))
        features['bed_bath_ratio'] = features.get('bedrooms', 1) / max(1, features.get('bathrooms', 1))
        
        # Cache for future requests
        self.cache[house_id] = features
        return features
```

### 2. **A/B Testing Framework**
```python
class ABTestingRouter:
    def __init__(self):
        self.models = {
            'v1.0.0': joblib.load('models/v1.0.0/model.joblib'),
            'v1.1.0': joblib.load('models/v1.1.0/model.joblib')
        }
        self.traffic_split = {
            'v1.0.0': 0.3,  # 30% of traffic
            'v1.1.0': 0.7   # 70% of traffic
        }
    
    def route_prediction(self, features, user_id):
        # Deterministic routing based on user_id
        hash_value = hash(user_id) % 100
        cumulative = 0
        
        for version, percentage in self.traffic_split.items():
            cumulative += percentage * 100
            if hash_value < cumulative:
                model = self.models[version]
                prediction = model.predict([features])[0]
                
                # Log for analysis
                self.log_prediction(user_id, version, prediction)
                return prediction, version
        
        # Fallback
        return self.models['v1.1.0'].predict([features])[0], 'v1.1.0'
```

### 3. **Model Performance Monitoring**
```python
class PerformanceMonitor:
    def __init__(self, window_size=1000):
        self.predictions = deque(maxlen=window_size)
        self.actuals = deque(maxlen=window_size)
    
    def record_prediction(self, prediction, actual=None):
        self.predictions.append(prediction)
        if actual is not None:
            self.actuals.append(actual)
    
    def calculate_metrics(self):
        if len(self.actuals) < 10:
            return None
        
        preds = np.array(self.predictions[-len(self.actuals):])
        acts = np.array(self.actuals)
        
        mae = np.mean(np.abs(preds - acts))
        mse = np.mean((preds - acts) ** 2)
        r2 = 1 - np.sum((preds - acts) ** 2) / np.sum((acts - np.mean(acts)) ** 2)
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'r2': float(r2),
            'sample_size': len(acts)
        }
```

## 📊 Production Checklist

### Before Deployment
- [ ] **Model Validation**: Test accuracy > baseline, check for bias
- [ ] **Performance Testing**: P95 latency < 100ms, memory < container limit
- [ ] **Error Handling**: Graceful degradation, circuit breakers implemented
- [ ] **Monitoring**: Metrics, logs, alerts configured
- [ ] **Security**: Input validation, rate limiting, authentication
- [ ] **Documentation**: API docs, runbooks, troubleshooting guide

### During Operation
- [ ] **Health Checks**: Regular /health endpoint monitoring
- [ ] **Performance Monitoring**: Track latency, error rates, throughput
- [ ] **Data Drift Detection**: Monitor input feature distributions
- [ ] **Model Decay Monitoring**: Track prediction accuracy over time
- [ ] **Resource Usage**: Monitor CPU, memory, disk I/O

### Maintenance
- [ ] **Regular Retraining**: Schedule based on performance decay
- [ ] **Version Rollouts**: Canary deployments, A/B testing
- [ ] **Backup & Recovery**: Model artifacts backed up, rollback procedure
- [ ] **Cost Optimization**: Right-size containers, auto-scaling configured

## 🚀 Advanced Topics

### 1. **Online Learning**
For services that need to adapt quickly:
```python
from river import linear_model, preprocessing, metrics

# Incremental learning model
model = preprocessing.StandardScaler() | linear_model.LinearRegression()
metric = metrics.MAE()

for x, y in stream:
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    model.learn_one(x, y)
```

### 2. **Model Explainability**
```python
import shap

# Generate SHAP explanations
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

# Feature importance for individual predictions
def explain_prediction(features):
    explanation = explainer(features.reshape(1, -1))
    return {
        'prediction': float(explanation.base_values + explanation.values.sum()),
        'feature_contributions': dict(zip(feature_names, explanation.values[0])),
        'base_value': float(explanation.base_values)
    }
```

### 3. **Multi-Model Ensemble**
```python
class ModelEnsemble:
    def __init__(self):
        self.models = {
            'random_forest': joblib.load('models/rf.joblib'),
            'gradient_boosting': joblib.load('models/gb.joblib'),
            'neural_net': joblib.load('models/nn.joblib')
        }
        self.weights = {'random_forest': 0.4, 'gradient_boosting': 0.4, 'neural_net': 0.2}
    
    def predict(self, X):
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)
        
        # Weighted ensemble
        ensemble_pred = sum(predictions[name] * self.weights[name] 
                          for name in self.models.keys())
        
        return {
            'ensemble_prediction': ensemble_pred,
            'individual_predictions': predictions,
            'uncertainty': np.std(list(predictions.values()))
        }
```

## 📚 Resources

### Essential Reading
1. **"Building Machine Learning Powered Applications"** - Emmanuel Ameisen
2. **"Designing Data-Intensive Applications"** - Martin Kleppmann (ML serving chapters)
3. **Google's ML Engineering Best Practices**: https://developers.google.com/machine-learning/guides

### Tools & Libraries
- **MLflow**: Model tracking and deployment
- **Seldon Core**: Kubernetes-native ML deployment
- **BentoML**: Model serving framework
- **Evidently AI**: ML monitoring and drift detection
- **Great Expectations**: Data validation for ML pipelines

### Monitoring & Observability
- **Prometheus + Grafana**: Metrics collection and visualization
- **ELK Stack**: Log aggregation and analysis
- **Jaeger**: Distributed tracing for ML pipelines
- **Arize AI**: ML-specific monitoring platform

---

**Remember**: The most sophisticated model is useless if it can't be reliably served in production. Focus on reliability, monitoring, and operational excellence alongside model accuracy.