# Databases & Docker: Gotchas and Best Practices

## 🚨 Common Gotchas for Database Development with Docker

### 1. **Docker Container Port Conflicts**
**❌ DON'T:**
```bash
# Wrong: Hardcoded ports that might conflict
services:
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"  # Conflicts with local PostgreSQL
```

**✅ DO:**
```bash
# Correct: Use different ports or check availability
services:
  postgres:
    image: postgres:15
    ports:
      - "5433:5432"  # Map container 5432 to host 5433
      
# Or use dynamic port assignment
ports:
  - "5432"  # Let Docker choose host port
```

**Why:** Port conflicts prevent container startup. Always check what's already running on your system.

### 2. **Database Data Persistence**
**❌ DON'T:**
```bash
# Wrong: Data lost when container stops
services:
  postgres:
    image: postgres:15
    # No volume mount - data disappears on container removal
```

**✅ DO:**
```bash
# Correct: Use named volumes for persistence
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:  # Named volume persists across container restarts
```

**Why:** Docker containers are ephemeral. Without volumes, database data is lost when container stops.

### 3. **Connection Pool Exhaustion**
**❌ DON'T:**
```python
# Wrong: Creating new connection for every query
def get_user(user_id):
    engine = create_engine(DATABASE_URL)  # New connection pool
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
    return result.fetchone()  # Connection closed, pool wasted
```

**✅ DO:**
```python
# Correct: Reuse engine with connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Create engine once, reuse globally
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,           # Maximum connections
    max_overflow=10,       # Additional connections allowed
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600      # Recycle connections after 1 hour
)

def get_user(user_id):
    with engine.connect() as conn:  # Reuses pool
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
    return result.fetchone()
```

**Why:** Creating new connections is expensive. Connection pools reuse connections, improving performance.

### 4. **Transaction Isolation Issues**
**❌ DON'T:**
```python
# Wrong: Mixing transaction boundaries
conn = engine.connect()
try:
    conn.execute(text("INSERT INTO users (name) VALUES ('Alice')"))
    # Some other operation that might fail
    external_api_call()  # Could raise exception
    conn.commit()  # Only called if no exception
except:
    conn.rollback()  # Might not be called if exception occurs before
    raise
finally:
    conn.close()  # Connection might be in bad state
```

**✅ DO:**
```python
# Correct: Use context managers for transactions
with engine.begin() as conn:  # Auto-commit/rollback
    conn.execute(text("INSERT INTO users (name) VALUES ('Alice')"))
    # If exception occurs here, transaction auto-rolls back
    external_api_call()
# Auto-commit on successful exit
```

**Why:** Manual transaction management is error-prone. Context managers ensure proper cleanup.

### 5. **N+1 Query Problem**
**❌ DON'T:**
```python
# Wrong: Querying in loop (N+1 queries)
users = session.query(User).all()
for user in users:
    # Separate query for each user's orders
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    user.order_count = len(orders)  # Inefficient!
```

**✅ DO:**
```python
# Correct: Use JOIN or eager loading
from sqlalchemy.orm import joinedload

# Single query with JOIN
users = session.query(User).options(joinedload(User.orders)).all()
for user in users:
    user.order_count = len(user.orders)  # Already loaded

# Or use aggregation in SQL
result = session.query(
    User.id,
    func.count(Order.id).label('order_count')
).join(Order).group_by(User.id).all()
```

**Why:** N+1 queries cause performance issues. Database round-trips are expensive.

### 6. **Docker Compose Network Issues**
**❌ DON'T:**
```python
# Wrong: Using localhost to connect to container
DATABASE_URL = "postgresql://user:pass@localhost:5432/db"  # Won't work
```

**✅ DO:**
```python
# Correct: Use service name as hostname
DATABASE_URL = "postgresql://user:pass@postgres:5432/db"  # 'postgres' is service name

# For external connections (from host machine)
DATABASE_URL = "postgresql://user:pass@localhost:5433/db"  # Use mapped port
```

**Why:** Containers have their own network. `localhost` inside container refers to the container itself, not host.

### 7. **Database Index Misuse**
**❌ DON'T:**
```sql
-- Wrong: Indexing every column
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_updated ON users(updated_at);
-- Too many indexes slow down writes
```

**✅ DO:**
```sql
-- Correct: Index based on query patterns
-- Composite index for common filters
CREATE INDEX idx_users_search ON users(name, email);

-- Index for foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Partial index for active records
CREATE INDEX idx_users_active ON users(id) WHERE active = true;
```

**Why:** Indexes improve read performance but slow down writes. Create indexes strategically based on query patterns.

### 8. **Bulk Insert Memory Issues**
**❌ DON'T:**
```python
# Wrong: Loading all data into memory
data = load_huge_csv("10gb_file.csv")  # Memory explosion!
session.bulk_insert_mappings(User, data)  # Still huge in memory
session.commit()
```

**✅ DO:**
```python
# Correct: Process in chunks
def insert_in_chunks(file_path, chunk_size=1000):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        records = chunk.to_dict('records')
        session.bulk_insert_mappings(User, records)
        session.commit()  # Commit each chunk
        session.expunge_all()  # Clear session to free memory
```

