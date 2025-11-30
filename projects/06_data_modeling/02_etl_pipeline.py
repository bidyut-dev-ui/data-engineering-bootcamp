import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "modeling_demo.db"

def populate_3nf(conn):
    print("Populating 3NF tables...")
    cursor = conn.cursor()
    
    # Regions
    regions = ['North America', 'Europe', 'Asia']
    cursor.executemany("INSERT INTO regions (name) VALUES (?)", [(r,) for r in regions])
    
    # Countries
    countries = [('USA', 1), ('Canada', 1), ('UK', 2), ('Germany', 2), ('Japan', 3)]
    cursor.executemany("INSERT INTO countries (name, region_id) VALUES (?, ?)", countries)
    
    # Products
    products = [('Laptop', 'Electronics', 1000), ('Mouse', 'Electronics', 20), ('Chair', 'Furniture', 150)]
    cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)
    
    # Customers
    customers = []
    for i in range(100):
        customers.append((f"Customer_{i}", f"user{i}@mail.com", random.randint(1, 5)))
    cursor.executemany("INSERT INTO customers (name, email, country_id) VALUES (?, ?, ?)", customers)
    
    # Orders & Items
    orders = []
    order_items = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(500):
        cust_id = random.randint(1, 100)
        date = (start_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO orders (customer_id, order_date) VALUES (?, ?)", (cust_id, date))
        order_id = cursor.lastrowid
        
        # Add 1-3 items per order
        for _ in range(random.randint(1, 3)):
            prod_id = random.randint(1, 3)
            qty = random.randint(1, 5)
            order_items.append((order_id, prod_id, qty))
            
    cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", order_items)
    conn.commit()

def etl_to_star_schema(conn):
    print("Running ETL: 3NF -> Star Schema...")
    cursor = conn.cursor()
    
    # 1. Load Dim_Customer (Denormalize Region -> Country -> Customer)
    cursor.execute("""
        INSERT INTO dim_customer (original_id, name, email, country, region)
        SELECT 
            c.id, c.name, c.email, co.name, r.name
        FROM customers c
        JOIN countries co ON c.country_id = co.id
        JOIN regions r ON co.region_id = r.id
    """)
    
    # 2. Load Dim_Product
    cursor.execute("""
        INSERT INTO dim_product (original_id, name, category, current_price)
        SELECT id, name, category, price FROM products
    """)
    
    # 3. Load Dim_Date (Simple generation based on orders)
    cursor.execute("""
        INSERT OR IGNORE INTO dim_date (date_key, full_date, year, month, day_of_week)
        SELECT DISTINCT 
            CAST(strftime('%Y%m%d', order_date) AS INTEGER),
            order_date,
            strftime('%Y', order_date),
            strftime('%m', order_date),
            strftime('%w', order_date)
        FROM orders
    """)
    
    # 4. Load Fact_Sales
    # We need to look up keys from dimensions
    cursor.execute("""
        INSERT INTO fact_sales (customer_key, product_key, date_key, quantity, total_amount)
        SELECT 
            dc.customer_key,
            dp.product_key,
            CAST(strftime('%Y%m%d', o.order_date) AS INTEGER),
            oi.quantity,
            (oi.quantity * dp.current_price)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN dim_customer dc ON o.customer_id = dc.original_id
        JOIN dim_product dp ON oi.product_id = dp.original_id
    """)
    
    conn.commit()

def main():
    conn = sqlite3.connect(DB_NAME)
    populate_3nf(conn)
    etl_to_star_schema(conn)
    print("Data populated and ETL complete.")
    conn.close()

if __name__ == "__main__":
    main()
