#!/usr/bin/env python3
"""
Chunking and Partitioning in PySpark

Learn how to process large datasets on 8GB RAM using:
- Partitioning
- Chunked reading
- Incremental processing
- Memory monitoring
"""

import sys
import time
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, year, month
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

def create_spark_session():
    """Create optimized SparkSession for large file processing."""
    return SparkSession.builder \
        .appName("Chunking-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.sql.files.maxPartitionBytes", "128m") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

def process_large_file_in_chunks():
    """Demonstrate processing files larger than RAM."""
    
    print("\n" + "="*60)
    print("Processing Large Files (500K+ rows on 8GB RAM)")
    print("="*60)
    
    spark = create_spark_session()
    
    large_file = "data/sales_large.csv"
    file_size = os.path.getsize(large_file) / (1024 * 1024)  # MB
    print(f"\nFile: {large_file}")
    print(f"Size: {file_size:.2f} MB")
    print(f"Your RAM: 8GB total, 2GB for Spark driver")
    
    # Method 1: Read with partitioning
    print("\n1. Reading with automatic partitioning:")
    start = time.time()
    
    # Spark automatically partitions large files
    df = spark.read.csv(large_file, header=True, inferSchema=True)
    
    # Check partitions
    num_partitions = df.rdd.getNumPartitions()
    print(f"  Partitions created: {num_partitions}")
    print(f"  Rows per partition: ~{df.count() / num_partitions:,.0f}")
    print(f"  Read time: {time.time() - start:.2f} seconds")
    
    # Show partition distribution
    print("\n  Partition distribution:")
    partition_counts = df.rdd.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    for i, count in enumerate(partition_counts[:5]):  # Show first 5
        print(f"    Partition {i}: {count:,} rows")
    if len(partition_counts) > 5:
        print(f"    ... and {len(partition_counts) - 5} more partitions")
    
    return df, spark

def repartition_for_better_performance(df):
    """Demonstrate repartitioning strategies."""
    
    print("\n" + "="*60)
    print("Repartitioning Strategies")
    print("="*60)
    
    initial_partitions = df.rdd.getNumPartitions()
    print(f"\nInitial partitions: {initial_partitions}")
    
    # Strategy 1: Repartition by column (for groupBy operations)
    print("\n1. Repartition by category (for category-based aggregations):")
    df_repartitioned = df.repartition(8, "category")
    new_partitions = df_repartitioned.rdd.getNumPartitions()
    print(f"  New partitions: {new_partitions}")
    print(f"  Partition column: category")
    
    # Check distribution
    print("\n  Category distribution across partitions:")
    category_counts = df_repartitioned.groupBy("category").count().orderBy(col("count").desc())
    category_counts.show()
    
    # Strategy 2: Coalesce (reduce partitions)
    print("\n2. Coalesce (reduce partitions for smaller output):")
    df_coalesced = df.coalesce(2)
    print(f"  Reduced from {initial_partitions} to {df_coalesced.rdd.getNumPartitions()} partitions")
    print("  Use coalesce() when reducing partitions (no shuffle)")
    print("  Use repartition() when increasing partitions (causes shuffle)")
    
    return df_repartitioned

def incremental_processing(df):
    """Process data incrementally to save memory."""
    
    print("\n" + "="*60)
    print("Incremental Processing Patterns")
    print("="*60)
    
    # Pattern 1: Process by date ranges
    print("\n1. Process by date ranges (simulate daily batches):")
    
    # Extract unique dates
    dates = df.select("transaction_date").distinct().orderBy("transaction_date").limit(5).collect()
    date_list = [row["transaction_date"] for row in dates]
    
    print(f"  Found {len(date_list)} unique dates (showing first 5)")
    
    # Simulate daily processing
    daily_totals = []
    for date in date_list:
        daily_df = df.filter(col("transaction_date") == date)
        daily_sum = daily_df.agg(sum("total_amount").alias("daily_total")).collect()[0]["daily_total"]
        daily_count = daily_df.count()
        daily_totals.append((date, daily_count, daily_sum))
        print(f"    Date {date}: {daily_count:,} transactions, ${daily_sum:,.2f}")
    
    # Pattern 2: Process by category chunks
    print("\n2. Process by category (one category at a time):")
    
    categories = df.select("category").distinct().collect()
    category_list = [row["category"] for row in categories]
    
    category_results = []
    for category in category_list:
        category_df = df.filter(col("category") == category)
        category_stats = category_df.agg(
            count("*").alias("count"),
            sum("total_amount").alias("total"),
            avg("total_amount").alias("avg_amount")
        ).collect()[0]
        
        category_results.append((
            category,
            category_stats["count"],
            category_stats["total"],
            category_stats["avg_amount"]
        ))
        
        # Clear intermediate DataFrame to free memory
        category_df.unpersist()
    
    print("\n  Category summary:")
    for category, count, total, avg in category_results:
        print(f"    {category:15} {count:6,} rows ${total:12,.2f} total (avg ${avg:,.2f})")
    
    return daily_totals, category_results

