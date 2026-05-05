# INTERVIEW QUESTIONS: Predictive Service (Week 20)

This document contains interview questions for ML Engineering, Model Serving, and Production ML Systems roles. Questions range from fundamental concepts to advanced system design.

## 📋 Table of Contents
1. [Fundamental Concepts](#fundamental-concepts)
2. [Model Serving & API Design](#model-serving--api-design)
3. [Performance & Scalability](#performance--scalability)
4. [Monitoring & Observability](#monitoring--observability)
5. [Error Handling & Resilience](#error-handling--resilience)
6. [Model Management](#model-management)
7. [Containerization & Deployment](#containerization--deployment)
8. [System Design](#system-design)
9. [Behavioral & Scenario-Based](#behavioral--scenario-based)
10. [Coding Exercises](#coding-exercises)

---

## Fundamental Concepts

### 1. **What is the difference between batch prediction and real-time prediction?**
**Expected Answer**: 
- **Batch Prediction**: Processing multiple predictions at once, often on a schedule (e.g., nightly). Suitable for non-time-sensitive tasks, better resource utilization, easier to debug.
- **Real-time Prediction**: Immediate prediction for individual requests. Requires low latency, more complex infrastructure, higher cost per prediction.

**Follow-up**: When would you choose one over the other?

### 2. **Explain model serialization formats (pickle, joblib, ONNX, PMML)**
**Expected Answer**:
- **Pickle**: Python-native, simple but insecure, version-dependent
- **Joblib**: Better for large numpy arrays, parallel loading
- **ONNX**: Framework-agnostic, optimized for inference
- **PMML**: XML-based, widely supported in enterprise systems
- **TensorFlow SavedModel**: TensorFlow-specific, includes computation graph

### 3. **What is model versioning and why is it important?**
**Expected Answer**: Tracking different versions of models with metadata (training data, hyperparameters, performance). Important for reproducibility, rollback, A/B testing, and compliance.

### 4. **Describe the ML model lifecycle**
**Expected Answer**: 
1. Data collection & preparation
2. Model training & validation
3. Model deployment & serving
4. Monitoring & maintenance
5. Retraining & iteration

### 5. **What are the challenges of serving ML models in production?**
**Expected Answer**:
- Model size and memory constraints
- Latency requirements
- Version management
- Data drift detection
- Scaling with traffic
- Cost optimization
- Security and privacy

---

## Model Serving & API Design

### 6. **Design a REST API for a housing price prediction service**
**Expected Answer**:
```python
# Endpoints:
GET  /health                    # Service health check
POST /predict                   # Single prediction
POST /predict/batch             # Batch prediction
GET  /model/info                # Model metadata
GET  /model/versions            # Available versions
POST /model/switch              # Switch active model version
```

**Follow-up**: What status codes would you use for each endpoint?

### 7. **How would you handle input validation for ML APIs?**
**Expected Answer**:
- Use Pydantic models with field constraints
- Validate data types, ranges, and business rules
- Check for missing values
- Validate feature distributions
- Return descriptive error messages (HTTP 422)

### 8. **What is the difference between synchronous and asynchronous prediction APIs?**
**Expected Answer**:
- **Synchronous**: Client waits for response, simpler but blocks resources
- **Asynchronous**: Client receives job ID, polls for results later, better for long-running predictions

### 9. **How would you design an API for A/B testing different model versions?**
**Expected Answer**:
- Include model version parameter in request
- Route traffic based on user ID or random sampling
- Log predictions with version tags
- Compare performance metrics per version

### 10. **What security considerations are important for ML APIs?**
**Expected Answer**:
- Authentication & authorization
- Rate limiting
- Input sanitization (prevent injection attacks)
- Data encryption in transit
- Model stealing protection
- Privacy protection (GDPR, HIPAA)

---

## Performance & Scalability

### 11. **How would you optimize batch prediction performance?**
**Expected Answer**:
- Vectorize operations instead of looping
- Use GPU acceleration if available
- Implement parallel processing
- Cache frequent predictions
- Use efficient data formats (Parquet, Arrow)
- Implement pagination for large batches

### 12. **What strategies would you use to reduce prediction latency?**
**Expected Answer**:
- Model quantization
- Hardware acceleration (GPU, TPU)
- Caching predictions
- Pre-warming models
- Load balancing
- CDN for static assets
- Connection pooling

### 13. **How would you handle memory constraints when serving large models?**
**Expected Answer**:
- Model quantization/pruning
- Lazy loading
- Model sharding
- Streaming predictions
- Memory-mapped files
- Swap to disk with careful management

### 14. **Describe horizontal vs vertical scaling for ML services**
**Expected Answer**:
- **Vertical**: Larger instances, simpler but limited, single point of failure
- **Horizontal**: More instances, complex but scalable, requires load balancing

### 15. **What is cold start problem and how do you mitigate it?**
**Expected Answer**: Delay when loading large models. Mitigations: pre-warming, keep-alive, smaller models, progressive loading.

---

## Monitoring & Observability

### 16. **What metrics would you monitor for an ML prediction service?**
**Expected Answer**:
- **Business**: Prediction volume, error rate, latency
- **Technical**: CPU/memory usage, queue length, throughput
- **Model**: Input distribution drift, prediction confidence, feature importance stability
- **Infrastructure**: Container health, disk I/O, network latency

### 17. **How would you detect data drift in production?**
**Expected Answer**:
- Statistical tests (KS test, χ² test)
- Monitor feature distributions
- Track prediction confidence changes
- Alert on significant distribution shifts
- Implement canary analysis

### 18. **What is model decay and how do you measure it?**
**Expected Answer**: Performance degradation over time due to changing data patterns. Measure by comparing production performance to validation performance, tracking accuracy metrics over time.

### 19. **Design a dashboard for monitoring ML service health**
**Expected Answer**:
- Real-time prediction metrics
- Error rates and types
- Latency percentiles (p50, p95, p99)
- Resource utilization
- Data drift indicators
- Model version performance comparison

### 20. **How would you implement structured logging for ML services?**
**Expected Answer**:
```python
import structlog

logger = structlog.get_logger()

logger.info("prediction_completed",
    prediction_id="123",
    model_version="v1.0",
    latency_ms=45.2,
    features={"square_feet": 2000},
    prediction=425000.50,
    confidence=0.85
)
```

---

## Error Handling & Resilience

### 21. **What error types should an ML API handle?**
**Expected Answer**:
- Input validation errors (422)
- Model loading errors (503)
- Prediction errors (500)
- Timeout errors (504)
- Rate limit exceeded (429)
- Authentication errors (401)

### 22. **How would you implement circuit breaker pattern for ML services?**
**Expected Answer**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.circuit_open = False
        self.last_failure_time = None
    
    def call(self, func, *args):
        if self.circuit_open:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.circuit_open = False
                self.failure_count = 0
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func(*args)
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.circuit_open = True
            raise
```

### 23. **What is graceful degradation in ML services?**
**Expected Answer**: When primary model fails, fall back to simpler model or cached values. Example: If deep learning model fails, use linear regression; if that fails, return historical average.

### 24. **How would you handle partial failures in batch prediction?**
**Expected Answer**:
- Implement idempotent operations
- Use checkpointing
- Retry with exponential backoff
- Log failed predictions for manual review
- Continue processing other items

### 25. **Design a retry strategy for unreliable model dependencies**
**Expected Answer**:
```python
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10),
       retry=retry_if_exception_type((TimeoutError, ConnectionError)))
def predict_with_retry(features):
    return model.predict(features)
```

---

## Model Management

### 26. **Describe a model registry architecture**
**Expected Answer**:
- Storage for model artifacts
- Metadata database (version, performance, training data)
- API for model management
- Access control and audit logging
- Integration with CI/CD pipeline

### 27. **How would you implement canary deployment for models?**
**Expected Answer**:
1. Deploy new model to small percentage of traffic
2. Monitor key metrics (error rate, latency, business metrics)
3. Gradually increase traffic if metrics are good
4. Roll back if issues detected
5. Complete rollout or abort based on results

### 28. **What is shadow deployment and when would you use it?**
**Expected Answer**: Running new model alongside old model without affecting predictions. Use for: validating performance, collecting comparison data, testing without risk.

### 29. **How would you manage model dependencies (library versions)?**
**Expected Answer**:
- Pin exact versions in requirements.txt
- Use virtual environments or containers
- Test compatibility during CI/CD
- Maintain backward compatibility when possible
- Document version requirements

### 30. **Describe a model retraining pipeline**
**Expected Answer**:
1. Trigger (schedule, performance decay, data drift)
2. Data collection and preprocessing
3. Model training and validation
4. Performance comparison with current model
5. Approval and deployment
6. Monitoring post-deployment

---

## Containerization & Deployment

### 31. **Design a Dockerfile for an ML service**
**Expected Answer**:
```dockerfile
# Multi-stage build
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
COPY models/ ./models/

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 32. **What are the benefits of using Kubernetes for ML serving?**
**Expected Answer**:
- Auto-scaling based on load
- Self-healing (restart failed containers)
- Rolling updates without downtime
- Resource management and isolation
- Service discovery and load balancing

### 33. **How would you configure resource limits for ML containers?**
**Expected Answer**:
```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2"
```

### 34. **Describe a CI/CD pipeline for ML models**
**Expected Answer**:
1. **CI**: Code linting, unit tests, integration tests, model validation
2. **Build**: Docker image creation, vulnerability scanning
3. **Test**: Deploy to staging, run smoke tests, performance tests
4. **Deploy**: Canary deployment to production, monitoring
5. **Verify**: Post-deployment validation, alert on issues

### 35. **What is infrastructure as code for ML deployments?**
**Expected Answer**: Using tools like Terraform, CloudFormation, or Pulumi to define and manage ML infrastructure (compute, storage, networking) in version-controlled configuration files.

---

## System Design

### 36. **Design a scalable ML prediction service for 1M requests/day**
**Expected Answer**:
- **Architecture**: Load balancer → API servers → Model servers → Cache → Database
- **Scaling**: Auto-scaling groups, read replicas, CDN
- **Caching**: Redis for frequent predictions
- **Monitoring**: Distributed tracing, centralized logging
- **Deployment**: Blue-green deployment, feature flags

### 37. **How would you design a system for online learning?**
**Expected Answer**:
- Streaming data pipeline (Kafka, Kinesis)
- Incremental model updates
- Version control for models
- A/B testing framework
- Performance monitoring with concept drift detection

### 38. **Design a feature store for ML services**
**Expected Answer**:
- **Storage**: Time-series database for feature values
- **Computation**: Batch and streaming feature computation
- **Serving**: Low-latency API for feature retrieval
- **Metadata**: Feature definitions, lineage, statistics
- **Monitoring**: Feature quality, freshness, drift

### 39. **How would you handle GDPR compliance for ML predictions?**
**Expected Answer**:
- Data anonymization
- Right to explanation (model interpretability)
- Data deletion capability
- Audit logging
- Privacy-preserving ML techniques
- Data minimization

### 40. **Design a multi-tenant ML platform**
**Expected Answer**:
- Resource isolation (namespaces, quotas)
- Authentication and authorization
- Custom model deployment per tenant
- Usage tracking and billing
- Tenant-specific monitoring
- Shared infrastructure with isolation

---

## Behavioral & Scenario-Based

### 41. **A model performs well in testing but poorly in production. How would you debug this?**
**Expected Answer**:
1. Check for data differences (training vs production)
2. Verify feature engineering pipeline
3. Check for data drift
4. Examine prediction confidence scores
5. Look for systematic errors
6. Compare with shadow deployment results

### 42. **You need to reduce prediction latency by 50%. What would you do?**
**Expected Answer**:
1. Profile to find bottlenecks
2. Optimize feature computation
3. Implement caching
4. Use lighter model architecture
5. Hardware acceleration
6. Batch predictions where possible

### 43. **How would you explain a complex ML model's prediction to a non-technical stakeholder?**
**Expected Answer**:
- Use feature importance scores
- Provide confidence intervals
- Give similar historical examples
- Use visualization (LIME, SHAP)
- Focus on business impact, not technical details

### 44. **You discover bias in your model's predictions. What steps would you take?**
**Expected Answer**:
1. Quantify the bias
2. Identify contributing features
3. Retrain with debiasing techniques
4. Implement fairness constraints
5. Monitor for bias in production
6. Document findings and actions

### 45. **How would you prioritize between model accuracy and inference speed?**
**Expected Answer**: Depends on use case. Real-time applications (autonomous vehicles) prioritize speed with minimum accuracy threshold. Batch applications (credit scoring) prioritize accuracy with reasonable time constraints.

---

## Coding Exercises

### 46. **Implement a batch prediction endpoint with FastAPI**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

class HouseFeatures(BaseModel):
    square_feet: int
    bedrooms: int
    bathrooms: int

class BatchPredictionRequest(BaseModel):
    houses: List[HouseFeatures]

# Mock model
def predict_batch(features_list):
    # Convert to numpy array
    X = np.array([[h.square_feet, h.bedrooms, h.bathrooms] 
                  for h in features_list])
    # Mock prediction: price = 100 * square_feet + 50000 * bedrooms
    return (100 * X[:, 0] + 50000 * X[:, 1]).tolist()

@app.post("/predict/batch")
async def batch_predict(request: BatchPredictionRequest):
    if len(request.houses) > 1000:
        raise HTTPException(400, "Batch size too large")
    
    predictions = predict_batch(request.houses)
    
    return {
        "predictions": predictions,
        "count": len(predictions),
        "model_version": "v1.0"
    }
```

### 47. **Implement input validation with custom business rules**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class HousingPredictionRequest(BaseModel):
    square_feet: int = Field(..., gt=0, le=10000)
    bedrooms: int = Field(..., ge=1, le=10)
    bathrooms: int = Field(..., ge=1, le=10)
    zip_code: Optional[str] = None
    
    @validator('square_feet')
    def validate_square_feet_per_bedroom(cls, v, values):
        if 'bedrooms' in values and v / values['bedrooms'] < 200:
            raise ValueError('Minimum 200 sqft per bedroom')
        return v
    
    @validator('bathrooms')
    def validate_bathrooms_vs_bedrooms(cls, v, values):
        if 'bedrooms' in values and v > values['bedrooms'] + 2:
            raise ValueError('Too many bathrooms for given bedrooms')
        return v
```

### 48. **Implement a simple model cache**
```python
from functools import lru_cache
from datetime import datetime, timedelta

class PredictionCache:
    def __init__(self, max_size=1000, ttl_seconds=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get_key(self, features):
        # Create hashable key from features
        return tuple(sorted(features.items()))
    
    def get(self, features):
        key = self.get_key(features)
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < self.ttl:
                return entry['prediction']
            else:
                del self.cache[key]
        return None
    
    def set(self, features, prediction):
        key = self.get_key(features)
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'prediction': prediction,
            'timestamp': datetime.now()
        }
```

### 49. **Implement a circuit breaker**
```python
import time
from functools import wraps

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError()
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            
            raise
```

### 50. **Implement model version routing**
```python
class ModelRouter:
    def __init__(self):
        self.models = {}
        self.traffic_split = {}
    
    def add_model(self, version, model, traffic_percentage):
        self.models[version] = model
        self.traffic_split[version] = traffic_percentage
    
    def predict(self, features, user_id=None):
        # Determine which model to use
        if user_id:
            # Deterministic routing based on user_id
            hash_val = hash(user_id) % 100
            cumulative = 0
            for version, percentage in self.traffic_split.items():
                cumulative += percentage
                if hash_val < cumulative * 100:
                    model = self.models[version]
                    break
        else:
            # Random routing
            import random
            version = random.choices(
                list(self.traffic_split.keys()),
                weights=list(self.traffic_split.values())
            )[0]
            model = self.models[version]
        
        prediction = model.predict(features)
        
        # Log for analysis
        self.log_prediction(user_id, version, prediction)
        
        return prediction, version
```

---

## 🎯 Interview Evaluation Rubric

### Technical Skills (40%)
- Understanding of ML concepts
- API design principles
- System architecture knowledge
- Performance optimization techniques

### Problem Solving (30%)
- Analytical approach to problems
- Consideration of trade-offs
- Creative solutions to constraints
- Debugging methodology

### Communication (20%)
- Clear explanation of concepts
- Ability to simplify complex topics
- Active listening and clarification
- Professional presentation

### Practical Experience (10%)
- Real-world deployment experience
- Knowledge of tools and frameworks
- Understanding of operational concerns
- Best practices implementation

---

## 📚 Recommended Preparation

### Books
1. **"Building Machine Learning Powered Applications"** - Emmanuel Ameisen
2. **"Designing Data-Intensive Applications"** - Martin Kleppmann
3. **"Machine Learning Engineering"** - Andriy Burkov

### Online Courses
1. **"Machine Learning Engineering for Production (MLOps)"** - Coursera
2. **"Deploying Machine Learning Models"** - Udemy
3. **"Full Stack Deep Learning"** - UC Berkeley

### Practice Platforms
1. **LeetCode**: System design questions
2. **HackerRank**: Algorithm challenges
3. **Kaggle**: ML competitions
4. **Design Gurus**: Grokking the System Design Interview

### Open Source Projects
1. **MLflow**: Model management
2. **Seldon Core**: Model deployment
3. **Kubeflow**: Kubernetes ML platform
4. **BentoML**: Model serving framework

---

**Good luck with your interviews! Remember: Focus on fundamentals, think aloud, and don't be afraid to ask clarifying questions.**