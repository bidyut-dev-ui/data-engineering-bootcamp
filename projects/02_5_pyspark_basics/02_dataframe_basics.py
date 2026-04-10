#!/usr/bin/env python3
"""
PySpark DataFrame Basics

Learn PySpark DataFrame operations with comparisons to Pandas.
Focus on memory-efficient operations for 8GB RAM.
"""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, max, min, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
import pandas as pd

def create_spark_session():
    """Create optimized SparkSession for 8GB RAM."""
    return SparkSession.builder \
        .appName("DataFrame-Basics") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

def compare_pandas_pyspark():
    """Compare Pandas vs PySpark syntax and performance."""
    
    print("\n" + "="*60)
    print("Pandas vs PySpark Comparison")
    print("="*60)
    
    # Sample data
    data = [
        ("Alice", 34, "Engineering", 75000),
        ("Bob", 45, "Sales", 65000),
        ("Charlie", 28, "Engineering", 82000),
        ("Diana", 32, "Marketing", 58000),
        ("Eve", 29, "Engineering", 78000)
    ]
    
    print("\n1. Creating DataFrames:")
    print("-" * 40)
    
    # Pandas
    print("Pandas:")
    pd_df = pd.DataFrame(data, columns=["Name", "Age", "Department", "Salary"])
    print(f"  Shape: {pd_df.shape}")
    print(f"  Memory: {pd_df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # PySpark
    spark = create_spark_session()
    spark_df = spark.createDataFrame(data, ["Name", "Age", "Department", "Salary"])
    print("\nPySpark:")
    print(f"  Count: {spark_df.count()}")
    print(f"  Partitions: {spark_df.rdd.getNumPartitions()}")
    
    print("\n2. Filtering (Age > 30):")
    print("-" * 40)
    
    # Pandas
    pd_filtered = pd_df[pd_df["Age"] > 30]
    print(f"Pandas: {len(pd_filtered)} rows")
    
    # PySpark
    spark_filtered = spark_df.filter(col("Age") > 30)
    print(f"PySpark: {spark_filtered.count()} rows")
    
    print("\n3. Aggregation (Average Salary by Department):")
    print("-" * 40)
    
    # Pandas
    pd_agg = pd_df.groupby("Department")["Salary"].mean().reset_index()
    print("Pandas result:")
    print(pd_agg)
    
    # PySpark
    spark_agg = spark_df.groupBy("Department").agg(avg("Salary").alias("avg_salary"))
    print("\nPySpark result:")
    spark_agg.show()
    
    spark.stop()
    return spark_df

def read_data_files(spark):
    """Read CSV and Parquet files, compare performance."""
    
    print("\n" + "="*60)
    print("Reading Data Files")
    print("="*60)
    
    # Read CSV
    print("\n1. Reading CSV file (sales_small.csv):")
    start = time.time()
    csv_df = spark.read.csv("data/sales_small.csv", header=True, inferSchema=True)
    csv_count = csv_df.count()
    csv_time = time.time() - start
    print(f"  Rows: {csv_count:,}")
    print(f"  Time: {csv_time:.2f} seconds")
    print(f"  Schema: {len(csv_df.columns)} columns")
    csv_df.printSchema()
    
    # Read Parquet
    print("\n2. Reading Parquet file (sales_small.parquet):")
    start = time.time()
    parquet_df = spark.read.parquet("data/sales_small.parquet")
    parquet_count = parquet_df.count()
    parquet_time = time.time() - start
    print(f"  Rows: {parquet_count:,}")
    print(f"  Time: {parquet_time:.2f} seconds")
    print(f"  Speedup: {csv_time/parquet_time:.1f}x faster than CSV")
    
    # Show sample data
    print("\n3. Sample data (first 5 rows):")
    parquet_df.show(5, truncate=False)
    
    return parquet_df

def dataframe_operations(df):
    """Demonstrate essential DataFrame operations."""
    
    print("\n" + "="*60)
    print("DataFrame Operations")
    print("="*60)
    
    # 1. Selecting columns
    print("\n1. Selecting columns:")
    selected = df.select("transaction_id", "customer_id", "category", "total_amount")
    print(f"  Selected {selected.count()} rows, {len(selected.columns)} columns")
    selected.show(3)
    
    # 2. Filtering with multiple conditions
    print("\n2. Filtering (Electronics > $500):")
    filtered = df.filter((col("category") == "Electronics") & (col("total_amount") > 500))
    print(f"  Found {filtered.count()} transactions")
    filtered.select("transaction_id", "category", "total_amount").show(5)
    
    # 3. Adding calculated column
    print("\n3. Adding calculated column (tax at 8%):")
    with_tax = df.withColumn("tax_amount", col("total_amount") * 0.08)
    with_tax.select("transaction_id", "total_amount", "tax_amount").show(5)
    
    # 4. GroupBy and Aggregation
    print("\n4. Aggregation by category:")
    agg_df = df.groupBy("category") \
               .agg(
                   count("*").alias("transaction_count"),
                   sum("total_amount").alias("total_revenue"),
                   avg("total_amount").alias("avg_transaction"),
                   max("total_amount").alias("max_transaction")
               ) \
               .orderBy(col("total_revenue").desc())
    
    agg_df.show()
    
    # 5. Window functions (rank within category)
    print("\n5. Top 3 transactions per category (using Window):")
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number
    
    window = Window.partitionBy("category").orderBy(col("total_amount").desc())
    ranked = df.withColumn("rank", row_number().over(window))
    top_per_category = ranked.filter(col("rank") <= 3)
    
    print(f"  Showing top 3 transactions per category:")
    top_per_category.select("category", "transaction_id", "total_amount", "rank").show(15)
    
    return agg_df

def join_operations(spark):
    """Demonstrate different types of joins."""
    
    print("\n" + "="*60)
    print("Join Operations")
    print("="*60)
    
    # Load datasets
    sales_df = spark.read.parquet("data/sales_small.parquet")
    customers_df = spark.read.csv("data/customers.csv", header=True, inferSchema=True)
    products_df = spark.read.csv("data/products.csv", header=True, inferSchema=True)
    
    print(f"Sales: {sales_df.count():,} rows")
    print(f"Customers: {customers_df.count():,} rows")
    print(f"Products: {products_df.count():,} rows")
    
    # 1. Inner Join
    print("\n1. Inner Join (sales + customers):")
    inner_join = sales_df.join(customers_df, "customer_id", "inner")
    print(f"  Result: {inner_join.count():,} rows (matches customer IDs)")
    
    # 2. Left Join
    print("\n2. Left Join (all sales, customer info if available):")
    left_join = sales_df.join(customers_df, "customer_id", "left")
    print(f"  Result: {left_join.count():,} rows (all sales)")
    
    # Check for nulls
    null_customers = left_join.filter(col("first_name").isNull()).count()
    print(f"  Sales without customer info: {null_customers}")
    
    # 3. Broadcast Join (for small lookup table)
    print("\n3. Broadcast Join (sales + products):")
    print("  Products table is small (14 rows) - good candidate for broadcast")
    
    # Method 1: Automatic (spark.sql.autoBroadcastJoinThreshold)
    auto_join = sales_df.join(products_df, "product_id", "left")
    
    # Method 2: Manual broadcast hint
    from pyspark.sql.functions import broadcast
    broadcast_join = sales_df.join(broadcast(products_df), "product_id", "left")
    
    print(f"  Auto join result: {auto_join.count():,} rows")
    print(f"  Broadcast join result: {broadcast_join.count():,} rows")
    
    # Show joined data
    print("\n4. Sample joined data (sales + customers + products):")
    joined_sample = inner_join.join(products_df, "product_id", "left") \
                             .select("transaction_id", "first_name", "last_name", 
                                     "product_name", "category", "total_amount") \
                             .limit(5)
    joined_sample.show(truncate=False)
    
    return inner_join

def memory_efficient_operations(spark):
    """Techniques for memory-efficient operations on 8GB RAM."""
    
    print("\n" + "="*60)
    print("Memory-Efficient Operations for 8GB RAM")
    print("="*60)
    
    df = spark.read.parquet("data/sales_large.parquet")
    print(f"Working with large dataset: {df.count():,} rows")
    
    # 1. Select only needed columns
    print("\n1. Column pruning (select only needed columns):")
    essential_cols = df.select("transaction_id", "customer_id", "category", "total_amount")
    print(f"  Reduced from {len(df.columns)} to {len(essential_cols.columns)} columns")
    
    # 2. Filter early
    print("\n2. Filter early (reduce data before operations):")
    filtered = df.filter(col("category").isin(["Electronics", "Clothing"])) \
                 .select("transaction_id", "category", "total_amount")
    print(f"  Filtered to {filtered.count():,} rows before aggregation")
    
    # 3. Use approximate functions for large datasets
    print("\n3. Approximate counting for large datasets:")
    approx_count = df.select("customer_id").distinct().count()
    print(f"  Distinct customers (exact): {approx_count:,}")
    
    # For truly large datasets, use approx_count_distinct
    from pyspark.sql.functions import approx_count_distinct
    approx_distinct = df.agg(approx_count_distinct("customer_id", rsd=0.05).alias("approx_distinct"))
    approx_result = approx_distinct.collect()[0]["approx_distinct"]
    print(f"  Distinct customers (approx, 5% error): {approx_result:,.0f}")
    
    # 4. Write intermediate results to disk
    print("\n4. Writing intermediate results (spill to disk):")
    print("  Configured via spark.memory.fraction and spark.sql.shuffle.partitions")
    print("  Spark automatically spills to disk when memory is full")
    
    # 5. Monitor memory usage
    print("\n5. Monitoring memory usage:")
    print("  Check Spark UI at http://localhost:4040")
    print("  Look for:")
    print("    - Storage Memory Used")
    print("    - Shuffle spill (memory/disk)")
    print("    - Task failures due to memory")
    
    return df

def main():
    """Main execution function."""
    
    print("="*60)
    print("PySpark DataFrame Basics Tutorial")
    print("="*60)
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Compare Pandas vs PySpark
        compare_pandas_pyspark()
        
        # Read data files
        df = read_data_files(spark)
        
        # DataFrame operations
        agg_df = dataframe_operations(df)
        
        # Join operations
        joined_df = join_operations(spark)
        
        # Memory-efficient operations
        large_df = memory_efficient_operations(spark)
        
        # Summary
        print("\n" + "="*60)
        print("✅ TUTORIAL COMPLETE!")
        print("="*60)
        print("\nYou've learned:")
        print("1. Pandas vs PySpark syntax comparison")
        print("2. Reading CSV vs Parquet files")
        print("3. Essential DataFrame operations (select, filter, agg)")
        print("4. Join operations (inner, left, broadcast)")
        print("5. Memory-efficient techniques for 8GB RAM")
        
        print("\nNext: Run 'python 03_chunking_pyspark.py' for large file processing")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Clean up
        spark.stop()
        print("\nSpark session stopped. Memory freed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())