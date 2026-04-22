# FastAPI Interview Questions

## 📋 Overview
This document contains 30+ interview questions covering FastAPI fundamentals, advanced patterns, performance optimization, and production readiness. Questions are categorized by difficulty and include detailed explanations where applicable.

## 🎯 Core Concepts

### 1. **What is FastAPI and how does it differ from Flask/Django?**
**Answer:** FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Key differences:
- **Performance:** Built on Starlette (async) and Pydantic, significantly faster than Flask/Django for API endpoints
- **Type Safety:** Uses Python type hints for automatic data validation, serialization, and documentation
- **Async Support:** Native async/await support out of the box
- **Automatic Documentation:** Generates OpenAPI and Swagger UI automatically
- **Dependency Injection:** Built-in dependency injection system for clean, testable code

### 2. **Explain the role of Pydantic in FastAPI**
**Answer:** Pydantic provides data validation and settings management using Python type annotations. In FastAPI:
- **Request Validation:** Automatically validates incoming request data against Pydantic models
- **Response Serialization:** Converts Python objects to JSON with proper type conversion
- **Documentation Generation:** Type hints become part of the OpenAPI schema
- **Settings Management:** Environment variables and configuration validation

### 3. **What are path parameters, query parameters, and request bodies in FastAPI?**
**Answer:**
- **Path Parameters:** Variables in the URL path (e.g., `/users/{user_id}`) - use for resource identification
- **Query Parameters:** Key-value pairs after `?` in URL (e.g., `?limit=10&offset=0`) - use for filtering, pagination
- **Request Body:** Data sent in POST/PUT/PATCH requests (typically JSON) - use for creating/updating resources

### 4. **How does FastAPI handle async endpoints?**
**Answer:** FastAPI supports both sync and async endpoints. For async:
- Use `async def` for endpoint functions
- Can `await` async functions (database queries, HTTP requests)
- FastAPI runs async endpoints in an event loop (ASGI server like Uvicorn)
- Sync endpoints run in thread pool to avoid blocking

## 🔧 Technical Implementation

### 5. **Write a basic FastAPI endpoint with path and query parameters**
```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None, limit: int = 10):
    return {"item_id": item_id, "q": q, "limit": limit}
```

### 6. **How do you create nested Pydantic models?**
```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    id: int
    name: str
    items: List[Item] = []
```

### 7. **Explain FastAPI's dependency injection system**
**Answer:** FastAPI's dependency injection allows you to declare dependencies that are automatically resolved and injected into path operation functions. Benefits:
- Code reuse and modularity
- Easy testing with mock dependencies
- Automatic resolution of complex dependencies
- Shared logic (authentication, database sessions, etc.)

```python
from fastapi import Depends, FastAPI

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### 8. **How do you handle file uploads in FastAPI?**
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

## 🚀 Performance & Optimization

### 9. **How do you optimize FastAPI for 8GB RAM environments?**
**Answer:**
- **Response Compression:** Enable GzipMiddleware
- **Connection Pooling:** Use async database drivers with connection pools
- **Memory Management:** Stream large responses, avoid loading entire datasets
- **Caching:** Implement response caching with Redis
- **Background Tasks:** Offload heavy processing to background tasks
- **Pagination:** Always implement pagination for list endpoints

### 10. **What are background tasks and when should you use them?**
**Answer:** Background tasks run after returning a response, useful for operations that don't need to complete before responding (email sending, data processing, logging).

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message)

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

### 11. **How do you implement response caching in FastAPI?**
**Answer:** Use cache decorators or middleware:
```python
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = redis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/expensive-operation/")
@cache(expire=60)  # Cache for 60 seconds
async def expensive_operation():
    # Expensive computation here
    return {"result": "computed"}
```

### 12. **Explain middleware in FastAPI and provide an example**
**Answer:** Middleware is code that runs before/after request processing. Common uses: CORS, logging, authentication.

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 🔐 Security & Authentication

### 13. **How do you implement JWT authentication in FastAPI?**
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate credentials
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}
```

