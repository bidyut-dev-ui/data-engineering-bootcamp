import pandas as pd
import random
from datetime import datetime, timedelta

def generate_source_data():
    print("Generating source CSVs...")
    
    # 1. Products (Source System A)
    products = [
        {'id': 101, 'name': 'Laptop', 'cat': 'Electronics', 'price': 1200},
        {'id': 102, 'name': 'Mouse', 'cat': 'Electronics', 'price': 25},
        {'id': 103, 'name': 'Desk', 'cat': 'Furniture', 'price': 300},
        {'id': 104, 'name': 'Chair', 'cat': 'Furniture', 'price': 150},
    ]
    pd.DataFrame(products).to_csv('data/products.csv', index=False)
    print(" - data/products.csv")
    
    # 2. Customers (Source System B)
    customers = []
    for i in range(50):
        customers.append({
            'id': i + 1,
            'name': f"Customer_{i}",
            'region': random.choice(['North', 'South', 'East', 'West']),
            'signup_date': '2023-01-15'
        })
    pd.DataFrame(customers).to_csv('data/customers.csv', index=False)
    print(" - data/customers.csv")
    
    # 3. Sales Transactions (Transactional System)
    transactions = []
    start_date = datetime(2023, 1, 1)
    for i in range(1000):
        transactions.append({
            'txn_id': 10000 + i,
            'cust_id': random.randint(1, 50),
            'prod_id': random.choice([101, 102, 103, 104]),
            'qty': random.randint(1, 5),
            'date': (start_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        })
    pd.DataFrame(transactions).to_csv('data/sales.csv', index=False)
    print(" - data/sales.csv")

if __name__ == "__main__":
    generate_source_data()
