# Databases & Docker Interview Questions

## 📋 Overview
This document contains interview questions covering Docker, database management, SQLAlchemy, and production database operations for data engineering roles. Questions are organized by difficulty and topic area.

## 🐳 Docker & Containerization

### 1. What is Docker Compose and how does it differ from Dockerfile?
**Answer:** Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file. While Dockerfile defines how to build a single container image, docker-compose.yml defines services, networks, volumes, and their relationships for a complete application stack.

**Follow-up:** When would you use Docker Compose vs Kubernetes?

### 2. How do you ensure database containers are ready before application starts?
**Answer:** Use health checks in docker-compose.yml:
```yaml
services:
  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    depends_on:
      condition: service_healthy
```

### 3. What are Docker volumes and why are they important for databases?
**Answer:** Docker volumes provide persistent storage that survives container restarts. For databases, volumes are critical because:
- Data persists across container lifecycle
- Enables backup and restore operations
- Allows multiple containers to share data
- Improves performance compared to bind mounts

### 4. How would you handle database schema migrations in a Dockerized environment?
**Answer:** Use Alembic with a migration strategy:
1. Include migration scripts in the application image
2. Run migrations as an init container or entrypoint script
3. Use version-controlled migration files
4. Implement rollback capabilities for failed migrations

## 🗄️ Database Connection Management

### 5. Explain connection pooling and its benefits
**Answer:** Connection pooling maintains a cache of database connections that can be reused, reducing:
- Connection establishment overhead (TCP handshake, authentication)
- Memory usage per connection
- Database server load
- Latency for frequent queries

**Example with SQLAlchemy:**
```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)
```

### 6. What happens when connection pool is exhausted?
**Answer:** Symptoms include:
- `TimeoutError` or `ConnectionPoolError`
- Increased latency
- Application threads blocking
- Database connection limits reached

**Solutions:**
- Increase pool size or max_overflow
- Implement connection timeout with retry logic
- Use connection validation (`pool_pre_ping=True`)
- Monitor and alert on pool usage

### 7. How do you handle database connection failures in production?
**Answer:** Implement resilience patterns:
1. **Retry with exponential backoff:** `tenacity` library
2. **Circuit breaker:** Fail fast after repeated failures
3. **Health checks:** Regular connection validation
4. **Fallback:** Read from cache or replica
5. **Graceful degradation:** Return partial data

## 🔧 SQLAlchemy & ORM

### 8. Compare SQLAlchemy Core vs ORM
**Answer:**
- **Core:** Lower-level, SQL expression language, better performance, more control
- **ORM:** Object-relational mapping, easier for CRUD, automatic session management
- **Use Core for:** Complex queries, bulk operations, performance-critical code
- **Use ORM for:** Business logic, rapid development, complex object graphs

### 9. What is the N+1 query problem and how do you solve it?
**Answer:** N+1 occurs when fetching related objects results in many individual queries instead of a single join.

**Problem:**
```python
# Bad: N+1 queries
users = session.query(User).all()
for user in users:
    print(user.orders)  # New query for each user
```

**Solution with eager loading:**
```python
# Good: 1 query with join
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.orders)).all()
```

### 10. How do you implement soft deletes with SQLAlchemy?
**Answer:** Add a `deleted_at` column and filter queries:
```python
class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    
    @hybrid_property
    def is_deleted(self):
        return self.deleted_at is not None
    
    @classmethod
    def filter_active(cls):
        return cls.deleted_at.is_(None)

# Usage
active_users = session.query(User).filter(User.filter_active()).all()
```

## 📊 Transaction Management

### 11. Explain ACID properties with examples
**Answer:**
- **Atomicity:** All operations succeed or all fail (bank transfer)
- **Consistency:** Database moves from one valid state to another (constraints maintained)
- **Isolation:** Concurrent transactions don't interfere (MVCC in PostgreSQL)
- **Durability:** Committed transactions survive crashes (WAL - Write Ahead Logging)

