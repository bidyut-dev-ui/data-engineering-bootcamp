#!/usr/bin/env python3
"""
Generate sample data for PySpark tutorials.

Creates CSV files with realistic data for testing PySpark operations
on 8GB RAM. Files are sized appropriately for memory constraints.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

def create_sales_data(num_rows, filename):
    """Generate sales transaction data."""
    
    print(f"Generating {num_rows:,} sales records...")
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Toys']
    
    # Generate dates (last 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    data = []
    for i in range(1, num_rows + 1):
        transaction_date = start_date + timedelta(days=random.randint(0, 90))
        category = random.choice(categories)
        
        # Price varies by category
        if category == 'Electronics':
            price = round(random.uniform(100, 2000), 2)
        elif category == 'Clothing':
            price = round(random.uniform(20, 300), 2)
        else:
            price = round(random.uniform(10, 500), 2)
        
        quantity = random.randint(1, 5)
        total = round(price * quantity, 2)
        
        # Customer IDs (some repeat for join operations)
        customer_id = random.randint(1, 5000)
        
        data.append({
            'transaction_id': i,
            'customer_id': customer_id,
            'product_id': random.randint(1000, 9999),
            'category': category,
            'price': price,
            'quantity': quantity,
            'total_amount': total,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'region': random.choice(['North', 'South', 'East', 'West']),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'])
        })
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"  Saved to {filename} ({file_size:.2f} MB)")
    
    return df

def create_customer_data(num_rows, filename):
    """Generate customer demographic data."""
    
    print(f"Generating {num_rows:,} customer records...")
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 
                   'Michael', 'Linda', 'William', 'Elizabeth']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
                  'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    data = []
    for i in range(1, num_rows + 1):
        join_date = datetime.now() - timedelta(days=random.randint(0, 1000))
        
        data.append({
            'customer_id': i,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'customer{i}@example.com',
            'join_date': join_date.strftime('%Y-%m-%d'),
            'membership_tier': random.choice(['Basic', 'Silver', 'Gold', 'Platinum']),
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'state': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
            'country': 'USA',
            'total_spent': round(random.uniform(100, 10000), 2),
            'last_purchase_date': (join_date + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"  Saved to {filename} ({file_size:.2f} MB)")
    
    return df

def create_product_data(filename):
    """Generate product catalog data."""
    
    print("Generating product catalog...")
    
    products = [
        {'product_id': 1001, 'product_name': 'Laptop Pro', 'category': 'Electronics', 'supplier': 'TechCorp'},
        {'product_id': 1002, 'product_name': 'Wireless Mouse', 'category': 'Electronics', 'supplier': 'TechCorp'},
        {'product_id': 1003, 'product_name': 'Smartphone X', 'category': 'Electronics', 'supplier': 'MobileInc'},
        {'product_id': 2001, 'product_name': 'T-Shirt', 'category': 'Clothing', 'supplier': 'FashionCo'},
        {'product_id': 2002, 'product_name': 'Jeans', 'category': 'Clothing', 'supplier': 'FashionCo'},
        {'product_id': 2003, 'product_name': 'Jacket', 'category': 'Clothing', 'supplier': 'OutdoorGear'},
        {'product_id': 3001, 'product_name': 'Coffee Maker', 'category': 'Home & Kitchen', 'supplier': 'HomeGoods'},
        {'product_id': 3002, 'product_name': 'Blender', 'category': 'Home & Kitchen', 'supplier': 'HomeGoods'},
        {'product_id': 4001, 'product_name': 'Python Cookbook', 'category': 'Books', 'supplier': 'BookHouse'},
        {'product_id': 4002, 'product_name': 'Data Science Guide', 'category': 'Books', 'supplier': 'BookHouse'},
        {'product_id': 5001, 'product_name': 'Yoga Mat', 'category': 'Sports', 'supplier': 'SportSupply'},
        {'product_id': 5002, 'product_name': 'Dumbbells', 'category': 'Sports', 'supplier': 'SportSupply'},
        {'product_id': 6001, 'product_name': 'Lego Set', 'category': 'Toys', 'supplier': 'ToyWorld'},
        {'product_id': 6002, 'product_name': 'Board Game', 'category': 'Toys', 'supplier': 'ToyWorld'},
    ]
    
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    
    print(f"  Saved to {filename}")
    
    return df

def create_parquet_files():
    """Convert CSV files to Parquet format for performance testing."""
    
    print("\nCreating Parquet versions for performance comparison...")
    
    files_to_convert = [
        ('data/sales_small.csv', 'data/sales_small.parquet'),
        ('data/sales_large.csv', 'data/sales_large.parquet'),
        ('data/customers.csv', 'data/customers.parquet'),
        ('data/products.csv', 'data/products.parquet')
    ]
    
    for csv_file, parquet_file in files_to_convert:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.to_parquet(parquet_file, index=False)
            
            csv_size = os.path.getsize(csv_file) / (1024 * 1024)
            parquet_size = os.path.getsize(parquet_file) / (1024 * 1024)
            
            print(f"  {os.path.basename(csv_file)}: {csv_size:.2f} MB → {parquet_size:.2f} MB "
                  f"({parquet_size/csv_size*100:.1f}% of original)")

def main():
    """Main function to generate all sample data."""
    
    print("="*60)
    print("Generating Sample Data for PySpark Tutorials")
    print("="*60)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate datasets
    print("\n1. Sales Data:")
    sales_small = create_sales_data(10000, 'data/sales_small.csv')      # 10K rows for quick testing
    sales_large = create_sales_data(500000, 'data/sales_large.csv')    # 500K rows for performance testing
    
    print("\n2. Customer Data:")
    customers = create_customer_data(5000, 'data/customers.csv')       # 5K customers
    
    print("\n3. Product Data:")
    products = create_product_data('data/products.csv')                # Small lookup table
    
    # Create Parquet versions
    create_parquet_files()
    
    # Summary
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    
    print("\nGenerated Files:")
    print("  data/sales_small.csv     - 10,000 rows (quick testing)")
    print("  data/sales_large.csv     - 500,000 rows (performance testing)")
    print("  data/customers.csv       - 5,000 rows (join operations)")
    print("  data/products.csv        - 14 rows (lookup table)")
    print("\n  Parquet versions also created for performance comparison")
    
    print("\nTotal Disk Usage:")
    total_size = 0
    for file in ['data/sales_small.csv', 'data/sales_large.csv', 
                 'data/customers.csv', 'data/products.csv']:
        if os.path.exists(file):
            total_size += os.path.getsize(file)
    
    print(f"  CSV files: {total_size / (1024 * 1024):.2f} MB")
    
    print("\n" + "="*60)
    print("Ready for PySpark tutorials!")
    print("="*60)
    print("\nNext: Run 'python 01_pyspark_setup.py' to test your PySpark configuration")

if __name__ == "__main__":
    main()