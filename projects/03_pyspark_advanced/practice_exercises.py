#!/usr/bin/env python3
"""
Advanced PySpark Practice Exercises

Practice exercises for PySpark advanced topics optimized for 8GB RAM environments.
Each exercise builds on advanced concepts: Catalyst optimizer, memory management,
join strategies, ML pipelines, streaming analytics, and FastAPI integration.

Note: These exercises assume PySpark is installed and configured for 8GB RAM.
"""

import sys
import os
import time
import json
import tempfile
from typing import Dict, List, Tuple, Any, Optional
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, sum as spark_sum, avg, count, max as spark_max, min as spark_min, when, year, month, lit, expr, broadcast, udf, pandas_udf, PandasUDFType
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType, TimestampType, ArrayType, FloatType
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
import psutil
import numpy as np
import pandas as pd

# ============================================================================
# Exercise 1: Catalyst Optimizer Deep Dive
# ============================================================================

def exercise_1_catalyst_optimizer() -> Dict[str, Any]:
    """
    Exercise 1: Understanding and Leveraging Catalyst Optimizer
    
    Tasks:
    1. Create two logically equivalent queries with different performance characteristics
    2. Use .explain() to compare logical and physical plans
    3. Implement predicate pushdown and column pruning manually
    4. Measure performance difference between optimized vs naive queries
    5. Analyze Catalyst optimization rules applied
    
    Returns:
        Dict: Results including execution times, plan differences, and optimization metrics
    """
    print("\n=== Exercise 1: Catalyst Optimizer Deep Dive ===")
    print("Analyzing Catalyst optimizer performance impact...")
    
    # TODO: Implement Catalyst optimizer analysis
    # 1. Create SparkSession with optimization enabled
    # 2. Generate sample dataset with multiple columns
    # 3. Write naive query (multiple unnecessary transformations)
    # 4. Write optimized query (predicate pushdown, column pruning)
    # 5. Compare execution plans and performance
    
    print("   [TODO: Implement Catalyst optimizer analysis]")
    return {
        "naive_query_time": 0.0,
        "optimized_query_time": 0.0,
        "performance_improvement": 0.0,
        "plan_differences": [],
        "catalyst_rules_applied": []
    }

# ============================================================================
# Exercise 2: Advanced Memory Management
# ============================================================================

