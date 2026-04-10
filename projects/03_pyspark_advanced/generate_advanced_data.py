#!/usr/bin/env python3
"""
Advanced PySpark Data Generator

Creates comprehensive datasets for testing advanced PySpark features:
- Catalyst Optimizer demonstrations
- Memory management scenarios
- Join strategies with skew
- ML pipeline training data
- Streaming analytics with timestamps
- API integration test data

Optimized for 8GB RAM with appropriate data sizes.
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
import random
import time
from pathlib import Path

def create_transactions_large(num_rows=500000, filename="data/transactions_large.csv"):
    """
    Create large transaction dataset for Catalyst optimizer testing.
    Includes various data types and patterns for optimization demonstrations.
    """
    print(f"Generating {num_rows:,} large transaction records...")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Product categories with different price ranges
    categories = {
        'Electronics': (100, 5000),
        'Clothing': (20, 500),
        'Home & Kitchen': (30, 800),
        'Books': (10, 100),
        'Sports': (50, 1500),
        'Toys': (15, 300),
        'Groceries': (5, 200),
        'Automotive': (100, 10000)
    }
    
    # Regions with different sales patterns
    regions = ['North', 'South', 'East', 'West', 'Central', 'International']
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']
    
    # Generate dates (last 2 years for time-series analysis)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    data = []
    for i in range(1, num_rows + 1):
        transaction_date = start_date + timedelta(days=random.randint(0, 730))
        category = random.choice(list(categories.keys()))
        min_price, max_price = categories[category]
        
        # Introduce some patterns for optimization demonstrations
        # 1. Some customers have predictable patterns (for predicate pushdown)
        customer_id = random.randint(1, 10000)
        
        # 2. Create some NULL values for null handling demonstrations
        region = random.choice(regions + [None] * 2)  # 1/3 chance of NULL
        
        # 3. Create some duplicate transactions (for deduplication testing)
        amount = round(random.uniform(min_price, max_price), 2)
        if i % 1000 == 0:  # Create some duplicates
            amount = data[-1]['amount'] if data else amount
        
        # 4. Create skewed data for join optimization
        if i % 10000 == 0:
            customer_id = 9999  # Highly frequent customer
        
        quantity = random.randint(1, 10)
        total = round(amount * quantity, 2)
        
        # 5. Create some outlier values for statistical analysis
        if i % 5000 == 0:
            amount = round(random.uniform(5000, 10000), 2)  # Large transaction
        
        data.append({
            'transaction_id': f"TXN-{i:08d}",
            'customer_id': f"CUST-{customer_id:05d}",
            'product_id': f"PROD-{random.randint(1000, 9999):04d}",
            'category': category,
            'amount': amount,
            'quantity': quantity,
            'total_amount': total,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'transaction_timestamp': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'region': region,
            'payment_method': random.choice(payment_methods),
            'discount_applied': random.choice([True, False]),
            'returned': random.random() < 0.05,  # 5% return rate
            'fraud_flag': random.random() < 0.01  # 1% fraud rate
        })
        
        # Progress indicator
        if i % 100000 == 0:
            print(f"  Generated {i:,} records...")
    
    df = pd.DataFrame(data)
    
    # Save to CSV with different options for testing
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"  Saved to {filename} ({file_size:.2f} MB, {len(df):,} rows)")
    
    # Also save a partitioned version for partitioning demonstrations
    if num_rows > 100000:
        partition_dir = "data/transactions_partitioned"
        os.makedirs(partition_dir, exist_ok=True)
        
        # Partition by category
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            if len(cat_df) > 0:
                cat_df.to_csv(f"{partition_dir}/category={category}.csv", index=False)
        
        print(f"  Also saved partitioned data to {partition_dir}/")
    
    return df

def create_customers_with_skew(num_rows=20000, filename="data/customers_skewed.csv"):
    """
    Create customer dataset with intentional skew for join strategy testing.
    Includes demographic and behavioral data.
    """
    print(f"Generating {num_rows:,} customer records with skew...")
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 
                   'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
                   'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah',
                   'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
                  'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
                  'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore']
    
    cities = {
        'New York': 'NY',
        'Los Angeles': 'CA', 
        'Chicago': 'IL',
        'Houston': 'TX',
        'Phoenix': 'AZ',
        'Philadelphia': 'PA',
        'San Antonio': 'TX',
        'San Diego': 'CA',
        'Dallas': 'TX',
        'San Jose': 'CA'
    }
    
    data = []
    for i in range(1, num_rows + 1):
        join_date = datetime.now() - timedelta(days=random.randint(0, 2000))
        
        # Create intentional skew: 20% of customers are in top tier
        if i % 5 == 0:
            membership_tier = random.choice(['Platinum', 'Gold'])
            city = 'New York'  # Skew location
            total_spent = round(random.uniform(5000, 50000), 2)
        else:
            membership_tier = random.choice(['Basic', 'Silver'])
            city = random.choice(list(cities.keys()))
            total_spent = round(random.uniform(100, 10000), 2)
        
        # Create some NULL values
        last_purchase_date = None if random.random() < 0.1 else (
            join_date + timedelta(days=random.randint(0, 90))
        ).strftime('%Y-%m-%d')
        
        # Create duplicate emails for deduplication testing
        email = f"customer{i}@example.com"
        if i % 100 == 0:
            email = f"customer{i-1}@example.com"  # Duplicate email
        
        data.append({
            'customer_id': f"CUST-{i:05d}",
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': email,
            'join_date': join_date.strftime('%Y-%m-%d'),
            'membership_tier': membership_tier,
            'city': city,
            'state': cities[city],
            'country': 'USA',
            'total_spent': total_spent,
            'last_purchase_date': last_purchase_date,
            'loyalty_points': int(total_spent * 10),
            'preferred_category': random.choice(['Electronics', 'Clothing', 'Books', 'Sports', 'Groceries']),
            'age_group': random.choice(['18-25', '26-35', '36-45', '46-55', '56+']),
            'income_bracket': random.choice(['Low', 'Medium', 'High', 'Very High'])
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"  Saved to {filename} ({file_size:.2f} MB, {len(df):,} rows)")
    
    return df

def create_ml_training_data(num_rows=100000, filename="data/ml_training.csv"):
    """
    Create dataset for ML pipeline testing with features and labels.
    Includes numerical, categorical, and missing values.
    """
    print(f"Generating {num_rows:,} ML training records...")
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    np.random.seed(42)
    
    # Generate synthetic features
    feature1 = np.random.normal(50, 15, num_rows)  # Normal distribution
    feature2 = np.random.exponential(10, num_rows)  # Exponential distribution
    feature3 = np.random.randint(0, 10, num_rows)   # Categorical encoded
    feature4 = np.random.uniform(0, 100, num_rows)  # Uniform distribution
    
    # Create some missing values (5% missing rate)
    mask = np.random.random(num_rows) < 0.05
    feature1 = np.where(mask, np.nan, feature1)
    
    mask = np.random.random(num_rows) < 0.03
    feature2 = np.where(mask, np.nan, feature2)
    
    # Create categorical features
    categories = ['A', 'B', 'C', 'D', 'E']
    cat_feature = np.random.choice(categories, num_rows, p=[0.4, 0.3, 0.15, 0.1, 0.05])
    
    # Generate target variable based on features with some noise
    # y = 2*feature1 + 0.5*feature2 + 3*feature3 + noise
    noise = np.random.normal(0, 5, num_rows)
    y = 2 * np.nan_to_num(feature1, nan=50) + \
        0.5 * np.nan_to_num(feature2, nan=10) + \
        3 * feature3 + \
        noise
    
    # Convert to binary classification (1 if y > median, else 0)
    threshold = np.median(y)
    target = (y > threshold).astype(int)
    
    # Create regression target (continuous)
    reg_target = y + np.random.normal(0, 10, num_rows)
    
    # Create dataframe
    df = pd.DataFrame({
        'feature1': feature1,
        'feature2': feature2,
        'feature3': feature3,
        'feature4': feature4,
        'cat_feature': cat_feature,
        'target_class': target,
        'target_regression': reg_target,
        'cluster_id': np.random.randint(0, 5, num_rows),  # For clustering
        'sample_weight': np.random.uniform(0.5, 2.0, num_rows)  # For weighted samples
    })
    
    # Add some outliers
    outlier_indices = np.random.choice(num_rows, size=int(num_rows * 0.01), replace=False)
    df.loc[outlier_indices, 'feature1'] = df.loc[outlier_indices, 'feature1'] * 5
    
    df.to_csv(filename, index=False)
    
    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
    print(f"  Saved to {filename} ({file_size:.2f} MB, {len(df):,} rows)")
    
    # Also save as Parquet for format comparison
    parquet_file = filename.replace('.csv', '.parquet')
    df.to_parquet(parquet_file, index=False)
    print(f"  Also saved as Parquet: {parquet_file}")
    
    return df

def create_streaming_data(num_files=10, output_dir="data/streaming"):
    """
    Create time-series streaming data with watermarks and late data.
    Generates multiple CSV files with timestamps for streaming analytics.
    """
    print(f"Generating {num_files} streaming data files...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate base time
    base_time = datetime.now() - timedelta(hours=24)
    
    for file_num in range(num_files):
        # Each file represents 5 minutes of data
        file_time = base_time + timedelta(minutes=file_num * 5)
        filename = f"{output_dir}/stream_data_{file_num:03d}.csv"
        
        # Generate 1000-5000 records per file
        num_records = random.randint(1000, 5000)
        
        data = []
        for i in range(num_records):
            # Add some jitter to timestamps within the 5-minute window
            record_time = file_time + timedelta(
                seconds=random.randint(0, 300),
                milliseconds=random.randint(0, 999)
            )
            
            # Generate different event types
            event_type = random.choice(['click', 'view', 'purchase', 'add_to_cart', 'search'])
            
            # User IDs with some repeating patterns
            user_id = f"USER-{random.randint(1, 1000):04d}"
            
            # Session IDs (some sessions span multiple files)
            session_id = f"SESS-{random.randint(1, 100):03d}"
            
            # Generate metrics
            duration = random.randint(1, 300) if event_type in ['view', 'click'] else None
            value = round(random.uniform(0.1, 100.0), 2) if event_type == 'purchase' else None
            
            data.append({
                'event_id': f"EVT-{file_num:03d}-{i:06d}",
                'event_type': event_type,
                'user_id': user_id,
                'session_id': session_id,
                'timestamp': record_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'duration_seconds': duration,
                'value_usd': value,
                'page_url': f"/products/{random.randint(1, 100)}",
                'device': random.choice(['mobile', 'desktop', 'tablet']),
                'browser': random.choice(['chrome', 'firefox', 'safari', 'edge']),
                'country': random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'IN'])
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        
        # Create some late arriving data (for watermark testing)
        if file_num >= 5 and random.random() < 0.3:
            late_filename = f"{output_dir}/late_data_{file_num:03d}.csv"
            late_df = df.copy()
            # Make timestamps 10 minutes earlier (simulating late data)
            late_times = [file_time - timedelta(minutes=10)] * len(late_df)
            late_df['timestamp'] = [t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for t in late_times]
            late_df.to_csv(late_filename, index=False)
            print(f"    Created late data file: {late_filename}")
    
    print(f"  Generated {num_files} streaming files in {output_dir}/")
    
    # Create a schema file for streaming
    schema = {
        "fields": [
            {"name": "event_id", "type": "string"},
            {"name": "event_type", "type": "string"},
            {"name": "user_id", "type": "string"},
            {"name": "session_id", "type": "string"},
            {"name": "timestamp", "type": "timestamp"},
            {"name": "duration_seconds", "type": "integer"},
            {"name": "value_usd", "type": "double"},
            {"name": "page_url", "type": "string"},
            {"name": "device", "type": "string"},
            {"name": "browser", "type": "string"},
            {"name": "country", "type": "string"}
        ]
    }
    
    with open(f"{output_dir}/schema.json", 'w') as f:
        json.dump(schema, f, indent=2)
    
    print(f"  Created schema file: {output_dir}/schema.json")
    
    return output_dir

def create_api_test_data(num_records=1000, filename="data/api_test_data.json"):
    """
    Create JSON data for API integration testing.
    Includes nested structures and various data types.
    """
    print(f"Generating {num_records:,} API test records...")
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    data = []
    for i in range(num_records):
        record = {
            "id": i + 1,
            "user": {
                "name": f"User_{i}",
                "email": f"user_{i}@example.com",
                "profile": {
                    "age": random.randint(18, 70),
                    "preferences": {
                        "theme": random.choice(["dark", "light"]),
                        "notifications": random.choice([True, False])
                    }
                }
            },
            "orders": [
                {
                    "order_id": f"ORD-{i}-{j}",
                    "amount": round(random.uniform(10.0, 500.0), 2),
                    "items": random.randint(1, 10),
                    "status": random.choice(["pending", "shipped", "delivered", "cancelled"])
                }
                for j in range(random.randint(1, 5))  # 1-5 orders per user
            ],
            "metadata": {
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
                "updated_at": datetime.now().isoformat(),
                "tags": random.sample(["vip", "new", "returning", "inactive", "premium"], k=random.randint(1, 3)),
                "score": round(random.uniform(0.0, 1.0), 3)
            },
            "active": random.choice([True, False]),
            "last_login": (datetime.now() - timedelta(hours=random.randint(1, 720))).isoformat()
        }
        data.append(record)
    
    # Save as JSON
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    file_size = os.path.getsize(filename) / 1024  # KB
    print(f"  Saved to {filename} ({file_size:.2f} KB, {len(data):,} records)")
    
    # Also save as JSON lines for streaming
    jsonl_file = filename.replace('.json', '.jsonl')
    with open(jsonl_file, 'w') as f:
        for record in data:
            f.write(json.dumps(record) + '\n')
    
    print(f"  Also saved as JSONL: {jsonl_file}")
    
    return data

def create_join_test_datasets():
    """
    Create specialized datasets for join strategy testing:
    - Small dimension table
    - Large fact table with skew
    - Medium-sized bridge table
    """
    print("Creating join test datasets...")
    
    os.makedirs("data/join_tests", exist_ok=True)
    
    # 1. Small dimension table (products)
    products = []
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports']
    for i in range(1, 1001):  # 1000 products
        products.append({
            'product_id': f"P{i:04d}",
            'product_name': f"Product {i}",
            'category': random.choice(categories),
            'price': round(random.uniform(10, 1000), 2),
            'supplier_id': f"SUP{random.randint(1, 50):03d}",
            'in_stock': random.choice([True, False]),
            'rating': round(random.uniform(1.0, 5.0), 1)
        })
    
    products_df = pd.DataFrame(products)
    products_df.to_csv("data/join_tests/products.csv", index=False)
    print(f"  Created products.csv ({len(products_df):,} rows)")
    
    # 2. Large fact table with skew (sales)
    sales = []
    # Create intentional skew: 80% of sales from 20% of products
    popular_products = [f"P{i:04d}" for i in range(1, 201)]  # First 200 products
    
    for i in range(1, 100001):  # 100,000 sales
        # Skew distribution
        if random.random() < 0.8:
            product_id = random.choice(popular_products)
        else:
            product_id = f"P{random.randint(1, 1000):04d}"
        
        sales.append({
            'sale_id': f"S{i:06d}",
            'product_id': product_id,
            'customer_id': f"C{random.randint(1, 5000):05d}",
            'quantity': random.randint(1, 10),
            'sale_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'region': random.choice(['North', 'South', 'East', 'West']),
            'discount': round(random.uniform(0, 0.3), 2)  # 0-30% discount
        })
    
    sales_df = pd.DataFrame(sales)
    sales_df.to_csv("data/join_tests/sales.csv", index=False)
    print(f"  Created sales.csv ({len(sales_df):,} rows) with intentional skew")
    
    # 3. Bridge table (product_categories)
    categories_df = pd.DataFrame({
        'category_id': range(1, 6),
        'category_name': categories,
        'department': ['Tech', 'Fashion', 'Home', 'Education', 'Sports'],
        'profit_margin': [0.25, 0.35, 0.20, 0.15, 0.30]
    })
    categories_df.to_csv("data/join_tests/categories.csv", index=False)
    print(f"  Created categories.csv ({len(categories_df):,} rows)")
    
    return {
        'products': products_df,
        'sales': sales_df,
        'categories': categories_df
    }

def main():
    """Main function to generate all datasets."""
    print("=" * 60)
    print("Advanced PySpark Data Generator")
    print("Generating comprehensive datasets for advanced tutorials")
    print("=" * 60)
    
    start_time = time.time()
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Generate all datasets
    print("\n1. Generating large transaction dataset for Catalyst optimizer...")
    transactions_df = create_transactions_large(500000, "data/transactions_large.csv")
    
    print("\n2. Generating customer dataset with skew for join strategies...")
    customers_df = create_customers_with_skew(20000, "data/customers_skewed.csv")
    
    print("\n3. Generating ML training data...")
    ml_df = create_ml_training_data(100000, "data/ml_training.csv")
    
    print("\n4. Generating streaming data files...")
    streaming_dir = create_streaming_data(10, "data/streaming")
    
    print("\n5. Generating API test data...")
    api_data = create_api_test_data(1000, "data/api_test_data.json")
    
    print("\n6. Generating join test datasets...")
    join_data = create_join_test_datasets()
    
    print("\n7. Creating sample Parquet files for format comparison...")
    # Convert some CSVs to Parquet
    transactions_df.to_parquet("data/transactions_large.parquet", index=False)
    customers_df.to_parquet("data/customers_skewed.parquet", index=False)
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("Data Generation Complete!")
    print("=" * 60)
    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"Files created in 'data/' directory:")
    print("  - transactions_large.csv/.parquet (500K rows)")
    print("  - customers_skewed.csv/.parquet (20K rows)")
    print("  - ml_training.csv/.parquet (100K rows)")
    print("  - streaming/*.csv (10 files with timestamps)")
    print("  - api_test_data.json/.jsonl (1K records)")
    print("  - join_tests/*.csv (products, sales, categories)")
    print("\nThese datasets support all advanced PySpark tutorials:")
    print("  • Catalyst Optimizer (01_catalyst_optimizer.py)")
    print("  • Memory Management (02_memory_management.py)")
    print("  • Join Strategies (03_join_strategies.py)")
    print("  • ML Pipeline (04_ml_pipeline.py)")
    print("  • Streaming Analytics (05_streaming_analytics.py)")
    print("  • FastAPI Integration (06_fastapi_integration.py)")
    print("=" * 60)

if __name__ == "__main__":
    main()