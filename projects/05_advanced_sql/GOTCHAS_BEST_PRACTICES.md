# Advanced SQL: Gotchas & Best Practices

This document covers common pitfalls, performance issues, and best practices for advanced SQL operations, with special attention to 8GB RAM constraints.

## 🚨 Common Gotchas

### 1. **CTE Performance Misconceptions**
```sql
-- Wrong: Assuming CTEs are always materialized (PostgreSQL doesn't materialize by default)
WITH SalesCTE AS (
    SELECT * FROM large_sales_table WHERE year = 2023
)
SELECT * FROM SalesCTE WHERE amount > 1000;
-- This may scan large_sales_table twice in PostgreSQL!

-- Correct: Use materialized CTE if needed (PostgreSQL 12+)
WITH SalesCTE AS MATERIALIZED (
    SELECT * FROM large_sales_table WHERE year = 2023
)
SELECT * FROM SalesCTE WHERE amount > 1000;
```

### 2. **Window Function Memory Explosion**
```sql
-- Wrong: Unbounded window frame on large dataset
SELECT 
    customer_id,
    SUM(amount) OVER (ORDER BY sale_date) -- No PARTITION BY means single huge partition
FROM sales; -- Memory explosion on 8GB RAM!

-- Correct: Use appropriate partitioning
SELECT 
    customer_id,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY sale_date)
FROM sales;
```

### 3. **Recursive CTE Infinite Loops**
```sql
-- Wrong: Missing termination condition
WITH RECURSIVE InfiniteCTE AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM InfiniteCTE -- No termination!
)
SELECT * FROM InfiniteCTE; -- Runs forever

-- Correct: Add termination condition
WITH RECURSIVE SafeCTE AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM SafeCTE WHERE n < 1000 -- Terminates at 1000
)
SELECT * FROM SafeCTE;
```

### 4. **Pivot Operations with Dynamic Columns**
```sql
-- Wrong: Hard-coded columns that may change
SELECT 
    SUM(CASE WHEN month = 'Jan' THEN sales END) as Jan,
    SUM(CASE WHEN month = 'Feb' THEN sales END) as Feb
    -- What about March, April, etc.?
FROM monthly_sales;

-- Correct: Consider dynamic SQL or application-layer pivot
-- Or use JSON/array aggregation
SELECT 
    jsonb_object_agg(month, sales) as monthly_data
FROM monthly_sales
GROUP BY year;
```

### 5. **Correlated Subquery Performance**
```sql
-- Wrong: Correlated subquery scanning entire table for each row
SELECT 
    e.name,
    (SELECT COUNT(*) FROM sales s WHERE s.employee_id = e.id) as sale_count
FROM employees e; -- O(n²) performance!

-- Correct: Use JOIN with aggregation
SELECT 
    e.name,
    COUNT(s.id) as sale_count
FROM employees e
LEFT JOIN sales s ON e.id = s.employee_id
GROUP BY e.id, e.name;
```

## 🏆 Best Practices

### 1. **Query Optimization for 8GB RAM**

#### Memory-Efficient CTEs
```sql
-- Use WHERE clauses early in CTEs
WITH FilteredData AS (
    SELECT * FROM large_table 
    WHERE created_at >= '2023-01-01' -- Filter early!
),
AggregatedData AS (
    SELECT customer_id, SUM(amount) as total
    FROM FilteredData
    GROUP BY customer_id
)
SELECT * FROM AggregatedData WHERE total > 1000;
```

#### Limit Window Function Scope
```sql
-- Process in chunks using partitions
SELECT 
    customer_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY sale_date 
        ROWS BETWEEN 30 PRECEDING AND CURRENT ROW -- 30-day window
    ) as rolling_30day_sum
FROM sales;
```

### 2. **Index Strategy for Advanced Queries**

#### Window Functions
```sql
-- Create composite index for window function performance
CREATE INDEX idx_sales_window ON sales (customer_id, sale_date, amount);
-- This supports: PARTITION BY customer_id ORDER BY sale_date
```

#### Recursive Queries
```sql
-- Index for hierarchical data
CREATE INDEX idx_employee_manager ON employees (manager_id, id);
-- Supports recursive CTEs finding subordinates
```

### 3. **Monitoring Query Performance**

#### Use EXPLAIN ANALYZE
```sql
EXPLAIN (ANALYZE, BUFFERS) 
WITH SalesCTE AS (
    SELECT customer_id, SUM(amount) as total
    FROM sales
    GROUP BY customer_id
)
SELECT * FROM SalesCTE WHERE total > 1000;
```

#### Check Memory Usage
```sql
-- Monitor query memory (PostgreSQL)
EXPLAIN (ANALYZE, VERBOSE, BUFFERS)
SELECT * FROM large_table 
ORDER BY created_at 
LIMIT 1000;
```

### 4. **Data Quality Patterns**

#### Validate Recursive CTEs
```sql
-- Add cycle detection
WITH RECURSIVE EmployeeHierarchy AS (
    SELECT 
        id, 
        name, 
        manager_id,
        1 as depth,
        ARRAY[id] as path
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT 
        e.id,
        e.name,
        e.manager_id,
        eh.depth + 1,
        eh.path || e.id
    FROM employees e
    JOIN EmployeeHierarchy eh ON e.manager_id = eh.id
    WHERE NOT e.id = ANY(eh.path) -- Prevent cycles
)
SELECT * FROM EmployeeHierarchy;
```

