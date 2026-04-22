# Advanced SQL Interview Questions

This document contains 30+ interview questions covering advanced SQL concepts including CTEs, window functions, recursive queries, and performance optimization. Each question includes a detailed answer and practical examples.

## 📊 Core Concepts

### 1. **What are Common Table Expressions (CTEs) and when should you use them?**

**Answer:**
CTEs (WITH clauses) are temporary named result sets that exist only for the duration of a query. They improve readability and maintainability of complex queries.

**When to use CTEs:**
- Breaking down complex queries into logical steps
- Recursive queries (hierarchical data)
- Reusing the same subquery multiple times
- Improving query readability

**Example:**
```sql
-- Without CTE (hard to read)
SELECT * FROM (
    SELECT customer_id, SUM(amount) as total
    FROM sales 
    GROUP BY customer_id
) t WHERE total > 1000;

-- With CTE (clear and readable)
WITH CustomerTotals AS (
    SELECT customer_id, SUM(amount) as total
    FROM sales 
    GROUP BY customer_id
)
SELECT * FROM CustomerTotals WHERE total > 1000;
```

### 2. **Explain the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()**

**Answer:**
- **ROW_NUMBER()**: Assigns a unique sequential integer to each row within the partition (1, 2, 3, 4...)
- **RANK()**: Assigns rank with gaps when there are ties (1, 2, 2, 4...)
- **DENSE_RANK()**: Assigns rank without gaps when there are ties (1, 2, 2, 3...)

**Example:**
```sql
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;
```

### 3. **What are window frames and how do they work?**

**Answer:**
Window frames define which rows are included in the window function calculation relative to the current row. Common frames:
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (default for ORDER BY)
- `ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING` (7-row sliding window)
- `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (entire partition)

**Example:**
```sql
-- 7-day moving average
SELECT 
    sale_date,
    amount,
    AVG(amount) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ) as moving_avg_7day