### 12. When would you use savepoints?
**Answer:** Savepoints allow partial rollback within a transaction:
```python
with session.begin():
    # Main transaction
    user = User(name="Alice")
    session.add(user)
    
    # Create savepoint
    savepoint = session.begin_nested()
    try:
        order = Order(user=user, amount=100)
        session.add(order)
        # This can fail without rolling back the entire transaction
        savepoint.commit()
    except:
        savepoint.rollback()
        # User still created, order not created
```

### 13. How do you handle deadlocks?
**Answer:**
1. **Retry logic:** Catch deadlock exceptions and retry
2. **Lock ordering:** Always acquire locks in same order
3. **Shorter transactions:** Reduce lock contention
4. **Isolation levels:** Use READ COMMITTED instead of SERIALIZABLE
5. **Monitoring:** Track deadlock frequency and patterns

## 🚀 Performance & Optimization

### 14. How do you optimize bulk inserts?
**Answer:**
```python
# Bad: Individual inserts
for item in data:
    session.add(Item(**item))

# Good: Bulk insert
session.bulk_insert_mappings(Item, data)
session.commit()

# Better: COPY command for PostgreSQL
from sqlalchemy import text
conn = engine.raw_connection()
cursor = conn.cursor()
cursor.copy_from(file, 'table', sep=',')
```

### 15. What database indexes would you create for an e-commerce schema?
**Answer:**
1. **Customers:** `email` (unique), `created_at` (for analytics)
2. **Products:** `category`, `price` (for filtering), `name` (for search)
3. **Orders:** `customer_id`, `order_date`, `status`
4. **OrderItems:** `order_id`, `product_id` (composite index)

**Considerations:**
- Balance read vs write performance
- Index maintenance overhead
- Covering indexes for frequent queries

### 16. How do you monitor database performance?
**Answer:**
1. **Query logging:** Log slow queries (>100ms)
2. **Explain plans:** Analyze query execution
3. **Connection pool metrics:** Active/idle connections
4. **Table statistics:** Row counts, index usage
5. **System metrics:** CPU, memory, disk I/O

## 🔄 Data Migration & Schema Evolution

### 17. How do you perform zero-downtime schema migrations?
**Answer:** Use expand-contract pattern:
1. **Expand:** Add new column nullable or with default
2. **Migrate:** Backfill data in batches
3. **Contract:** Make column NOT NULL, drop old column
4. **Deploy:** Application code using new schema

**Example adding `discount_percentage`:**
```sql
-- Phase 1: Add nullable column
ALTER TABLE products ADD COLUMN discount_percentage DECIMAL(5,2);

-- Phase 2: Backfill in batches
UPDATE products SET discount_percentage = 0 WHERE discount_percentage IS NULL;

-- Phase 3: Make NOT NULL
ALTER TABLE products ALTER COLUMN discount_percentage SET NOT NULL;
```

### 18. How do you handle data migrations for large tables?
**Answer:**
1. **Batch processing:** Update in chunks of 1000-10000 rows
2. **Off-peak execution:** Schedule during low traffic
3. **Progress tracking:** Log completion percentage
4. **Rollback plan:** Backup before migration
5. **Validation:** Verify data integrity after migration

## 🛡️ Backup & Recovery

### 19. Describe your database backup strategy
**Answer:**
- **Full backups:** Weekly via `pg_dump`
- **Incremental backups:** Daily WAL archiving
- **Offsite storage:** Cloud storage (S3, GCS)
- **Retention policy:** 30 days daily, 12 months monthly
- **Testing:** Regular restore tests
- **Monitoring:** Backup success/failure alerts

### 20. How do you restore from backup with minimal downtime?
**Answer:**
1. **Point-in-time recovery:** Use WAL archiving
2. **Standby replica:** Promote replica to primary
3. **Blue-green deployment:** Restore to separate environment
4. **Data validation:** Verify integrity before cutover

