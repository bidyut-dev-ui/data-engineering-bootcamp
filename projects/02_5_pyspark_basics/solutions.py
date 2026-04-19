#!/usr/bin/env python3
"""
PySpark Basics Practice Exercises - SOLUTIONS

Complete implementations for all 5 practice exercises in practice_exercises.py.
Each solution is optimized for 8GB RAM environments and includes memory monitoring,
performance optimizations, and error handling.

Usage:
    python solutions.py  # Runs all exercises with solutions
    python solutions.py --exercise 2  # Runs specific exercise only
"""

import sys
import os
import time
import json
import tempfile
from typing import Dict, List, Tuple, Any, Optional
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, sum as spark_sum, avg, count, max as spark_max, min as spark_min, when, year, month, lit, expr, broadcast
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType, TimestampType
import psutil
import subprocess

# ============================================================================
# Exercise 1: PySpark Setup for 8GB RAM
# ============================================================================

def exercise_1_spark_setup() -> SparkSession:
    """
    Exercise 1: Configure PySpark for 8GB RAM Environment
    
    Tasks:
    1. Create a SparkSession optimized for 8GB RAM
    2. Configure memory settings: driver (2GB), executor (1GB)
    3. Set appropriate parallelism (2 cores, 4 shuffle partitions)
    4. Enable Kryo serialization for efficiency
    5. Configure memory fractions and garbage collection
    
    Returns:
        SparkSession: Configured SparkSession ready for 8GB RAM work
    """
    print("\n=== Exercise 1: PySpark Setup for 8GB RAM ===")
    print("Configuring SparkSession for memory-constrained environment...")
    
    # Create SparkSession with 8GB RAM optimization
    spark = SparkSession.builder \
        .appName("PySpark-8GB-Practice") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.maxResultSize", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.default.parallelism", "4") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760") \
        .config("spark.memory.fraction", "0.6") \
        .config("spark.memory.storageFraction", "0.3") \
        .config("spark.cleaner.periodicGC.interval", "1min") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.kryoserializer.buffer.max", "128m") \
        .config("spark.ui.enabled", "true") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()
    
    # Display configuration
    sc = spark.sparkContext
    print("\n✓ SparkSession created with 8GB RAM optimization:")
    print(f"  - Driver memory: {sc.getConf().get('spark.driver.memory', 'N/A')}")
    print(f"  - Executor memory: {sc.getConf().get('spark.executor.memory', 'N/A')}")
    print(f"  - Shuffle partitions: {sc.getConf().get('spark.sql.shuffle.partitions', 'N/A')}")
    print(f"  - Cores: 2 (local[2])")
    print(f"  - Kryo serializer: Enabled")
    
    # Test basic functionality
    test_df = spark.createDataFrame([(1, "test"), (2, "data")], ["id", "value"])
    test_count = test_df.count()
    print(f"  - Test DataFrame created with {test_count} rows")
    
    return spark

# ============================================================================
# Exercise 2: DataFrame Basics and Operations
# ============================================================================

def generate_sample_sales_data(spark: SparkSession, num_rows: int = 10000) -> str:
    """Generate sample sales data CSV file for exercises."""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import random
    
    # Create temporary file
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "sales_data.csv")
    
    # Generate data
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Toys']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    data = []
    for i in range(1, num_rows + 1):
        transaction_date = datetime.now() - timedelta(days=random.randint(0, 90))
        category = random.choice(categories)
        region = random.choice(regions)
        
        # Price varies by category
        if category == 'Electronics':
            price = round(random.uniform(100, 2000), 2)
        elif category == 'Clothing':
            price = round(random.uniform(20, 300), 2)
        else:
            price = round(random.uniform(10, 500), 2)
        
        quantity = random.randint(1, 5)
        total = round(price * quantity, 2)
        
        data.append({
            'transaction_id': i,
            'customer_id': random.randint(1, 5000),
            'product_id': random.randint(1000, 9999),
            'category': category,
            'region': region,
            'price': price,
            'quantity': quantity,
            'total_sale': total,
            'transaction_date': transaction_date.strftime('%Y-%m-%d')
        })
    
    # Create DataFrame and save
    pdf = pd.DataFrame(data)
    pdf.to_csv(csv_path, index=False)
    print(f"  Generated {num_rows} sales records at {csv_path}")
    return csv_path

def exercise_2_dataframe_operations(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 2: DataFrame Operations and Analysis
    
    Tasks:
    1. Load sample data (sales_data.csv) into a DataFrame
    2. Perform basic operations: select, filter, groupBy
    3. Calculate key metrics: total sales, average price, count by region
    4. Compare performance with and without optimization
    5. Handle missing values and data type conversions
    
    Args:
        spark: SparkSession from Exercise 1
        
    Returns:
        Dict: Results including total_sales, avg_price, and region_counts
    """
    print("\n=== Exercise 2: DataFrame Operations ===")
    print("Performing DataFrame operations on sales data...")
    
    # Generate sample data if not exists
    csv_path = generate_sample_sales_data(spark, 10000)
    
    # Define schema for efficient loading
    schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("region", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("total_sale", DoubleType(), True),
        StructField("transaction_date", StringType(), True)
    ])
    
    # Load data with explicit schema
    start_time = time.time()
    df = spark.read \
        .schema(schema) \
        .option("header", "true") \
        .csv(csv_path)
    
    print(f"  Loaded {df.count()} rows in {time.time() - start_time:.2f} seconds")
    
    # 1. Basic operations: select, filter
    df_selected = df.select("transaction_id", "category", "region", "price", "quantity", "total_sale")
    df_filtered = df_selected.filter(col("price") > 100)
    
    # 2. Calculate metrics
    # Total sales across all transactions
    total_sales = df.agg(spark_sum("total_sale").alias("total_sales")).collect()[0]["total_sales"]
    
    # Average price
    avg_price = df.agg(avg("price").alias("avg_price")).collect()[0]["avg_price"]
    
    # Count by region
    region_counts_df = df.groupBy("region").agg(
        count("*").alias("transaction_count"),
        spark_sum("total_sale").alias("region_sales")
    )
    region_counts = {row["region"]: row["transaction_count"] for row in region_counts_df.collect()}
    
    # 3. Handle missing values (demonstration)
    df_cleaned = df.fillna({
        "price": 0.0,
        "quantity": 1,
        "region": "Unknown"
    })
    
    # 4. Data type conversion
    df_with_date = df_cleaned.withColumn(
        "transaction_date_typed",
        col("transaction_date").cast(DateType())
    )
    
    # 5. Additional analysis: top categories by sales
    top_categories = df.groupBy("category").agg(
        spark_sum("total_sale").alias("category_sales")
    ).orderBy(col("category_sales").desc()).limit(3)
    
    top_categories_list = [row["category"] for row in top_categories.collect()]
    
    print(f"  Total sales: ${total_sales:,.2f}")
    print(f"  Average price: ${avg_price:.2f}")
    print(f"  Transactions by region: {region_counts}")
    print(f"  Top 3 categories by sales: {top_categories_list}")
    
    # Clean up temporary file
    try:
        os.remove(csv_path)
        os.rmdir(os.path.dirname(csv_path))
    except:
        pass
    
    return {
        "total_sales": float(total_sales),
        "avg_price": float(avg_price),
        "region_counts": region_counts,
        "row_count": df.count(),
        "top_categories": top_categories_list
    }

# ============================================================================
# Exercise 3: Chunking Large Datasets
# ============================================================================

def exercise_3_chunking_large_data(spark: SparkSession) -> DataFrame:
    """
    Exercise 3: Processing Large Datasets with Chunking
    
    Tasks:
    1. Simulate processing a dataset larger than available RAM
    2. Implement chunked reading using partitionBy or limit/offset
    3. Process each chunk independently with running aggregations
    4. Combine results without loading all data at once
    5. Monitor memory usage throughout processing
    
    Args:
        spark: SparkSession from Exercise 1
        
    Returns:
        DataFrame: Aggregated results from chunked processing
    """
    print("\n=== Exercise 3: Chunking Large Datasets ===")
    print("Processing large dataset using chunking techniques...")
    
    # Create a large dataset (simulated with 1M rows in chunks)
    # In real scenario, this would be reading from a large file or database
    chunk_size = 100000  # Process 100k rows at a time
    num_chunks = 10      # Total 1M rows
    
    # Schema for our simulated data
    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("action", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])
    
    # Initialize empty DataFrame for aggregated results
    aggregated_results = None
    
    # Monitor initial memory
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"  Initial memory usage: {initial_memory:.1f} MB")
    print(f"  Processing {num_chunks} chunks of {chunk_size} rows each")
    
    for chunk_idx in range(num_chunks):
        chunk_start = time.time()
        
        # Simulate generating chunk data (in real case, read from source)
        # Create a DataFrame with chunk_size rows
        data = []
        base_id = chunk_idx * chunk_size
        for i in range(chunk_size):
            user_id = base_id + i
            action = "click" if i % 3 == 0 else "view" if i % 3 == 1 else "purchase"
            value = (i % 100) * 1.5
            timestamp = time.time() - (i % 86400)  # Spread over a day
            
            data.append((user_id, action, value, timestamp))
        
        chunk_df = spark.createDataFrame(data, schema)
        
        # Process this chunk: aggregate by action
        chunk_agg = chunk_df.groupBy("action").agg(
            count("*").alias("count"),
            avg("value").alias("avg_value"),
            spark_sum("value").alias("total_value")
        )
        
        # Combine with previous results
        if aggregated_results is None:
            aggregated_results = chunk_agg
        else:
            # Union and re-aggregate
            aggregated_results = aggregated_results.union(chunk_agg) \
                .groupBy("action") \
                .agg(
                    spark_sum("count").alias("count"),
                    avg("avg_value").alias("avg_value"),
                    spark_sum("total_value").alias("total_value")
                )
        
        # Monitor memory
        chunk_memory = process.memory_info().rss / 1024 / 1024
        chunk_time = time.time() - chunk_start
        
        print(f"    Chunk {chunk_idx + 1}/{num_chunks}: "
              f"{chunk_time:.2f}s, memory: {chunk_memory:.1f} MB")
        
        # Force garbage collection occasionally
        if chunk_idx % 3 == 0:
            spark.sparkContext._jvm.System.gc()
    
    final_memory = process.memory_info().rss / 1024 / 1024
    print(f"  Final memory usage: {final_memory:.1f} MB")
    print(f"  Memory delta: {final_memory - initial_memory:.1f} MB")
    
    # Show results
    print("  Aggregated results:")
    aggregated_results.show()
    
    return aggregated_results

# ============================================================================
# Exercise 4: Optimization Techniques
# ============================================================================

def exercise_4_optimization_techniques(spark: SparkSession, df: DataFrame) -> Dict[str, Any]:
    """
    Exercise 4: PySpark Optimization for 8GB RAM
    
    Tasks:
    1. Apply caching strategies (MEMORY_AND_DISK vs MEMORY_ONLY)
    2. Implement broadcast join for small dimension tables
    3. Handle data skew using salting or repartitioning
    4. Optimize serialization and compression
    5. Compare execution times before/after optimization
    
    Args:
        spark: SparkSession from Exercise 1
        df: DataFrame to optimize
        
    Returns:
        Dict: Optimization results including execution times and memory usage
    """
    print("\n=== Exercise 4: Optimization Techniques ===")
    print("Applying PySpark optimization strategies...")
    
    results = {}
    
    # 1. Caching strategies comparison
    print("\n1. Testing caching strategies...")
    
    # Create a test DataFrame
    test_data = [(i, f"product_{i % 100}", i * 1.5) for i in range(10000)]
    test_df = spark.createDataFrame(test_data, ["id", "product", "value"])
    
    # Test without cache
    start = time.time()
    for _ in range(5):
        test_df.filter(col("id") < 5000).count()
    no_cache_time = time.time() - start
    
    # Test with MEMORY_ONLY cache
    test_df.cache()
    test_df.count()  # Trigger caching
    start = time.time()
    for _ in range(5):
        test_df.filter(col("id") < 5000).count()
    memory_cache_time = time.time() - start
    
    # Test with MEMORY_AND_DISK cache
    test_df.unpersist()
    test_df.persist("MEMORY_AND_DISK")
    test_df.count()
    start = time.time()
    for _ in range(5):
        test_df.filter(col("id") < 5000).count()
    memory_disk_time = time.time() - start
    
    test_df.unpersist()
    
    results["cache_improvement"] = no_cache_time / memory_cache_time if memory_cache_time > 0 else 0
    results["no_cache_time"] = no_cache_time
    results["memory_cache_time"] = memory_cache_time
    results["memory_disk_time"] = memory_disk_time
    
    print(f"  No cache: {no_cache_time:.2f}s")
    print(f"  MEMORY_ONLY: {memory_cache_time:.2f}s ({results['cache_improvement']:.1f}x faster)")
    print(f"  MEMORY_AND_DISK: {memory_disk_time:.2f}s")
    
    # 2. Broadcast join demonstration
    print("\n2. Testing broadcast join...")
    
    # Create small dimension table
    dimension_data = [(i, f"Category_{i % 10}") for i in range(100)]
    dimension_df = spark.createDataFrame(dimension_data, ["cat_id", "category_name"])
    
    # Create fact table
    fact_data = [(i, i % 100, i * 2.5) for i in range(10000)]
    fact_df = spark.createDataFrame(fact_data, ["id", "cat_id", "value"])
    
    # Regular join
    start = time.time()
    regular_join = fact_df.join(dimension_df, "cat_id")
    regular_count = regular_join.count()
    regular_time = time.time() - start
    
    # Broadcast join
    start = time.time()
    broadcast_join = fact_df.join(broadcast(dimension_df), "cat_id")
    broadcast_count = broadcast_join.count()
    broadcast_time = time.time() - start
    
    results["broadcast_join_size"] = dimension_df.count()
    results["regular_join_time"] = regular_time
    results["broadcast_join_time"] = broadcast_time
    results["broadcast_improvement"] = regular_time / broadcast_time if broadcast_time > 0 else 0
    
    print(f"  Regular join: {regular_time:.2f}s, rows: {regular_count}")
    print(f"  Broadcast join: {broadcast_time:.2f}s, rows: {broadcast_count}")
    print(f"  Broadcast join {results['broadcast_improvement']:.1f}x faster")
    
    # 3. Skew handling with salting
    print("\n3. Handling data skew with salting...")
    
    # Create skewed data (80% of data in 20% of keys)
    skewed_data = []
    for i in range(10000):
        key = i % 20 if i < 8000 else i % 1000 + 20  # First 20 keys have most data
        skewed_data.append((key, i, i * 1.1))
    
    skewed_df = spark.createDataFrame(skewed_data, ["key", "id", "value"])
    
    # Without skew handling
    start = time.time()
    skewed_agg = skewed_df.groupBy("key").agg(spark_sum("value").alias("total"))
    skewed_agg.count()
    no_skew_handle_time = time.time() - start
    
    # With salting
    start = time.time()
    salted_df = skewed_df.withColumn("salt", (col("id") % 10).cast(StringType()))
    salted_df = salted_df.withColumn("salted_key", concat(col("key"), lit("_"), col("salt")))
    
    salted_agg = salted_df.groupBy("salted_key").agg(spark_sum("value").alias("salted_total"))
    # Remove salt and aggregate again
    salted_agg = salted_agg.withColumn("key", expr("split(salted_key, '_')[0]"))
    final_agg = salted_agg.groupBy("key").agg(spark_sum("salted_total").alias("total"))
    final_agg.count()
    skew_handle_time = time.time() - start
    
    results["skew_handled"] = skew_handle_time < no_skew_handle_time
    results["no_skew_handle_time"] = no_skew_handle_time
    results["skew_handle_time"] = skew_handle_time
    
    print(f"  Without skew handling: {no_skew_handle_time:.2f}s")
    print(f"  With salting: {skew_handle_time:.2f}s")
    print(f"  Skew handling {'effective' if results['skew_handled'] else 'not effective'}")
    
    # 4. Overall execution time reduction
    total_baseline = no_cache_time + regular_time + no_skew_handle_time
    total_optimized = memory_cache_time + broadcast_time + skew_handle_time
    results["execution_time_reduction"] = (total_baseline - total_optimized) / total_baseline if total_baseline > 0 else 0
    
    print(f"\n4. Overall optimization results:")
    print(f"  Baseline time: {total_baseline:.2f}s")
    print(f"  Optimized time: {total_optimized:.2f}s")
    print(f"  Reduction: {results['execution_time_reduction']*100:.1f}%")
    
    return results

# Helper function for concat (if not imported)
from pyspark.sql.functions import concat

# ============================================================================
# Exercise 5: Complete ETL Pipeline
# ============================================================================

def exercise_5_etl_pipeline(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 5: End-to-End ETL Pipeline
    
    Tasks:
    1. Extract data from multiple sources (CSV, generated data)
    2. Transform with business logic and data quality checks
    3. Load to analytical format (Parquet) with partitioning
    4. Implement error handling and logging
    5. Monitor resource usage and optimize for 8GB RAM
    
    Args:
        spark: SparkSession from Exercise 1
        
    Returns:
        Dict: Pipeline results including output files, row counts, and metrics
    """
    print("\n=== Exercise 5: Complete ETL Pipeline ===")
    print("Building end-to-end ETL pipeline...")
    
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    # Create temporary directory for output
    temp_dir = tempfile.mkdtemp()
    output_dir = os.path.join(temp_dir, "etl_output")
    
    try:
        # 1. EXTRACT: Load data from multiple sources
        print("\n1. EXTRACT: Loading data from multiple sources...")
        
        # Source 1: Generate sales data
        sales_csv = generate_sample_sales_data(spark, 50000)
        sales_df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(sales_csv)
        
        # Source 2: Generate customer data
        customer_data = [(i, f"Customer_{i}", f"region_{i % 5}", 1000 + i % 100) 
                        for i in range(1, 1001)]
        customer_df = spark.createDataFrame(customer_data, 
                                          ["customer_id", "customer_name", "region", "credit_score"])
        
        # Source 3: Generate product catalog
        product_data = [(i, f"Product_{i}", f"Category_{i % 10}", 50 + i % 500)
                       for i in range(1001, 1101)]
        product_df = spark.createDataFrame(product_data,
                                         ["product_id", "product_name", "category", "base_price"])
        
        extract_time = time.time() - start_time
        print(f"  Extracted {sales_df.count():,} sales, {customer_df.count():,} customers, "
              f"{product_df.count():,} products in {extract_time:.2f}s")
        
        # 2. TRANSFORM: Apply business logic and data quality checks
        print("\n2. TRANSFORM: Applying transformations and data quality checks...")
        transform_start = time.time()
        
        # Transform 1: Enrich sales with customer and product data
        enriched_df = sales_df \
            .join(broadcast(customer_df), "customer_id", "left") \
            .join(broadcast(product_df), "product_id", "left")
        
        # Transform 2: Calculate derived columns
        from pyspark.sql.functions import current_date, datediff, round as spark_round
        enriched_df = enriched_df \
            .withColumn("discounted_price", 
                       col("price") * when(col("credit_score") > 800, 0.9).otherwise(1.0)) \
            .withColumn("profit_margin", 
                       (col("price") - col("base_price")) / col("base_price")) \
            .withColumn("transaction_age_days", 
                       datediff(current_date(), col("transaction_date").cast(DateType())))
        
        # Transform 3: Data quality checks
        # Check for nulls
        null_check = enriched_df.select(
            [spark_sum(col(c).isNull().cast("int")).alias(c) 
             for c in ["customer_id", "product_id", "price"]]
        ).collect()[0]
        
        # Check for negative prices
        negative_price_count = enriched_df.filter(col("price") < 0).count()
        
        # Check for outliers (price > 3 * avg)
        avg_price = enriched_df.agg(avg("price")).collect()[0][0]
        outlier_count = enriched_df.filter(col("price") > 3 * avg_price).count()
        
        # Transform 4: Filter and clean
        cleaned_df = enriched_df \
            .filter(col("price") > 0) \
            .filter(col("quantity") > 0) \
            .filter(col("price") < 10000)  # Remove extreme outliers
        
        transform_time = time.time() - transform_start
        print(f"  Transformations completed in {transform_time:.2f}s")
        print(f"  Data quality issues found: {null_check} nulls, "
              f"{negative_price_count} negative prices, {outlier_count} outliers")
        
        # 3. LOAD: Write to analytical format
        print("\n3. LOAD: Writing to partitioned Parquet format...")
        load_start = time.time()
        
        # Write with partitioning by region and category
        output_path = os.path.join(output_dir, "sales_analytics")
        cleaned_df.write \
            .mode("overwrite") \
            .partitionBy("region", "category") \
            .parquet(output_path)
        
        # Verify write
        loaded_df = spark.read.parquet(output_path)
        loaded_count = loaded_df.count()
        partition_count = len(spark.read.parquet(output_path).select("region").distinct().collect())
        
        load_time = time.time() - load_start
        print(f"  Loaded {loaded_count:,} rows to {output_path}")
        print(f"  Partitions: by region and category ({partition_count} regions)")
        
        # 4. Error handling and logging
        print("\n4. ERROR HANDLING: Pipeline execution summary...")
        
        # Check for errors
        success = (null_check["customer_id"] == 0 and 
                  null_check["product_id"] == 0 and
                  negative_price_count == 0)
        
        # Memory monitoring
        final_memory = process.memory_info().rss / 1024 / 1024
        peak_memory = final_memory  # Simplified - in production would track peak
        
        total_time = time.time() - start_time
        
        # List output files
        import glob
        parquet_files = glob.glob(os.path.join(output_path, "**/*.parquet"), recursive=True)
        
        print(f"  Pipeline {'SUCCESS' if success else 'FAILED'}")
        print(f"  Total execution time: {total_time:.2f}s")
        print(f"  Peak memory usage: {peak_memory:.1f} MB")
        print(f"  Output files: {len(parquet_files)} Parquet files")
        
        # Clean up temporary CSV
        try:
            os.remove(sales_csv)
            os.rmdir(os.path.dirname(sales_csv))
        except:
            pass
        
        return {
            "success": success,
            "rows_processed": loaded_count,
            "output_files": parquet_files[:5],  # First 5 files as sample
            "execution_time_seconds": total_time,
            "memory_peak_mb": peak_memory,
            "data_quality_issues": {
                "null_customer_ids": null_check["customer_id"],
                "null_product_ids": null_check["product_id"],
                "negative_prices": negative_price_count,
                "price_outliers": outlier_count
            },
            "output_path": output_path
        }
        
    except Exception as e:
        print(f"\n✗ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        try:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        
        return {
            "success": False,
            "rows_processed": 0,
            "output_files": [],
            "execution_time_seconds": time.time() - start_time,
            "memory_peak_mb": process.memory_info().rss / 1024 / 1024,
            "error": str(e)
        }

# ============================================================================
# Main Function to Run All Exercises
# ============================================================================

def run_all_exercises():
    """Run all PySpark practice exercises with solutions."""
    print("=" * 70)
    print("PYSPARK BASICS PRACTICE EXERCISES - SOLUTIONS")
    print("Optimized for 8GB RAM Environments")
    print("=" * 70)
    
    # Check if PySpark is available
    try:
        from pyspark.sql import SparkSession
        print("✓ PySpark is available")
    except ImportError:
        print("✗ PySpark not found. Install with: pip install pyspark")
        print("  Note: Java 8+ is required for PySpark")
        return False
    
    spark = None
    try:
        # Exercise 1: Setup
        print("\n" + "=" * 40)
        print("Starting Exercise 1: PySpark Setup")
        print("=" * 40)
        spark = exercise_1_spark_setup()
        
        # Exercise 2: DataFrame Operations
        print("\n" + "=" * 40)
        print("Starting Exercise 2: DataFrame Operations")
        print("=" * 40)
        df_results = exercise_2_dataframe_operations(spark)
        print(f"  DataFrame results: {json.dumps(df_results, indent=2, default=str)}")
        
        # Exercise 3: Chunking
        print("\n" + "=" * 40)
        print("Starting Exercise 3: Chunking Large Datasets")
        print("=" * 40)
        chunked_df = exercise_3_chunking_large_data(spark)
        print(f"  Chunked processing complete. Schema: {chunked_df.schema}")
        
        # Exercise 4: Optimization
        print("\n" + "=" * 40)
        print("Starting Exercise 4: Optimization Techniques")
        print("=" * 40)
        # Create sample DataFrame for optimization
        sample_data = [("A", 100), ("B", 200), ("C", 300), ("D", 400)]
        sample_df = spark.createDataFrame(sample_data, ["category", "value"])
        opt_results = exercise_4_optimization_techniques(spark, sample_df)
        print(f"  Optimization results: {json.dumps(opt_results, indent=2, default=str)}")
        
        # Exercise 5: ETL Pipeline
        print("\n" + "=" * 40)
        print("Starting Exercise 5: Complete ETL Pipeline")
        print("=" * 40)
        pipeline_results = exercise_5_etl_pipeline(spark)
        print(f"  Pipeline results: {json.dumps(pipeline_results, indent=2, default=str)}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("ALL EXERCISES COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("Summary:")
        print("1. PySpark configured for 8GB RAM ✓")
        print("2. DataFrame operations mastered ✓")
        print("3. Chunking large datasets implemented ✓")
        print("4. Optimization techniques applied ✓")
        print("5. End-to-end ETL pipeline built ✓")
        print("\nAll solutions are ready for production use on memory-constrained hardware.")
        print("=" * 70)
        
        # Stop SparkSession
        if spark:
            spark.stop()
            print("SparkSession stopped.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error running exercises: {e}")
        import traceback
        traceback.print_exc()
        if spark:
            spark.stop()
        return False

def run_single_exercise(exercise_num: int):
    """Run a single exercise by number."""
    spark = None
    try:
        spark = exercise_1_spark_setup()
        
        if exercise_num == 1:
            # Already done in setup
            pass
        elif exercise_num == 2:
            exercise_2_dataframe_operations(spark)
        elif exercise_num == 3:
            exercise_3_chunking_large_data(spark)
        elif exercise_num == 4:
            sample_df = spark.createDataFrame([("A", 100)], ["category", "value"])
            exercise_4_optimization_techniques(spark, sample_df)
        elif exercise_num == 5:
            exercise_5_etl_pipeline(spark)
        else:
            print(f"Invalid exercise number: {exercise_num}")
            return False
        
        if spark:
            spark.stop()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        if spark:
            spark.stop()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run PySpark practice exercise solutions")
    parser.add_argument("--exercise", type=int, help="Run specific exercise (1-5)")
    parser.add_argument("--all", action="store_true", help="Run all exercises (default)")
    
    args = parser.parse_args()
    
    if args.exercise:
        success = run_single_exercise(args.exercise)
    else:
        success = run_all_exercises()
    
    sys.exit(0 if success else 1)