FROM sales;
```

## 🔄 Window Functions

### 4. **How do LAG() and LEAD() functions work?**

**Answer:**
- **LAG(column, offset)**: Accesses data from a previous row
- **LEAD(column, offset)**: Accesses data from a following row

**Use cases:**
- Month-over-month growth calculations
- Comparing current value with previous/next
- Time-series analysis

**Example:**
```sql
SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) as mom_growth
FROM monthly_sales;
```

### 5. **Explain the FIRST_VALUE() and LAST_VALUE() functions**

**Answer:**
- **FIRST_VALUE(column)**: Returns the first value in the window frame
- **LAST_VALUE(column)**: Returns the last value in the window frame (careful with default frame!)

**Example:**
```sql
SELECT 
    customer_id,
    order_date,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as first_purchase_amount,
    LAST_VALUE(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as latest_purchase_amount
FROM orders;
```

### 6. **What is the NTILE() function and when would you use it?**

**Answer:**
NTILE(n) divides rows into n approximately equal buckets (quartiles, deciles, percentiles).

**Use cases:**
- Customer segmentation (top 20% by revenue)
- Performance quartiles
- Data distribution analysis

**Example:**
```sql
-- Divide customers into 4 quartiles by total spend
WITH CustomerSpend AS (
    SELECT 
        customer_id,
        SUM(amount) as total_spend
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id,
    total_spend,
    NTILE(4) OVER (ORDER BY total_spend DESC) as spend_quartile
FROM CustomerSpend;
```

## 🔄 Recursive Queries

### 7. **What are recursive CTEs and how do they work?**

**Answer:**
Recursive CTEs allow queries to reference themselves, useful for hierarchical data (org charts, bill of materials).

**Structure:**
1. **Anchor member**: Base case (non-recursive)
2. **Recursive member**: References the CTE itself
3. **Termination condition**: Stops when no more rows returned

**Example:**
```sql
WITH RECURSIVE EmployeeHierarchy AS (
    -- Anchor: Top-level managers (no manager)
    SELECT id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive: Subordinates
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN EmployeeHierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM EmployeeHierarchy ORDER BY level, name;
```

### 8. **How would you find all ancestors of an employee?**

**Answer:**
Use recursive CTE going upward in the hierarchy.

**Example:**
```sql
WITH RECURSIVE Ancestors AS (
    -- Start with the employee
    SELECT id, name, manager_id, 1 as depth
    FROM employees WHERE id = 123
    
    UNION ALL
    
    -- Go up to managers
    SELECT e.id, e.name, e.manager_id, a.depth + 1
    FROM employees e
    JOIN Ancestors a ON e.id = a.manager_id
)
SELECT * FROM Ancestors ORDER BY depth DESC;
```

## ⚡ Performance & Optimization

### 9. **How do you optimize a query with multiple CTEs?**

**Answer:**
1. **Filter early**: Apply WHERE clauses in the earliest possible CTE
2. **Avoid unnecessary columns**: Select only needed columns
3. **Use indexes**: Ensure appropriate indexes on join/where columns
4. **Consider materialization**: Use MATERIALIZED if CTE is referenced multiple times

**Example:**
```sql
-- Optimized: Filter in first CTE
WITH FilteredSales AS (
    SELECT customer_id, amount, sale_date
    FROM sales 
    WHERE sale_date >= '2023-01-01'  -- Early filter!
),
CustomerTotals AS (
    SELECT customer_id, SUM(amount) as total
    FROM FilteredSales
    GROUP BY customer_id
)
SELECT * FROM CustomerTotals WHERE total > 1000;
```

### 10. **What's the performance impact of window functions?**

**Answer:**
Window functions can be memory-intensive but are often more efficient than alternatives:

**Advantages:**
- Avoid self-joins (which are O(n²))
- Process data in single pass
- Leverage indexes on PARTITION BY/ORDER BY columns

**Memory considerations:**
- Large partitions can cause memory pressure
- Use appropriate frame clauses to limit window size
- Monitor with EXPLAIN ANALYZE

### 11. **How do you handle pagination with window functions?**

**Answer:**
Use ROW_NUMBER() or OFFSET/LIMIT with caution.

**Example:**
```sql
-- Efficient pagination with window function
WITH PaginatedData AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY created_at DESC) as row_num
    FROM large_table
    WHERE status = 'active'
)
SELECT * FROM PaginatedData 
WHERE row_num BETWEEN 1001 AND 1100;  -- Page 11 (100 rows per page)
```

## 🎯 Real-World Scenarios

### 12. **How would you calculate running totals?**

**Answer:**
Use SUM() with appropriate window frame.

**Example:**
```sql
SELECT 
    transaction_date,
    amount,
    SUM(amount) OVER (
        ORDER BY transaction_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM transactions;
```

### 13. **How do you find gaps in sequential data?**

**Answer:**
Use LAG() to compare with previous value.

**Example:**
```sql
WITH NumberedRows AS (
    SELECT 
        id,
        LAG(id, 1) OVER (ORDER BY id) as prev_id
    FROM sequential_data
)
SELECT 
    prev_id + 1 as gap_start,
    id - 1 as gap_end
FROM NumberedRows
WHERE id - prev_id > 1;
```

### 14. **How would you deduplicate data using window functions?**

**Answer:**
Use ROW_NUMBER() to identify duplicates.

**Example:**
```sql
WITH RankedDuplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY email, customer_id 
            ORDER BY created_at DESC
        ) as row_num
    FROM customers
)
DELETE FROM customers 
WHERE id IN (
    SELECT id FROM RankedDuplicates WHERE row_num > 1
);
```

## 📈 Advanced Patterns

### 15. **Explain the difference between ROWS and RANGE in window frames**

**Answer:**
- **ROWS**: Physical rows (based on row position)
- **RANGE**: Logical rows (based on column values)

**Example:**
```sql
-- ROWS: 3 rows before current row
SELECT 
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) as avg_rows

-- RANGE: All rows with date within 3 days of current
SELECT 
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date 
        RANGE BETWEEN INTERVAL '3 days' PRECEDING AND CURRENT ROW
    ) as avg_range
