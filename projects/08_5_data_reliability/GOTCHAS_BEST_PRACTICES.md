# Data Reliability Engineering: Gotchas & Best Practices

This guide covers common pitfalls and best practices for building reliable data pipelines with ACID transactions, idempotency, and robust error handling in memory-constrained environments (8GB RAM).

## 🚨 Critical Gotchas

### 1. **Partial Data Ingestion Without Transactions**
```python
# WRONG: Committing each row individually
for row in data:
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", row)
    conn.commit()  # Partial state persists if crash occurs later

# CORRECT: Use atomic transactions
try:
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", data)
    conn.commit()  # All or nothing
except Exception as e:
    conn.rollback()  # Clean rollback on failure
    raise
```

### 2. **Non-Idempotent Pipeline Execution**
```python
# WRONG: Pipeline that fails on re-run
def process_data(data):
    for item in data:
        cursor.execute("INSERT INTO table VALUES (?)", (item,))  # Fails on duplicate keys
    conn.commit()

# CORRECT: Idempotent upsert pattern
def process_data_idempotent(data):
    for item in data:
        cursor.execute("""
            INSERT INTO table (id, value) 
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET value = excluded.value
        """, (item['id'], item['value']))
    conn.commit()
```

### 3. **Missing Error Recovery Mechanisms**
```python
# WRONG: No recovery from mid-pipeline failures
def process_large_file(filename):
    data = read_entire_file(filename)  # Memory explosion risk
    process_all(data)  # If fails, entire process must restart

# CORRECT: Checkpoint-based recovery
def process_large_file_with_checkpoints(filename):
    checkpoint = load_checkpoint()
    for chunk in read_file_in_chunks(filename, start=checkpoint):
        try:
            process_chunk(chunk)
            save_checkpoint(current_position)
        except Exception as e:
            log_error(e)
            # Can resume from checkpoint
            break
```

### 4. **Race Conditions in Concurrent Processing**
```python
# WRONG: Multiple processes updating same data
def update_counter():
    current = get_counter()
    set_counter(current + 1)  # Race condition!

# CORRECT: Atomic database operations
def update_counter_safely():
    cursor.execute("UPDATE counters SET value = value + 1 WHERE id = ?", (counter_id,))
```

## ✅ Best Practices

### 1. **ACID Transaction Design**

**Atomicity Pattern:**
```python
def atomic_operation(data):
    """Execute multiple operations atomically."""
    try:
        # Begin transaction (implicit in most DB drivers)
        cursor.execute("INSERT INTO table1 ...", data['table1'])
        cursor.execute("UPDATE table2 ...", data['table2'])
        cursor.execute("DELETE FROM table3 ...", data['table3'])
        
        # Commit only if all succeed
        conn.commit()
        return True
    except Exception as e:
        # Rollback everything on any failure
        conn.rollback()
        log_error(f"Transaction failed: {e}")
        return False
```

**Isolation Level Selection:**
```sql
-- Choose appropriate isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- Default, balances consistency & performance
-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;  -- Highest consistency, lower performance
-- SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;  -- Fastest, but dirty reads possible
```

### 2. **Idempotent Pipeline Design**

**Idempotent Load Pattern:**
```python
def idempotent_load(data, batch_id):
    """
    Load data idempotently using batch tracking.
    
    Args:
        data: List of records to load
        batch_id: Unique identifier for this load batch
    """
    # Check if batch already processed
    if is_batch_processed(batch_id):
        print(f"Batch {batch_id} already processed, skipping")
        return
    
    # Process with upsert
    for record in data:
        cursor.execute("""
            INSERT INTO target_table (id, value, batch_id)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                value = excluded.value,
                batch_id = excluded.batch_id,
                updated_at = CURRENT_TIMESTAMP
            WHERE target_table.batch_id != excluded.batch_id
        """, (record['id'], record['value'], batch_id))
    
    # Mark batch as processed
    mark_batch_processed(batch_id)
    conn.commit()
```

**Change Data Capture (CDC) Pattern:**
```python
def incremental_load_with_cdc(last_processed_timestamp):
    """
    Load only new/changed records since last run.
    """
    new_records = cursor.execute("""
        SELECT * FROM source_table
        WHERE updated_at > ? OR created_at > ?
        ORDER BY updated_at
    """, (last_processed_timestamp, last_processed_timestamp))
    
    # Process with idempotent upsert
    process_idempotently(new_records)
    
    # Update last processed timestamp
    update_last_processed_timestamp(max_update_time)
```

### 3. **Robust Error Handling & Recovery**

**Retry with Exponential Backoff:**
```python
import time
from datetime import datetime, timedelta

def robust_database_operation(operation_func, max_retries=5, initial_delay=1):
    """Execute database operation with retry logic."""
    delay = initial_delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return operation_func()
        except (OperationalError, InterfaceError) as e:
            last_exception = e
            if "deadlock" in str(e).lower() or "timeout" in str(e).lower():
                print(f"Retryable error on attempt {attempt + 1}: {e}")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                continue
            else:
                raise
        except Exception as e:
            # Non-retryable error
            raise
    
    # All retries exhausted
    raise Exception(f"Operation failed after {max_retries} attempts: {last_exception}")
```

**Deadlock Prevention:**
```sql
-- Always acquire locks in consistent order
-- WRONG: Process A locks table1 then table2, Process B locks table2 then table1
-- CORRECT: Both processes lock tables in same order (table1 then table2)

-- Use lock timeouts
SET lock_timeout = '5s';  -- Fail fast instead of waiting indefinitely

-- Keep transactions short
BEGIN;
-- Do minimal work
COMMIT;  -- Release locks quickly
```

### 4. **Data Quality & Consistency Checks**

**Pre-Load Validation:**
```python
def validate_before_load(data):
    """Validate data quality before loading."""
    errors = []
    
    # Check required fields
    for i, record in enumerate(data):
        if not record.get('id'):
            errors.append(f"Record {i}: Missing required field 'id'")
        
        # Type validation
        if not isinstance(record.get('amount'), (int, float)):
            errors.append(f"Record {i}: Invalid type for 'amount'")
        
        # Business rule validation
        if record.get('amount', 0) < 0:
            errors.append(f"Record {i}: Negative amount not allowed")
    
    if errors:
        raise ValidationError(f"Validation failed: {errors}")
    
    return True
```

**Post-Load Reconciliation:**
```python
def verify_load_completeness(source_count, target_table):
    """Verify all source records were loaded correctly."""
    loaded_count = cursor.execute(f"SELECT COUNT(*) FROM {target_table}").fetchone()[0]
    
    if source_count != loaded_count:
        raise DataLossError(
            f"Data loss detected: Source={source_count}, Loaded={loaded_count}"
        )
    
    # Verify no duplicates
    duplicate_count = cursor.execute(f"""
        SELECT COUNT(*) FROM (
            SELECT id, COUNT(*) as cnt 
            FROM {target_table} 
            GROUP BY id 
            HAVING COUNT(*) > 1
        ) duplicates
    """).fetchone()[0]
    
    if duplicate_count > 0:
        raise DataQualityError(f"Found {duplicate_count} duplicate records")
```

### 5. **Memory-Constrained Processing (8GB RAM)**

**Streaming Processing Pattern:**
```python
def process_large_dataset_streaming(input_file, chunk_size=10000):
    """Process large datasets without loading everything into memory."""
    processed_count = 0
    
    with open(input_file, 'r') as f:
        chunk = []
        for line in f:
            record = parse_line(line)
            chunk.append(record)
            
            if len(chunk) >= chunk_size:
                process_chunk(chunk)
                processed_count += len(chunk)
                chunk = []
                
                # Monitor memory usage
                if get_memory_usage_mb() > 6000:  # Leave 2GB buffer
                    chunk_size = max(1000, chunk_size // 2)
                    print(f"Reducing chunk size to {chunk_size} due to memory pressure")
        
        # Process final chunk
        if chunk:
            process_chunk(chunk)
            processed_count += len(chunk)
    
    return processed_count
```

**Disk Spilling for Large Operations:**
```python
import tempfile
import pandas as pd

def large_join_with_disk_spill(left_data, right_data):
    """Perform large join operations with disk spilling."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write intermediate results to disk
        left_path = os.path.join(tmpdir, 'left.parquet')
        right_path = os.path.join(tmpdir, 'right.parquet')
        
        left_data.to_parquet(left_path)
        right_data.to_parquet(right_path)
        
        # Process in chunks
        result_chunks = []
        for left_chunk in pd.read_parquet(left_path, chunksize=10000):
            for right_chunk in pd.read_parquet(right_path, chunksize=10000):
                joined = pd.merge(left_chunk, right_chunk, on='key')
                result_chunks.append(joined)
        
        return pd.concat(result_chunks, ignore_index=True)
```

### 6. **Monitoring & Observability**

**Pipeline Health Metrics:**
```python
class PipelineMetrics:
    def __init__(self):
        self.start_time = None
        self.records_processed = 0
        self.errors = []
    
    def record_success(self, count=1):
        self.records_processed += count
    
    def record_error(self, error):
        self.errors.append({
            'timestamp': datetime.now(),
            'error': str(error)
        })
    
    def get_summary(self):
        duration = datetime.now() - self.start_time
        return {
            'duration_seconds': duration.total_seconds(),
            'records_processed': self.records_processed,
            'error_count': len(self.errors),
            'throughput': self.records_processed / max(duration.total_seconds(), 1),
            'success_rate': 1.0 - (len(self.errors) / max(self.records_processed, 1))
        }
```

**Alerting on Data Issues:**
```python
def monitor_data_quality_thresholds():
    """Monitor and alert on data quality issues."""
    metrics = calculate_data_quality_metrics()
    
    # Check thresholds
    if metrics['null_rate'] > 0.05:  # More than 5% nulls
        send_alert(f"High null rate: {metrics['null_rate']:.1%}")
    
    if metrics['freshness_hours'] > 24:  # Data older than 24 hours
        send_alert(f"Data freshness issue: {metrics['freshness_hours']} hours")
    
    if metrics['row_count_change'] > 0.2:  # More than 20% change
        send_alert(f"Unusual row count change: {metrics['row_count_change']:.1%}")
```

## 🎯 Key Principles for Data Reliability

### 1. **Design for Failure**
- Assume any component can fail at any time
- Build idempotent processes that can be safely retried
- Implement comprehensive logging for debugging failures

### 2. **Maintain Data Integrity**
- Use database constraints (NOT NULL, UNIQUE, FOREIGN KEY)
- Implement application-level validation
- Regular data quality checks and reconciliation

### 3. **Optimize for Observability**
- Log all significant operations
- Track metrics for performance and quality
- Implement alerting for abnormal conditions

### 4. **Balance Consistency & Performance**
- Choose appropriate isolation levels
- Use optimistic locking when possible
- Implement retry logic for transient failures

### 5. **Plan for Scale**
- Design for incremental processing
- Implement checkpointing for long-running jobs
- Monitor resource usage and adjust accordingly

## 📊 Common Anti-Patterns to Avoid

1. **The "Big Bang" Load**: Loading all data at once without checkpointing
2. **Silent Failures**: Not logging or alerting on errors
3. **Over-optimistic Locking**: Assuming no conflicts will occur
4. **Missing Rollback Plans**: No way to undo partial changes
5. **Hardcoded Configuration**: Cannot adjust behavior without code changes
6. **Ignoring Resource Limits**: Not monitoring memory/CPU usage

## 🔧 Quick Reference

### Transaction Best Practices:
```python
# Good transaction pattern
with conn:
    cursor.execute("...")  # Auto-commits on success, rolls back on exception
    cursor.execute("...")

# Explicit transaction control
try:
    conn.begin()
    # ... operations ...
    conn.commit()
except:
    conn.rollback()
    raise
```

### Idempotency Patterns:
- Use UPSERT (INSERT ... ON CONFLICT ...)
- Track processed batches
- Use idempotent keys (deterministic based on data)
- Implement deduplication logic

### Error Handling Patterns:
- Retry with exponential backoff for transient errors
- Circuit breaker pattern for persistent failures
- Dead letter queues for unprocessable records
- Comprehensive logging with correlation IDs

By following these best practices and avoiding common gotchas, you can build data pipelines that are reliable, maintainable, and production-ready even in resource-constrained environments.