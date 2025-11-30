# Weeks 15-16: Mini-Project 4 - Data API Service

**Goal**: Build a production-ready REST API that serves data from the Data Warehouse you built in Week 8, with proper Dockerization and deployment patterns.

## Scenario
The Data Warehouse is ready, but analysts and dashboards need easy access to the data. Your task is to build a FastAPI service that:
1. Connects to the Postgres Data Warehouse
2. Exposes analytical endpoints (sales by region, top customers, etc.)
3. Runs in Docker for easy deployment
4. Includes proper error handling and logging

## Concepts Covered
1. **Database Integration**: Connecting FastAPI to Postgres
2. **Analytical Queries**: Aggregations, joins, and window functions
3. **Dockerization**: Multi-stage builds, environment variables
4. **Docker Compose**: Orchestrating API + Database
5. **API Design**: RESTful patterns for analytics
6. **Error Handling**: Proper HTTP status codes
7. **Documentation**: Comprehensive API docs

## Structure
- `app/main.py`: Main FastAPI application
- `app/database.py`: Database connection and models
- `app/routers/`: Modular route handlers
    - `sales.py`: Sales analytics endpoints
    - `customers.py`: Customer analytics endpoints
- `Dockerfile`: Production-ready container image
- `docker-compose.yml`: Full stack (API + Warehouse DB)
- `requirements.txt`: Python dependencies
- `tests/`: API tests (optional)

## Instructions

### Week 15: Building the API

#### 1. Setup
Navigate to the folder:
```bash
cd projects/12_data_api_service
source ../00_setup_and_refresher/venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

#### 2. Start the Warehouse Database
First, ensure the warehouse from Week 8 is running:
```bash
cd ../07_warehouse_builder
docker compose up -d
cd ../12_data_api_service
```

**Verify**: The warehouse should be accessible at `localhost:5434`

#### 3. Run the API Locally
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs`

#### 4. Test the Endpoints

**Endpoint 1: Health Check**
```bash
curl http://localhost:8000/health
```
**Expected Output**: `{"status":"healthy","database":"connected"}`

**Endpoint 2: Sales Summary**
```bash
curl http://localhost:8000/api/sales/summary
```
**Expected Output**:
```json
{
  "total_sales": 1234567.89,
  "total_transactions": 1000,
  "average_order_value": 1234.57
}
```

**Endpoint 3: Sales by Region**
```bash
curl http://localhost:8000/api/sales/by-region
```
**Expected Output**:
```json
[
  {"region": "North", "total_sales": 450000.00, "transaction_count": 320},
  {"region": "South", "total_sales": 380000.00, "transaction_count": 275},
  ...
]
```

**Endpoint 4: Top Customers**
```bash
curl "http://localhost:8000/api/customers/top?limit=5"
```
**Expected Output**: Top 5 customers by total spend.

**Endpoint 5: Product Performance**
```bash
curl http://localhost:8000/api/sales/by-product
```
**Expected Output**: Sales breakdown by product category.

### Week 16: Dockerization & Deployment

#### 5. Build the Docker Image
```bash
docker build -t data-api-service .
```

**What Happens**:
- Multi-stage build for smaller image size
- Dependencies installed
- Application code copied
- Non-root user created for security

#### 6. Run with Docker Compose
Stop the local server (Ctrl+C) and run:
```bash
docker compose up --build
```

**What's Different**:
- API runs in a container
- Automatically connects to warehouse DB
- Environment variables managed via docker-compose
- Health checks enabled

Visit `http://localhost:8000/docs` - same API, now containerized!

#### 7. Test the Full Stack
```bash
# Check running containers
docker compose ps

# View API logs
docker compose logs api

# Test the API
curl http://localhost:8000/api/sales/summary
```

#### 8. Cleanup
```bash
docker compose down
```

## API Endpoints Reference

### Sales Analytics
- `GET /api/sales/summary` - Overall sales metrics
- `GET /api/sales/by-region` - Regional breakdown
- `GET /api/sales/by-product` - Product performance
- `GET /api/sales/trends?start_date=2023-01-01&end_date=2023-12-31` - Time series

### Customer Analytics
- `GET /api/customers/top?limit=10` - Top customers by spend
- `GET /api/customers/{customer_id}/history` - Customer purchase history
- `GET /api/customers/by-region` - Customer distribution

### Metadata
- `GET /health` - Service health check
- `GET /api/info` - API version and stats

## Homework / Challenge

### Challenge 1: Add Filtering
Extend `/api/sales/by-region`:
1. Add optional `start_date` and `end_date` query parameters
2. Filter sales within the date range
3. Add validation (end_date must be after start_date)

### Challenge 2: Add Caching
Modify `app/main.py`:
1. Install `pip install cachetools`
2. Cache the `/api/sales/summary` response for 5 minutes
3. Add a `X-Cache-Hit` header to indicate cache status

### Challenge 3: Add Authentication
Create `app/auth.py`:
1. Implement API key authentication
2. Protect all `/api/*` endpoints
3. Add a `X-API-Key` header requirement
4. Return `401 Unauthorized` for invalid keys

### Challenge 4: Add Tests
Create `tests/test_api.py`:
1. Use `pytest` and `httpx`
2. Test each endpoint
3. Mock the database for faster tests
4. Aim for 80%+ code coverage

## Expected Learning Outcomes
After completing Weeks 15-16, you should be able to:
- ✅ Build a production-ready FastAPI service
- ✅ Connect to a Postgres Data Warehouse
- ✅ Design RESTful analytical endpoints
- ✅ Dockerize a Python application
- ✅ Use Docker Compose for multi-service apps
- ✅ Handle errors and edge cases properly
- ✅ Write comprehensive API documentation

## Troubleshooting

**Issue**: Cannot connect to database
- **Solution**: Ensure warehouse is running: `cd ../07_warehouse_builder && docker compose ps`
- Check connection string in `app/database.py`

**Issue**: Docker build fails
- **Solution**: Check `requirements.txt` for typos. Ensure Docker has enough memory (4GB+).

**Issue**: API returns empty data
- **Solution**: Verify warehouse has data: `cd ../07_warehouse_builder && python etl_loader.py`

## Production Considerations
When deploying to production, consider:
1. **Environment Variables**: Never hardcode credentials
2. **Connection Pooling**: Use SQLAlchemy's pool settings
3. **Rate Limiting**: Prevent abuse with `slowapi`
4. **Monitoring**: Add Prometheus metrics
5. **CORS**: Configure allowed origins
6. **HTTPS**: Use reverse proxy (Nginx, Traefik)