FROM daily_sales;
```

### 16. **How do you handle cumulative distribution with window functions?**

**Answer:**
Use CUME_DIST() or PERCENT_RANK().

**Example:**
```sql
SELECT 
    employee_id,
    salary,
    CUME_DIST() OVER (ORDER BY salary) as cumulative_dist,
    PERCENT_RANK() OVER (ORDER BY salary) as percent_rank
FROM employees;
```

## 🛠️ Practical Exercises

### 17. **Write a query to find the second highest salary**

**Answer:**
```sql
WITH RankedSalaries AS (
    SELECT 
        salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
)
SELECT DISTINCT salary
FROM RankedSalaries
WHERE rank = 2;
```

### 18. **Find employees who earn more than their department average**

**Answer:**
```sql
WITH DeptAverages AS (
    SELECT 
        department,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
)
SELECT 
    e.name,
    e.department,
    e.salary,
    da.avg_salary
FROM employees e
JOIN DeptAverages da ON e.department = da.department
WHERE e.salary > da.avg_salary;
```

### 19. **Calculate month-over-month growth percentage**

**Answer:**
```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY month)) * 100.0 / 
        LAG(revenue, 1) OVER (ORDER BY month), 
        2
    ) as growth_percentage
FROM MonthlyRevenue;
```

## 🧠 Problem-Solving Questions

### 20. **You have a table with timestamps. How would you find concurrent sessions?**

**Answer:**
Use window functions to count overlapping intervals.

**Example:**
```sql
WITH SessionEvents AS (
    SELECT 
        session_id,
        start_time as event_time,
        1 as event_type  -- session start
    FROM sessions
    UNION ALL
    SELECT 
        session_id,
        end_time as event_time,
        -1 as event_type  -- session end
    FROM sessions
)
SELECT 
    event_time,
    SUM(event_type) OVER (ORDER BY event_time) as concurrent_sessions
FROM SessionEvents
ORDER BY event_time;
```

### 21. **How would you pivot rows to columns without using PIVOT operator?**

**Answer:**
Use conditional aggregation.

**Example:**
```sql
SELECT 
    customer_id,
    SUM(CASE WHEN product_category = 'Electronics' THEN amount ELSE 0 END) as electronics_sales,
    SUM(CASE WHEN product_category = 'Clothing' THEN amount ELSE 0 END) as clothing_sales,
    SUM(CASE WHEN product_category = 'Books' THEN amount ELSE 0 END) as books_sales
FROM sales
GROUP BY customer_id;
```

## 🚀 Advanced Topics

### 22. **What are lateral joins and when would you use them?**

**Answer:**
LATERAL joins allow subqueries in the FROM clause to reference columns from preceding tables.

**Use cases:**
- Correlated subqueries in FROM clause
- Row-by-row processing
- Complex calculations

**Example:**
```sql
SELECT 
    d.department_name,
    emp.employee_name,
    emp.salary
FROM departments d
CROSS JOIN LATERAL (
    SELECT name as employee_name, salary
    FROM employees e
    WHERE e.department_id = d.id
    ORDER BY salary DESC
    LIMIT 3
) emp;
```

### 23. **Explain the difference between UNION and UNION ALL**

**Answer:**
- **UNION**: Removes duplicates (slower, needs sorting)
- **UNION ALL**: Includes all rows (faster, preserves duplicates)

**Performance tip:** Use UNION ALL unless you specifically need to remove duplicates.

### 24. **How do you optimize recursive CTEs for large hierarchies?**

**Answer:**
1. **Add depth limit**: WHERE level < 10
2. **Use indexes**: On parent-child relationship columns
3. **Consider materialized paths**: Store full path as array
4. **Batch processing**: Process levels in batches

## 📊 Data Analysis Questions

### 25. **How would you calculate median in SQL?**

**Answer:**
Use PERCENTILE_CONT() or manual calculation.

**Example:**
```sql
-- Using window functions
SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
FROM employees;

