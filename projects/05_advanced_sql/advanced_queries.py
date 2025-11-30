from sqlalchemy import create_engine, text
import pandas as pd

DATABASE_URL = "postgresql://user:password@localhost:5433/adv_sql_db"

def run_query(engine, query, title):
    print(f"\n=== {title} ===")
    print(query)
    print("-" * 30)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        print(df)

def main():
    engine = create_engine(DATABASE_URL)
    
    # 1. CTE (Common Table Expression)
    # Calculate total sales per employee, then find those above average.
    cte_query = """
    WITH EmployeeSales AS (
        SELECT 
            e.name, 
            SUM(s.amount) as total_sales
        FROM employees e
        JOIN sales s ON e.id = s.employee_id
        GROUP BY e.name
    ),
    AverageSales AS (
        SELECT AVG(total_sales) as avg_sales FROM EmployeeSales
    )
    SELECT 
        es.name, 
        es.total_sales,
        av.avg_sales
    FROM EmployeeSales es, AverageSales av
    WHERE es.total_sales > av.avg_sales
    ORDER BY es.total_sales DESC;
    """
    run_query(engine, cte_query, "CTE: Top Performing Employees")
    
    # 2. Window Function: RANK()
    # Rank employees by salary within their department
    rank_query = """
    SELECT 
        name, 
        department, 
        salary,
        RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
    FROM employees
    """
    run_query(engine, rank_query, "Window Function: Salary Rank per Dept")
    
    # 3. Window Function: LAG()
    # Compare each sale with the previous sale for the same employee
    lag_query = """
    SELECT 
        employee_id,
        sale_date,
        amount,
        LAG(amount, 1) OVER (PARTITION BY employee_id ORDER BY sale_date) as prev_amount,
        amount - LAG(amount, 1) OVER (PARTITION BY employee_id ORDER BY sale_date) as diff
    FROM sales
    WHERE employee_id = 1
    LIMIT 10;
    """
    run_query(engine, lag_query, "Window Function: LAG (Previous Sale Comparison)")

if __name__ == "__main__":
    main()
