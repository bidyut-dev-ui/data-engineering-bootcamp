# FastAPI Gotchas & Best Practices for 8GB RAM Environments

## 🚨 Common Gotchas in FastAPI Development

### 1. **Memory Leaks with Large Response Objects**
```python
# ❌ WRONG: Returning entire database in single response
@app.get("/items")
def get_all_items():
    items = db.query(Item).all()  # Could load millions of rows!
    return items

# ✅ CORRECT: Use pagination and streaming
@app.get("/items")
def get_items(skip: int = 0, limit: int = 100):
    items = db.query(Item).offset(skip).limit(limit).all()
    return {"items": items, "pagination": {"skip": skip, "limit": limit}}
```

### 2. **Blocking I/O Operations in Async Endpoints**
```python
# ❌ WRONG: Blocking I/O in async endpoint
@app.get("/data")
async def get_data():
    result = heavy_sync_operation()  # Blocks event loop!
    return result

# ✅ CORRECT: Use thread pool for blocking operations
@app.get("/data")
async def get_data():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, heavy_sync_operation)
    return result
```

### 3. **Missing Response Models Leading to Data Exposure**
```python
# ❌ WRONG: Returning full User object with password
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # Includes password hash!

# ✅ CORRECT: Use response_model to exclude sensitive fields
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

### 4. **Infinite Recursion with Pydantic Models**
```python
# ❌ WRONG: Circular reference causes recursion
class User(BaseModel):
    id: int
    posts: List["Post"]  # Circular reference
    
class Post(BaseModel):
    id: int
    author: User  # Circular reference!

# ✅ CORRECT: Use separate models for relationships
class UserBase(BaseModel):
    id: int
    username: str

class PostResponse(BaseModel):
    id: int
    author_id: int  # Reference only ID, not full object
```

### 5. **Validation Overhead with Large Nested Models**
```python
# ❌ WRONG: Deeply nested validation on every request
class DeepNested(BaseModel):
    level1: List[Dict[str, List[Dict[str, Any]]]]  # Very expensive!

# ✅ CORRECT: Flatten structures or validate incrementally
@app.post("/data")
async def process_data(data: List[Dict[str, Any]]):
    # Validate in chunks
    chunk_size = 100
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        # Process chunk
```

## 🏆 Best Practices for Production FastAPI

### 1. **Dependency Injection for Testability**
```python
# ✅ GOOD: Injectable dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### 2. **Proper Error Handling**
```python
# ✅ GOOD: Comprehensive error handling
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "path": request.url.path,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 3. **Memory-Efficient File Uploads**
```python
# ✅ GOOD: Stream large files to avoid memory issues
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Process in chunks
    chunk_size = 1024 * 1024  # 1MB chunks
    total_size = 0
    
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total_size += len(chunk)
        # Process chunk immediately
        process_chunk(chunk)
    
    return {"filename": file.filename, "size": total_size}
```

### 4. **Response Compression for Large Payloads**
```python
# ✅ GOOD: Enable compression for large responses
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses > 1KB
```

### 5. **Connection Pooling for Database**
```python
# ✅ GOOD: Efficient connection management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure for 8GB RAM
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Small pool for memory constraints
    max_overflow=10,       # Allow some overflow
    pool_recycle=300,      # Recycle connections every 5 minutes
    pool_pre_ping=True     # Check connections before using
)
```

## ⚡ Performance Optimization for 8GB RAM

### 1. **Response Caching Strategy**
```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

# Use LRU cache with size limit
@lru_cache(maxsize=128)
def get_cached_data(key: str):
    return expensive_operation(key)

# Or use FastAPI-Cache with Redis/Memcached for production
@app.get("/expensive")
@cache(expire=60)  # Cache for 60 seconds
def expensive_endpoint():
    return compute_expensive_result()
```

### 2. **Memory Monitoring Middleware**
```python
import psutil
import os
from fastapi import Request
from fastapi.responses import JSONResponse