### 14. **What security best practices should you follow in FastAPI?**
**Answer:**
- Always use HTTPS in production
- Implement rate limiting
- Validate and sanitize all inputs
- Use environment variables for secrets (never hardcode)
- Implement proper authentication and authorization
- Set security headers (CORS, CSP, HSTS)
- Keep dependencies updated
- Use Pydantic for automatic validation

### 15. **How do you handle CORS in FastAPI?**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allowed methods
    allow_headers=["*"],  # Allowed headers
)
```

## 🧪 Testing & Debugging

### 16. **How do you write tests for FastAPI applications?**
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 9.99}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
```

### 17. **How do you debug FastAPI applications?**
**Answer:**
- Use `uvicorn.run(app, reload=True)` for auto-reload during development
- Enable debug mode: `app = FastAPI(debug=True)`
- Use logging with Python's logging module
- Integrate with debugging tools (pdb, VS Code debugger)
- Use FastAPI's automatic error responses
- Monitor with application performance monitoring (APM) tools

### 18. **What tools can you use for API monitoring and observability?**
**Answer:**
- **Prometheus + Grafana:** For metrics collection and visualization
- **OpenTelemetry:** For distributed tracing
- **Sentry:** For error tracking
- **Logging:** Structured logging with JSON format
- **Health Checks:** `/health` endpoint for monitoring
- **Performance Profiling:** cProfile, py-spy for performance analysis

## 📊 Database Integration

### 19. **How do you integrate SQLAlchemy with FastAPI?**
```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 20. **What are the benefits of using async database drivers?**
**Answer:**
- **Non-blocking I/O:** Don't block the event loop while waiting for database responses
- **Better concurrency:** Handle more simultaneous requests
- **Improved performance:** Especially for I/O-bound operations
- **Compatibility:** Works well with FastAPI's async architecture

Popular async drivers: `asyncpg` (PostgreSQL), `aiomysql` (MySQL), `motor` (MongoDB).

## 🚨 Error Handling

### 21. **How do you create custom exception handlers in FastAPI?**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class CustomException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error: {exc.detail}"},
    )

@app.get("/raise-custom/")
async def raise_custom():
    raise CustomException(detail="Something went wrong")
```

### 22. **What HTTP status codes should you use for different scenarios?**
**Answer:**
- `200 OK`: Successful GET request
- `201 Created`: Successful POST request (resource created)
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request syntax
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Validation error (FastAPI default)
- `500 Internal Server Error`: Server error

## 🔄 Advanced Patterns

### 23. **How do you implement WebSocket endpoints in FastAPI?**
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### 24. **Explain FastAPI's response models and when to use them**
**Answer:** Response models define the structure of response data, providing:
- Automatic serialization
- Documentation generation
- Data filtering (exclude sensitive fields)
- Type validation

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    # Exclude internal fields from response
    class Config:
        exclude = {"internal_id"}

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    # Database query returns dict with all fields
    item = get_item_from_db(item_id)
    return item  # Automatically filtered by response_model
```

### 25. **How do you handle versioning in FastAPI APIs?**
**Answer:**
1. **URL Versioning:** `/v1/users`, `/v2/users`
2. **Header Versioning:** `Accept: application/vnd.api.v1+json`
3. **Query Parameter:** `/users?version=1`
4. **Content Negotiation:** Different response based on Accept header

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/users")
async def get_users(api_version: str = Header("v1")):
    if api_version == "v1":
        return {"users": "v1 response"}
    elif api_version == "v2":
        return {"users": "v2 response"}
```

## 🏗️ Production Deployment

