from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import random

app = FastAPI(title="Monitored API")

# Prometheus metrics
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'api_active_requests',
    'Number of active requests'
)

data_processed = Counter(
    'data_records_processed_total',
    'Total number of data records processed'
)

pipeline_errors = Counter(
    'pipeline_errors_total',
    'Total pipeline errors',
    ['error_type']
)

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    active_requests.inc()
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    active_requests.dec()
    
    return response

# Routes
@app.get("/")
def read_root():
    return {"message": "Monitored API with Prometheus"}

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/data/process")
def process_data(records: int = 100):
    """Simulate data processing"""
    # Simulate processing time
    time.sleep(random.uniform(0.1, 0.5))
    
    # Track processed records
    data_processed.inc(records)
    
    return {
        "status": "success",
        "records_processed": records
    }

@app.get("/data/error")
def simulate_error():
    """Simulate an error for testing"""
    pipeline_errors.labels(error_type="validation_error").inc()
    return {"status": "error", "message": "Simulated error"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }
