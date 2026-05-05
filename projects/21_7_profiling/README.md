# Project 21.7: Performance Profiling & Optimization

## Problem Statement
A pipeline that takes 1 hour today might take 10 hours next month as data grows. A Team Lead must be able to find the exact line of code or SQL query that is slow and optimize it.

**The Goal:** Master **Python Profiling** and **SQL Execution Plans**.

## 1. Python Profiling (The Solution)
Use `pyinstrument` to see where your code spends the most time.

### Example: Finding a slow function
```python
# slow_pipeline.py
import time
from pyinstrument import Profiler

def process_heavy():
    # Simulate a slow loop
    data = []
    for i in range(1000000):
        data.append(i * 2)
    return data

profiler = Profiler()
profiler.start()

process_heavy()

profiler.stop()
profiler.print() # Prints a "Flame Graph" of time spent
```

## 2. SQL Execution Plans
**Problem:** A `SELECT` query on a table with 10M rows takes 30 seconds.

**Solution:** Use `EXPLAIN ANALYZE` to see if the database is doing a "Full Table Scan".

```sql
-- Before Optimization
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
-- Result: "Seq Scan on users  (cost=0.00..1234.00 rows=1 width=50) (actual time=29.50..29.50 rows=1 loops=1)"

-- After Optimization (Adding an Index)
CREATE INDEX idx_users_email ON users(email);

EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
-- Result: "Index Scan using idx_users_email on users (cost=0.29..8.30 rows=1 width=50) (actual time=0.01..0.01 rows=1 loops=1)"
```

## 3. Memory Profiling
**Problem:** Your Spark job crashes with "Out of Memory".

**Solution:** Use `memory_profiler` to track peak memory usage.
```python
from memory_profiler import profile

@profile
def load_large_file():
    # Avoid: df = pd.read_csv("huge.csv") 
    # Solution: use chunking
    for chunk in pd.read_csv("huge.csv", chunksize=10000):
        process(chunk)
```

## Exercise
**Problem:** You have a Python script that calls an API for every row in a 1,000,000 row CSV. It's too slow.

**Solution:**
1.  **Batching:** Change the API call to accept 100 IDs at a time.
2.  **Parallelism:** Use `concurrent.futures.ThreadPoolExecutor` to make 10 API calls at the same time instead of 1 by 1.