### 26. **How do you deploy FastAPI applications in production?**
**Answer:**
- **ASGI Server:** Use Uvicorn, Hypercorn, or Daphne
- **Process Manager:** Use Gunicorn with Uvicorn workers
- **Containerization:** Docker with multi-stage builds
- **Orchestration:** Kubernetes, Docker Compose
- **Reverse Proxy:** Nginx or Traefik
- **Monitoring:** Prometheus, Grafana, logging
- **CI/CD:** Automated testing and deployment

### 27. **What are the recommended settings for Gunicorn with Uvicorn workers?**
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 50
```

### 28. **How do you implement health checks in FastAPI?**
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    # Check database connection
    # Check external service dependencies
    # Check disk space, memory, etc.
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "services": {
                "database": "connected",
                "cache": "connected",
                "storage": "available"
            }
        }
    )
```

## 🎓 Behavioral & Scenario-Based Questions

### 29. **"You need to build a high-traffic API that processes 10,000 requests per second. How would you architect it with FastAPI?"**
**Answer:**
- Use async endpoints with non-blocking I/O
- Implement connection pooling for databases
- Add caching layer (Redis) for frequent queries
- Use message queue (RabbitMQ/Kafka) for background processing
- Implement rate limiting and circuit breakers
- Deploy with multiple workers behind a load balancer
- Monitor performance metrics and auto-scale based on load

### 30. **"How would you migrate a Flask application to FastAPI?"**
**Answer:**
1. **Incremental Migration:** Start with new endpoints in FastAPI
2. **Route Mapping:** Map Flask routes to FastAPI endpoints
3. **Middleware Conversion:** Convert Flask middleware to FastAPI middleware
4. **Dependency Injection:** Replace Flask's request context with FastAPI dependencies
5. **Testing:** Ensure all tests pass in both frameworks
6. **Performance Testing:** Compare performance before/after migration
7. **Documentation:** Update API documentation (automatically generated in FastAPI)

### 31. **"What would you do if your FastAPI application starts experiencing memory leaks?"**
**Answer:**
1. **Identify:** Use memory profiler (memray, tracemalloc)
2. **Isolate:** Test endpoints individually to find leak source
3. **Common Causes:** Unclosed database connections, circular references, caching without expiration
4. **Fix:** Implement proper resource cleanup, use context managers
5. **Prevent:** Add memory monitoring, set resource limits, implement health checks

### 32. **"Explain how you would implement rate limiting in FastAPI"**
```python
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited-endpoint")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "This is rate limited"}
```

## 📚 Preparation Tips

### 33. **Key Areas to Focus On:**
- **Async Programming:** Understand async/await, event loops
- **Pydantic Models:** Master data validation and serialization
- **Dependency Injection:** Know how to create and use dependencies
- **Database Integration:** SQLAlchemy, async drivers
- **Security:** Authentication, authorization, CORS
- **Testing:** TestClient, mocking dependencies
- **Deployment:** ASGI servers, Docker, Kubernetes

### 34. **Common FastAPI Interview Topics:**
1. Difference between FastAPI and other Python web frameworks
2. Automatic OpenAPI documentation
3. Handling file uploads and downloads
4. WebSocket implementation
5. Background tasks vs Celery
6. Middleware and CORS handling
7. Response models and serialization
8. Error handling and custom exceptions
9. Testing strategies
10. Performance optimization techniques

### 35. **Practice Exercises to Try:**
1. Build a CRUD API with authentication
2. Implement file upload with validation
3. Create a WebSocket chat application
4. Build a rate-limited API
5. Implement database migrations with Alembic
6. Create a monitoring dashboard with health checks
7. Build a microservices architecture with FastAPI
8. Implement caching with Redis
9. Create an API with versioning
10. Build a real-time notification system

## 🔗 Related Resources in This Repository
- `practice_exercises.py` - Hands-on exercises to practice FastAPI concepts
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and best practices
- `main.py` - Example FastAPI application
- `02_advanced.py` - Advanced FastAPI patterns

---
*Last Updated: 2026-04-20*  
*Use these questions to prepare for FastAPI interviews at all levels, from junior to senior positions.*