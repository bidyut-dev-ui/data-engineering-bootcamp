#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 2: Memory Management & Tuning for 8GB RAM

This tutorial focuses on PySpark memory management, garbage collection tuning,
and optimization techniques for resource-constrained environments.

Key Concepts:
- Spark Memory Architecture (On-Heap vs Off-Heap)
- Garbage Collection Tuning
- Serialization Optimization (Kryo vs Java)
- Caching Strategies
- Memory Monitoring and Debugging

Optimized for 8GB RAM with detailed configuration examples.
"""

import time
import psutil
import gc
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rand, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark import StorageLevel
import pandas as pd

def create_memory_optimized_spark_session():
    """Create a SparkSession with advanced memory tuning for 8GB RAM"""
    return SparkSession.builder \
        .appName("Memory-Management-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.memory.offHeap.enabled", "true") \
        .config("spark.memory.offHeap.size", "512m") \
        .config("spark.executor.extraJavaOptions",
                "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 " +
                "-XX:ConcGCThreads=2 -XX:ParallelGCThreads=2 " +
                "-XX:MaxGCPauseMillis=200") \
        .config("spark.driver.extraJavaOptions",
                "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 " +
                "-XX:ConcGCThreads=2 -XX:ParallelGCThreads=2 " +
                "-XX:MaxGCPauseMillis=200") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.kryoserializer.buffer.max", "128m") \
        .config("spark.memory.fraction", "0.6") \
        .config("spark.memory.storageFraction", "0.5") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def generate_large_dataset(spark, num_rows=200000, num_cols=20):
    """Generate a large dataset for memory testing"""
    print(f"Generating large dataset: {num_rows:,} rows × {num_cols} columns")
    
    # Create schema with many columns
    fields = [StructField(f"col_{i}", DoubleType(), True) for i in range(num_cols)]
    fields.insert(0, StructField("id", IntegerType(), False))
    fields.insert(1, StructField("category", StringType(), True))
    schema = StructType(fields)
    
    # Generate data using pandas (simpler for demo)
    import numpy as np
    np.random.seed(42)
    
    data = {}
    data['id'] = list(range(num_rows))
    data['category'] = np.random.choice(['A', 'B', 'C', 'D', 'E'], num_rows)
    
    for i in range(num_cols):
        data[f'col_{i}'] = np.random.randn(num_rows)
    
    pdf = pd.DataFrame(data)
    df = spark.createDataFrame(pdf, schema=schema)
    
    print(f"Dataset created: {df.count():,} rows, {len(df.columns)} columns")
    print(f"Approximate size: {df.rdd.getNumPartitions()} partitions")
    
    return df

def demonstrate_memory_architecture():
    """Explain Spark memory architecture"""
    print("\n" + "="*80)
    print("SPARK MEMORY ARCHITECTURE")
    print("="*80)
    
    print("""
Spark Memory is divided into several regions:

1. **Execution Memory**: Used for shuffles, joins, sorts, and aggregations
   - Controlled by spark.memory.fraction (default: 0.6)
   - Shared between storage and execution

2. **Storage Memory**: Used for caching and broadcast variables
   - Controlled by spark.memory.storageFraction (default: 0.5 of the above)
   - Can be borrowed by execution if needed

3. **User Memory**: Reserved for user data structures
   - Remaining after execution/storage (1 - spark.memory.fraction)

4. **Reserved Memory**: System reserved (300MB)

