# FastAPI Database Integration: Gotchas & Best Practices

## Overview
This document covers common pitfalls, optimization techniques, and best practices when integrating FastAPI with databases. Learn from real-world experience to build robust, performant, and maintainable database-backed APIs.

## Critical Gotchas

### 1. **Connection Leaks**
**Problem**: Forgetting to close database connections leads to resource exhaustion.
```python
# ❌ WRONG - Connection never closed
def get_items():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    return cursor.fetchall()  # Connection remains open!

# ✅ CORRECT - Use context managers
def get_items():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        return cursor.fetchall()
```

**Best Practice**: Always use context managers (`with` statements) or ensure `finally` blocks close connections.

### 2. **N+1 Query Problem**
**Problem**: Making separate database queries for each item in a list.
```python
# ❌ WRONG - N+1 queries
books = get_all_books()
for book in books:
    author = get_author(book.author_id)  # Separate query per book

# ✅ CORRECT - Single query with JOIN
SELECT books.*, authors.name 
FROM books 
JOIN authors ON books.author_id = authors.id
```

**Detection**: Monitor query counts in logs. Use SQLAlchemy's `lazy='joined'` or `selectinload()`.

### 3. **Transaction Management Errors**
**Problem**: Partial updates when exceptions occur mid-transaction.
```python
# ❌ WRONG - No transaction rollback
def update_inventory(item_id, quantity):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET quantity = ? WHERE id = ?", (quantity, item_id))
    # If this fails, previous update persists
    update_audit_log(item_id, quantity)  
    conn.commit()
    conn.close()

# ✅ CORRECT - Use transactions with rollback
def update_inventory(item_id, quantity):
    conn = sqlite3.connect('test.db')
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET quantity = ? WHERE id = ?", (quantity, item_id))
        update_audit_log(item_id, quantity)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### 4. **SQL Injection Vulnerabilities**
**Problem**: Concatenating user input into SQL queries.
```python
# ❌ WRONG - SQL injection vulnerability
user_input = "'; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ CORRECT - Parameterized queries
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (user_input,))
```

**Rule**: Never use string formatting for SQL queries. Always use parameterized queries.

### 5. **Blocking Database Calls in Async Endpoints**
**Problem**: Blocking database calls stall the entire event loop.
```python
# ❌ WRONG - Blocking call in async endpoint
@app.get("/items/")
async def read_items():
    items = sync_db_query()  # Blocks event loop
    return items

# ✅ CORRECT - Use async database driver or run in thread pool
@app.get("/items/")
async def read_items():
    loop = asyncio.get_event_loop()
    items = await loop.run_in_executor(None, sync_db_query)
    return items
```

**Better**: Use native async database drivers like `asyncpg`, `aiosqlite`, or async SQLAlchemy.

## Performance Best Practices

### 1. **Connection Pooling**
**Always use connection pooling in production**:
```python
# SQLAlchemy example
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)
```

**Pool Sizing Formula**: 
- `pool_size = (core_count * 2) + effective_spindle_count`
- For SSDs: `pool_size = (core_count * 2)`

### 2. **Query Optimization**
- **Index strategically**: Add indexes on foreign keys, frequently filtered columns, and sort columns.
- **Avoid SELECT ***: Select only needed columns.
- **Use EXPLAIN ANALYZE**: Profile query performance.
- **Batch operations**: Use `executemany()` for bulk inserts.

### 3. **Caching Strategy**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Cache expensive database queries
@app.get("/expensive-query/")
@cache(expire=300)  # Cache for 5 minutes
async def expensive_query():
    return complex_database_operation()
```

**Cache Invalidation**: Use version-based or time-based invalidation for mutable data.

## Database-Specific Considerations

### SQLite
- **File locking**: SQLite uses file-level locking; concurrent writes are limited.
- **WAL mode**: Enable Write-Ahead Logging for better concurrency:
  ```python
  conn.execute("PRAGMA journal_mode=WAL")
  ```
- **Memory database**: Use `:memory:` for testing, but data disappears on connection close.

### PostgreSQL
- **Connection limits**: PostgreSQL has max_connections setting (default 100).
- **Prepared statements**: Use `PREPARE` for repeated queries.
- **JSONB**: Use JSONB for flexible schema, not JSON or TEXT.

### MySQL/MariaDB
- **Transaction isolation**: Default is REPEATABLE READ; consider READ COMMITTED for web apps.
- **Engine selection**: Use InnoDB (supports transactions), not MyISAM.

## Error Handling Patterns

### 1. **Graceful Degradation**
```python
from fastapi import HTTPException
import psycopg2

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    try:
        return get_item_from_db(item_id)
    except psycopg2.OperationalError as e:
        # Database connection error
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable"
        )
    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
```

### 2. **Retry Logic for Transient Errors**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def database_operation_with_retry():
    return risky_database_call()
```

## Security Best Practices

### 1. **Credential Management**
- Never hardcode database credentials
- Use environment variables or secret management services
- Rotate credentials regularly

### 2. **Principle of Least Privilege**
- Database user should have minimal required permissions
- Separate read/write users if possible
- Use different credentials for different environments

### 3. **Input Validation**
```python
from pydantic import BaseModel, constr, conint

class ItemCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    price: conint(gt=0, lt=1000000)
    # Database constraints should mirror validation
```

## Testing Considerations

### 1. **Test Database Isolation**
- Use separate database for testing
- Consider SQLite in-memory database for unit tests
- Use transactions that roll back after each test

### 2. **Factory Pattern for Test Data**
```python
def create_test_item(**kwargs):
    defaults = {
        'name': 'Test Item',
        'price': 9.99,
        'category': 'test'
    }
    defaults.update(kwargs)
    return ItemModel(**defaults)
```

### 3. **Mock External Dependencies**
```python
@pytest.fixture
def mock_db_session(mocker):
    mock_session = mocker.Mock()
    mocker.patch('app.database.get_session', return_value=mock_session)
    return mock_session
```

## Monitoring and Observability

### 1. **Key Metrics to Track**
- Database connection pool usage
- Query execution time (95th and 99th percentiles)
- Error rates by error type
- Transaction rollback rate

### 2. **Slow Query Logging**
```python
# SQLAlchemy event listener for slow queries
from sqlalchemy import event
import time

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.1:  # Log slow queries > 100ms
        logger.warning(f"Slow query: {total:.3f}s - {statement}")
```

## Migration Strategy

### 1. **Version Control for Database Schema**
- Use migration tools (Alembic, Django migrations)
- Never modify production schema directly
- Test migrations on staging first

### 2. **Zero-Downtime Deployments**
- Add columns as NULLABLE first, then populate, then make NOT NULL
- For removing columns: create new column, migrate data, remove old column
- Use feature flags for schema changes

## Conclusion

Building robust FastAPI applications with databases requires attention to:
1. **Resource management** (connections, transactions)
2. **Performance optimization** (query tuning, caching, pooling)
3. **Security** (injection prevention, credential management)
4. **Error handling** (graceful degradation, retries)
5. **Observability** (monitoring, logging)

By following these best practices and avoiding common gotchas, you'll create database-backed APIs that are performant, secure, and maintainable.