## 🔗 Multi-Database & Integration

### 21. How do you sync data between PostgreSQL and SQLite?
**Answer:**
```python
def sync_postgres_to_sqlite(postgres_engine, sqlite_engine, table_name, chunk_size=1000):
    """Sync data in chunks to manage memory."""
    with postgres_engine.connect() as pg_conn, sqlite_engine.connect() as sqlite_conn:
        # Get total count
        total = pg_conn.execute(f"SELECT COUNT(*) FROM {table_name}").scalar()
        
        # Process in chunks
        for offset in range(0, total, chunk_size):
            data = pg_conn.execute(
                f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}"
            ).fetchall()
            
            # Insert into SQLite
            if data:
                sqlite_conn.execute(
                    f"INSERT OR REPLACE INTO {table_name} VALUES ({','.join(['?']*len(data[0]))})",
                    data
                )
```

### 22. How do you handle database-specific SQL differences?
**Answer:**
1. **Use SQLAlchemy's dialect system:** Abstracts differences
2. **Conditional SQL:** Check database version/type
3. **Common table expressions:** Use standard SQL features
4. **Testing:** Test on all target databases

## 🏭 Production Readiness

### 23. What environment-specific configurations do you need?
**Answer:**
- **Development:** Local Docker, debug logging, sample data
- **Testing:** Isolated databases, fixture data, fast cleanup
- **Staging:** Production-like data, monitoring, load testing
- **Production:** Connection pooling, read replicas, backup, monitoring

### 24. How do you implement database health checks?
**Answer:**
```python
from fastapi import APIRouter, HTTPException
import psycopg2
from sqlalchemy import text

router = APIRouter()

@router.get("/health/database")
async def database_health():
    """Check database connectivity and basic functionality."""
    try:
        with engine.connect() as conn:
            # Simple query to verify connectivity
            result = conn.execute(text("SELECT 1")).scalar()
            
            # Check connection pool stats
            pool = engine.pool
            status = {
                "status": "healthy",
                "connections_active": pool.checkedin(),
                "connections_idle": pool.checkedout(),
                "response_time_ms": 10  # Example metric
            }
            return status
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")
```

### 25. Describe circuit breaker pattern for database connections
**Answer:**
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def execute_query(query, params=None):
    """Execute query with circuit breaker protection."""
    try:
        with engine.connect() as conn:
            return conn.execute(text(query), params or {})
    except OperationalError as e:
        # Counts toward circuit breaker failure threshold
        raise
```

## 💼 Scenario-Based Questions

### 26. "Our application is experiencing slow database performance. How would you investigate?"
**Answer:**
1. **Check monitoring:** Connection pool usage, slow query log
2. **Identify bottlenecks:** `EXPLAIN ANALYZE` on slow queries
3. **Review indexes:** Missing or unused indexes
4. **Check locks:** `pg_locks`, `pg_stat_activity`
5. **System resources:** CPU, memory, disk I/O
6. **Application patterns:** N+1 queries, inefficient ORM usage

### 27. "How would you design a database schema for a ride-sharing app?"
**Answer:**
```sql
-- Core tables
CREATE TABLE users (id SERIAL, name TEXT, email TEXT UNIQUE);
CREATE TABLE drivers (id SERIAL, user_id INT, vehicle_info JSONB);
CREATE TABLE rides (
    id SERIAL,
    rider_id INT,
    driver_id INT,
    start_location GEOGRAPHY,
    end_location GEOGRAPHY,
    status TEXT, -- requested, accepted, in_progress, completed, cancelled
    fare DECIMAL(10,2),
    created_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);
CREATE TABLE payments (id SERIAL, ride_id INT, amount DECIMAL(10,2), status TEXT);

