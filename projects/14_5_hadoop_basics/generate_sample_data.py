#!/usr/bin/env python3
"""
Week 14.5 - Hadoop Basics: Sample Data Generator
================================================

This script generates sample data files for Hadoop tutorials.
It creates various types of data (text, CSV, JSON) that can be used
for HDFS, MapReduce, Hive, and Spark processing demonstrations.

The data is generated with realistic patterns and distributions
to simulate real-world data engineering scenarios.

Key Features:
1. Generates text data for MapReduce word counting
2. Creates structured CSV data for Hive tables
3. Produces JSON data for Spark processing
4. All data sizes optimized for 8GB RAM constraints
5. Configurable output formats and sizes
"""

import os
import json
import csv
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

def generate_text_data_for_mapreduce(output_file, num_lines=1000, words_per_line=20):
    """
    Generate text data for MapReduce word counting exercises.
    
    Args:
        output_file: Path to output text file
        num_lines: Number of lines to generate
        words_per_line: Average words per line
    """
    print(f"📝 Generating text data for MapReduce: {output_file}")
    
    # Common words with realistic frequency distribution
    common_words = [
        'data', 'engineering', 'hadoop', 'mapreduce', 'spark', 'python',
        'processing', 'analysis', 'database', 'query', 'cluster', 'node',
        'memory', 'storage', 'file', 'system', 'distributed', 'computing',
        'algorithm', 'optimization', 'performance', 'scalability', 'reliability',
        'batch', 'streaming', 'etl', 'pipeline', 'workflow', 'orchestration'
    ]
    
    # Less common technical terms
    tech_terms = [
        'hdfs', 'yarn', 'hive', 'hbase', 'zookeeper', 'kafka', 'flume',
        'sqoop', 'oozie', 'impala', 'presto', 'drill', 'tez', 'mahout',
        'ambari', 'cloudera', 'hortonworks', 'aws', 'azure', 'gcp'
    ]
    
    # General English words
    general_words = [
        'the', 'and', 'for', 'with', 'from', 'this', 'that', 'have', 'which',
        'their', 'would', 'there', 'been', 'some', 'other', 'more', 'first',
        'water', 'called', 'who', 'oil', 'its', 'now', 'find', 'long', 'down'
    ]
    
    # Combine all word lists with different weights
    all_words = common_words * 5 + tech_terms * 3 + general_words * 2
    
    with open(output_file, 'w') as f:
        for line_num in range(1, num_lines + 1):
            # Vary words per line for more realistic data
            actual_words = random.randint(words_per_line - 5, words_per_line + 5)
            line_words = [random.choice(all_words) for _ in range(actual_words)]
            
            # Add some punctuation and formatting
            line = ' '.join(line_words)
            
            # Every 10th line, add a special pattern for testing
            if line_num % 10 == 0:
                line += " data engineering hadoop spark"
            
            f.write(line + '\n')
    
    file_size = os.path.getsize(output_file)
    print(f"   Generated {num_lines} lines, {file_size / 1024:.1f} KB")
    print(f"   Word count: ~{num_lines * words_per_line:,} words")
    
    return output_file

def generate_csv_data_for_hive(output_file, num_rows=5000):
    """
    Generate structured CSV data for Hive table ingestion.
    
    Args:
        output_file: Path to output CSV file
        num_rows: Number of rows to generate
    """
    print(f"📊 Generating CSV data for Hive: {output_file}")
    
    # Define realistic data distributions
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'IT', 'Support']
    locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin', 'Singapore', 'Sydney', 'Toronto']
    job_titles = [
        'Data Engineer', 'Software Engineer', 'Data Scientist', 'Analyst',
        'Manager', 'Director', 'VP', 'Architect', 'Developer', 'Admin'
    ]
    
    # Salary ranges by department (min, max)
    salary_ranges = {
        'Engineering': (80000, 180000),
        'Sales': (60000, 150000),
        'Marketing': (50000, 120000),
        'HR': (45000, 100000),
        'Finance': (70000, 160000),
        'Operations': (55000, 130000),
        'IT': (60000, 140000),
        'Support': (40000, 90000)
    }
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = [
            'employee_id', 'first_name', 'last_name', 'email', 'department',
            'job_title', 'salary', 'hire_date', 'location', 'manager_id',
            'performance_rating', 'years_experience'
        ]
        writer.writerow(header)
        
        # Generate employee data
        start_date = datetime(2015, 1, 1)
        
        for emp_id in range(1, num_rows + 1):
            # Basic employee info
            first_name = random.choice(['John', 'Jane', 'Robert', 'Mary', 'Michael', 'Sarah', 
                                       'David', 'Lisa', 'James', 'Jennifer', 'William', 'Linda'])
            last_name = random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
                                      'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'])
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            
            # Department and related attributes
            department = random.choice(departments)
            job_title = random.choice(job_titles)
            
            # Salary based on department
            min_salary, max_salary = salary_ranges[department]
            salary = random.randint(min_salary, max_salary)
            
            # Hire date (more recent hires are more common)
            days_ago = random.randint(0, 365 * 10)  # Up to 10 years
            hire_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            location = random.choice(locations)
            
            # Manager ID (some employees have managers, some don't)
            manager_id = random.choice([0] + list(range(1, min(100, emp_id))))
            
            # Performance rating (1-5, normally distributed)
            performance_rating = min(5, max(1, int(random.gauss(3.5, 1.0))))
            
            # Years of experience
            years_experience = random.randint(0, 30)
            
            # Write row
            row = [
                emp_id, first_name, last_name, email, department,
                job_title, salary, hire_date, location, manager_id,
                performance_rating, years_experience
            ]
            writer.writerow(row)
    
    file_size = os.path.getsize(output_file)
    print(f"   Generated {num_rows} rows, {file_size / 1024:.1f} KB")
    print(f"   Schema: {len(header)} columns")
    
    return output_file

def generate_json_data_for_spark(output_file, num_records=1000):
    """
    Generate JSON data for Spark processing exercises.
    
    Args:
        output_file: Path to output JSON file
        num_records: Number of JSON records to generate
    """
    print(f"📄 Generating JSON data for Spark: {output_file}")
    
    # Product categories and prices
    product_categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports', 'Toys', 'Beauty', 'Food']
    
    # Customer locations
    locations = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'IN']
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay']
    
    records = []
    
    for i in range(1, num_records + 1):
        # Generate transaction data
        transaction_id = f"TXN{10000 + i}"
        customer_id = f"CUST{random.randint(1000, 9999)}"
        
        # Transaction date (last 90 days)
        days_ago = random.randint(0, 90)
        transaction_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Product details
        product_id = f"PROD{random.randint(1, 100)}"
        product_name = f"Product {random.randint(1, 50)}"
        category = random.choice(product_categories)
        
        # Price based on category
        category_prices = {
            'Electronics': (50, 2000),
            'Clothing': (10, 200),
            'Home': (20, 500),
            'Books': (5, 50),
            'Sports': (30, 300),
            'Toys': (5, 100),
            'Beauty': (5, 150),
            'Food': (1, 50)
        }
        min_price, max_price = category_prices[category]
        price = round(random.uniform(min_price, max_price), 2)
        
        quantity = random.randint(1, 5)
        total_amount = round(price * quantity, 2)
        
        # Customer details
        customer_location = random.choice(locations)
        payment_method = random.choice(payment_methods)
        
        # Transaction status (mostly successful)
        status = random.choices(['SUCCESS', 'FAILED', 'PENDING'], weights=[90, 5, 5])[0]
        
        # Create record
        record = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "transaction_date": transaction_date,
            "product": {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price": price
            },
            "quantity": quantity,
            "total_amount": total_amount,
            "customer_location": customer_location,
            "payment_method": payment_method,
            "status": status,
            "metadata": {
                "generated_by": "hadoop_sample_generator",
                "version": "1.0",
                "record_index": i
            }
        }
        
        records.append(record)
    
    # Write JSON file (one record per line for Spark)
    with open(output_file, 'w') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')
    
    file_size = os.path.getsize(output_file)
    print(f"   Generated {num_records} JSON records, {file_size / 1024:.1f} KB")
    print(f"   Format: JSON Lines (one JSON object per line)")
    
    return output_file

def generate_log_data_for_analysis(output_file, num_entries=2000):
    """
    Generate log file data for log analysis exercises.
    
    Args:
        output_file: Path to output log file
        num_entries: Number of log entries to generate
    """
    print(f"📋 Generating log data for analysis: {output_file}")
    
    # Log levels with realistic distribution
    log_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG']
    level_weights = [70, 15, 10, 5]  # Mostly INFO, some WARN/ERROR, little DEBUG
    
    # Log components
    components = [
        'WebServer', 'Database', 'Cache', 'API', 'AuthService',
        'PaymentService', 'NotificationService', 'BatchProcessor'
    ]
    
    # Error messages
    error_messages = [
        'Connection timeout', 'Database connection failed', 'Invalid credentials',
        'File not found', 'Memory allocation error', 'Network unreachable',
        'Disk space low', 'CPU usage high', 'Service unavailable'
    ]
    
    # User IDs
    user_ids = [f"user_{i}" for i in range(1, 101)] + ['anonymous', 'system', 'admin']
    
    with open(output_file, 'w') as f:
        for i in range(1, num_entries + 1):
            # Timestamp
            seconds_ago = random.randint(0, 86400)  # Last 24 hours
            timestamp = (datetime.now() - timedelta(seconds=seconds_ago)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Log level
            level = random.choices(log_levels, weights=level_weights)[0]
            
            # Component
            component = random.choice(components)
            
            # Message
            if level == 'ERROR':
                message = random.choice(error_messages)
                # Add some context
                message += f" for user {random.choice(user_ids)}"
            elif level == 'WARN':
                message = f"Performance degradation detected in {component}"
            elif level == 'DEBUG':
                message = f"Processing request {random.randint(1000, 9999)}"
            else:  # INFO
                actions = ['processed', 'retrieved', 'updated', 'created', 'deleted']
                resources = ['user profile', 'order', 'payment', 'notification', 'report']
                message = f"{random.choice(actions)} {random.choice(resources)}"
            
            # Optional additional fields
            extra = ""
            if random.random() > 0.7:  # 30% of entries have extra data
                extra_fields = []
                if random.random() > 0.5:
                    extra_fields.append(f"duration={random.randint(10, 5000)}ms")
                if random.random() > 0.5:
                    extra_fields.append(f"memory={random.randint(100, 2000)}MB")
                if random.random() > 0.5:
                    extra_fields.append(f"thread={random.randint(1, 50)}")
                
                if extra_fields:
                    extra = " [" + ", ".join(extra_fields) + "]"
            
            # Write log entry
            f.write(f"{timestamp} [{level}] {component}: {message}{extra}\n")
    
    file_size = os.path.getsize(output_file)
    print(f"   Generated {num_entries} log entries, {file_size / 1024:.1f} KB")
    print(f"   Format: Standard log format with timestamp, level, component, message")
    
    return output_file

def create_sample_data_directory():
    """
    Create a directory for sample data and generate all file types.
    """
    data_dir = Path("sample_data")
    data_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("Generating Sample Data for Hadoop Tutorials")
    print("=" * 70)
    
    # Generate all data types
    text_file = generate_text_data_for_mapreduce(
        data_dir / "mapreduce_input.txt",
        num_lines=500,
        words_per_line=15
    )
    
    csv_file = generate_csv_data_for_hive(
        data_dir / "hive_employees.csv",
        num_rows=1000
    )
    
    json_file = generate_json_data_for_spark(
        data_dir / "spark_transactions.json",
        num_records=500
    )
    
    log_file = generate_log_data_for_analysis(
        data_dir / "system_logs.log",
        num_entries=1000
    )
    
    # Create a README file for the sample data
    readme_content = """# Sample Data for Hadoop Tutorials

This directory contains sample data files generated for the Hadoop Basics tutorials.

## Files:

1. `mapreduce_input.txt`
   - Purpose: Text data for MapReduce word counting exercises
   - Size: ~500 lines, ~7,500 words
   - Format: Plain text, one sentence per line
   - Use with: Tutorial 03_mapreduce_wordcount.py

2. `hive_employees.csv`
   - Purpose: Structured data for Hive table ingestion
   - Size: 1,000 rows, 12 columns
   - Format: CSV with header row
   - Schema: employee_id, first_name, last_name, email, department, job_title, salary, hire_date, location, manager_id, performance_rating, years_experience
   - Use with: Tutorial 04_hive_basics.py

3. `spark_transactions.json`
   - Purpose: JSON data for Spark processing exercises
   - Size: 500 JSON records
   - Format: JSON Lines (one JSON object per line)
   - Schema: Nested JSON with transaction details
   - Use with: Tutorial 05_hadoop_spark_integration.py

4. `system_logs.log`
   - Purpose: Log file data for log analysis exercises
   - Size: 1,000 log entries
   - Format: Standard log format with timestamp, level, component, message
   - Use with: Custom MapReduce or Spark log analysis jobs

## Data Characteristics:

- All data is synthetically generated with realistic patterns
- Data sizes are optimized for 8GB RAM constraints
- Files are small enough for quick processing but large enough to demonstrate distributed processing concepts
- Data includes intentional patterns for testing (e.g., certain words appear more frequently)

## Usage Tips:

1. For HDFS exercises: Upload these files to HDFS using `hdfs dfs -put`
2. For MapReduce: Use the text file as input for word counting
3. For Hive: Load the CSV file into Hive tables
4. For Spark: Read the JSON file using Spark's JSON reader
5. For custom exercises: Modify the generation scripts to create larger or different datasets

## Regenerating Data:

To regenerate with different parameters, run:
```bash
python generate_sample_data.py
```

Or modify the parameters in the script for larger datasets.
"""
    
    with open(data_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("\n" + "=" * 70)
    print("✅ Sample Data Generation Complete!")
    print("=" * 70)
    print(f"\nGenerated files in: {data_dir}/")
    print("Total size: ~{:.1f} KB".format(
        sum(os.path.getsize(f) for f in data_dir.iterdir() if f.is_file()) / 1024
    ))
    print("\nReady for use in Hadoop tutorials!")

def main():
    """
    Main function to generate all sample data files.
    """
    create_sample_data_directory()

if __name__ == "__main__":
    main()