For 8GB RAM with our configuration:
- Driver Memory: 2GB
- Executor Memory: 1GB
- Off-Heap Memory: 512MB
- Storage/Execution: 60% of heap (1.2GB driver, 600MB executor)
""")

def benchmark_serialization(df):
    """Compare Kryo vs Java serialization"""
    print("\n" + "="*80)
    print("SERIALIZATION BENCHMARK: Kryo vs Java")
    print("="*80)
    
    # Test Java serialization
    print("\n1. Java Serialization (Default):")
    spark_java = SparkSession.builder \
        .appName("Java-Serialization") \
        .master("local[2]") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "512m") \
        .config("spark.serializer", "org.apache.spark.serializer.JavaSerializer") \
        .getOrCreate()
    
    try:
        start_time = time.time()
        java_df = spark_java.createDataFrame(df.rdd, df.schema)
        java_df.cache()
        java_count = java_df.count()
        java_time = time.time() - start_time
        print(f"Count: {java_count:,} rows")
        print(f"Time: {java_time:.2f} seconds")
        print(f"Memory used: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
    finally:
        spark_java.stop()
    
    # Test Kryo serialization
    print("\n2. Kryo Serialization (Optimized):")
    spark_kryo = SparkSession.builder \
        .appName("Kryo-Serialization") \
        .master("local[2]") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "512m") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.kryoserializer.buffer.max", "128m") \
        .config("spark.kryo.registrationRequired", "false") \
        .getOrCreate()
    
    try:
        start_time = time.time()
        kryo_df = spark_kryo.createDataFrame(df.rdd, df.schema)
        kryo_df.cache()
        kryo_count = kryo_df.count()
        kryo_time = time.time() - start_time
        print(f"Count: {kryo_count:,} rows")
        print(f"Time: {kryo_time:.2f} seconds")
        print(f"Memory used: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
        
        # Calculate improvement
        improvement = ((java_time - kryo_time) / java_time) * 100
        print(f"\nPerformance Improvement: {improvement:.1f}% faster with Kryo")
    finally:
        spark_kryo.stop()

def demonstrate_caching_strategies(df):
    """Show different caching strategies and their memory impact"""
    print("\n" + "="*80)
    print("CACHING STRATEGIES COMPARISON")
    print("="*80)
    
    # Clear any existing cache
    spark.catalog.clearCache()
    
    # Strategy 1: No caching
    print("\n1. No Caching (Recompute each time):")
    start_time = time.time()
    for i in range(3):
        result = df.filter(col("category") == "A").agg({"col_0": "sum"})
        result.collect()
    no_cache_time = time.time() - start_time
    print(f"Time for 3 iterations: {no_cache_time:.2f} seconds")
    
    # Strategy 2: MEMORY_ONLY caching
    print("\n2. MEMORY_ONLY Caching:")
    df_cached = df.filter(col("category") == "A").cache()
    df_cached.count()  # Trigger caching
    
    start_time = time.time()
    for i in range(3):
        result = df_cached.agg({"col_0": "sum"})
        result.collect()
    memory_only_time = time.time() - start_time
    print(f"Time for 3 iterations: {memory_only_time:.2f} seconds")
    print(f"Storage level: {df_cached.storageLevel}")
    
    # Strategy 3: MEMORY_AND_DISK caching
    print("\n3. MEMORY_AND_DISK Caching (Spill to disk if memory full):")
    df_memory_disk = df.filter(col("category") == "B").persist(StorageLevel.MEMORY_AND_DISK)
    df_memory_disk.count()  # Trigger caching
    
    start_time = time.time()
    for i in range(3):
        result = df_memory_disk.agg({"col_1": "sum"})
        result.collect()
    memory_disk_time = time.time() - start_time
    print(f"Time for 3 iterations: {memory_disk_time:.2f} seconds")
    print(f"Storage level: {df_memory_disk.storageLevel}")
    
    # Strategy 4: DISK_ONLY caching (for very large datasets)
    print("\n4. DISK_ONLY Caching (Memory constrained):")
    df_disk = df.filter(col("category") == "C").persist(StorageLevel.DISK_ONLY)
    df_disk.count()  # Trigger caching
    
    start_time = time.time()
    for i in range(3):
        result = df_disk.agg({"col_2": "sum"})
        result.collect()
    disk_only_time = time.time() - start_time
    print(f"Time for 3 iterations: {disk_only_time:.2f} seconds")
    print(f"Storage level: {df_disk.storageLevel}")
    
    # Summary
    print("\n" + "-"*40)
    print("CACHING STRATEGY SUMMARY:")
    print(f"No Cache:        {no_cache_time:.2f}s")
    print(f"MEMORY_ONLY:     {memory_only_time:.2f}s ({((no_cache_time - memory_only_time)/no_cache_time*100):.1f}% faster)")
    print(f"MEMORY_AND_DISK: {memory_disk_time:.2f}s ({((no_cache_time - memory_disk_time)/no_cache_time*100):.1f}% faster)")
    print(f"DISK_ONLY:       {disk_only_time:.2f}s ({((no_cache_time - disk_only_time)/no_cache_time*100):.1f}% faster)")
    
    # Cleanup
    df_cached.unpersist()
    df_memory_disk.unpersist()
    df_disk.unpersist()

def demonstrate_garbage_collection_tuning():
    """Show GC tuning impact"""
    print("\n" + "="*80)
    print("GARBAGE COLLECTION TUNING")
    print("="*80)
    
    print("""