def exercise_2_memory_management(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 2: Memory Management and Garbage Collection Tuning
    
    Tasks:
    1. Monitor memory usage during different Spark operations
    2. Compare storage levels (MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY)
    3. Tune garbage collection parameters for 8GB RAM
    4. Implement memory-aware partitioning strategies
    5. Handle out-of-memory scenarios with graceful degradation
    
    Args:
        spark: SparkSession configured for 8GB RAM
        
    Returns:
        Dict: Memory usage metrics, GC performance, and optimization recommendations
    """
    print("\n=== Exercise 2: Advanced Memory Management ===")
    print("Analyzing memory management and GC tuning...")
    
    # TODO: Implement memory management analysis
    # 1. Create large DataFrame that exceeds available memory
    # 2. Test different storage levels and measure performance
    # 3. Monitor GC activity with different JVM options
    # 4. Implement partitioning to reduce memory pressure
    # 5. Simulate OOM and implement recovery strategies
    
    print("   [TODO: Implement memory management analysis]")
    return {
        "memory_usage_before_mb": 0,
        "memory_usage_after_mb": 0,
        "gc_time_ms": 0,
        "storage_level_performance": {},
        "partitioning_improvement": 0.0
    }

# ============================================================================
# Exercise 3: Join Strategies and Skew Handling
# ============================================================================

def exercise_3_join_strategies(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 3: Advanced Join Strategies and Data Skew Handling
    
    Tasks:
    1. Implement and compare different join strategies (broadcast, sort-merge, shuffle-hash)
    2. Create and handle severely skewed datasets
    3. Apply salting techniques for skewed joins
    4. Implement two-stage aggregation for skewed data
    5. Monitor and optimize shuffle operations
    
    Args:
        spark: SparkSession configured for 8GB RAM
        
    Returns:
        Dict: Join performance metrics, skew handling effectiveness, shuffle statistics
    """
    print("\n=== Exercise 3: Join Strategies and Skew Handling ===")
    print("Analyzing join strategies and skew handling...")
    
    # TODO: Implement join strategies analysis
    # 1. Create datasets with different size characteristics
    # 2. Implement broadcast, sort-merge, and shuffle-hash joins
    # 3. Create skewed dataset (80/20 distribution)
    # 4. Apply salting and measure performance improvement
    # 5. Analyze shuffle metrics and optimize
    
    print("   [TODO: Implement join strategies analysis]")
    return {
        "broadcast_join_time": 0.0,
        "sort_merge_join_time": 0.0,
        "shuffle_hash_join_time": 0.0,
        "skew_ratio": 0.0,
        "salting_improvement": 0.0,
        "shuffle_bytes": 0
    }

# ============================================================================
# Exercise 4: ML Pipeline with PySpark MLlib
# ============================================================================

def exercise_4_ml_pipeline(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 4: Machine Learning Pipeline with PySpark MLlib
    
    Tasks:
    1. Build complete ML pipeline with feature engineering
    2. Implement cross-validation and hyperparameter tuning
    3. Handle class imbalance with sampling techniques
    4. Evaluate model performance with multiple metrics
    5. Optimize ML pipeline for 8GB RAM constraints
    
    Args:
        spark: SparkSession configured for 8GB RAM
        
    Returns:
        Dict: Model performance metrics, training times, memory usage
    """
    print("\n=== Exercise 4: ML Pipeline with PySpark MLlib ===")
    print("Building and evaluating ML pipeline...")
    
    # TODO: Implement ML pipeline
    # 1. Generate or load classification dataset
    # 2. Build feature engineering pipeline (StringIndexer, OneHotEncoder, VectorAssembler)
    # 3. Train LogisticRegression and RandomForest models
    # 4. Implement cross-validation with ParamGridBuilder
    # 5. Evaluate with AUC, accuracy, precision, recall
    
    print("   [TODO: Implement ML pipeline]")
    return {
        "logistic_regression_auc": 0.0,
        "random_forest_auc": 0.0,
        "training_time_seconds": 0.0,
        "cross_validation_score": 0.0,
        "feature_importance": {}
    }

# ============================================================================
# Exercise 5: Structured Streaming Analytics
# ============================================================================

def exercise_5_streaming_analytics(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 5: Real-time Analytics with Structured Streaming
    
    Tasks:
    1. Set up simulated streaming data source
    2. Implement windowed aggregations and watermarking
    3. Handle late-arriving data and state management
    4. Output streaming results to sink (memory, console, file)
    5. Monitor streaming query progress and performance
    
    Args:
        spark: SparkSession configured for 8GB RAM
        
    Returns:
        Dict: Streaming metrics, latency measurements, state management statistics
    """
    print("\n=== Exercise 5: Structured Streaming Analytics ===")
    print("Implementing real-time streaming analytics...")
    
    # TODO: Implement streaming analytics
    # 1. Create simulated streaming source (rate source or memory)
    # 2. Implement windowed aggregations with watermark
    # 3. Handle state with checkpointing
    # 4. Output to console and measure latency
    # 5. Monitor query progress and resource usage
    
    print("   [TODO: Implement streaming analytics]")
    return {
        "streaming_latency_ms": 0.0,
        "processing_rate_rows_per_second": 0.0,
        "watermark_delay_seconds": 0,
        "state_store_size_mb": 0.0,
        "checkpoint_usage": {}
    }

# ============================================================================
# Exercise 6: PySpark-FastAPI Integration
# ============================================================================

def exercise_6_fastapi_integration(spark: SparkSession) -> Dict[str, Any]:
    """
    Exercise 6: Integrating PySpark with FastAPI REST API
    
    Tasks:
    1. Create FastAPI application with PySpark session management
    2. Implement REST endpoints for data querying and ML inference
    3. Handle concurrent requests with Spark session pooling
    4. Implement caching strategies for frequently accessed data
    5. Monitor API performance and resource usage
    
    Args:
        spark: SparkSession configured for 8GB RAM
        
    Returns:
        Dict: API performance metrics, concurrent request handling, caching effectiveness
    """
    print("\n=== Exercise 6: PySpark-FastAPI Integration ===")
    print("Building integrated PySpark-FastAPI application...")
    
    # TODO: Implement FastAPI integration
    # 1. Create FastAPI app with startup/shutdown events for Spark
    # 2. Implement endpoints for data query, aggregation, ML inference
    # 3. Test concurrent requests with session management
    # 4. Implement DataFrame caching for frequent queries
    # 5. Measure response times and memory usage
    
    print("   [TODO: Implement FastAPI integration]")
    return {
        "api_response_time_ms": 0.0,
        "concurrent_requests_handled": 0,
        "cache_hit_rate": 0.0,
        "spark_session_reuse_count": 0,
        "memory_usage_per_request_mb": 0.0
    }

# ============================================================================
# Main Function to Run All Exercises
# ============================================================================

def main():
    """Run all advanced PySpark practice exercises in sequence."""
    print("=" * 70)
    print("ADVANCED PYSPARK PRACTICE EXERCISES")
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
        # Create optimized SparkSession
        print("\n" + "=" * 40)
        print("Creating SparkSession for 8GB RAM...")
        print("=" * 40)
        
        spark = SparkSession.builder \
            .appName("Advanced-PySpark-Practice") \
            .master("local[2]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "1g") \
            .config("spark.sql.shuffle.partitions", "4") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        print("✓ SparkSession created with advanced configuration")
        
        # Exercise 1: Catalyst Optimizer
        print("\n" + "=" * 40)
        print("Starting Exercise 1: Catalyst Optimizer Deep Dive")
        print("=" * 40)
        catalyst_results = exercise_1_catalyst_optimizer()
        print(f"   Catalyst results: {catalyst_results}")
        
        # Exercise 2: Memory Management
        print("\n" + "=" * 40)
        print("Starting Exercise 2: Advanced Memory Management")
        print("=" * 40)
        memory_results = exercise_2_memory_management(spark)
        print(f"   Memory management results: {memory_results}")
        
        # Exercise 3: Join Strategies
        print("\n" + "=" * 40)
        print("Starting Exercise 3: Join Strategies and Skew Handling")
        print("=" * 40)
        join_results = exercise_3_join_strategies(spark)
        print(f"   Join strategies results: {join_results}")
        
        # Exercise 4: ML Pipeline
        print("\n" + "=" * 40)
        print("Starting Exercise 4: ML Pipeline with PySpark MLlib")
        print("=" * 40)
        ml_results = exercise_4_ml_pipeline(spark)
        print(f"   ML pipeline results: {ml_results}")
        
        # Exercise 5: Streaming Analytics
        print("\n" + "=" * 40)
        print("Starting Exercise 5: Structured Streaming Analytics")
        print("=" * 40)
        streaming_results = exercise_5_streaming_analytics(spark)
        print(f"   Streaming analytics results: {streaming_results}")
        
        # Exercise 6: FastAPI Integration
        print("\n" + "=" * 40)
        print("Starting Exercise 6: PySpark-FastAPI Integration")
        print("=" * 40)
        api_results = exercise_6_fastapi_integration(spark)
        print(f"   FastAPI integration results: {api_results}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("EXERCISES COMPLETED")
        print("=" * 70)
        print("All advanced practice exercises have been executed.")
        print("Implement the TODO sections to complete each exercise.")
        print("\nNext steps:")
        print("1. Complete Exercise 1-6 implementations")
        print("2. Create solutions in solutions.py")
        print("3. Test with actual PySpark installation and FastAPI")
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