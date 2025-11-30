# Week 8.5: Data Reliability Engineering

**Goal**: Learn to build pipelines that don't break when things go wrong.

## Scenario
You are building a payment processing pipeline. If the script crashes halfway, you cannot afford to have "half-processed" payments. You also need to be able to re-run the script safely without double-charging users.

## Concepts Covered
1. **ACID Transactions**:
   - **Atomicity**: All or nothing.
   - **Consistency**: Database rules are enforced.
   - **Isolation**: Transactions don't interfere.
   - **Durability**: Saved data survives power loss.
2. **Idempotency**: The property that `f(x) = f(f(x))`. Running the pipeline twice produces the same result as running it once.
3. **Upsert**: "Update if exists, Insert if new".

## Instructions

### 1. Setup
```bash
cd projects/08_5_data_reliability
python setup_db.py
```

### 2. The Problem (Unreliable Ingest)
Run the script that simulates a crash without transactions.
```bash
python 01_unreliable_ingest.py
```
**Observation**: The script crashes after inserting 2 users. The database is left in a "partial" state. If you try to run it again, it will fail with `UNIQUE constraint failed`.

### 3. The Solution (Robust Ingest)
Reset the database and run the robust version.
```bash
python setup_db.py
python 02_robust_ingest.py
```
**Observation**:
1. **Run 1**: Script crashes, but **ROLLBACK** happens. Database remains empty (Clean state).
2. **Run 2**: Script runs successfully. All 3 users inserted.
3. **Run 3**: Script runs *again* with same data. **Idempotency** handles it (no errors, no duplicates).

## Deep Dive

### **Transactions (The "A" in ACID)**
```python
try:
    # Do work...
    cursor.execute(...)
    cursor.execute(...)
    conn.commit() # Save everything
except:
    conn.rollback() # Undo everything
```

### **Idempotency (The "Safe Re-run")**
Never assume your script runs only once. Airflow might retry it.
**Pattern**:
```sql
INSERT INTO table (...) VALUES (...)
ON CONFLICT (id) DO UPDATE ...
```

## Interview Questions

**Q: What is the difference between TRUNCATE and DELETE?**
A: `DELETE` scans and deletes rows one by one (transactional, slower). `TRUNCATE` drops the data pages (DDL, faster, cannot be rolled back in some DBs).

**Q: How do you handle duplicate data arriving in your pipeline?**
A: Use an Idempotent ingestion strategy (Upsert/Merge), or land data in a staging table and deduplicate before loading to the main table.

**Q: What is a "Race Condition"?**
A: When two processes try to modify the same data at the same time, leading to unpredictable results. Solved by Locking or Isolation Levels.

## Homework / Challenge
1. Modify `02_robust_ingest.py` to read from a CSV file instead of a hardcoded list.
2. Add a `processed_at` timestamp column to the table and update it on upsert.
