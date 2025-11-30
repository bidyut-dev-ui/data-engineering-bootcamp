import sqlite3
import time

DB_NAME = "modeling_demo.db"

def run_query(conn, query, name):
    start = time.time()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    end = time.time()
    print(f"\n--- {name} ---")
    print(f"Time: {(end - start)*1000:.4f} ms")
    print(f"Rows returned: {len(rows)}")
    # print(rows[0] if rows else "No data")

def main():
    conn = sqlite3.connect(DB_NAME)
    
    print("=== Query Comparison: 3NF vs Star Schema ===")
    print("Goal: Calculate Total Sales by Region")
    
    # 1. 3NF Query (Lots of Joins)
    query_3nf = """
        SELECT 
            r.name, 
            SUM(p.price * oi.quantity) as total_sales
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        JOIN customers c ON o.customer_id = c.id
        JOIN countries co ON c.country_id = co.id
        JOIN regions r ON co.region_id = r.id
        GROUP BY r.name
    """
    run_query(conn, query_3nf, "3NF Query (5 Joins)")
    
    # 2. Star Schema Query (Fewer Joins)
    query_star = """
        SELECT 
            dc.region, 
            SUM(fs.total_amount) as total_sales
        FROM fact_sales fs
        JOIN dim_customer dc ON fs.customer_key = dc.customer_key
        GROUP BY dc.region
    """
    run_query(conn, query_star, "Star Schema Query (1 Join)")
    
    conn.close()

if __name__ == "__main__":
    main()