Garbage Collection (GC) Tuning Guidelines for 8GB RAM:

1. **Use G1GC**: Better for large heaps with predictable pause times
   -XX:+UseG1GC

2. **Initiating Heap Occupancy**: Start GC earlier (35% for Spark workloads)
   -XX:InitiatingHeapOccupancyPercent=35

3. **Parallel GC Threads**: Match to CPU cores (2 for local[2])
   -XX:ParallelGCThreads=2

4. **ConcGC Threads**: Concurrent garbage collection threads
   -XX:ConcGCThreads=2

5. **Max GC Pause**: Target maximum pause time
   -XX:MaxGCPauseMillis=200

6. **Young Generation Size**: Adjust for Spark's object allocation pattern
   -XX:G1NewSizePercent=20 -XX:G1MaxNewSizePercent=40

Example configuration for 8GB RAM:
spark.executor.extraJavaOptions: "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 
-XX:ConcGCThreads=2 -XX:ParallelGCThreads=2 -XX:MaxGCPauseMillis=200"
""")

def memory_monitoring_techniques(spark):
    """Show how to monitor memory usage"""
    print("\n" + "="*80)
    print("MEMORY MONITORING TECHNIQUES")
    print("="*80)
    
    # Get Spark UI URL
    ui_url = spark.sparkContext.uiWebUrl
    print(f"Spark UI: {ui_url}")
    print("Access Spark UI at http://localhost:4040 for detailed memory metrics")
    
    # Show current memory usage
    memory_status = spark.sparkContext.getExecutorMemoryStatus
    print("\nExecutor Memory Status:")
    for executor, (used, total) in memory_status.items():
        print(f"  {executor}: {used / 1024 / 1024:.1f}MB used / {total / 1024 / 1024:.1f}MB total")
    
    # Show storage memory
    storage_info = spark.sparkContext.getRDDStorageInfo()
    print("\nRDD Storage Info:")
    for info in storage_info:
        if info.memSize > 0:
            print(f"  RDD {info.id}: {info.memSize / 1024 / 1024:.1f}MB in memory")
    
    # System memory
    print("\nSystem Memory Info:")
    vm = psutil.virtual_memory()
    print(f"  Total: {vm.total / 1024 / 1024:.1f} MB")
    print(f"  Available: {vm.available / 1024 / 1024:.1f} MB")
    print(f"  Used: {vm.used / 1024 / 1024:.1f} MB")
    print(f"  Percent: {vm.percent}%")
    
    # Process memory
    process = psutil.Process()
    print(f"\nProcess Memory (PID {process.pid}):")
    print(f"  RSS: {process.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"  VMS: {process.memory_info().vms / 1024 / 1024:.1f} MB")

def demonstrate_off_heap_memory():
    """Show off-heap memory configuration and benefits"""
    print("\n" + "="*80)
    print("OFF-HEAP MEMORY CONFIGURATION")
    print("="*80)
    
    print("""