**Why:** Large datasets can exhaust memory. Chunking keeps memory usage bounded.

## 🏆 Best Practices for Database Development

### 1. **Use Environment Variables for Configuration**
```python
import os
from sqlalchemy import create_engine

# Read from environment with defaults
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
```

**Benefit:** Configuration is separated from code, making it easy to switch between environments.

### 2. **Implement Connection Health Checks**
```python
from sqlalchemy import text
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def check_database_health(engine):
    """Check if database is reachable and responsive."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return result.scalar() == 1

# Use in application startup
if not check_database_health(engine):
    logger.error("Database health check failed")
    raise RuntimeError("Cannot connect to database")
```

**Benefit:** Early detection of database issues improves application reliability.

### 3. **Use Alembic for Schema Migrations**
```python
# alembic/versions/001_initial_schema.py
"""Initial schema creation."""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')
```

**Benefit:** Version-controlled, reproducible schema changes with rollback capability.

### 4. **Implement Query Timeout**
```python
from sqlalchemy import event
from sqlalchemy.exc import OperationalError

# Set statement timeout at connection level
@event.listens_for(engine, "connect")
def set_statement_timeout(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET statement_timeout = 30000")  # 30 seconds
    cursor.close()

# Or per-query timeout
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

try:
    result = session.execute(
        text("SELECT * FROM large_table"),
        execution_options={"timeout": 10}  # 10 second timeout
    )
except OperationalError as e:
    if "canceling statement due to statement timeout" in str(e):
        logger.warning("Query timed out")
```

**Benefit:** Prevents long-running queries from blocking database resources.

### 5. **Use Read Replicas for Scaling**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Primary for writes
primary_engine = create_engine(PRIMARY_DB_URL)

# Replicas for reads
replica_engines = [
    create_engine(REPLICA1_DB_URL),
    create_engine(REPLICA2_DB_URL),
]

def get_read_session():
    """Get session for read operations (round-robin replicas)."""
    import random
    engine = random.choice(replica_engines)
    return sessionmaker(bind=engine)()

def get_write_session():
    """Get session for write operations (always primary)."""
    return sessionmaker(bind=primary_engine)()
```

**Benefit:** Distributes read load, improving performance for read-heavy applications.

### 6. **Monitor Database Performance**
```python
import psutil
import time
from sqlalchemy import event

# Track query performance
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 1.0:  # Log slow queries (> 1 second)
        logger.warning(f"Slow query ({total:.2f}s): {statement[:100]}...")
        
    # Track memory usage
    memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
    if memory_mb > 1024:  # Alert if > 1GB
        logger.warning(f"High memory usage: {memory_mb:.0f}MB")
```

**Benefit:** Proactive monitoring helps identify performance issues before they affect users.

### 7. **Secure Database Credentials**
```python
# Use secret management
from cryptography.fernet import Fernet
import os

def encrypt_password(password: str) -> str:
    key = os.getenv("ENCRYPTION_KEY")
    cipher = Fernet(key.encode())
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    key = os.getenv("ENCRYPTION_KEY")
    cipher = Fernet(key.encode())
    return cipher.decrypt(encrypted_password.encode()).decode()

# Store encrypted in environment
os.environ["DB_PASSWORD"] = encrypt_password("my_secret_password")
```

**Benefit:** Protects sensitive credentials from exposure in logs or version control.

### 8. **Implement Connection Retry Logic**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError, InterfaceError

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((OperationalError, InterfaceError))
)
def execute_with_retry(query, params=None):
    """Execute query with automatic retry on connection failures."""
    with engine.connect() as conn:
        return conn.execute(query, params or {})
```

**Benefit:** Handles transient network issues gracefully, improving application resilience.

## 🔧 Performance Tips for 8GB RAM

### Memory Optimization
1. **Limit connection pool size**: 5-10 connections max
2. **Use server-side cursors** for large result sets
3. **Stream query results** instead of loading all at once
4. **Enable query result caching** at application level
5. **Use `fetchmany()`** instead of `fetchall()` for large queries

### Docker Optimization
1. **Set memory limits** in docker-compose:
   ```yaml
   services:
     postgres:
       image: postgres:15
       deploy:
         resources:
           limits:
             memory: 2G  # Limit container memory
   ```
2. **Use `.dockerignore`** to exclude unnecessary files
3. **Enable Docker build cache** for faster rebuilds
4. **Use multi-stage builds** to reduce image size

### Database Optimization
1. **Tune PostgreSQL configuration** for limited memory:
   ```sql
   -- In postgresql.conf
   shared_buffers = 512MB      # 25% of available RAM
   work_mem = 16MB             # Per-operation memory
   maintenance_work_mem = 128MB # For maintenance operations
   ```
2. **Regularly vacuum and analyze** tables
3. **Use partial indexes** for filtered queries
4. **Implement partitioning** for large tables

## 📚 Further Reading

1. **PostgreSQL Documentation**: https://www.postgresql.org/docs/
2. **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
3. **Docker Documentation**: https://docs.docker.com/
4. **"Designing Data-Intensive Applications"** by Martin Kleppmann

---

*Last Updated: 2026-04-19*  
*Next Review: Quarterly*