def write_partitioned_output(df):
    """Write output in partitioned format for efficient querying."""
    
    print("\n" + "="*60)
    print("Writing Partitioned Output")
    print("="*60)
    
    # Add year and month columns for partitioning
    from pyspark.sql.functions import to_date, substring
    df_with_date = df.withColumn("transaction_year", substring(col("transaction_date"), 1, 4)) \
                     .withColumn("transaction_month", substring(col("transaction_date"), 6, 2))
    
    print("\n1. Writing with partitionBy (year/month):")
    print("  Creates directory structure: year=2024/month=01/")
    
    output_path = "data/output/partitioned_sales"
    
    # Write partitioned data
    df_with_date.write \
        .partitionBy("transaction_year", "transaction_month") \
        .mode("overwrite") \
        .parquet(output_path)
    
    # Check what was written
    print(f"\n  Output written to: {output_path}")
    
    # List partitions created
    import subprocess
    try:
        result = subprocess.run(
            ["find", output_path, "-type", "d", "-name", "year=*"],
            capture_output=True,
            text=True
        )
        partitions = result.stdout.strip().split('\n')
        print(f"  Partitions created: {len([p for p in partitions if p])}")
        
        # Show sample partition structure
        for partition in partitions[:3]:
            if partition:
                print(f"    {partition}")
        if len(partitions) > 3:
            print(f"    ... and {len(partitions) - 3} more")
            
    except:
        print("  (Could not list partitions - directory browsing not available)")
    
    # Benefits of partitioning
    print("\n2. Benefits of partitioned writing:")
    print("  - Faster queries (prune partitions)")
    print("  - Smaller files per partition")
    print("  - Easier data management")
    print("  - Better compression")
    
    return output_path

def memory_monitoring_tips():
    """Tips for monitoring and managing memory."""
    
    print("\n" + "="*60)
    print("Memory Monitoring & Management for 8GB RAM")
    print("="*60)
    
    print("\n1. Monitor memory usage:")
    print("  Command: htop (in another terminal)")
    print("  Spark UI: http://localhost:4040")
    print("  Key metrics:")
    print("    - Storage Memory Used")
    print("    - Shuffle spill (memory/disk)")
    print("    - GC time (high = memory pressure)")
    
    print("\n2. Reduce memory usage:")
    print("  - Use .select() to keep only needed columns")
    print("  - Filter early with .filter()")
    print("  - Use .persist(StorageLevel.DISK_ONLY) for intermediate results")
    print("  - Increase spark.sql.shuffle.partitions (more, smaller tasks)")
    
    print("\n3. Handle out-of-memory errors:")
    print("  - Reduce spark.driver.memory (try 1g instead of 2g)")
    print("  - Increase spark.memory.fraction (default 0.6)")
    print("  - Use .coalesce() to reduce partitions")
    print("  - Process in smaller batches")
    
    print("\n4. Checkpointing for long operations:")
    print("  spark.sparkContext.setCheckpointDir('checkpoints/')")
    print("  df.checkpoint()  # Saves to disk, breaks lineage")
    
    print("\n5. Garbage collection tuning:")
    print("  Add to spark-submit/spark-defaults.conf:")
    print("    spark.executor.extraJavaOptions=-XX:+UseG1GC")
    print("    spark.executor.extraJavaOptions=-XX:InitiatingHeapOccupancyPercent=35")

def main():
    """Main execution function."""
    
    print("="*60)
    print("PySpark Chunking & Partitioning Tutorial")
    print("="*60)
    print("\nLearn to process large datasets on 8GB RAM")
    
    spark = None
    
    try:
        # Process large file
        df, spark = process_large_file_in_chunks()
        
        # Repartitioning strategies
        df_repartitioned = repartition_for_better_performance(df)
        
        # Incremental processing
        daily_totals, category_results = incremental_processing(df)
        
        # Write partitioned output
        output_path = write_partitioned_output(df)
        
        # Memory monitoring tips
        memory_monitoring_tips()
        
        # Summary
        print("\n" + "="*60)
        print("✅ CHUNKING TUTORIAL COMPLETE!")
        print("="*60)
        
        print("\nKey techniques learned:")
        print("1. Automatic partitioning of large files")
        print("2. Repartitioning for better performance")
        print("3. Incremental processing by date/category")
        print("4. Partitioned writing for efficient storage")
        print("5. Memory monitoring for 8GB RAM")
        
        print(f"\nProcessed: {df.count():,} rows on 8GB RAM")
        print(f"Output: Partitioned Parquet files in {output_path}")
        
        print("\nNext: Run 'python 04_optimization_techniques.py' for advanced optimization")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Clean up
        if spark:
            spark.stop()
            print("\nSpark session stopped. Memory freed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())