@app.middleware("http")
async def memory_monitor(request: Request, call_next):
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    response = await call_next(request)
    
    memory_after = process.memory_info().rss / 1024 / 1024
    memory_used = memory_after - memory_before
    
    # Add header for monitoring
    response.headers["X-Memory-Used-MB"] = str(round(memory_used, 2))
    
    # Log if memory usage is high
    if memory_used > 100:  # 100MB threshold
        logger.warning(f"High memory usage: {memory_used}MB for {request.url.path}")
    
    return response
```

### 3. **Chunked Responses for Large Datasets**
```python
from fastapi.responses import StreamingResponse
import json

@app.get("/large-dataset")
async def get_large_dataset():
    async def generate():
        # Stream data in chunks
        for chunk in get_data_in_chunks(chunk_size=1000):
            yield json.dumps(chunk) + "\n"
    
    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"  # Newline-delimited JSON
    )
```

### 4. **Background Tasks for Heavy Processing**
```python
from fastapi import BackgroundTasks

def process_data_async(data: dict):
    # Heavy processing that doesn't block response
    time.sleep(5)  # Simulate processing
    save_to_database(data)

@app.post("/process")
async def process_request(
    data: dict,
    background_tasks: BackgroundTasks
):
    # Return immediately, process in background
    background_tasks.add_task(process_data_async, data)
    return {"status": "processing", "job_id": "123"}
```

## 🔧 Configuration for 8GB RAM

### 1. **Uvicorn Worker Settings**
```bash
# Optimal for 8GB RAM
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2 \           # 2 workers for 8GB RAM
  --limit-concurrency 100 \ # Limit concurrent requests
  --timeout-keep-alive 30 \ # Close idle connections
  --log-level info
```

### 2. **Database Connection Pool Settings**
```python
# SQLAlchemy configuration for 8GB RAM
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Small pool
    max_overflow=10,       # Limited overflow
    pool_recycle=300,      # Recycle connections
    pool_pre_ping=True,
    echo=False             # Disable SQL logging in production
)
```

### 3. **Middleware Configuration**
```python
app = FastAPI()

# Add only necessary middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## 🐛 Debugging Common Issues

### 1. **High Memory Usage**
```python
# Debug memory usage
import tracemalloc

tracemalloc.start()

# ... your code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 memory consumers ]")
for stat in top_stats[:10]:
    print(stat)
```

### 2. **Slow Response Times**
```python
# Add timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    if process_time > 1.0:  # Log slow requests
        logger.warning(f"Slow request: {request.url.path} took {process_time:.2f}s")
    
    return response
```

### 3. **Connection Pool Exhaustion**
```python
# Monitor connection pool
from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug(f"Connection checked out: {connection_record.info}")

@event.listens_for(Pool, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    logger.debug(f"Connection checked in: {connection_record.info}")
```

## 📚 Learning Path

### From This Module:
1. **Basic FastAPI Setup** → RESTful API design
2. **Pydantic Models** → Data validation and serialization  
3. **Dependency Injection** → Clean architecture
4. **Error Handling** → Production-ready APIs
5. **Performance Optimization** → Scalable applications

### To Next Modules:
- **10_fastapi_db** → Database integration with FastAPI
- **19_secure_api** → Authentication and security
- **20_tested_pipeline** → Testing FastAPI applications
- **21_monitored_platform** → Monitoring and observability

## 🎯 Key Takeaways for Interviews

1. **Always use response models** to control what data gets exposed
2. **Implement proper error handling** with custom exceptions
3. **Use dependency injection** for testability and clean architecture
4. **Optimize for memory constraints** with pagination, streaming, and caching
5. **Monitor performance metrics** in production (response time, memory usage)
6. **Document your API** using FastAPI's automatic OpenAPI generation
7. **Implement security best practices** (CORS, rate limiting, input validation)