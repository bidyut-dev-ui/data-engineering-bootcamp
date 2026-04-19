#!/usr/bin/env python3
"""
Week 14.5 - Hadoop Basics: Hive Integration Tutorial
====================================================

This tutorial covers Apache Hive - a data warehouse infrastructure built on Hadoop.
We'll learn how to use Hive for SQL-like querying of data stored in HDFS.

Learning Objectives:
1. Understand Hive architecture and components
2. Create Hive tables (managed and external)
3. Load data from HDFS into Hive tables
4. Run HiveQL queries for data analysis
5. Integrate Hive with Python using PyHive
6. Optimize for 8GB RAM constraints

Prerequisites:
- Hadoop cluster running (from 01_hadoop_docker_setup.py)
- Hive service available (included in docker-compose.yml)
- `pyhive` and `thrift` Python libraries installed (in requirements.txt)
"""

import os
import csv
import random
from datetime import datetime, timedelta
from pyhive import hive
from pyhive.exc import OperationalError

# Hive connection configuration
HIVE_HOST = "localhost"
HIVE_PORT = 10000  # HiveServer2 port
HIVE_USERNAME = "hive"
HIVE_DATABASE = "default"

def create_hive_connection():
    """
    Create a connection to HiveServer2 using PyHive.
    
    Returns:
        hive.Connection: Connection object for Hive operations
    """
    try:
        connection = hive.connect(
            host=HIVE_HOST,
            port=HIVE_PORT,
            username=HIVE_USERNAME,
            database=HIVE_DATABASE
        )
        print(f"✅ Connected to Hive at {HIVE_HOST}:{HIVE_PORT}")
        return connection
    except Exception as e:
        print(f"❌ Failed to connect to Hive: {e}")
        print("Make sure Hive service is running in Hadoop cluster")
        return None