Off-Heap Memory Benefits:
1. **Reduced GC Pressure**: Objects stored off-heap don't affect GC
2. **Large Memory Regions**: Can allocate beyond JVM heap limits
3. **Memory Sharing**: Can be shared between processes

Configuration for 8GB RAM:
spark.memory.offHeap.enabled = true
spark.memory.offHeap.size = 512m

Use Cases:
- Large broadcast variables
- Memory-intensive operations
- When GC pauses are problematic

Limitations:
- Slower access than on-heap
- Manual memory management required
- Not all Spark operations support off-heap
""")

def memory_optimization_exercises(df):
    """Provide hands-on memory optimization exercises"""
    print("\n" + "="*80)
    print("MEMORY OPTIMIZATION EXERCISES")
    print("="*80)
    
    print("""
Exercise 1: Cache Strategy Selection
------------------------------------------------
1. Create a DataFrame with 100K rows and 50 columns
2. Apply three different caching strategies:
   - MEMORY_ONLY
   - MEMORY_AND_DISK  
   - DISK_ONLY
3. Measure memory usage and performance for each
4. Determine which is best for your 8GB system

Exercise 2: Garbage Collection Tuning
------------------------------------------------
1. Run a memory-intensive operation with default GC
2. Run the same operation with G1GC tuned settings
3. Compare GC pause times and total execution time
4. Use Spark UI to monitor GC activity

Exercise 3: Serialization Comparison
------------------------------------------------
1. Serialize a large DataFrame using Java serializer
2. Serialize the same DataFrame using Kryo serializer
3. Compare serialized size and deserialization time
4. Measure memory footprint difference

Exercise 4: Off-Heap Memory Experiment
------------------------------------------------
1. Configure Spark with 512MB off-heap memory
2. Run operations that use broadcast variables
3. Monitor off-heap usage in Spark UI
4. Compare performance with/without off-heap

Exercise 5: Memory Leak Detection
------------------------------------------------
1. Intentionally create a memory leak (cache without unpersist)
2. Monitor memory growth over iterations
3. Use Spark UI storage tab to identify leaked RDDs
4. Fix the leak and verify memory stabilizes
""")

def main():
    """Main execution function"""
    print("="*80)
    print("ADVANCED PYSPARK: MEMORY MANAGEMENT & TUNING")
    print("="*80)
    print("This tutorial focuses on memory optimization for 8GB RAM systems.")
    print("All examples use production-grade tuning techniques.\n")
    
    # Initialize Spark with memory optimization
    global spark
    spark = create_memory_optimized_spark_session()
    
    try:
        # Generate dataset
        df = generate_large_dataset(spark, num_rows=100000, num_cols=15)
        
        # Run demonstrations
        demonstrate_memory_architecture()
        benchmark_serialization(df)
        demonstrate_caching_strategies(df)
        demonstrate_garbage_collection_tuning()
        memory_monitoring_techniques(spark)
        demonstrate_off_heap_memory()
        memory_optimization_exercises(df)
        
        print("\n" + "="*80)
        print("TUTORIAL COMPLETE")
        print("="*80)
        print("Key Takeaways:")
        print("1. Use Kryo serialization for better performance and smaller size")
        print("2. Choose caching strategy based on data reuse pattern")
        print("3. Tune G1GC for predictable pause times")
        print("4. Enable off-heap memory for large operations")
        print("5. Monitor memory usage with Spark UI and psutil")
        print("\nNext: Run 03_join_strategies.py for join optimization techniques")
        
    finally:
        # Cleanup
        spark.catalog.clearCache()
        spark.stop()
        print("\nSpark session stopped. Memory released.")

if __name__ == "__main__":
    main()