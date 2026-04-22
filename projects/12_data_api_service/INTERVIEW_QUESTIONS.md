# Data API Service Interview Questions

This document contains comprehensive interview questions for Data API Service development roles, covering FastAPI, database integration, Docker, deployment, and production considerations.

## 📋 Table of Contents

1. [Core Concepts](#core-concepts)
2. [FastAPI & Python](#fastapi--python)
3. [Database Integration](#database-integration)
4. [API Design & Architecture](#api-design--architecture)
5. [Docker & Containerization](#docker--containerization)
6. [Performance & Optimization](#performance--optimization)
7. [Security](#security)
8. [Monitoring & Observability](#monitoring--observability)
9. [Deployment & DevOps](#deployment--devops)
10. [Scenario-Based Questions](#scenario-based-questions)
11. [Practical Exercises](#practical-exercises)
12. [Behavioral Questions](#behavioral-questions)

## 🎯 Core Concepts

### 1. **What is a Data API Service and how does it differ from a traditional web API?**

**Expected Answer:**
A Data API Service is specifically designed to expose data warehouse or analytical data through RESTful endpoints. Key differences:
- **Purpose**: Traditional web APIs often handle CRUD operations, while Data APIs focus on analytical queries, aggregations, and data insights
- **Response Patterns**: Data APIs typically return aggregated results, time-series data, or analytical summaries rather than individual records
- **Authentication**: Often uses API keys or service accounts rather than user sessions
- **Rate Limiting**: Based on query complexity and data volume rather than user identity
- **Caching**: Heavy use of response caching for expensive analytical queries

**Follow-up:**
- How would you design rate limiting for analytical queries vs CRUD operations?
- What caching strategies are most effective for Data APIs?

### 2. **Explain the role of a Data API Service in a modern data platform architecture.**

**Expected Answer:**
The Data API Service sits between the data warehouse/lake and data consumers (dashboards, applications, analysts). Key roles:
1. **Abstraction Layer**: Hides database complexity from consumers
2. **Query Optimization**: Transforms consumer requests into efficient database queries
3. **Security Gateway**: Enforces access controls and data governance
4. **Performance Layer**: Implements caching, pagination, and response compression
5. **Monitoring Point**: Collects usage metrics and query performance data

**Memory Considerations (8GB RAM):**
- Discuss connection pooling strategies to prevent memory exhaustion
- Explain response streaming for large result sets
- Describe memory-efficient serialization techniques

### 3. **Compare REST, GraphQL, and gRPC for building Data API Services.**

**Expected Answer:**
| Aspect | REST | GraphQL | gRPC |
|--------|------|---------|------|
| **Data Fetching** | Multiple endpoints, over/under-fetching | Single endpoint, precise fetching | Protocol buffers, binary format |
| **Performance** | HTTP/1.1, text-based | HTTP/1.1, text-based | HTTP/2, binary, streaming |
| **Caching** | Built-in HTTP caching | Client-side caching | Limited caching support |
| **Schema** | OpenAPI/Swagger | Strongly typed schema | Protocol buffers |
| **Best For** | Simple CRUD, caching needs | Complex queries, mobile apps | Microservices, high performance |

**For Data APIs:**
- REST is best for simple aggregations with caching needs
- GraphQL excels when consumers need flexible querying
- gRPC is ideal for internal microservices communication

## 🐍 FastAPI & Python

### 4. **How does FastAPI's dependency injection system work and why is it useful for Data APIs?**

**Expected Answer:**
FastAPI uses Python's type hints and function parameters for dependency injection. Key benefits for Data APIs:
1. **Database Session Management**: Automatic session lifecycle
2. **Authentication/Authorization**: Centralized security checks
3. **Request Validation**: Input validation before business logic
4. **Testing**: Easy mocking of dependencies
5. **Configuration**: Environment-based configuration injection

**Example:**
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/sales")
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()
```

**Memory Considerations:**
- Discuss connection pool management in dependency functions
- Explain how to prevent memory leaks with generator dependencies

### 5. **What are Pydantic models and how do they help with API development?**

**Expected Answer:**
Pydantic models provide data validation and serialization using Python type annotations. Benefits:
1. **Input Validation**: Automatic validation of request data
2. **Output Serialization**: Clean JSON serialization of responses
3. **Documentation**: Automatic OpenAPI schema generation
4. **Type Safety**: Runtime type checking
5. **Performance**: Compiled validation for speed

**Data API Example:**
```python
from pydantic import BaseModel, validator
from datetime import date
from typing import List

class SalesQuery(BaseModel):
    start_date: date
    end_date: date
    regions: List[str] = []
    min_amount: float = 0
    
    @validator('end_date')
    def end_date_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
```

### 6. **How would you handle asynchronous operations in a Data API Service?**

**Expected Answer:**
Asynchronous operations are crucial for I/O-bound Data APIs. Strategies:
1. **Async Database Drivers**: Use asyncpg or async SQLAlchemy
2. **Background Tasks**: Use FastAPI's `BackgroundTasks` for non-critical operations
3. **Message Queues**: Offload heavy processing to Celery or Redis queues
4. **Streaming Responses**: Use `StreamingResponse` for large datasets
5. **Connection Pooling**: Async connection pools for better concurrency

**Memory Considerations:**
- Async operations can increase memory usage due to concurrent operations
- Need to limit concurrent async operations based on available memory
- Use semaphores to control concurrency

## 🗄️ Database Integration

### 7. **Explain connection pooling in SQLAlchemy and how to configure it for 8GB RAM.**

**Expected Answer:**
Connection pooling reuses database connections to avoid the overhead of establishing new connections. SQLAlchemy provides `QueuePool` by default.

**Configuration for 8GB RAM:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Maximum connections in pool
    max_overflow=5,         # Additional connections allowed
    pool_timeout=30,        # Seconds to wait for connection
    pool_recycle=3600,      # Recycle connections every hour
    pool_pre_ping=True,     # Validate connections before use
    echo=False              # Disable SQL logging in production
)
```

**Memory Calculation:**
- Each PostgreSQL connection: ~2-10MB
- 15 connections max: ~150MB
- Additional memory for query results: 500MB-1GB
- Total database memory: ~1-1.5GB of 8GB available

### 8. **How would you optimize analytical queries for a Data API?**

**Expected Answer:**
1. **Indexing Strategy**:
   - Composite indexes on frequently queried columns
   - Partial indexes for common filter conditions
   - BRIN indexes for time-series data

2. **Query Optimization**:
   - Use `EXPLAIN ANALYZE` to identify bottlenecks
   - Avoid `SELECT *` - specify only needed columns
   - Use window functions instead of multiple queries
   - Implement materialized views for expensive aggregations

3. **Application-Level Optimization**:
   - Implement query result caching
   - Use pagination for large result sets
   - Implement query timeout and cancellation

### 9. **What is the N+1 query problem and how do you solve it in Data APIs?**

**Expected Answer:**
The N+1 query problem occurs when you fetch a list of items (1 query) and then make additional queries for each item's related data (N queries).

**Example (Problem):**
```python
# Get all sales (1 query)
sales = db.query(Sale).all()
for sale in sales:
    # Get customer for each sale (N queries)
    customer = db.query(Customer).filter_by(id=sale.customer_id).first()
```

**Solutions:**
1. **Eager Loading**:
```python
from sqlalchemy.orm import joinedload
sales = db.query(Sale).options(joinedload(Sale.customer)).all()
```

2. **Single Query with Joins**:
```python
results = db.query(Sale, Customer).join(Customer).all()
```

3. **Batch Loading**:
```python
from sqlalchemy.orm import selectinload
sales = db.query(Sale).options(selectinload(Sale.customer)).all()
```

## 🏗️ API Design & Architecture

### 10. **Design RESTful endpoints for sales analytics data.**

**Expected Answer:**
```python
# Collection endpoints
GET    /api/sales                    # List sales with filtering
POST   /api/sales                    # Create new sale (if applicable)

# Resource endpoints
GET    /api/sales/{id}               # Get specific sale
PUT    /api/sales/{id}               # Update sale
DELETE /api/sales/{id}               # Delete sale

# Analytical endpoints
GET    /api/sales/summary            # Aggregated summary
GET    /api/sales/by-region          # Group by region
GET    /api/sales/by-product         # Group by product
GET    /api/sales/trends             # Time series analysis
GET    /api/sales/top-customers      # Ranking endpoints

# Filtering and pagination
GET    /api/sales?start_date=2023-01-01&end_date=2023-12-31&page=1&limit=100
```

**Response Format:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 100,
    "total": 5000,
    "pages": 50
  },
  "metadata": {
    "query_time_ms": 45,
    "cached": false
  }
}
```

### 11. **How would you implement pagination for large analytical result sets?**

**Expected Answer:**
1. **Offset-Based Pagination** (Simple but inefficient for large offsets):
```sql
SELECT * FROM sales ORDER BY id LIMIT 100 OFFSET 200;
```

2. **Cursor-Based Pagination** (Better performance):
```python
@app.get("/api/sales")
def get_sales(
    limit: int = 100,
    cursor: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale)
    
    if cursor:
        # Decode cursor and filter
        last_id = decode_cursor(cursor)
        query = query.filter(Sale.id > last_id)
    
    results = query.order_by(Sale.id).limit(limit).all()
    
    # Create next cursor
    next_cursor = encode_cursor(results[-1].id) if results else None
    
    return {
        "data": results,
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor
        }
    }
```

**Memory Considerations:**
- Cursor-based pagination reduces database memory usage
- Server-side pagination prevents transferring large result sets
- Consider keyset pagination for time-series data

### 12. **What strategies would you use for API versioning?**

**Expected Answer:**
1. **URL Versioning** (Most common):
```
/api/v1/sales
/api/v2/sales
```

2. **Header Versioning**:
```
GET /api/sales
Accept: application/vnd.company.v1+json
```

3. **Query Parameter Versioning**:
```
GET /api/sales?version=1
```

4. **Content Negotiation**:
```python
@app.get("/api/sales")
def get_sales(version: int = Header(1)):
    if version == 1:
        return v1_response()
    elif version == 2:
        return v2_response()
```

**Recommendation for Data APIs:**
- Use URL versioning for clarity and cacheability
- Maintain backward compatibility for at least 6 months
- Use feature flags for gradual rollouts

## 🐳 Docker & Containerization

### 13. **Create a production-ready Dockerfile for a FastAPI Data API Service.**

**Expected Answer:**
```dockerfile
# Multi-stage build for minimal image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ app/

# Set permissions
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 14. **How would you configure Docker Compose for a Data API Service with PostgreSQL?**

**Expected Answer:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: warehouse
      POSTGRES_USER: api_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U api_user -d warehouse"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://api_user:${DB_PASSWORD}@postgres:5432/warehouse
      LOG_LEVEL: INFO
    depends_on:
      postgres:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
```

### 15. **What are the memory considerations when running containers on 8GB RAM?**

**Expected Answer:**
1. **Container Memory Limits**:
   - API container: 1.5-2GB
   - PostgreSQL container: 3-4GB
   - Leave 1-2GB for OS and other processes

2. **Configuration Strategies**:
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1.5G
        reservations:
          memory: 1G
    environment:
      # Reduce Python memory usage
      PYTHONMALLOC: malloc
      # Limit worker processes
      WEB_CONCURRENCY: 2
```

3. **Monitoring and Optimization**:
   - Use `docker stats` to monitor memory usage
   - Implement OOM killer configuration
   - Use memory-efficient base images (Alpine)
   - Configure swap if available

## ⚡ Performance & Optimization

### 16. **How would you implement caching in a Data API Service?**

**Expected Answer:**
1. **Response Caching** (FastAPI middleware):
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.get("/api/sales/summary")
@cache(expire=300)  # 5 minutes
async def get_sales_summary():
    return expensive_query()
```

2. **Database Query Caching**:
```python
from sqlalchemy_cache import Cache
cache = Cache(RedisBackend(redis_url))

@cache.cached(timeout=300, key_prefix="sales_summary")
def get_sales_summary():
    return db.query(...).all()
```

3. **CDN Caching** for static analytical results

**Cache Invalidation Strategies:**
- Time-based expiration (TTL)
- Write-through caching on data updates
- Cache tagging for related data invalidation
- Manual cache busting via admin endpoints

### 17. **What techniques would you use to reduce API response size?**

**Expected Answer:**
1. **Response Compression**:
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

2. **Field Selection**:
```
GET /api/sales?fields=id,amount,date
```

3. **Pagination** to limit result sets

4. **Binary Formats**:
```python
from fastapi.responses import ORJSONResponse
@app.get("/api/sales", response_class=ORJSONResponse)
def get_sales():
    return large_dataset  # 30-50% smaller than JSON
```

5. **Protocol Buffers** for internal APIs:
```python
from pydantic import BaseModel
import google.protobuf.json_format as json_format

class SalesProto:
    # Protocol buffer definition
    pass

@app.get("/api/sales", response_model=SalesProto)
def get_sales():
    return SalesProto(data=...)
```

### 18. **How would you handle rate limiting for analytical queries?**

**Expected Answer:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Different limits for different endpoints
@app.get("/api/sales/summary")
@limiter.limit("100/hour")
def get_summary():
    return ...

@app.get("/api/sales/detailed")
@limiter.limit("10/hour")  # More restrictive for expensive queries
def get_detailed():
    return ...

# Dynamic rate limiting based on query complexity
def get_complexity_limit(request):
    query_params = dict(request.query_params)
    complexity = calculate_complexity(query_params)
    return f"{max(100 // complexity, 1)}/hour"
```

## 🔒 Security

### 19. **Implement API key authentication for a Data API Service.**

**Expected Answer:**
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not api_key:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API key missing"
        )
    
    # Validate API key against database
    key_record = db.query(APIKey).filter(
        APIKey.key == api_key,
        APIKey.is_active == True
    ).first()
    
    if not key_record:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    # Check rate limits
    if key_record.requests_today >= key_record.daily_limit:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily limit exceeded"
        )
    
    return key_record

@app.get("/api/sales")
def get_sales(api_key: APIKey = Depends(get_api_key)):
    # Update usage counter
    api_key.requests_today += 1
    db.commit()
    
    return get_sales_data()
```

### 20. **What security measures would you implement for a public Data API?**

**Expected Answer:**
1. **Authentication & Authorization**:
   - API keys with rate limits
   - OAuth2 for user-facing APIs
   - Role-based access control (RBAC)

2. **Input Validation**:
   - SQL injection prevention (use ORM/parameterized queries)
   - Request size limits
   - Query complexity limits

3. **Output Security**:
   - Data masking for sensitive fields
   - Response size limits
   - CORS configuration

4. **Infrastructure Security**:
   - HTTPS enforcement
   - WAF (Web Application Firewall)
   - DDoS protection
   - Regular security audits

5. **Monitoring & Logging**:
   - Audit logs for all API calls
   - Anomaly detection for suspicious patterns
   - Regular security scanning

## 📊 Monitoring & Observability

### 21. **What metrics would you monitor for a Data API Service?**

**Expected Answer:**
1. **Business Metrics**:
   - API usage by endpoint
   - Data volume served
   - Top consumers/tenants

2. **Performance Metrics**:
   - Response time (p50, p95, p99)
   - Request rate (RPS)
   - Error rate (4xx, 5xx)
   - Database query performance

3. **Resource Metrics**:
   - Memory usage (RSS, heap)
   - CPU utilization
   - Database connection pool usage
   - Cache hit ratio

4. **Availability Metrics**:
   - Uptime percentage
   - Health check status
   - Dependency status (database, cache)

**Implementation with Prometheus:**
```python
from prometheus_client import Counter, Histogram, generate_latest

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

### 22. **How would you implement structured logging for debugging?**

**Expected Answer:**
```python
import structlog
import logging
import json

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
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    with structlog.contextvars.bound_contextvars(
        request_id=request_id,
        endpoint=request.url.path,
        method=request.method,
        client_ip=request.client.host
    ):
        logger.info("request_started")
        
        try:
            response = await call_next(request)
            
            logger.info("request_completed",
                status_code=response.status_code,
                duration_ms=(time.time() - start_time) * 1000
            )
            
            return response
        except Exception as e:
            logger.error("request_failed", error=str(e), exc_info=True)
            raise
```

## 🚀 Deployment & DevOps

### 23. **Describe a CI/CD pipeline for a Data API Service.**

**Expected Answer:**
1. **Continuous Integration**:
   - Code linting (black, flake8, mypy)
   - Unit tests with pytest
   - Integration tests with test database
   - Security scanning (bandit, safety)
   - Docker image build and vulnerability scan

2. **Continuous Deployment**:
   - Environment-specific configurations (dev, staging, prod)
   - Database migrations with versioning
   - Blue-green deployment for zero downtime
   - Health checks and rollback automation
   - Canary releases for critical changes

3. **Infrastructure as Code**:
   - Docker Compose for local development
   - Kubernetes manifests or Terraform for production
   - Environment variable management
   - Secret management (Vault, AWS Secrets Manager)

**Example GitHub Actions:**
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          docker-compose -f docker-compose.test.yml up --abort-on-container-exit
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to staging
        run: |
          kubectl apply -f k8s/staging/
          kubectl rollout status deployment/api
```

### 24. **How would you handle database migrations in a Data API Service?**

**Expected Answer:**
1. **Migration Tool**: Use Alembic with SQLAlchemy
2. **Version Control**: Store migration files in Git
3. **Automation**: Run migrations as part of deployment
4. **Rollback Plan**: Always have backward-compatible migrations
5. **Testing**: Test migrations on staging before production

**Alembic Configuration:**
```python
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://user:pass@localhost/warehouse

# Migration file example
"""create sales table
Revision ID: abc123
Revises: 
Create Date: 2023-01-01 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'sales',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('region', sa.String(50), nullable=False)
    )
    
    op.create_index('idx_sales_date', 'sales', ['date'])
    op.create_index('idx_sales_region', 'sales', ['region'])

def downgrade():
    op.drop_table('sales')
```

**Deployment Strategy:**
- Run migrations before deploying new API version
- Use health checks to verify migration success
- Have rollback migrations ready
- Consider zero-downtime migrations for large tables

## 🎭 Scenario-Based Questions

### 25. **The API is experiencing slow response times during business hours. How would you diagnose and fix this?**

**Diagnosis Steps:**
1. **Check Metrics**:
   - Response time percentiles (p95, p99)
   - Database query performance
   - Connection pool usage
   - Memory and CPU usage

2. **Common Causes**:
   - Database connection pool exhaustion
   - Missing indexes on frequently queried tables
   - Inefficient queries (N+1, full table scans)
   - Memory pressure causing garbage collection pauses
   - Network latency between services

3. **Investigation Tools**:
   - Database query logs with `log_min_duration_statement`
   - Application profiling with py-spy or cProfile
   - APM tools (Datadog, New Relic)
   - Database monitoring (pg_stat_statements)

**Fix Strategies:**
1. **Immediate**:
   - Increase connection pool size (if connections are bottleneck)
   - Add missing indexes
   - Implement query caching
   - Scale horizontally (add more API instances)

2. **Long-term**:
   - Query optimization and refactoring
   - Database read replicas for analytical queries
   - Response caching with Redis
   - Asynchronous processing for heavy operations

### 26. **Users report receiving incomplete data from paginated endpoints. What could be causing this?**

**Possible Causes:**
1. **Race Conditions**: Data changing between page requests
2. **Inconsistent Ordering**: Missing ORDER BY clause causing random ordering
3. **Cursor Issues**: Cursor-based pagination with non-unique cursor values
4. **Filter Changes**: Filters applied inconsistently across pages
5. **Data Deletion**: Records deleted between page requests

**Solutions:**
1. **Stable Ordering**:
```sql
-- Always include unique column in ORDER BY
SELECT * FROM sales 
ORDER BY date DESC, id ASC  -- id ensures uniqueness
LIMIT 100 OFFSET 200;
```

2. **Cursor Pagination**: Use immutable cursor values (timestamps with IDs)

3. **Snapshot Isolation**: Use database transactions for consistent reads
```python
@app.get("/api/sales")
def get_sales(page: int = 1, limit: int = 100):
    with db.begin():
        # Transaction ensures consistent view
        return db.query(Sale).order_by(Sale.id).offset((page-1)*limit).limit(limit).all()
```

4. **Client Guidance**: Document pagination behavior and limitations

### 27. **The database connection pool is constantly exhausted. How would you resolve this?**

**Investigation:**
1. **Monitor Metrics**:
   - Connection pool size vs. active connections
   - Connection wait time
   - Query duration
   - Application concurrency

2. **Common Causes**:
   - Pool size too small for traffic
   - Long-running queries holding connections
   - Connection leaks (not closing sessions)
   - Database performance issues

**Solutions:**
1. **Increase Pool Size** (temporary):
```python
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)
```

2. **Optimize Queries**:
   - Add indexes to slow queries
   - Implement query timeouts
   - Use read replicas for analytical queries

3. **Fix Connection Leaks**:
```python
# Use context managers for sessions
def get_data():
    with Session() as session:
        return session.query(...).all()
    
# Or ensure proper cleanup in dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

4. **Implement Connection Pool Monitoring**:
```python
from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "checkout")
def on_checkout(dbapi_conn, connection_record, connection_proxy):
    # Log connection checkout
    logger.debug("Connection checked out", pool_size=connection_proxy.size())

@event.listens_for(Pool, "checkin")
def on_checkin(dbapi_conn, connection_record):
    # Log connection checkin
    logger.debug("Connection checked in")
```

### 28. **How would you handle a breaking schema change in the data warehouse?**

**Strategy:**
1. **Backward Compatibility**:
   - Maintain old and new schemas simultaneously
   - Use API versioning to phase out old schema
   - Implement schema adapters in the API layer

2. **Migration Plan**:
```python
# Schema adapter pattern
def get_sales_data(version: int = 1):
    if version == 1:
        return get_sales_v1()
    elif version == 2:
        return get_sales_v2()
    else:
        raise HTTPException(400, "Unsupported version")

# Database view for backward compatibility
CREATE VIEW sales_v1 AS
SELECT 
    id,
    amount,
    date,
    region,
    NULL as new_column  -- Placeholder for new schema
FROM sales;

CREATE VIEW sales_v2 AS
SELECT 
    id,
    amount,
    date,
    region,
    new_column
FROM sales;
```

3. **Communication**:
   - Notify API consumers well in advance
   - Provide migration guides and tools
   - Maintain deprecated endpoints with sunset headers
   - Monitor usage of old endpoints

4. **Timeline**:
   - Week 1-2: Deploy new schema alongside old
   - Week 3-4: Notify consumers, update documentation
   - Week 5-8: Monitor migration, provide support
   - Week 9-12: Sunset old schema, remove support

## 💻 Practical Exercises

### 29. **Implement a health check endpoint with dependency status.**

**Expected Solution:**
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
import redis
import requests

app = FastAPI()

def get_db_health(db: Session) -> Dict[str, Any]:
    """Check database health"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "latency_ms": 0}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

def get_cache_health() -> Dict[str, Any]:
    """Check Redis cache health"""
    try:
        r = redis.Redis(host="redis", port=6379)
        start = time.time()
        r.ping()
        latency = (time.time() - start) * 1000
        return {"status": "healthy", "latency_ms": latency}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

def get_external_api_health() -> Dict[str, Any]:
    """Check external API dependency"""
    try:
        start = time.time()
        response = requests.get("https://api.external.com/health", timeout=5)
        latency = (time.time() - start) * 1000
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "latency_ms": latency,
            "status_code": response.status_code
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check endpoint"""
    checks = {
        "database": get_db_health(db),
        "cache": get_cache_health(),
        "external_api": get_external_api_health(),
        "service": {"status": "healthy"}  # Self-check
    }
    
    # Determine overall status
    all_healthy = all(check["status"] == "healthy" for check in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks":