#!/usr/bin/env python3
"""
Week 14.5 - Hadoop Basics: Hadoop-Spark Integration Tutorial
============================================================

This tutorial covers integrating Apache Spark with Hadoop ecosystem.
We'll learn how to use Spark to process data stored in HDFS and
compare MapReduce vs Spark performance for 8GB RAM constraints.

Learning Objectives:
1. Understand Spark architecture and how it integrates with Hadoop
2. Read/write data between HDFS and Spark DataFrames
3. Compare MapReduce vs Spark for common data processing tasks
4. Optimize Spark for 8GB RAM constraints
5. Use Spark SQL with Hive metastore

Prerequisites:
- Hadoop cluster running (from 01_hadoop_docker_setup.py)
- PySpark installed (in requirements.txt)
- Basic understanding of HDFS and Hive (from previous tutorials)
"""

import os
import time
import random
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum as spark_sum, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

def create_spark_session(app_name="Hadoop-Spark-Integration"):
    """
    Create a Spark session optimized for 8GB RAM.
    
    Args:
        app_name: Name of the Spark application
    
    Returns:
        SparkSession: Configured Spark session
    """
    print(f"🚀 Creating Spark session: {app_name}")
    
    # Configuration for 8GB RAM laptop
    spark = (SparkSession.builder
        .appName(app_name)
        .master("local[2]")  # Use 2 cores (leaves resources for Hadoop)
        .config("spark.driver.memory", "2g")
        .config("spark.executor.memory", "2g")
        .config("spark.sql.shuffle.partitions", "4")  # Reduce shuffle partitions
        .config("spark.default.parallelism", "4")
        .config("spark.sql.adaptive.enabled", "true")  # Adaptive query execution
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.dynamicAllocation.enabled", "false")  # Disable for local mode
        .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000")  # Connect to HDFS
        .enableHiveSupport()  # Enable Hive integration
        .getOrCreate())
    
    print(f"✅ Spark session created with 8GB RAM optimization")
    print(f"   Driver memory: {spark.conf.get('spark.driver.memory')}")
    print(f"   Executor memory: {spark.conf.get('spark.executor.memory')}")
    print(f"   HDFS URL: {spark.conf.get('spark.hadoop.fs.defaultFS')}")
    
    return spark

def generate_sample_data_to_hdfs(spark, num_records=10000):
    """
    Generate sample data and write to HDFS for processing.
    
    Args:
        spark: Spark session
        num_records: Number of records to generate
    """
    print(f"\n📝 Generating {num_records:,} sample records to HDFS")
    
    # Define schema for sales data
    schema = StructType([
        StructField("transaction_id", IntegerType(), False),
        StructField("customer_id", IntegerType(), False),
        StructField("product_id", IntegerType(), False),
        StructField("product_category", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("price", DoubleType(), False),
        StructField("transaction_date", DateType(), False),
        StructField("store_location", StringType(), False)
    ])
    
    # Generate sample data
    data = []
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports']
    locations = ['NYC', 'SF', 'LA', 'Chicago', 'Miami', 'Seattle']
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(1, num_records + 1):
        transaction_date = start_date.replace(
            day=random.randint(1, 28),
            month=random.randint(1, 12)
        )
        
        record = (
            i,  # transaction_id
            random.randint(1000, 9999),  # customer_id
            random.randint(1, 100),  # product_id
            random.choice(categories),  # product_category
            random.randint(1, 5),  # quantity
            round(random.uniform(10.0, 500.0), 2),  # price
            transaction_date,  # transaction_date
            random.choice(locations)  # store_location
        )
        data.append(record)
    
    # Create DataFrame
    df = spark.createDataFrame(data, schema=schema)
    
    # Write to HDFS in Parquet format (optimized for Spark)
    hdfs_path = "hdfs://localhost:9000/user/spark/sales_data"
    df.write.mode("overwrite").parquet(hdfs_path)
    
    # Count records to verify
    record_count = df.count()
    print(f"✅ Generated {record_count:,} records")
    print(f"📁 Written to HDFS: {hdfs_path}")
    print(f"   Format: Parquet (columnar storage, optimized for analytics)")
    
    return hdfs_path

def demonstrate_spark_hdfs_integration(spark, hdfs_path):
    """
    Demonstrate reading data from HDFS and basic Spark operations.
    
    Args:
        spark: Spark session
        hdfs_path: Path to data in HDFS
    """
    print("\n" + "=" * 70)
    print("Spark-HDFS Integration Demonstration")
    print("=" * 70)
    
    # Read data from HDFS
    print("\n1. Reading data from HDFS:")
    df = spark.read.parquet(hdfs_path)
    print(f"   Read {df.count():,} records from {hdfs_path}")
    print(f"   Schema: {len(df.schema.fields)} columns")
    
    # Show sample data
    print("\n2. Sample data (first 5 rows):")
    df.show(5, truncate=False)
    
    # Basic aggregations
    print("\n3. Basic Aggregations with Spark:")
    
    # Total sales
    total_sales = df.agg(
        spark_sum(col("quantity") * col("price")).alias("total_revenue")
    ).collect()[0]["total_revenue"]
    print(f"   Total Revenue: ${total_sales:,.2f}")
    
    # Sales by category
    print("\n   Sales by Product Category:")
    category_sales = df.groupBy("product_category") \
        .agg(
            count("*").alias("transaction_count"),
            spark_sum("quantity").alias("total_quantity"),
            spark_sum(col("quantity") * col("price")).alias("category_revenue")
        ) \
        .orderBy(col("category_revenue").desc())
    
    category_sales.show(truncate=False)
    
    # Monthly sales trend
    print("\n   Monthly Sales Trend:")
    monthly_sales = df.groupBy(
        col("transaction_date").substr(1, 7).alias("month")
    ).agg(
        count("*").alias("transaction_count"),
        spark_sum(col("quantity") * col("price")).alias("monthly_revenue")
    ).orderBy("month")
    
    monthly_sales.show(truncate=False)
    
    return df

def compare_mapreduce_vs_spark(spark, df):
    """
    Compare MapReduce vs Spark for the same data processing task.
    
    Args:
        spark: Spark session
        df: Spark DataFrame with sales data
    """
    print("\n" + "=" * 70)
    print("MapReduce vs Spark Performance Comparison")
    print("=" * 70)
    
    # Task: Calculate total revenue by category
    print("\nTask: Calculate total revenue by product category")
    
    # Spark implementation (in-memory, optimized)
    print("\n1. Spark Implementation (DataFrame API):")
    start_time = time.time()
    
    spark_result = df.groupBy("product_category") \
        .agg(spark_sum(col("quantity") * col("price")).alias("revenue")) \
        .orderBy(col("revenue").desc()) \
        .collect()
    
    spark_time = time.time() - start_time
    
    print(f"   Execution time: {spark_time:.2f} seconds")
    print(f"   Results:")
    for row in spark_result[:3]:  # Show top 3
        print(f"     {row['product_category']}: ${row['revenue']:,.2f}")
    
    # Simulate MapReduce approach (conceptual)
    print("\n2. MapReduce Implementation (conceptual):")
    print("   - Map phase: Emit (category, quantity * price) for each transaction")
    print("   - Shuffle phase: Group by category")
    print("   - Reduce phase: Sum values for each category")
    print("   - Would require: HDFS read, disk I/O, network shuffle")
    
    # Performance comparison
    print("\n3. Performance Comparison for 8GB RAM:")
    print("   Spark advantages:")
    print("   - In-memory processing (faster for iterative algorithms)")
    print("   - Catalyst optimizer (query optimization)")
    print("   - Tungsten engine (memory and CPU efficiency)")
    print("   - DataFrame API (declarative, easier to write)")
    
    print("\n   MapReduce advantages:")
    print("   - Better fault tolerance (recomputes failed tasks)")
    print("   - Handles datasets larger than memory (spills to disk)")
    print("   - Simpler model for batch processing")
    
    print("\n   Recommendation for 8GB RAM:")
    print("   - Use Spark for interactive analytics and ML")
    print("   - Use MapReduce for very large batch jobs (> memory)")
    print("   - Always monitor memory usage with spark.ui.port=4040")

def demonstrate_spark_sql_with_hive(spark):
    """
    Demonstrate Spark SQL integration with Hive metastore.
    
    Args:
        spark: Spark session
    """
    print("\n" + "=" * 70)
    print("Spark SQL with Hive Integration")
    print("=" * 70)
    
    # Create a temporary view
    print("\n1. Creating temporary view for SQL queries:")
    spark.sql("CREATE DATABASE IF NOT EXISTS spark_demo")
    spark.sql("USE spark_demo")
    
    # Create a sample table
    sample_data = [
        (1, "Alice", "Engineering", 75000),
        (2, "Bob", "Sales", 65000),
        (3, "Charlie", "Marketing", 60000),
        (4, "Diana", "Engineering", 80000),
        (5, "Eve", "Sales", 70000)
    ]
    
    sample_df = spark.createDataFrame(
        sample_data,
        ["id", "name", "department", "salary"]
    )
    
    # Save as Hive table
    sample_df.write.mode("overwrite").saveAsTable("spark_demo.employees")
    
    print("   Created Hive table: spark_demo.employees")
    
    # Query using Spark SQL
    print("\n2. Querying with Spark SQL:")
    
    # Complex SQL query
    query = """
    SELECT 
        department,
        COUNT(*) as employee_count,
        AVG(salary) as avg_salary,
        PERCENTILE(salary, 0.5) as median_salary
    FROM spark_demo.employees
    GROUP BY department
    ORDER BY avg_salary DESC
    """
    
    result = spark.sql(query)
    print("   Department salary analysis:")
    result.show(truncate=False)
    
    # Join with other data
    print("\n3. Demonstrating SQL joins:")
    # Create another table
    dept_budget_data = [
        ("Engineering", 1000000),
        ("Sales", 800000),
        ("Marketing", 600000)
    ]
    
    dept_budget_df = spark.createDataFrame(
        dept_budget_data,
        ["department", "annual_budget"]
    )
    
    dept_budget_df.createOrReplaceTempView("department_budgets")
    
    join_query = """
    SELECT 
        e.department,
        COUNT(e.id) as headcount,
        AVG(e.salary) as avg_salary,
        SUM(e.salary) as total_salary_cost,
        b.annual_budget,
        (b.annual_budget - SUM(e.salary)) as budget_remaining
    FROM spark_demo.employees e
    JOIN department_budgets b ON e.department = b.department
    GROUP BY e.department, b.annual_budget
    """
    
    join_result = spark.sql(join_query)
    print("   Department budget analysis:")
    join_result.show(truncate=False)

def optimization_tips_for_8gb_ram():
    """
    Provide optimization tips for running Spark on 8GB RAM.
    """
    print("\n" + "=" * 70)
    print("Spark Optimization for 8GB RAM")
    print("=" * 70)
    
    print("\n1. Memory Configuration:")
    print("   spark.driver.memory=2g          # Leave room for OS and Hadoop")
    print("   spark.executor.memory=2g        # Per executor memory")
    print("   spark.memory.fraction=0.6       # Lower if experiencing OOM")
    print("   spark.memory.storageFraction=0.3  # Balance storage/execution")
    
    print("\n2. Execution Configuration:")
    print("   spark.sql.shuffle.partitions=4  # Fewer partitions = less memory")
    print("   spark.default.parallelism=4     # Match CPU cores")
    print("   spark.locality.wait=0s          # Faster task scheduling")
    
    print("\n3. Data Processing Tips:")
    print("   - Use .cache() selectively (monitor memory)")
    print("   - Use .persist(StorageLevel.MEMORY_AND_DISK) for large datasets")
    print("   - Filter early with .where() before joins")
    print("   - Use columnar formats (Parquet/ORC) for storage")
    
    print("\n4. Monitoring:")
    print("   - Access Spark UI at http://localhost:4040")
    print("   - Monitor storage memory usage")
    print("   - Check GC pauses in logs")
    print("   - Use spark.sparkContext.getExecutorMemoryStatus to check memory")

def main():
    """
    Main tutorial function demonstrating Hadoop-Spark integration.
    """
    print("=" * 70)
    print("Hadoop-Spark Integration Tutorial")
    print("=" * 70)
    
    # Create optimized Spark session
    spark = create_spark_session()
    
    # Generate sample data to HDFS
    hdfs_path = generate_sample_data_to_hdfs(spark, num_records=5000)
    
    # Demonstrate Spark-HDFS integration
    df = demonstrate_spark_hdfs_integration(spark, hdfs_path)
    
    # Compare MapReduce vs Spark
    compare_mapreduce_vs_spark(spark, df)
    
    # Demonstrate Spark SQL with Hive
    demonstrate_spark_sql_with_hive(spark)
    
    # Provide optimization tips
    optimization_tips_for_8gb_ram()
    
    # Cleanup
    print(f"\n🧹 Cleaning Up:")
    try:
        spark.sql("DROP DATABASE IF EXISTS spark_demo CASCADE")
        print("   Dropped Spark demo database")
    except:
        pass
    
    # Stop Spark session
    spark.stop()
    print("   Stopped Spark session")
    
    print("\n" + "=" * 70)
    print("✅ Hadoop-Spark Integration Tutorial Completed!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Spark provides faster in-memory processing vs MapReduce")
    print("2. Spark can read/write directly from/to HDFS")
    print("3. Spark SQL integrates with Hive metastore for unified metadata")
    print("4. For 8GB RAM: optimize memory settings and partition counts")
    print("5. Use columnar formats (Parquet) for better performance")

if __name__ == "__main__":
    main()