def execute_hive_query(connection, query, fetch_results=True):
    """
    Execute a HiveQL query and optionally fetch results.
    
    Args:
        connection: Hive connection
        query: HiveQL query string
        fetch_results: Whether to fetch and return results
    
    Returns:
        list: Query results if fetch_results=True, else None
    """
    try:
        cursor = connection.cursor()
        print(f"📝 Executing HiveQL: {query[:100]}..." if len(query) > 100 else f"📝 Executing HiveQL: {query}")
        
        cursor.execute(query)
        
        if fetch_results:
            results = cursor.fetchall()
            print(f"   Query returned {len(results)} rows")
            return results
        else:
            print("   Query executed successfully")
            return None
    except OperationalError as e:
        print(f"❌ Hive query error: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

def create_sample_csv_data(filename, num_rows=1000):
    """
    Generate sample CSV data for Hive ingestion.
    
    Args:
        filename: Output CSV file name
        num_rows: Number of rows to generate
    """
    print(f"📝 Generating sample CSV data: {filename}")
    
    # Sample data schema
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin', 'Singapore']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['employee_id', 'name', 'department', 'salary', 'hire_date', 'location'])
        
        # Write data rows
        start_date = datetime(2018, 1, 1)
        for i in range(1, num_rows + 1):
            emp_id = i
            name = f"Employee_{i}"
            dept = random.choice(departments)
            salary = random.randint(50000, 150000)
            hire_date = start_date + timedelta(days=random.randint(0, 365*3))
            location = random.choice(locations)
            
            writer.writerow([emp_id, name, dept, salary, hire_date.strftime('%Y-%m-%d'), location])
    
    file_size = os.path.getsize(filename)
    print(f"   Generated {num_rows} rows, {file_size / 1024:.1f} KB")

def demonstrate_hive_architecture():
    """
    Explain Hive architecture and components.
    """
    print("\n" + "=" * 70)
    print("Hive Architecture for 8GB RAM Constraints")
    print("=" * 70)
    
    print("\n1. Hive Components:")
    print("   - HiveServer2: Thrift server for client connections")
    print("   - Metastore: Stores table metadata (schema, location, etc.)")
    print("   - Driver: Compiles HiveQL to MapReduce/Tez/Spark jobs")
    print("   - Execution Engine: Executes the compiled jobs")
    
    print("\n2. Table Types:")
    print("   - Managed Tables: Hive controls data lifecycle")
    print("   - External Tables: Hive references external HDFS data")
    print("   - For 8GB RAM: Use external tables to avoid data duplication")
    
    print("\n3. Storage Formats:")
    print("   - TextFile: Simple but inefficient")
    print("   - ORC: Optimized Row Columnar (best for analytics)")
    print("   - Parquet: Columnar storage (good for Spark integration)")
    print("   - For 8GB RAM: ORC provides best compression and performance")
    
    print("\n4. Execution Engines:")
    print("   - MapReduce: Original engine (slow but reliable)")
    print("   - Tez: DAG-based engine (faster, better for 8GB RAM)")
    print("   - Spark: Spark integration (requires Spark cluster)")

def create_hive_tables(connection):
    """
    Create Hive tables for demonstration.
    
    Args:
        connection: Hive connection
    """
    print("\n1. Creating Hive Database:")
    execute_hive_query(connection, "CREATE DATABASE IF NOT EXISTS demo_db", fetch_results=False)
    execute_hive_query(connection, "USE demo_db", fetch_results=False)
    
    print("\n2. Creating Managed Table (Hive controls data):")
    managed_table_query = """
    CREATE TABLE IF NOT EXISTS employees_managed (
        employee_id INT,
        name STRING,
        department STRING,
        salary INT,
        hire_date DATE,
        location STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    """
    execute_hive_query(connection, managed_table_query, fetch_results=False)
    
    print("\n3. Creating External Table (points to HDFS location):")
    external_table_query = """
    CREATE EXTERNAL TABLE IF NOT EXISTS employees_external (
        employee_id INT,
        name STRING,
        department STRING,
        salary INT,
        hire_date DATE,
        location STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '/user/hive/warehouse/demo_db.db/employees_external'
    """
    execute_hive_query(connection, external_table_query, fetch_results=False)
    
    print("\n4. Creating ORC Table (optimized storage format):")
    orc_table_query = """
    CREATE TABLE IF NOT EXISTS employees_orc (
        employee_id INT,
        name STRING,
        department STRING,
        salary INT,
        hire_date DATE,
        location STRING
    )
    STORED AS ORC
    TBLPROPERTIES ("orc.compress"="SNAPPY")
    """
    execute_hive_query(connection, orc_table_query, fetch_results=False)

def load_data_and_run_queries(connection, csv_file):
    """
    Load data into Hive tables and run demonstration queries.
    
    Args:
        connection: Hive connection
        csv_file: Path to CSV data file
    """
    # First, upload CSV to HDFS (simulated - in real scenario use hdfs command)
    print(f"\n5. Loading data from {csv_file} into Hive:")
    
    # For demonstration, we'll use local file path
    # In production, you would: hdfs dfs -put data.csv /user/hive/warehouse/
    
    load_query = f"""
    LOAD DATA LOCAL INPATH '{csv_file}'
    OVERWRITE INTO TABLE employees_managed
    """
    execute_hive_query(connection, load_query, fetch_results=False)
    
    print("\n6. Running Analytical Queries:")
    
    # Query 1: Basic aggregation
    print("\n   Query 1: Department-wise average salary")
    query1 = """
    SELECT department, 
           COUNT(*) as employee_count,
           AVG(salary) as avg_salary,
           MIN(salary) as min_salary,
           MAX(salary) as max_salary
    FROM employees_managed
    GROUP BY department
    ORDER BY avg_salary DESC
    """
    results1 = execute_hive_query(connection, query1)
    if results1:
        for dept, count, avg_sal, min_sal, max_sal in results1:
            print(f"      {dept}: {count} employees, avg ${avg_sal:.0f}")
    
    # Query 2: Time-based analysis
    print("\n   Query 2: Hiring trends by year")
    query2 = """
    SELECT YEAR(hire_date) as hire_year,
           COUNT(*) as hires,
           AVG(salary) as avg_starting_salary
    FROM employees_managed
    GROUP BY YEAR(hire_date)
    ORDER BY hire_year
    """
    results2 = execute_hive_query(connection, query2)
    if results2:
        for year, hires, avg_salary in results2:
            print(f"      {year}: {hires} hires, avg ${avg_salary:.0f}")
    
    # Query 3: Complex analysis with window function
    print("\n   Query 3: Salary ranking within departments")
    query3 = """
    SELECT name, 
           department,
           salary,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
    FROM employees_managed
    WHERE department IN ('Engineering', 'Sales')
    ORDER BY department, dept_rank
    LIMIT 10
    """
    results3 = execute_hive_query(connection, query3)
    if results3:
        print("      Top earners in Engineering & Sales:")
        for name, dept, salary, rank in results3:
            print(f"        {rank}. {name} ({dept}): ${salary}")

def demonstrate_partitioning_and_bucketing():
    """
    Demonstrate Hive partitioning and bucketing for performance.
    """
    print("\n" + "=" * 70)
    print("Hive Performance Optimization")
    print("=" * 70)
    
    print("\n1. Partitioning (for 8GB RAM):")
    print("   - Divides table into directories by column values")
    print("   - Example: PARTITIONED BY (department STRING, hire_year INT)")
    print("   - Benefits: Query pruning, faster scans")
    print("   - Use when: Column has low cardinality, used in WHERE clauses")
    
    print("\n2. Bucketing:")
    print("   - Divides data into fixed number of files")
    print("   - Example: CLUSTERED BY (employee_id) INTO 32 BUCKETS")
    print("   - Benefits: Efficient joins, sampling")
    print("   - Use when: Column has high cardinality, used in JOINs")
    
    print("\n3. Compression (critical for 8GB RAM):")
    print("   - ORC with SNAPPY: Good balance of speed and compression")
    print("   - Reduces storage and memory footprint")
    print("   - Enables processing larger datasets within RAM limits")

def main():
    """
    Main tutorial function demonstrating Hive integration.
    """
    print("=" * 70)
    print("Hive Integration Tutorial")
    print("=" * 70)
    
    # Create Hive connection
    connection = create_hive_connection()
    if not connection:
        return
    
    # Demonstrate Hive architecture
    demonstrate_hive_architecture()
    
    # Generate sample data
    csv_file = "employee_data.csv"
    create_sample_csv_data(csv_file, num_rows=500)
    
    # Create Hive tables
    create_hive_tables(connection)
    
    # Load data and run queries
    load_data_and_run_queries(connection, csv_file)
    
    # Demonstrate partitioning and bucketing
    demonstrate_partitioning_and_bucketing()
    
    # Show optimization for 8GB RAM
    print("\n" + "=" * 70)
    print("8GB RAM Optimization Tips for Hive")
    print("=" * 70)
    
    print("\n1. Memory Settings:")
    print("   SET hive.tez.container.size=1024;  # 1GB per container")
    print("   SET hive.tez.java.opts=-Xmx819m;   # Leave room for OS")
    
    print("\n2. Query Optimization:")
    print("   - Use WHERE clauses to filter early")
    print("   - Avoid SELECT * (fetch only needed columns)")
    print("   - Use LIMIT during development")
    
    print("\n3. Storage Optimization:")
    print("   - Use ORC format with compression")
    print("   - Partition large tables")
    print("   - Consider bucketing for join performance")
    
    # Cleanup
    print(f"\n4. Cleaning Up:")
    execute_hive_query(connection, "DROP DATABASE IF EXISTS demo_db CASCADE", fetch_results=False)
    
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"   Removed {csv_file}")
    
    # Close connection
    connection.close()
    
    print("\n" + "=" * 70)
    print("✅ Hive Tutorial Completed Successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Hive provides SQL-like interface for Hadoop data")
    print("2. External tables avoid data duplication (better for 8GB RAM)")
    print("3. ORC format with compression reduces storage and memory usage")
    print("4. Partitioning and bucketing improve query performance")
    print("5. PyHive enables Python integration with HiveServer2")

if __name__ == "__main__":
    main()