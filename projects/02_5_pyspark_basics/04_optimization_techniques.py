#!/usr/bin/env python3
"""
PySpark Optimization Techniques for 8GB RAM

Advanced optimization strategies for memory-constrained environments:
- Caching strategies
- Broadcast joins
- Data skew handling
- Serialization optimization
"""

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast, sum, avg, count
from pyspark.storagelevel import StorageLevel

def create_optimized_spark_session():
    """Create SparkSession with optimization settings."""
    
    return SparkSession.builder \
        .appName("Optimization-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .getOrCreate()

def caching_strategies(spark):
    """Demonstrate different caching strategies."""
    
    print("\n" + "="*60)
    print("Caching Strategies")
    print("="*60)
    
    # Load data
    df = spark.read.parquet("data/sales_large.parquet")
    print(f"Dataset: {df.count():,} rows")
    
    # Strategy 1: No caching (baseline)
    print("\n1. No caching (baseline):")
    start = time.time()
    for i in range(3):
        result = df.filter(col("category") == "Electronics").count()
    no_cache_time = time.time() - start
    print(f"  3 iterations: {no_cache_time:.2f} seconds")
    
    # Strategy 2: Cache in memory
    print("\n2. Cache in memory (MEMORY_ONLY):")
    df_cached = df.filter(col("category") == "Electronics").cache()
    df_cached.count()  # Trigger caching
    
    start = time.time()
    for i in range(3):
        result = df_cached.count()
    memory_cache_time = time.time() - start
    print(f"  3 iterations: {memory_cache_time:.2f} seconds")
    print(f"  Speedup: {no_cache_time/memory_cache_time:.1f}x")
    
    # Strategy 3: Cache on disk
    print("\n3. Cache on disk (DISK_ONLY):")
    df_disk = df.filter(col("category") == "Clothing").persist(StorageLevel.DISK_ONLY)
    df_disk.count()  # Trigger caching
    
    start = time.time()
    for i in range(3):
        result = df_disk.count()
    disk_cache_time = time.time() - start
    print(f"  3 iterations: {disk_cache_time:.2f} seconds")
    
    # Strategy 4: Memory and disk
    print("\n4. Memory and disk (MEMORY_AND_DISK):")
    df_memory_disk = df.filter(col("total_amount") > 1000).persist(StorageLevel.MEMORY_AND_DISK)
    df_memory_disk.count()
    
    start = time.time()
    for i in range(3):
        result = df_memory_disk.count()
    memory_disk_time = time.time() - start
    print(f"  3 iterations: {memory_disk_time:.2f} seconds")
    
    # When to use each
    print("\n5. When to use each caching level:")
    print("  MEMORY_ONLY: Small datasets, frequent reuse")
    print("  DISK_ONLY: Large datasets, infrequent reuse")
    print("  MEMORY_AND_DISK: Medium datasets, some memory pressure")
    print("  OFF_HEAP: Advanced, requires extra configuration")
    
    # Clean up
    df_cached.unpersist()
    df_disk.unpersist()
    df_memory_disk.unpersist()
    
    return df

def broadcast_join_demo(spark):
    """Demonstrate broadcast join for small lookup tables."""
    
    print("\n" + "="*60)
    print("Broadcast Join Optimization")
    print("="*60)
    
    # Load data
    sales_df = spark.read.parquet("data/sales_large.parquet")
    products_df = spark.read.csv("data/products.csv", header=True, inferSchema=True)
    
    print(f"Sales data: {sales_df.count():,} rows")
    print(f"Products data: {products_df.count():,} rows (small lookup table)")
    
    # Regular join (shuffle join)
    print("\n1. Regular join (shuffle join):")
    start = time.time()
    regular_join = sales_df.join(products_df, "product_id", "left")
    regular_count = regular_join.count()
    regular_time = time.time() - start
    print(f"  Time: {regular_time:.2f} seconds")
    print(f"  Result: {regular_count:,} rows")
    
    # Broadcast join
    print("\n2. Broadcast join (no shuffle):")
    start = time.time()
    broadcast_join = sales_df.join(broadcast(products_df), "product_id", "left")
    broadcast_count = broadcast_join.count()
    broadcast_time = time.time() - start
    print(f"  Time: {broadcast_time:.2f} seconds")
    print(f"  Result: {broadcast_count:,} rows")
    print(f"  Speedup: {regular_time/broadcast_time:.1f}x")
    
    # Check execution plan
    print("\n3. Execution plan comparison:")
    print("  Regular join plan (simplified):")
    print("    Exchange (shuffle) -> SortMergeJoin")
    print("  Broadcast join plan:")
    print("    Broadcast -> BroadcastHashJoin")
    
    # When to use broadcast join
    print("\n4. Broadcast join guidelines:")
    print("  Use when one table is small (< spark.sql.autoBroadcastJoinThreshold)")
    print("  Default threshold: 10MB (10,485,760 bytes)")
    print("  Manual broadcast: df1.join(broadcast(df2), ...)")
    print("  Automatic: Set spark.sql.autoBroadcastJoinThreshold")
    
    return broadcast_join

def handle_data_skew(spark):
    """Techniques to handle data skew."""
    
    print("\n" + "="*60)
    print("Handling Data Skew")
    print("="*60)
    
    # Create skewed data
    print("\n1. Identifying data skew:")
    
    # Load sales data
    df = spark.read.parquet("data/sales_large.parquet")
    
    # Check distribution
    print("  Category distribution:")
    category_dist = df.groupBy("category").count().orderBy(col("count").desc())
    category_dist.show()
    
    # Find skew
    counts = [row["count"] for row in category_dist.collect()]
    if counts:
        skew_ratio = max(counts) / min(counts) if min(counts) > 0 else float('inf')
        print(f"  Skew ratio (max/min): {skew_ratio:.1f}")
        print(f"  {'High skew detected' if skew_ratio > 10 else 'Relatively balanced'}")
    
    # Technique 1: Salting for skewed joins
    print("\n2. Salting technique for skewed joins:")
    print("  Add random salt to skewed keys")
    print("  Example: category_skewed -> category_salt_1, category_salt_2")
    
    # Technique 2: Increase partitions for skewed data
    print("\n3. Increase partitions for skewed operations:")
    print("  Before aggregation:")
    print(f"    Partitions: {df.rdd.getNumPartitions()}")
    
    df_repartitioned = df.repartition(16, "category")
    print(f"  After repartition by category:")
    print(f"    Partitions: {df_repartitioned.rdd.getNumPartitions()}")
    
    # Technique 3: Two-phase aggregation
    print("\n4. Two-phase aggregation for skewed groups:")
    print("  Phase 1: Local aggregation within partitions")
    print("  Phase 2: Global aggregation")
    
    # Demonstrate with sample
    print("\n  Example - Two-phase category aggregation:")
    
    # Phase 1: Local aggregation (within partition)
    local_agg = df_repartitioned.groupBy("category").agg(
        sum("total_amount").alias("local_total"),
        count("*").alias("local_count")
    )
    
    # Phase 2: Global aggregation
    global_agg = local_agg.groupBy("category").agg(
        sum("local_total").alias("global_total"),
        sum("local_count").alias("global_count")
    )
    
    print("  Results:")
    global_agg.orderBy(col("global_total").desc()).show()
    
    # Technique 4: Adaptive Query Execution (AQE)
    print("\n5. Adaptive Query Execution (AQE):")
    print("  Enabled by default in Spark 3.0+")
    print("  Automatically handles skew with:")
    print("    - spark.sql.adaptive.skewJoin.enabled=true")
    print("    - spark.sql.adaptive.coalescePartitions.enabled=true")
    
    return df

def serialization_optimization(spark):
    """Optimize serialization for better performance."""
    
    print("\n" + "="*60)
    print("Serialization Optimization")
    print("="*60)
    
    # Default vs Kryo serialization
    print("\n1. Serialization methods:")
    print("  Java Serialization (default):")
    print("    - Simple, works with any Java object")
    print("    - Slow, large size")
    
    print("\n  Kryo Serialization (recommended):")
    print("    - Faster, smaller size")
    print("    - Requires registration of custom classes")
    
    # Enable Kryo
    print("\n2. Enabling Kryo serialization:")
    print("  In SparkSession builder:")
    print("    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer')")
    
    # Register custom classes if needed
    print("\n3. Registering custom classes for Kryo:")
    print("  .config('spark.kryo.classesToRegister', 'com.example.MyClass,com.example.OtherClass')")
    
    # Data size comparison
    print("\n4. Data size comparison:")
    
    # Create sample RDD
    data = [(i, f"item_{i}", i * 10.5) for i in range(1000)]
    rdd = spark.sparkContext.parallelize(data, 4)
    
    # Cache with different serialization
    rdd.persist(StorageLevel.MEMORY_ONLY_SER)  # Serialized in memory
    
    print(f"  RDD with {rdd.count()} elements cached with serialization")
    print("  Memory usage reduced compared to MEMORY_ONLY")
    
    # Clean up
    rdd.unpersist()
    
    # Best practices
    print("\n5. Serialization best practices:")
    print("  - Use Kryo for production workloads")
    print("  - Register custom classes for performance")
    print("  - Use MEMORY_ONLY_SER for large datasets")
    print("  - Monitor serialization time in Spark UI")

def configuration_tuning():
    """Key configuration parameters for 8GB RAM."""
    
    print("\n" + "="*60)
    print("Configuration Tuning for 8GB RAM")
    print("="*60)
    
    print("\n1. Memory configuration:")
    print("  spark.driver.memory = 2g")
    print("  spark.executor.memory = 1g")
    print("  spark.memory.fraction = 0.6")
    print("  spark.memory.storageFraction = 0.3")
    
    print("\n2. Parallelism configuration:")
    print("  spark.default.parallelism = 4")
    print("  spark.sql.shuffle.partitions = 8")
    print("  spark.sql.files.maxPartitionBytes = 128m")
    
    print("\n3. Garbage collection:")
    print("  spark.executor.extraJavaOptions = -XX:+UseG1GC")
    print("  spark.executor.extraJavaOptions = -XX:InitiatingHeapOccupancyPercent=35")
    
    print("\n4. Adaptive Query Execution (AQE):")
    print("  spark.sql.adaptive.enabled = true")
    print("  spark.sql.adaptive.coalescePartitions.enabled = true")
    print("  spark.sql.adaptive.skewJoin.enabled = true")
    
    print("\n5. Shuffle optimization:")
    print("  spark.shuffle.compress = true")
    print("  spark.shuffle.spill.compress = true")
    print("  spark.shuffle.file.buffer = 32k")

def main():
    """Main execution function."""
    
    print("="*60)
    print("PySpark Optimization Techniques for 8GB RAM")
    print("="*60)
    
    spark = create_optimized_spark_session()
    
    try:
        # Caching strategies
        df = caching_strategies(spark)
        
        # Broadcast joins
        joined_df = broadcast_join_demo(spark)
        
        # Data skew handling
        skewed_df = handle_data_skew(spark)
        
        # Serialization optimization
        serialization_optimization(spark)
        
        # Configuration tuning
        configuration_tuning()
        
        # Summary
        print("\n" + "="*60)
        print("✅ OPTIMIZATION TUTORIAL COMPLETE!")
        print("="*60)
        
        print("\nKey optimizations for 8GB RAM:")
        print("1. Caching: Choose right StorageLevel for your data size")
        print("2. Broadcast joins: For small lookup tables (<10MB)")
        print("3. Skew handling: Salting, repartitioning, two-phase aggregation")
        print("4. Serialization: Use Kryo for better performance")
        print("5. Configuration: Tune memory, parallelism, and AQE")
        
        print("\nMonitoring tools:")
        print("  - Spark UI: http://localhost:4040")
        print("  - htop: Monitor system memory")
        print("  - Spark logs: Check for GC warnings")
        
        print("\nNext: Run 'python 05_etl_pipeline.py' for complete ETL example")
        
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