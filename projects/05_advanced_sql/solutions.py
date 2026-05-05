#!/usr/bin/env python3
"""
Solutions for Advanced SQL Practice Exercises
"""

from sqlalchemy import create_engine, text
import pandas as pd

DATABASE_URL = "postgresql://user:password@localhost:5433/adv_sql_db"
engine = create_engine(DATABASE_URL)

def run_query(query, description):
    print(f"\n--- {description} ---")
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
        print(df.head(10))
        return df

def solution_1_cte():
    query = """
    WITH emp_sales AS (
        SELECT employee_id, SUM(amount) as total_sales
        FROM sales
        GROUP BY employee_id
    ),
    dept_avgs AS (
        SELECT department, AVG(salary) as avg_salary
        FROM employees
        GROUP BY department
    )
    SELECT e.name, e.department, s.total_sales, d.avg_salary
    FROM employees e
    LEFT JOIN emp_sales s ON e.id = s.employee_id
    JOIN dept_avgs d ON e.department = d.department
    WHERE s.total_sales > d.avg_salary OR s.total_sales IS NULL
    """
    run_query(query, "Employees above Dept Avg or No Sales")

def solution_2_ranking():
    query = """
    SELECT name, department, salary,
           RANK() OVER(PARTITION BY department ORDER BY salary DESC) as rank,
           DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) as dense_rank,
           ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) as row_num
    FROM employees
    """
    run_query(query, "Ranking Functions Comparison")

def solution_3_lag_lead():
    query = """
    WITH monthly_sales AS (
        SELECT DATE_TRUNC('month', sale_date) as month, SUM(amount) as sales
        FROM sales
        GROUP BY 1
    )
    SELECT month, sales,
           LAG(sales) OVER(ORDER BY month) as prev_month_sales,
           (sales - LAG(sales) OVER(ORDER BY month)) / LAG(sales) OVER(ORDER BY month) * 100 as growth_pct
    FROM monthly_sales
    """
    run_query(query, "Month-over-Month Growth")

def solution_4_window_agg():
    query = """
    SELECT sale_date, amount,
           SUM(amount) OVER(ORDER BY sale_date) as running_total,
           AVG(amount) OVER(ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
    FROM sales
    LIMIT 20
    """
    run_query(query, "Running Total and Moving Average")

def solution_5_recursive():
    # Note: setup_db doesn't create manager_id, let's mock the logic
    print("\n--- Recursive CTE (Logic Only) ---")
    print("""
    WITH RECURSIVE subordinates AS (
        SELECT id, name, manager_id FROM employees WHERE name = 'CEO'
        UNION ALL
        SELECT e.id, e.name, e.manager_id
        FROM employees e
        INNER JOIN subordinates s ON s.id = e.manager_id
    )
    SELECT * FROM subordinates;
    """)

if __name__ == "__main__":
    try:
        solution_1_cte()
        solution_2_ranking()
        solution_3_lag_lead()
        solution_4_window_agg()
        solution_5_recursive()
    except Exception as e:
        print(f"Error: {e}. Make sure database is running (docker-compose up -d)")