#### Handle NULLs in Window Functions
```sql
-- Use COALESCE or IGNORE NULLS
SELECT 
    customer_id,
    sale_date,
    amount,
    LAG(amount, 1, 0) OVER ( -- Default to 0 if no previous
        PARTITION BY customer_id 
        ORDER BY sale_date
    ) as prev_amount
FROM sales;
```

### 5. **Production-Ready Patterns**

#### Time-Series Analysis
```sql
-- Efficient time-series with date bins
WITH TimeSeries AS (
    SELECT 
        date_trunc('day', sale_date) as day,
        customer_id,
        SUM(amount) as daily_total
    FROM sales
    WHERE sale_date >= NOW() - INTERVAL '90 days'
    GROUP BY 1, 2
)
SELECT 
    day,
    customer_id,
    daily_total,
    AVG(daily_total) OVER (
        PARTITION BY customer_id
        ORDER BY day
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as weekly_moving_avg
FROM TimeSeries;
```

#### Cohort Analysis
```sql
-- Memory-efficient cohort analysis
WITH FirstPurchases AS (
    SELECT 
        customer_id,
        MIN(sale_date) as first_purchase_date,
        DATE_TRUNC('month', MIN(sale_date)) as cohort_month
    FROM sales
    GROUP BY customer_id
),
MonthlyActivity AS (
    SELECT 
        fp.cohort_month,
        DATE_TRUNC('month', s.sale_date) as activity_month,
        COUNT(DISTINCT s.customer_id) as active_customers
    FROM FirstPurchases fp
    JOIN sales s ON fp.customer_id = s.customer_id
    GROUP BY 1, 2
)
SELECT 
    cohort_month,
    activity_month,
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) as months_since_cohort,
    active_customers
FROM MonthlyActivity
ORDER BY 1, 2;
```

## ⚡ Performance Tips for 8GB RAM

### 1. **Batch Large Operations**
```sql
-- Process in batches instead of all at once
DO $$
DECLARE
    batch_size INT := 10000;
    offset_val INT := 0;
BEGIN
    LOOP
        WITH BatchCTE AS (
            SELECT * FROM large_table
            ORDER BY id
            LIMIT batch_size OFFSET offset_val
        )
        -- Process batch
        PERFORM process_batch_data((SELECT array_agg(id) FROM BatchCTE));
        
        offset_val := offset_val + batch_size;
        EXIT WHEN NOT EXISTS (SELECT 1 FROM large_table WHERE id > offset_val);
    END LOOP;
END $$;
```

### 2. **Use Temporary Tables for Complex Queries**
```sql
-- Create temp table for intermediate results
CREATE TEMPORARY TABLE temp_sales_summary AS
SELECT customer_id, SUM(amount) as total_sales
FROM sales
GROUP BY customer_id;

-- Use temp table in subsequent queries
SELECT * FROM temp_sales_summary WHERE total_sales > 1000;

-- Clean up
DROP TABLE temp_sales_summary;
```

### 3. **Optimize Join Order**
```sql
-- Put smallest table first in joins
SELECT *
FROM small_table s  -- Small table first
JOIN large_table l ON s.id = l.small_id
WHERE l.created_at >= '2023-01-01';
```

### 4. **Avoid SELECT ***
```sql
-- Select only needed columns
SELECT 
    customer_id,
    sale_date,
    amount
FROM sales
WHERE sale_date >= '2023-01-01';
-- Instead of: SELECT * FROM sales
```

## 🔍 Debugging Tips

### 1. **Check Query Plan**
```bash
# Use pg_stat_statements to identify slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 2. **Monitor Memory Usage**
```sql
-- Check current memory usage
SELECT 
    pid,
    query,
    state,
    usename,
    now() - query_start as duration,
    pg_size_pretty(pg_total_relation_size(relid)) as relation_size
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;
```

### 3. **Test with EXPLAIN**
```sql
-- Compare different query formulations
EXPLAIN SELECT * FROM table1 WHERE id IN (SELECT id FROM table2);
EXPLAIN SELECT * FROM table1 WHERE EXISTS (SELECT 1 FROM table2 WHERE table2.id = table1.id);
```

## 📚 Learning Resources

1. **PostgreSQL Documentation**: Window Functions, CTEs, Performance
2. **Use The Index, Luke**: SQL indexing guide
3. **Modern SQL**: Window functions and CTEs in detail
4. **SQL Performance Explained**: Book by Markus Winand

## 🎯 Key Takeaways

1. **CTEs are not always materialized** - Understand your database's behavior
2. **Window functions need careful partitioning** - Avoid single huge partitions
3. **Recursive CTEs need termination conditions** - Prevent infinite loops
4. **Monitor memory usage** - Critical for 8GB RAM systems
5. **Use appropriate indexes** - Especially for window functions and recursive queries
6. **Test with EXPLAIN ANALYZE** - Always verify query plans
7. **Batch large operations** - Process data in manageable chunks
8. **Select only needed columns** - Reduce memory footprint

By following these best practices and avoiding common gotchas, you can write efficient, production-ready advanced SQL queries that perform well even within 8GB RAM constraints.