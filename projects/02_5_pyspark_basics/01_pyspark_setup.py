#!/usr/bin/env python3
"""
PySpark Setup for 8GB RAM

This script demonstrates how to configure PySpark to run efficiently
on a laptop with 8GB RAM. Key optimizations:
- Limited driver/executor memory
- Reduced parallelism
- Efficient garbage collection
"""

import os
import sys
from pyspark.sql import SparkSession
import time

def create_spark_session(app_name="PySpark-8GB"):
    """
    Create a SparkSession optimized for 8GB RAM environment.
    
    Memory allocation:
    - Total RAM: 8GB
    - Driver: 2GB (handles metadata, scheduling)
    - Executor: 1GB (per core, processes data)
    - System/OS: ~5GB remaining
    """
    
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[2]")  # Use 2 cores (not all CPU cores)
    
    # Memory configuration for 8GB total RAM
    spark = spark.config("spark.driver.memory", "2g") \
                 .config("spark.executor.memory", "1g") \
                 .config("spark.driver.maxResultSize", "1g")
    
    # Performance optimizations for low memory
    spark = spark.config("spark.sql.shuffle.partitions", "4") \
                 .config("spark.default.parallelism", "4") \
                 .config("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10MB
    
    # Memory management
    spark = spark.config("spark.memory.fraction", "0.6") \
                 .config("spark.memory.storageFraction", "0.3") \
                 .config("spark.cleaner.periodicGC.interval", "1min")
    
    # Serialization (more efficient than Java serialization)
    spark = spark.config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    
    # UI configuration (optional, disable to save memory)
    spark = spark.config("spark.ui.enabled", "true") \
                 .config("spark.ui.port", "4040")
    
    return spark.getOrCreate()

def test_basic_operations(spark):
    """Test that PySpark is working correctly with basic operations."""
    
    print("\n" + "="*60)
    print("Testing PySpark Basic Operations")
    print("="*60)
    
    # 1. Create a simple DataFrame
    print("\n1. Creating test DataFrame...")
    data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    
    print(f"DataFrame created with {df.count()} rows")
    df.show()
    
    # 2. Perform basic transformations
    print("\n2. Testing transformations...")
    df_filtered = df.filter(df.Age > 30)
    print(f"Rows with Age > 30: {df_filtered.count()}")
    df_filtered.show()
    
    # 3. Aggregation
    print("\n3. Testing aggregation...")
    df_agg = df.groupBy().agg({"Age": "avg", "Age": "max"})
    df_agg.show()
    
    # 4. Schema inspection
    print("\n4. Schema inspection:")
    df.printSchema()
    
    return df

def monitor_resources(spark):
    """Display Spark configuration and resource usage."""
    
    print("\n" + "="*60)
    print("Spark Configuration & Resources")
    print("="*60)
    
    # Get Spark context
    sc = spark.sparkContext
    
    # Display configuration
    print("\nKey Configuration Parameters:")
    config_keys = [
        "spark.driver.memory",
        "spark.executor.memory", 
        "spark.master",
        "spark.sql.shuffle.partitions",
        "spark.default.parallelism"
    ]
    
    for key in config_keys:
        try:
            value = sc.getConf().get(key)
            print(f"  {key}: {value}")
        except:
            print(f"  {key}: Not set")
    
    # Display available cores
    print(f"\nAvailable Cores: {sc.defaultParallelism}")
    
    # Display Spark UI URL
    ui_url = spark.sparkContext.uiWebUrl
    if ui_url:
        print(f"Spark UI: {ui_url}")
        print("  Open in browser to monitor jobs and memory usage")
    else:
        print("Spark UI: Not available (disabled or memory constraint)")
    
    # Memory info
    print("\nMemory Information:")
    print("  Driver Memory: 2GB (configured)")
    print("  Executor Memory: 1GB (configured)")
    print("  Recommended for 8GB RAM: Leave ~5GB for OS/other processes")

def cleanup(spark):
    """Properly clean up Spark resources."""
    print("\n" + "="*60)
    print("Cleaning Up Resources")
    print("="*60)
    
    # Stop Spark session
    spark.stop()
    
    # Force garbage collection
    import gc
    gc.collect()
    
    print("Spark session stopped")
    print("Memory freed up for next operation")

def main():
    """Main execution function."""
    
    print("="*60)
    print("PySpark Setup for 8GB RAM Environment")
    print("="*60)
    
    print("\nSystem Information:")
    print(f"  Python: {sys.version}")
    print(f"  Working Directory: {os.getcwd()}")
    
    # Create optimized Spark session
    print("\nCreating SparkSession with 8GB RAM optimization...")
    start_time = time.time()
    
    try:
        spark = create_spark_session("8GB-RAM-Tutorial")
        setup_time = time.time() - start_time
        print(f"SparkSession created in {setup_time:.2f} seconds")
        
        # Test basic operations
        test_basic_operations(spark)
        
        # Monitor resources
        monitor_resources(spark)
        
        # Success message
        print("\n" + "="*60)
        print("✅ SETUP SUCCESSFUL!")
        print("="*60)
        print("\nPySpark is now configured for your 8GB RAM environment.")
        print("\nNext steps:")
        print("1. Run 02_dataframe_basics.py for DataFrame operations")
        print("2. Monitor memory usage with 'htop' in another terminal")
        print("3. Access Spark UI at http://localhost:4040 (if enabled)")
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to create SparkSession")
        print(f"Error details: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check Java installation: java -version")
        print("2. Ensure you have at least Java 8 installed")
        print("3. Try reducing memory further: spark.driver.memory=1g")
        return 1
    
    finally:
        # Always clean up
        if 'spark' in locals():
            cleanup(spark)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())