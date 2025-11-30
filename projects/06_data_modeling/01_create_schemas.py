import sqlite3
import os

DB_NAME = "modeling_demo.db"

def create_connection():
    return sqlite3.connect(DB_NAME)

def setup_3nf(conn):
    print("Creating 3NF Schema (Normalized)...")
    cursor = conn.cursor()
    
    # 1. Regions
    cursor.execute("CREATE TABLE IF NOT EXISTS regions (id INTEGER PRIMARY KEY, name TEXT)")
    
    # 2. Countries (depends on Regions)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            region_id INTEGER,
            FOREIGN KEY(region_id) REFERENCES regions(id)
        )
    """)
    
    # 3. Customers (depends on Countries)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            email TEXT,
            country_id INTEGER,
            FOREIGN KEY(country_id) REFERENCES countries(id)
        )
    """)
    
    # 4. Products
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)")
    
    # 5. Orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY, 
            customer_id INTEGER, 
            order_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)
    
    # 6. Order Items (Many-to-Many link)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER, 
            product_id INTEGER, 
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    conn.commit()

def setup_star_schema(conn):
    print("Creating Star Schema (Denormalized)...")
    cursor = conn.cursor()
    
    # 1. Dim_Customer (Contains Country and Region info flattened)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_key INTEGER PRIMARY KEY, -- Surrogate Key
            original_id INTEGER,
            name TEXT,
            email TEXT,
            country TEXT,
            region TEXT
        )
    """)
    
    # 2. Dim_Product
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_key INTEGER PRIMARY KEY,
            original_id INTEGER,
            name TEXT,
            category TEXT,
            current_price REAL
        )
    """)
    
    # 3. Dim_Date (Time dimension)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key INTEGER PRIMARY KEY, -- YYYYMMDD
            full_date TEXT,
            year INTEGER,
            month INTEGER,
            day_of_week TEXT
        )
    """)
    
    # 4. Fact_Sales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales (
            id INTEGER PRIMARY KEY,
            customer_key INTEGER,
            product_key INTEGER,
            date_key INTEGER,
            quantity INTEGER,
            total_amount REAL,
            FOREIGN KEY(customer_key) REFERENCES dim_customer(customer_key),
            FOREIGN KEY(product_key) REFERENCES dim_product(product_key),
            FOREIGN KEY(date_key) REFERENCES dim_date(date_key)
        )
    """)
    conn.commit()

def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        
    conn = create_connection()
    setup_3nf(conn)
    setup_star_schema(conn)
    print("Schemas created successfully in 'modeling_demo.db'.")
    conn.close()

if __name__ == "__main__":
    main()
