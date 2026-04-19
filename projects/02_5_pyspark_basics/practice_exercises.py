#!/usr/bin/env python3
"""
PySpark Basics Practice Exercises

Practice exercises for PySpark fundamentals optimized for 8GB RAM environments.
Each exercise builds on the previous one, covering setup, DataFrame operations,
chunking, optimization, and complete ETL pipelines.

Note: These exercises assume PySpark is installed and configured for 8GB RAM.
"""

import sys
import os
from typing import Dict, List, Tuple, Any, Optional
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, sum, avg, count, max, min, when, year, month
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

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
    
    # TODO: Implement SparkSession configuration
    # 1. Use SparkSession.builder with app name "PySpark-8GB-Practice"
    # 2. Set master to "local[2]" for 2 cores
    # 3. Configure driver memory to "2g", executor memory to "1g"
    # 4. Set spark.sql.shuffle.partitions to 4
    # 5. Enable KryoSerializer
    # 6. Set appropriate memory fractions and GC interval
    
    print("   [TODO: Implement SparkSession configuration]")
    return None

# ============================================================================
# Exercise 2: DataFrame Basics and Operations
# ============================================================================

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
    
    # TODO: Implement DataFrame operations
    # 1. Load sales_data.csv (create sample if missing)
    # 2. Calculate total sales (quantity * price)
    # 3. Group by region and calculate metrics
    # 4. Handle any missing or invalid data
    # 5. Return dictionary with results
    
    print("   [TODO: Implement DataFrame operations]")
    return {
        "total_sales": 0,
        "avg_price": 0.0,
        "region_counts": {},
        "row_count": 0
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
    
    # TODO: Implement chunked processing
    # 1. Generate or load large dataset (1M+ rows simulated)
    # 2. Process in chunks (e.g., 100k rows at a time)
    # 3. Maintain running totals for aggregations
    # 4. Monitor and log memory usage
    # 5. Return aggregated DataFrame
    
    print("   [TODO: Implement chunked processing]")
    return spark.createDataFrame([], StructType([]))

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
    
    # TODO: Implement optimization techniques
    # 1. Compare caching strategies
    # 2. Demonstrate broadcast join
    # 3. Handle skewed data
    # 4. Measure performance improvements
    # 5. Return optimization metrics
    
    print("   [TODO: Implement optimization techniques]")
    return {
        "cache_improvement": 0.0,
        "broadcast_join_size": 0,
        "skew_handled": False,
        "execution_time_reduction": 0.0
    }

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
    
    # TODO: Implement complete ETL pipeline
    # 1. Extract from multiple sources
    # 2. Apply transformations and data quality checks
    # 3. Load to partitioned Parquet format
    # 4. Implement comprehensive error handling
    # 5. Return pipeline execution metrics
    
    print("   [TODO: Implement ETL pipeline]")
    return {
        "success": False,
        "rows_processed": 0,
        "output_files": [],
        "execution_time_seconds": 0,
        "memory_peak_mb": 0
    }

# ============================================================================
# Main Function to Run All Exercises
# ============================================================================

def main():
    """Run all PySpark practice exercises in sequence."""
    print("=" * 70)
    print("PYSPARK BASICS PRACTICE EXERCISES")
    print("Optimized for 8GB RAM Environments")
    print("=" * 70)
    
    # Check if PySpark is available
    try:
        from pyspark.sql import SparkSession
        print("✓ PySpark is available")
    except ImportError:
        print("✗ PySpark not found. Install with: pip install pyspark")
        print("  Note: Java 8+ is required for PySpark")
        return
    
    try:
        # Exercise 1: Setup
        print("\n" + "=" * 40)
        print("Starting Exercise 1: PySpark Setup")
        print("=" * 40)
        spark = exercise_1_spark_setup()
        
        if spark is None:
            print("⚠ Exercise 1 not implemented. Using default SparkSession.")
            spark = SparkSession.builder \
                .appName("PySpark-Practice") \
                .master("local[2]") \
                .getOrCreate()
        
        # Exercise 2: DataFrame Operations
        print("\n" + "=" * 40)
        print("Starting Exercise 2: DataFrame Operations")
        print("=" * 40)
        df_results = exercise_2_dataframe_operations(spark)
        print(f"   DataFrame results: {df_results}")
        
        # Exercise 3: Chunking
        print("\n" + "=" * 40)
        print("Starting Exercise 3: Chunking Large Datasets")
        print("=" * 40)
        chunked_df = exercise_3_chunking_large_data(spark)
        print(f"   Chunked processing complete. Schema: {chunked_df.schema}")
        
        # Exercise 4: Optimization
        print("\n" + "=" * 40)
        print("Starting Exercise 4: Optimization Techniques")
        print("=" * 40)
        # Create sample DataFrame for optimization
        sample_data = [("A", 100), ("B", 200), ("C", 300), ("D", 400)]
        sample_df = spark.createDataFrame(sample_data, ["category", "value"])
        opt_results = exercise_4_optimization_techniques(spark, sample_df)
        print(f"   Optimization results: {opt_results}")
        
        # Exercise 5: ETL Pipeline
        print("\n" + "=" * 40)
        print("Starting Exercise 5: Complete ETL Pipeline")
        print("=" * 40)
        pipeline_results = exercise_5_etl_pipeline(spark)
        print(f"   Pipeline results: {pipeline_results}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("EXERCISES COMPLETED")
        print("=" * 70)
        print("All practice exercises have been executed.")
        print("Implement the TODO sections to complete each exercise.")
        print("\nNext steps:")
        print("1. Complete Exercise 1-5 implementations")
        print("2. Create solutions in solutions.py")
        print("3. Test with actual PySpark installation")
        print("=" * 70)
        
        # Stop SparkSession
        spark.stop()
        print("SparkSession stopped.")
        
    except Exception as e:
        print(f"\n✗ Error running exercises: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)