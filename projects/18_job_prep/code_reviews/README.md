# Task 3.2: Code Review Exercises for Team Leads

## Problem Statement
A Team Lead must be able to spot performance, security, and maintainability issues in a Pull Request (PR) in under 5 minutes.

## PR for Review: "Add Sales Processing Logic"
**Junior Engineer's Code:**
```python
import pandas as pd
import sqlite3

def process_sales(filepath):
    # Load all data into memory
    df = pd.read_csv(filepath)
    
    # Connect to DB
    conn = sqlite3.connect("prod.db")
    
    # Loop through rows and insert
    for index, row in df.iterrows():
        query = f"INSERT INTO sales VALUES ({row['id']}, '{row['name']}', {row['amount']})"
        conn.execute(query)
        
    conn.commit()
    conn.close()
```

---

## 🚩 The Solution (Your Review Comments)

1.  **Security Risk (SQL Injection):** 
    - *Comment:* "CRITICAL: Never use f-strings for SQL queries. This is vulnerable to SQL injection. Use parameterized queries: `conn.execute('INSERT INTO sales VALUES (?, ?, ?)', (row['id'], ...))`."

2.  **Performance Bottleneck (Looping):**
    - *Comment:* "Avoid `iterrows()` for database inserts. It's extremely slow for large datasets. Use `df.to_sql('sales', conn, if_exists='append', index=False)` for a bulk insert."

3.  **Memory Management:**
    - *Comment:* "On our 8GB RAM machines, loading a large CSV at once might crash the pod. Consider using `pd.read_csv(filepath, chunksize=1000)` to process data in batches."

4.  **Error Handling:**
    - *Comment:* "What happens if the CSV is missing? Wrap this in a `try...except` block or use a context manager for the DB connection to ensure it closes even if an error occurs."

## Exercise
**Problem:** A PR adds a hardcoded API key: `API_KEY = "12345-abcde"`.

**Solution:**
- *Review Comment:* "Security violation: Please remove the hardcoded API key. Move this to an environment variable and access it via `os.getenv('MY_API_KEY')`. Update our `.env.example` file accordingly."
