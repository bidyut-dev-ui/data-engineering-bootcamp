# Week 13: FastAPI Fundamentals

**Goal**: Learn the core concepts of FastAPI: routes, path parameters, query parameters, request/response models, and automatic API documentation.

## Scenario
You are building a microservice for a product catalog. The service needs to expose RESTful endpoints that other teams can consume. FastAPI provides automatic validation, serialization, and interactive documentation.

## Concepts Covered
1. **Routes**: Defining GET, POST, PUT, DELETE endpoints
2. **Path Parameters**: Dynamic URL segments (e.g., `/items/{item_id}`)
3. **Query Parameters**: Optional filters (e.g., `/items?q=laptop`)
4. **Pydantic Models**: Type-safe request/response validation
5. **Automatic Documentation**: Swagger UI and ReDoc
6. **Type Hints**: Python 3.6+ type annotations for validation

## Structure
- `main.py`: The FastAPI application with multiple endpoints
- `01_tutorial.py`: Step-by-step tutorial script
- `02_advanced.py`: Advanced patterns (optional parameters, validation)

## Instructions

### 1. Setup
Activate your environment:
```bash
cd projects/09_fastapi_basics
source ../00_setup_and_refresher/venv/bin/activate
pip install fastapi uvicorn
```

### 2. Run Tutorial 1: Basic App
Start the development server:
```bash
uvicorn main:app --reload
```

**What You'll See**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### 3. Explore the API

#### Interactive Documentation (Swagger UI)
Open `http://localhost:8000/docs` in your browser.

**What You'll See**:
- All endpoints listed with their methods (GET, POST, PUT)
- "Try it out" buttons to test each endpoint
- Automatic request/response schemas

#### Alternative Documentation (ReDoc)
Open `http://localhost:8000/redoc` for a different view.

### 4. Test the Endpoints

#### Test 1: Root Endpoint
```bash
curl http://localhost:8000/
```
**Expected Output**: `{"Hello":"World"}`

#### Test 2: Path Parameter
```bash
curl http://localhost:8000/items/42
```
**Expected Output**: `{"item_id":42,"q":null}`

#### Test 3: Query Parameter
```bash
curl "http://localhost:8000/items/42?q=laptop"
```
**Expected Output**: `{"item_id":42,"q":"laptop"}`

#### Test 4: POST Request
Using the Swagger UI:
1. Click on `PUT /items/{item_id}`
2. Click "Try it out"
3. Enter `item_id`: 1
4. Enter request body:
   ```json
   {
     "name": "Laptop",
     "price": 999.99,
     "is_offer": true
   }
   ```
5. Click "Execute"

**Expected Output**: `{"item_name":"Laptop","item_id":1}`

### 5. Run Tutorial 2: Advanced Patterns
```bash
uvicorn 02_advanced:app --reload --port 8001
```
Visit `http://localhost:8001/docs` to see:
- Optional parameters with defaults
- Validation (min/max values, string patterns)
- Response models

## Homework / Challenge

### Challenge 1: Extend the API
Modify `main.py`:
1. Add a `DELETE /items/{item_id}` endpoint
2. Add validation: `price` must be > 0
3. Add a `description` field to the `Item` model (optional)

### Challenge 2: Build a User API
Create `03_challenge.py`:
1. Define a `User` model with: `id`, `username`, `email`, `is_active`
2. Create endpoints:
   - `POST /users/` - Create a user
   - `GET /users/{user_id}` - Get user by ID
   - `GET /users/` - List all users (with optional `?skip=0&limit=10`)
3. Store users in a list (in-memory)

### Challenge 3: Validation
Add validation to your User API:
1. `email` must match email format
2. `username` must be 3-20 characters
3. Return proper HTTP status codes (201 for creation, 404 for not found)

## Expected Learning Outcomes
After completing this week, you should be able to:
- ✅ Create a FastAPI application from scratch
- ✅ Define routes with path and query parameters
- ✅ Use Pydantic models for validation
- ✅ Test APIs using Swagger UI
- ✅ Understand automatic documentation generation