-- Key considerations:
-- 1. Location data indexing (PostGIS for spatial queries)
-- 2. Ride status state machine
-- 3. Payment transaction integrity
-- 4. Driver availability tracking
-- 5. Rating system denormalization
```

### 28. "How do you ensure data consistency across microservices?"
**Answer:**
1. **Saga pattern:** Distributed transactions with compensation
2. **Event sourcing:** Append-only event log
3. **Outbox pattern:** Reliable event publishing
4. **CDC (Change Data Capture):** Debezium for database changes
5. **Idempotent consumers:** Handle duplicate events

## 📈 Memory-Constrained Environments (8GB RAM)

### 29. How do you optimize database operations for 8GB RAM?
**Answer:**
1. **Connection pooling:** Limit pool size (5-10 connections)
2. **Query optimization:** Use `LIMIT`, avoid `SELECT *`
3. **Batch processing:** Process data in chunks
4. **Index carefully:** Each index consumes memory
5. **Monitor memory:** Use `pg_stat_activity`, `pg_buffercache`
6. **Configure PostgreSQL:** `shared_buffers = 2GB`, `work_mem = 64MB`

### 30. What are the signs of memory pressure in a database?
**Answer:**
- **High cache hit ratio dropping:** Increased disk I/O
- **Frequent connection errors:** Can't allocate memory
- **Slow queries:** Memory spills to disk
- **OOM killer activity:** Processes being killed
- **Swap usage:** System using swap space

## 🧪 Testing & Quality

### 31. How do you test database interactions?
**Answer:**
1. **Unit tests:** Mock database layer
2. **Integration tests:** Test container with real database
3. **Migration tests:** Verify upgrade/downgrade paths
4. **Performance tests:** Load testing with realistic data
5. **Data integrity tests:** Constraints, relationships

### 32. What database constraints do you always implement?
**Answer:**
1. **NOT NULL:** Required fields
2. **UNIQUE:** Email, username, business keys
3. **FOREIGN KEY:** Referential integrity
4. **CHECK:** Domain validation (price > 0)
5. **EXCLUDE:** Complex constraints (no overlapping reservations)

## 🔗 Integration with Data Engineering Pipeline

### 33. How does this module integrate with other projects in the bootcamp?
**Answer:**
- **PySpark projects:** Database as source/sink for ETL
- **FastAPI projects:** SQLAlchemy models for REST APIs
- **Airflow projects:** Database operators for workflow
- **AWS projects:** RDS vs local Docker comparison
- **Capstone project:** Production database design

## 📚 Preparation Tips

### Study Resources:
1. **Docker Documentation:** Compose file reference
2. **PostgreSQL Manual:** Configuration, performance tuning
3. **SQLAlchemy Documentation:** ORM, Core, best practices
4. **Alembic Documentation:** Migration strategies
5. **Real-world patterns:** Database design patterns book

### Practice Exercises:
1. Implement connection pooling with different configurations
2. Create and run database migrations
3. Optimize slow queries with EXPLAIN ANALYZE
4. Design schema for a real-world application
5. Implement backup and restore procedures

### Common Pitfalls to Avoid:
1. **No connection pooling:** Creating new connections per query
2. **N+1 queries:** Inefficient ORM usage
3. **Missing indexes:** Full table scans on large tables
4. **Long transactions:** Lock contention
5. **No monitoring:** Blind operations in production

## 🎯 Interview Strategy

### When Asked About Experience:
- Describe specific projects with database challenges
- Mention metrics improved (latency reduced by X%, throughput increased by Y%)
- Discuss trade-offs made in design decisions

### When Asked About Scaling:
- Start with vertical scaling (better hardware)
- Move to read replicas for read-heavy workloads
- Discuss partitioning/sharding for very large datasets
- Mention caching layer (Redis) before database

### When Asked About Debugging:
- Explain systematic approach: monitor → identify → test → fix
- Mention tools used (pg_stat_activity, EXPLAIN, slow query log)
- Discuss collaboration with DevOps/SRE teams

---

*Last Updated: April 2026*  
*Related Files: `practice_exercises.py`, `GOTCHAS_BEST_PRACTICES.md`, `solutions.py`*