-- Manual calculation
WITH RankedSalaries AS (
    SELECT 
        salary,
        ROW_NUMBER() OVER (ORDER BY salary) as row_num,
        COUNT(*) OVER () as total_count
    FROM employees
)
SELECT AVG(salary) as median_salary
FROM RankedSalaries
WHERE row_num IN (
    (total_count + 1) / 2,
    (total_count + 2) / 2
);
```

### 26. **How do you perform cohort analysis with SQL?**

**Answer:**
Track groups of users over time.

**Example:**
```sql
WITH FirstPurchases AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
MonthlyActivity AS (
    SELECT 
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        COUNT(DISTINCT o.customer_id) as active_customers
    FROM FirstPurchases fp
    JOIN orders o ON fp.customer_id = o.customer_id
    GROUP BY 1, 2
)
SELECT 
    cohort_month,
    activity_month,
    EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) as months_since_cohort,
    active_customers,
    FIRST_VALUE(active_customers) OVER (
        PARTITION BY cohort_month 
        ORDER BY activity_month
    ) as cohort_size,
    ROUND(active_customers * 100.0 / 
        FIRST_VALUE(active_customers) OVER (
            PARTITION BY cohort_month 
            ORDER BY activity_month
        ), 2) as retention_rate
FROM MonthlyActivity
ORDER BY 1, 2;
```

## 🔧 Technical Deep Dive

### 27. **How does PostgreSQL execute window functions?**

**Answer:**
PostgreSQL processes window functions in these steps:
1. **Filter/Join**: Apply WHERE and JOIN conditions
2. **Partitioning**: Group rows by PARTITION BY columns
3. **Sorting**: Sort within partitions by ORDER BY
4. **Frame calculation**: Apply window frame
5. **Function evaluation**: Calculate window function per row

**Performance implications:**
- Sorting is expensive for large partitions
- Frame calculations can be memory-intensive
- Consider indexes on PARTITION BY/ORDER BY columns

### 28. **What are the limitations of recursive CTEs?**

**Answer:**
1. **Depth limits**: Some databases have recursion depth limits
2. **Performance**: Can be slow for deep hierarchies
3. **Cycle detection**: Must be handled manually
4. **Memory usage**: Can be high for large result sets

**Mitigation strategies:**
- Add depth limits
- Use iterative approaches for very deep hierarchies
- Consider alternative data structures (nested sets, materialized paths)

## 🎯 Behavioral Questions

### 29. **Describe a time you used advanced SQL to solve a complex business problem**

**Answer structure:**
1. **Situation**: Briefly describe the business problem
2. **Task**: What needed to be accomplished
3. **Action**: How you used advanced SQL (specific functions/techniques)
4. **Result**: Business impact and performance improvements

**Example answer:**
"I needed to analyze customer retention for an e-commerce platform. The business wanted to understand how different customer cohorts behaved over time. I used recursive CTEs to track customer cohorts and window functions with RANGE frames to calculate retention rates. This revealed that customers acquired through referral programs had 40% higher 6-month retention, leading to increased investment in referral marketing."

### 30. **How do you stay updated with SQL advancements?**

**Answer:**
- Follow database vendor release notes (PostgreSQL, MySQL, etc.)
- Read SQL blogs and publications
- Participate in database communities
- Experiment with new features in test environments
- Attend conferences and webinars

## 📚 Preparation Tips

### 1. **Practice with Real Data**
- Use sample databases (Northwind, AdventureWorks)
- Create your own datasets with realistic distributions
- Test edge cases and large volumes

### 2. **Understand Execution Plans**
- Learn to read EXPLAIN ANALYZE output
- Identify performance bottlenecks
- Test different query formulations

### 3. **Master Multiple Databases**
- Understand dialect differences
- Know proprietary extensions
- Be aware of performance characteristics

### 4. **Prepare for Whiteboarding**
- Practice writing queries without IDE assistance
- Explain your thought process
- Consider alternative approaches

## 🎓 Key Takeaways

1. **CTEs improve readability** but understand their performance implications
2. **Window functions are powerful** for analytics but need careful partitioning
3. **Recursive CTEs solve hierarchical problems** but require termination conditions
4. **Performance optimization** requires understanding execution plans and indexing
5. **Real-world SQL** combines technical knowledge with business understanding

By mastering these concepts and practicing with real scenarios, you'll be well-prepared for advanced SQL interviews in data engineering roles.