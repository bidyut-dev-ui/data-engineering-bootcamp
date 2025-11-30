import time
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Connection details (Port 5433 as per docker-compose)
DATABASE_URL = "postgresql://user:password@localhost:5433/adv_sql_db"

def wait_for_db(engine):
    print("Waiting for database...")
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            break
        except OperationalError:
            time.sleep(2)

def generate_data(engine):
    print("Generating data...")
    
    with engine.connect() as conn:
        # 1. Create Tables
        conn.execute(text("""
            DROP TABLE IF EXISTS sales;
            DROP TABLE IF EXISTS employees;
            
            CREATE TABLE employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                department VARCHAR(50),
                salary INT
            );
            
            CREATE TABLE sales (
                id SERIAL PRIMARY KEY,
                employee_id INT,
                amount DECIMAL(10, 2),
                sale_date DATE
            );
        """))
        
        # 2. Insert Employees
        departments = ['Sales', 'Marketing', 'Engineering', 'HR']
        employees = []
        for i in range(20):
            name = f"Employee_{i}"
            dept = random.choice(departments)
            salary = random.randint(50000, 150000)
            employees.append({'name': name, 'dept': dept, 'salary': salary})
            
        conn.execute(text("""
            INSERT INTO employees (name, department, salary) 
            VALUES (:name, :dept, :salary)
        """), employees)
        
        # 3. Insert Sales
        sales_data = []
        start_date = datetime(2023, 1, 1)
        for _ in range(1000):
            emp_id = random.randint(1, 20)
            amount = round(random.uniform(100, 5000), 2)
            date = start_date + timedelta(days=random.randint(0, 365))
            sales_data.append({'eid': emp_id, 'amt': amount, 'dt': date})
            
        conn.execute(text("""
            INSERT INTO sales (employee_id, amount, sale_date) 
            VALUES (:eid, :amt, :dt)
        """), sales_data)
        
        conn.commit()
        print("Inserted 20 employees and 1000 sales records.")

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    wait_for_db(engine)
    generate_data(engine)
