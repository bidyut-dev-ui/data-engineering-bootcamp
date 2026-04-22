# Data API Service: Gotchas & Best Practices

This document outlines common pitfalls, anti-patterns, and best practices for building production-ready data API services with FastAPI, PostgreSQL, and Docker.

## 🚨 Critical Gotchas

### 1. **Database Connection Pool Exhaustion**

#### WRONG: Unlimited connections leading to resource exhaustion
```python
# Anti-pattern: Creating new engine for each request
from sqlalchemy import create_engine

def get_db():
    engine = create_engine(DATABASE_URL)  # New connection each time
    return engine.connect()
```

#### CORRECT: Connection pooling with proper limits
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Maximum connections in pool
    max_overflow=5,         # Additional connections allowed
    pool_timeout=30,        # Wait time for connection
    pool_recycle=3600,      # Recycle connections every hour
    pool_pre_ping=True      # Validate connections before use
)

# Dependency injection for sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Why it matters on 8GB RAM:**
- Each PostgreSQL connection consumes ~2-10MB of memory
- Unbounded connections can exhaust available memory
- Connection pooling reduces memory fragmentation

### 2. **N+1 Query Problem in Analytical Endpoints**

#### WRONG: Multiple queries for related data
```python
# Anti-pattern: Querying customer details for each sale
sales = db.query(Sale).all()
for sale in sales:
    customer = db.query(Customer).filter_by(id=sale.customer_id).first()
    # Process customer data...
```

#### CORRECT: Single query with joins
```python
# Best practice: Single query with proper joins
results = db.query(
    Sale.id,
    Sale.amount,
    Customer.name,
    Customer.region
).join(Customer, Sale.customer_id == Customer.id).all()

# Or use SQLAlchemy relationships with eager loading
sales = db.query(Sale).options(joinedload(Sale.customer)).all()
```

**Memory Impact:**
- N+1 queries increase database load and memory usage
- Large result sets without pagination can exhaust memory
- Proper indexing reduces query memory footprint

### 3. **Memory Leaks in Long-Running API Processes**

#### WRONG: Global variables accumulating data
```python
# Anti-pattern: Global cache without size limits
CACHE = {}

@app.get("/api/data")
def get_data():
    data = expensive_query()
    CACHE["data"] = data  # Never cleared, grows indefinitely
    return data
```

#### CORRECT: Bounded cache with LRU eviction
```python
from functools import lru_cache
from cachetools import LRUCache

# Python's built-in LRU cache
@lru_cache(maxsize=128)
def get_cached_data(key: str):
    return expensive_query(key)

# Or use cachetools for more control
cache = LRUCache(maxsize=1000, getsizeof=len)

@app.get("/api/data")
def get_data(key: str):
    if key not in cache:
        cache[key] = expensive_query(key)
    return cache[key]
```

### 4. **Docker Image Bloat**

#### WRONG: Single-stage build with development dependencies
```dockerfile
# Anti-pattern: All dependencies in final image
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt  # Includes dev dependencies
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

#### CORRECT: Multi-stage build for minimal image
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ app/
ENV PATH=/root/.local/bin:$PATH
USER 1001  # Non-root user for security
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Image Size Impact:**
- Development dependencies can add 200-500MB
- Multi-stage builds reduce image size by 60-80%
- Smaller images deploy faster and use less disk space

### 5. **Missing Database Indexes for Analytical Queries**

#### WRONG: Full table scans on large datasets
```sql
-- Anti-pattern: Query without indexes
SELECT region, SUM(amount) 
FROM sales 
WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY region;
-- Without indexes on date and region, this scans entire table
```

#### CORRECT: Proper indexing strategy
```sql
-- Create composite index for common query patterns
CREATE INDEX idx_sales_date_region 
ON sales(date, region);

-- Create separate indexes for different access patterns
CREATE INDEX idx_sales_customer_date 
ON sales(customer_id, date);

-- Use partial indexes for filtered queries
CREATE INDEX idx_active_customers 
ON customers(id) 
WHERE status = 'active';
```

**Query Performance:**
- Full table scans on 1M+ rows can timeout
- Proper indexes reduce query time from seconds to milliseconds
- Indexes increase write overhead but are essential for reads

## 🏗️ Architecture Best Practices

### 1. **API Design Patterns**

#### Use Resource-Oriented Design
```python
# Good: Clear resource hierarchy
@app.get("/api/sales")              # Collection
@app.get("/api/sales/{sale_id}")    # Single resource
@app.get("/api/sales/{sale_id}/items")  # Sub-resource

# Good: Consistent response formats
class SalesResponse(BaseModel):
    data: List[Sale]
    pagination: PaginationInfo
    metadata: ResponseMetadata
```

#### Implement Proper Error Handling
```python
# Custom exception hierarchy
class APIError(Exception):
    """Base API error"""
    pass

class ValidationError(APIError):
    """Input validation failed"""
    pass

class ResourceNotFoundError(APIError):
    """Requested resource not found"""
    pass

# Global exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "validation_failed", "details": str(exc)}
    )
```

### 2. **Memory Management for 8GB RAM**

#### Implement Response Streaming
```python
from fastapi.responses import StreamingResponse
import json

@app.get("/api/large-dataset")
async def get_large_dataset():
    """Stream large dataset to avoid memory exhaustion"""
    def generate():
        # Generator yields data in chunks
        for chunk in get_data_chunks():
            yield json.dumps(chunk) + "\n"
    
    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )
```

#### Use Chunked Database Queries
```python
from sqlalchemy.orm import Query

def get_large_resultset_chunked(query: Query, chunk_size: int = 1000):
    """Yield results in chunks to control memory usage"""
    offset = 0
    while True:
        chunk = query.offset(offset).limit(chunk_size).all()
        if not chunk:
            break
        yield chunk
        offset += chunk_size
```

#### Configure Gunicorn/Uvicorn Workers
```yaml
# gunicorn_config.py
workers = 2                    # Match CPU cores (not memory)
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5

# Memory-aware configuration
max_requests = 1000           # Restart workers after N requests
max_requests_jitter = 50      # Add randomness to restart timing
```

### 3. **Database Optimization**

#### Connection Pool Tuning for 8GB RAM
```python
# Optimal pool configuration for 8GB RAM
POOL_CONFIG = {
    "pool_size": min(10, (os.cpu_count() or 2) * 2),
    "max_overflow": 5,
    "pool_timeout": 30,
    "pool_recycle": 1800,      # 30 minutes
    "pool_pre_ping": True,
    "echo": False,             # Disable SQL logging in production
}

# Calculate based on available memory
import psutil
available_memory_gb = psutil.virtual_memory().available / (1024**3)
if available_memory_gb < 4:
    # Conservative settings for low memory
    POOL_CONFIG["pool_size"] = 5
    POOL_CONFIG["max_overflow"] = 2
```

#### Query Optimization Techniques
```python
# 1. Select only needed columns
query = db.query(Sale.id, Sale.amount, Sale.date)  # Good
query = db.query(Sale)  # Bad - fetches all columns

# 2. Use exists() for existence checks
if db.query(exists().where(Sale.customer_id == customer_id)).scalar():
    # Good - stops at first match
    pass

# 3. Batch updates and inserts
# Bad: Individual inserts in loop
for item in data:
    db.add(Sale(**item))
    
# Good: Batch insert
db.bulk_insert_mappings(Sale, data)
db.commit()
```

### 4. **Docker Production Configuration**

#### Resource Limits in Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/warehouse
    deploy:
      resources:
        limits:
          memory: 2G      # Hard limit
          cpus: '1.0'
        reservations:
          memory: 1G      # Guaranteed minimum
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### Security Hardening
```dockerfile
# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Read-only filesystem where possible
VOLUME ["/tmp", "/var/log"]

# Security scanning
# Run: docker scan <image-name>
```

### 5. **Monitoring and Observability**

#### Structured Logging Configuration
```python
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage with context
logger.info("api_request", 
    endpoint=request.url.path,
    method=request.method,
    duration_ms=processing_time,
    user_agent=request.headers.get("user-agent")
)
```

#### Metrics Collection
```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Instrument endpoints
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

## 🔧 Performance Optimization Checklist

### For 8GB RAM Environments:

#### ✅ **Database Layer**
- [ ] Connection pool size limited to 10-15 connections
- [ ] Query result streaming enabled for large datasets
- [ ] Appropriate indexes on frequently queried columns
- [ ] Regular vacuum and analyze on PostgreSQL
- [ ] Query timeout configuration (30-60 seconds)

#### ✅ **API Layer**
- [ ] Response compression enabled (gzip/brotli)
- [ ] Response caching for static/expensive endpoints
- [ ] Request size limits (10MB default)
- [ ] Pagination implemented for list endpoints
- [ ] Rate limiting to prevent abuse

#### ✅ **Container Layer**
- [ ] Multi-stage Docker builds
- [ ] Memory limits in docker-compose (2-3GB per service)
- [ ] Health checks with dependency verification
- [ ] Non-root user execution
- [ ] Read-only filesystem where possible

#### ✅ **Monitoring Layer**
- [ ] Memory usage metrics collection
- [ ] Connection pool metrics monitoring
- [ ] Slow query logging (>100ms)
- [ ] Error rate tracking and alerting
- [ ] Request/response size monitoring

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Database migrations tested and versioned
- [ ] Environment variables validated
- [ ] Health checks passing
- [ ] Load testing completed
- [ ] Rollback procedure documented

### Post-Deployment
- [ ] Monitor memory usage for 24 hours
- [ ] Verify connection pool behavior
- [ ] Check error rates and latency
- [ ] Validate cache hit ratios
- [ ] Confirm backup procedures

## 📊 Expected Performance on 8GB RAM

### With Proper Optimization:
- **API Response Time**: < 100ms for cached endpoints, < 500ms for database queries
- **Concurrent Users**: 50-100 with connection pooling
- **Memory Usage**: 1.5-2.5GB for API + database connections
- **Throughput**: 100-200 requests/second for simple endpoints

### Common Bottlenecks to Monitor:
1. **Database Connection Wait Time** - indicates pool exhaustion
2. **Garbage Collection Pauses** - indicates memory pressure
3. **Query Planning Time** - indicates missing indexes
4. **Network Latency** - indicates infrastructure issues

## 🎯 Key Takeaways

1. **Connection Management is Critical**: Proper pooling prevents resource exhaustion
2. **Memory is a Scarce Resource**: Implement streaming, pagination, and caching
3. **Indexes are Not Optional**: Analytical queries require proper indexing
4. **Monitoring is Production Requirement**: You can't optimize what you don't measure
5. **Security is Not an Afterthought**: Implement from day one

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/14/core/pooling.html)
- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Prometheus Metrics for APIs](https://prometheus.io/docs/practices/instrumentation/)