# Week 6: Advanced SQL

**Goal**: Master advanced SQL concepts like CTEs (Common Table Expressions) and Window Functions, which are crucial for Data Engineering interviews and complex transformations.

## Concepts Covered
1. **CTEs (`WITH` clauses)**: Making complex queries readable by breaking them into steps.
2. **Window Functions**:
   - `RANK()` / `DENSE_RANK()`: Ranking rows within a group.
   - `LAG()` / `LEAD()`: Accessing previous/next rows (useful for time-series).
   - `ROW_NUMBER()`: Unique numbering.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../05_advanced_sql
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Start Database
We are using port **5433** this time to avoid conflicts with Week 5.
```bash
docker compose up -d
```

### 3. Populate Data
Run the setup script to create tables and generate dummy data:
```bash
python setup_db.py
```

### 4. Run Tutorial
Execute the advanced queries:
```bash
python advanced_queries.py
```
Read the code in `advanced_queries.py` to understand how the SQL works.

### 5. Cleanup
```bash
docker compose down
```

## Homework / Challenge
Create `02_challenge.py`:
1. Write a query using a **Window Function** to calculate the **Running Total** of sales for each employee over time.
   - Hint: `SUM(amount) OVER (PARTITION BY ... ORDER BY ...)`
2. Write a query using a **CTE** to find the **Department** with the highest average employee salary.
