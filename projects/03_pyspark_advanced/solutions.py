#!/usr/bin/env python3
"""
Advanced PySpark Solutions

Complete implementations for all advanced PySpark practice exercises.
Optimized for 8GB RAM environments.

Note: This file contains the solutions to the exercises in practice_exercises.py.
Run with: python solutions.py
"""

import sys
import os
import time
import json
import tempfile
import threading
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
import random
import gc

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, sum as spark_sum, avg, count, max as spark_max, min as spark_min,
    when, year, month, lit, expr, broadcast, udf, pandas_udf, PandasUDFType,
    window, explode, array, rand, row_number, rank, desc, asc, 
    from_unixtime, unix_timestamp, current_timestamp, date_add
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, 
    DateType, TimestampType, ArrayType, FloatType, BooleanType, LongType
)
from pyspark.sql.window import Window
from pyspark.storagelevel import StorageLevel
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler, MinMaxScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.regression import LinearRegression
from pyspark.ml.clustering import KMeans

import psutil
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ============================================================================
# Helper Functions
# ============================================================================

def create_optimized_spark_session() -> SparkSession:
    """Create SparkSession optimized for 8GB RAM."""
    return SparkSession.builder \
        .appName("Advanced-PySpark-Solutions") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10MB \
        .config("spark.executor.extraJavaOptions", 
                "-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=35") \
        .getOrCreate()

def generate_sample_data(spark: SparkSession, num_rows: int = 10000) -> DataFrame:
    """Generate sample data for exercises."""
    data = []
    for i in range(num_rows):
        data.append((
            i,  # id
            f"user_{i % 1000}",  # user_id
            f"product_{i % 100}",  # product_id
            random.randint(1, 1000),  # amount
            random.randint(1, 5),  # rating
            random.choice(["A", "B", "C", "D", "E"]),  # category
            datetime.now() - timedelta(days=random.randint(0, 365)),  # timestamp
            random.random() * 100,  # feature1
            random.random() * 50,   # feature2
            random.random() * 200,  # feature3
            random.choice([0, 1])   # label
        ))
    
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("user_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("amount", IntegerType(), True),
        StructField("rating", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("feature3", DoubleType(), True),
        StructField("label", IntegerType(), True)
    ])
    
    return spark.createDataFrame(data, schema)

def monitor_memory() -> Dict[str, float]:
    """Monitor current memory usage."""
    process = psutil.Process()
    system = psutil.virtual_memory()
    
    return {
        "process_rss_mb": process.memory_info().rss / 1024 / 1024,
        "process_vms_mb": process.memory_info().vms / 1024 / 1024,
        "system_used_percent": system.percent,
        "system_available_mb": system.available / 1024 / 1024
    }

# ============================================================================
# Exercise 1: Catalyst Optimizer Deep Dive - SOLUTION
# ============================================================================

def exercise_1_catalyst_optimizer_solution() -> Dict[str, Any]:
    """
    Solution for Exercise 1: Catalyst Optimizer Deep Dive
    """
    print("\n=== Exercise 1: Catalyst Optimizer Deep Dive ===")
    print("Analyzing Catalyst optimizer performance impact...")
    
    # Create SparkSession with optimization enabled
    spark = create_optimized_spark_session()
    
    # Generate sample dataset
    df = generate_sample_data(spark, 5000)
    df.createOrReplaceTempView("sales_data")
    
    # Naive query: Multiple unnecessary transformations
    start_time = time.time()
    naive_result = spark.sql("""
        SELECT * FROM (
            SELECT 
                user_id, 
                product_id, 
                amount,
                rating,
                category,
                timestamp,
                feature1,
                feature2,
                feature3,
                label
            FROM sales_data
        ) t1
        WHERE amount > 500
        AND rating >= 3
        AND category IN ('A', 'B', 'C')
        ORDER BY amount DESC
    """)
    naive_count = naive_result.count()
    naive_time = time.time() - start_time
    
    print(f"Naive query execution time: {naive_time:.2f}s")
    print("Naive query plan:")
    naive_result.explain()
    
    # Optimized query: Predicate pushdown, column pruning
    start_time = time.time()
    optimized_result = spark.sql("""
        SELECT 
            user_id,
            product_id,
            amount,
            rating
        FROM sales_data
        WHERE amount > 500
        AND rating >= 3
        AND category IN ('A', 'B', 'C')
        ORDER BY amount DESC
    """)
    optimized_count = optimized_result.count()
    optimized_time = time.time() - start_time
    
    print(f"\nOptimized query execution time: {optimized_time:.2f}s")
    print("Optimized query plan:")
    optimized_result.explain()
    
    # Analyze plan differences
    naive_plan = spark.sql("""
        EXPLAIN EXTENDED
        SELECT * FROM (
            SELECT * FROM sales_data
        ) t1
        WHERE amount > 500
    """).collect()[0][0]
    
    optimized_plan = spark.sql("""
        EXPLAIN EXTENDED
        SELECT user_id, amount FROM sales_data WHERE amount > 500
    """).collect()[0][0]
    
    # Check Catalyst rules applied
    catalyst_rules = []
    if "Filter" in optimized_plan and "Project" in optimized_plan:
        catalyst_rules.append("ColumnPruning")
    if "PushedFilters" in optimized_plan:
        catalyst_rules.append("PredicatePushdown")
    
    spark.stop()
    
    return {
        "naive_query_time": naive_time,
        "optimized_query_time": optimized_time,
        "performance_improvement": ((naive_time - optimized_time) / naive_time * 100) if naive_time > 0 else 0,
        "row_counts_match": naive_count == optimized_count,
        "catalyst_rules_applied": catalyst_rules,
        "plan_differences": [
            "Optimized query uses column pruning (selects only needed columns)",
            "Optimized query pushes filters earlier in execution",
            "Optimized query avoids unnecessary subquery"
        ]
    }

# ============================================================================
# Exercise 2: Advanced Memory Management - SOLUTION
# ============================================================================

def exercise_2_memory_management_solution(spark: SparkSession) -> Dict[str, Any]:
    """
    Solution for Exercise 2: Memory Management and Garbage Collection Tuning
    """
    print("\n=== Exercise 2: Advanced Memory Management ===")
    print("Analyzing memory management and GC tuning...")
    
    # 1. Monitor initial memory usage
    initial_memory = monitor_memory()
    
    # 2. Create large DataFrame that would exceed memory if not managed
    df = generate_sample_data(spark, 20000)
    
    # 3. Test different storage levels
    storage_levels = {
        "MEMORY_ONLY": StorageLevel.MEMORY_ONLY,
        "MEMORY_AND_DISK": StorageLevel.MEMORY_AND_DISK,
        "DISK_ONLY": StorageLevel.DISK_ONLY,
        "MEMORY_ONLY_SER": StorageLevel.MEMORY_ONLY_SER
    }
    
    storage_performance = {}
    for level_name, level in storage_levels.items():
        print(f"\nTesting {level_name}...")
        
        # Persist with this storage level
        df_persisted = df.persist(level)
        
        # Force materialization
        start_time = time.time()
        count = df_persisted.count()
        persist_time = time.time() - start_time
        
        # Measure memory after persistence
        memory_after = monitor_memory()
        
        storage_performance[level_name] = {
            "persist_time_seconds": persist_time,
            "row_count": count,
            "memory_increase_mb": memory_after["process_rss_mb"] - initial_memory["process_rss_mb"]
        }
        
        # Unpersist
        df_persisted.unpersist()
        gc.collect()
    
    # 4. Test partitioning strategies
    print("\nTesting partitioning strategies...")
    
    # Unpartitioned
    start_time = time.time()
    unpartitioned_count = df.groupBy("category").agg(spark_sum("amount").alias("total_amount")).count()
    unpartitioned_time = time.time() - start_time
    
    # Partitioned by category
    df_partitioned = df.repartition(10, "category")
    start_time = time.time()
    partitioned_count = df_partitioned.groupBy("category").agg(spark_sum("amount").alias("total_amount")).count()
    partitioned_time = time.time() - start_time
    
    # 5. Simulate OOM scenario with recovery
    print("\nSimulating memory pressure scenario...")
    
    # Create multiple DataFrames to increase memory pressure
    dfs = []
    for i in range(5):
        dfs.append(generate_sample_data(spark, 5000).withColumnRenamed("amount", f"amount_{i}"))
    
    # Try to join them all (might cause OOM on 8GB)
    try:
        # Start with first DataFrame
        combined = dfs[0]
        for i in range(1, len(dfs)):
            combined = combined.join(dfs[i], "user_id", "inner")
        
        # This might fail on 8GB RAM
        combined_count = combined.count()
        oom_occurred = False
    except Exception as e:
        if "Java heap space" in str(e) or "OutOfMemory" in str(e):
            print("OOM simulated successfully - implementing recovery...")
            oom_occurred = True
            
            # Recovery strategy: Process in chunks
            chunk_results = []
            for i, df_chunk in enumerate(dfs):
                chunk_result = df_chunk.groupBy("user_id").agg(spark_sum(f"amount_{i if i > 0 else ''}").alias(f"total_{i}"))
                chunk_results.append(chunk_result)
            
            # Combine results incrementally
            from functools import reduce
            final_result = reduce(lambda a, b: a.join(b, "user_id", "outer"), chunk_results)
            recovered_count = final_result.count()
        else:
            raise
    
    # Final memory measurement
    final_memory = monitor_memory()
    
    return {
        "memory_usage_before_mb": initial_memory["process_rss_mb"],
        "memory_usage_after_mb": final_memory["process_rss_mb"],
        "storage_level_performance": storage_performance,
        "partitioning_improvement": (unpartitioned_time - partitioned_time) / unpartitioned_time * 100 if unpartitioned_time > 0 else 0,
        "unpartitioned_time_seconds": unpartitioned_time,
        "partitioned_time_seconds": partitioned_time,
        "oom_simulated": oom_occurred,
        "recovery_strategy": "chunked_processing" if oom_occurred else "not_needed"
    }

# ============================================================================
# Exercise 3: Join Strategies and Skew Handling - SOLUTION
# ============================================================================

def exercise_3_join_strategies_solution(spark: SparkSession) -> Dict[str, Any]:
    """
    Solution for Exercise 3: Advanced Join Strategies and Data Skew Handling
    """
    print("\n=== Exercise 3: Join Strategies and Skew Handling ===")
    print("Analyzing join strategies and skew handling...")
    
    # 1. Create datasets with different characteristics
    # Small dataset for broadcast join
    small_data = [(i, f"small_{i}", random.randint(1, 100)) for i in range(100)]
    small_df = spark.createDataFrame(small_data, ["id", "name", "value"])
    
    # Medium dataset for sort-merge join
    medium_data = [(i, f"medium_{i}", random.randint(1, 1000)) for i in range(10000)]
    medium_df = spark.createDataFrame(medium_data, ["id", "name", "value"])
    
    # Large dataset for shuffle-hash join
    large_data = [(i, f"large_{i}", random.randint(1, 10000)) for i in range(100000)]
    large_df = spark.createDataFrame(large_data, ["id", "name", "value"])
    
    # 2. Create skewed dataset (80/20 distribution)
    skewed_data = []
    for i in range(10000):
        # 80% of data has keys 1-10, 20% has keys 11-1000
        if random.random() < 0.8:
            key = random.randint(1, 10)
        else:
            key = random.randint(11, 1000)
        skewed_data.append((key, f"skewed_{i}", random.randint(1, 1000)))
    
    skewed_df = spark.createDataFrame(skewed_data, ["key", "name", "value"])
    
    # 3. Test different join strategies
    join_times = {}
    
    # Broadcast join (small with medium)
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")  # Disable auto-broadcast for testing
    start_time = time.time()
    broadcast_result = small_df.join(broadcast(medium_df), "id", "inner")
    broadcast_count = broadcast_result.count()
    join_times["broadcast"] = time.time() - start_time
    
    # Sort-merge join (medium with large)
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")  # Re-enable
    start_time = time.time()
    sort_merge_result = medium_df.join(large_df, "id", "inner")
    sort_merge_count = sort_merge_result.count()
    join_times["sort_merge"] = time.time() - start_time
    
    # Shuffle-hash join (force with hint)
    start_time = time.time()
    shuffle_hash_result = medium_df.hint("shuffle_hash").join(large_df, "id", "inner")
    shuffle_hash_count = shuffle_hash_result.count()
    join_times["shuffle_hash"] = time.time() - start_time
    
    # 4. Analyze skew
    skew_analysis = skewed_df.groupBy("key").count().orderBy("count", ascending=False)
    skew_stats = skew_analysis.limit(20).collect()
    
    top_keys = [row["key"] for row in skew_stats[:5]]
    top_counts = [row["count"] for row in skew_stats[:5]]
    total_count = skewed_df.count()
    skew_ratio = sum(top_counts) / total_count if total_count > 0 else 0
    
    print(f"Skew ratio (top 5 keys / total): {skew_ratio:.2%}")
    
    # 5. Apply salting technique for skewed join
    print("\nApplying salting technique for skewed join...")
    
    # Create another dataset to join with skewed data
    other_data = [(i, f"other_{i}", random.randint(1, 100)) for i in range(1, 1001)]
    other_df = spark.createDataFrame(other_data, ["key", "other_name", "other_value"])
    
    # Regular join (will be slow due to skew)
    start_time = time.time()
    regular_join = skewed_df.join(other_df, "key", "inner")
    regular_count = regular_join.count()
    regular_time = time.time() - start_time
    
    # Salted join
    salt_buckets = 10
    
    # Add salt to skewed DataFrame
    skewed_salted = skewed_df.withColumn("salted_key", 
                                         expr(f"concat(key, '_', cast(rand() * {salt_buckets} as int))"))
    
    # Explode other DataFrame to match all salt values
    from pyspark.sql.functions import array, lit
    salt_values = [lit(f"{i}") for i in range(salt_buckets)]
    other_exploded = other_df.withColumn("salted_key", 
                                         explode(array(salt_values)))
    
    # Join on salted key
    start_time = time.time()
    salted_join = skewed_salted.join(other_exploded, "salted_key")
    salted_count = salted_join.count()
    salted_time = time.time() - start_time
    
    # 6. Monitor shuffle metrics
    shuffle_metrics = {
        "regular_join_shuffle_bytes": regular_join.rdd.context._jsc.sc().statusTracker().getJobIdsForGroup().toString(),
        "salted_join_shuffle_bytes": salted_join.rdd.context._jsc.sc().statusTracker().getJobIdsForGroup().toString()
    }
    
    return {
        "broadcast_join_time": join_times["broadcast"],
        "sort_merge_join_time": join_times["sort_merge"],
        "shuffle_hash_join_time": join_times["shuffle_hash"],
        "skew_ratio": skew_ratio,
        "top_skewed_keys": top_keys[:3],
        "regular_skewed_join_time": regular_time,
        "salted_skewed_join_time": salted_time,
        "salting_improvement": ((regular_time - salted_time) / regular_time * 100) if regular_time > 0 else 0,
        "row_counts_match": regular_count == salted_count,
        "shuffle_bytes_estimate": "N/A (requires Spark UI)"
    }

# ============================================================================
# Exercise 4: ML Pipeline with PySpark MLlib - SOLUTION
# ============================================================================

def exercise_4_ml_pipeline_solution(spark: SparkSession) -> Dict[str, Any]:
    """
    Solution for Exercise 4: Machine Learning Pipeline with PySpark MLlib
    """
    print("\n=== Exercise 4: ML Pipeline with PySpark MLlib ===")
    print("Building and evaluating ML pipeline...")
    
    # 1. Generate classification dataset
    np.random.seed(42)
    n_samples = 5000
    
    # Create synthetic data with clear patterns
    data = []
    for i in range(n_samples):
        # Features
        age = np.random.normal(35, 10)
        income = np.random.normal(50000, 15000)
        credit_score = np.random.normal(700, 100)
        
        # Create target with some pattern
        if age > 40 and income > 60000:
            label = 1  # High probability of approval
        elif age < 25 and income < 30000:
            label = 0  # Low probability of approval
        else:
            # Random with bias
            label = 1 if np.random.random() > 0.3 else 0
        
        # Add some noise
        if np.random.random() < 0.1:
            label = 1 - label  # Flip label for 10% of samples
        
        data.append((float(age), float(income), float(credit_score), int(label), f"category_{i % 5}"))
    
    # Create DataFrame
    schema = StructType([
        StructField("age", DoubleType(), True),
        StructField("income", DoubleType(), True),
        StructField("credit_score", DoubleType(), True),
        StructField("label", IntegerType(), True),
        StructField("category", StringType(), True)
    ])
    
    df = spark.createDataFrame(data, schema)
    
    # 2. Handle class imbalance (if any)
    class_counts = df.groupBy("label").count().collect()
    print(f"Class distribution: {class_counts}")
    
    # 3. Build feature engineering pipeline
    # StringIndexer for categorical column
    indexer = StringIndexer(inputCol="category", outputCol="category_index")
    
    # OneHotEncoder for categorical features (but for 8GB RAM, consider frequency encoding)
    # Instead of OneHotEncoder, we'll use StringIndexer only to save memory
    # For high-cardinality, consider target encoding or frequency encoding
    
    # VectorAssembler for numerical features
    assembler = VectorAssembler(
        inputCols=["age", "income", "credit_score", "category_index"],
        outputCol="features"
    )
    
    # 4. Build models
    # Logistic Regression
    lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=10, regParam=0.01)
    
    # Random Forest (memory intensive, use with caution on 8GB)
    rf = RandomForestClassifier(featuresCol="features", labelCol="label", 
                                numTrees=10, maxDepth=5, seed=42)
    
    # 5. Create pipelines
    lr_pipeline = Pipeline(stages=[indexer, assembler, lr])
    rf_pipeline = Pipeline(stages=[indexer, assembler, rf])
    
    # 6. Split data
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    
    # 7. Train and evaluate Logistic Regression
    print("\nTraining Logistic Regression...")
    lr_start = time.time()
    lr_model = lr_pipeline.fit(train_df)
    lr_time = time.time() - lr_start
    
    lr_predictions = lr_model.transform(test_df)
    lr_evaluator = BinaryClassificationEvaluator(labelCol="label")
    lr_auc = lr_evaluator.evaluate(lr_predictions)
    
    # 8. Train and evaluate Random Forest
    print("Training Random Forest...")
    rf_start = time.time()
    rf_model = rf_pipeline.fit(train_df)
    rf_time = time.time() - rf_start
    
    rf_predictions = rf_model.transform(test_df)
    rf_auc = lr_evaluator.evaluate(rf_predictions)
    
    # 9. Cross-validation for hyperparameter tuning (simplified for 8GB)
    print("\nPerforming simplified cross-validation...")
    
    # Create parameter grid
    paramGrid = ParamGridBuilder() \
        .addGrid(lr.regParam, [0.01, 0.1]) \
        .addGrid(lr.elasticNetParam, [0.0, 0.5]) \
        .build()
    
    # CrossValidator (reduced folds for 8GB RAM)
    crossval = CrossValidator(estimator=lr_pipeline,
                              estimatorParamMaps=paramGrid,
                              evaluator=BinaryClassificationEvaluator(labelCol="label"),
                              numFolds=3,  # Reduced from 5 for memory
                              parallelism=2,  # Limit parallel execution
                              seed=42)
    
    cv_start = time.time()
    cv_model = crossval.fit(train_df.limit(2000))  # Limit data for CV to save memory
    cv_time = time.time() - cv_start
    
    cv_predictions = cv_model.transform(test_df)
    cv_auc = lr_evaluator.evaluate(cv_predictions)
    
    # 10. Feature importance (for Random Forest)
    rf_model_final = rf_model.stages[-1]
    feature_importance = {}
    if hasattr(rf_model_final, 'featureImportances'):
        importance = rf_model_final.featureImportances
        features = ["age", "income", "credit_score", "category_index"]
        for i, feature in enumerate(features):
            if i < len(importance):
                feature_importance[feature] = float(importance[i])
    
    return {
        "logistic_regression_auc": lr_auc,
        "random_forest_auc": rf_auc,
        "cross_validation_best_auc": cv_auc,
        "logistic_regression_training_seconds": lr_time,
        "random_forest_training_seconds": rf_time,
        "cross_validation_time_seconds": cv_time,
        "feature_importance": feature_importance,
        "model_performance_summary": {
            "logistic_regression": f"AUC: {lr_auc:.3f}, Time: {lr_time:.1f}s",
            "random_forest": f"AUC: {rf_auc:.3f}, Time: {rf_time:.1f}s",
            "cross_validated_lr": f"AUC: {cv_auc:.3f}, Time: {cv_time:.1f}s"
        }
    }

# ============================================================================
# Exercise 5: Structured Streaming Analytics - SOLUTION
# ============================================================================

def exercise_5_streaming_analytics_solution(spark: SparkSession) -> Dict[str, Any]:
    """
    Solution for Exercise 5: Real-time Analytics with Structured Streaming
    """
    print("\n=== Exercise 5: Structured Streaming Analytics ===")
    print("Implementing real-time streaming analytics...")
    
    # Note: For demonstration, we'll simulate streaming with rate source
    # In production, you'd connect to Kafka, Kinesis, etc.
    
    # 1. Create simulated streaming source
    print("Creating simulated streaming source...")
    
    # Create a rate source (simulated streaming)
    streaming_df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 10) \
        .option("numPartitions", 2) \
        .load()
    
    # Add some business logic columns
    from pyspark.sql.functions import col, when
    enriched_df = streaming_df \
        .withColumn("user_id", (col("value") % 100).cast("integer")) \
        .withColumn("amount", (rand() * 1000).cast("integer")) \
        .withColumn("category", when(col("value") % 10 == 0, "A")
                               .when(col("value") % 10 == 1, "B")
                               .otherwise("C")) \
        .withColumn("event_time", col("timestamp"))
    
    # 2. Implement windowed aggregations with watermark
    print("Implementing windowed aggregations...")
    
    # Define watermark (10 seconds) and window (5 seconds)
    windowed_counts = enriched_df \
        .withWatermark("event_time", "10 seconds") \
        .groupBy(
            window(col("event_time"), "5 seconds"),
            col("category")
        ) \
        .agg(
            count("*").alias("event_count"),
            spark_sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount")
        )
    
    # 3. Create memory sink for testing
    print("Setting up memory sink...")
    
    # Define query
    query_name = "streaming_demo"
    checkpoint_location = tempfile.mkdtemp()
    
    streaming_query = windowed_counts \
        .writeStream \
        .queryName(query_name) \
        .outputMode("append") \
        .format("memory") \
        .option("checkpointLocation", checkpoint_location) \
        .trigger(processingTime="2 seconds") \
        .start()
    
    # 4. Run for a short time to collect metrics
    print("Running streaming query for 10 seconds...")
    start_time = time.time()
    
    # Let it run for 10 seconds
    for i in range(5):
        time.sleep(2)
        
        # Check progress
        progress = spark.streams.active[0].lastProgress
        if progress:
            print(f"Batch {i+1}: {progress['numInputRows']} rows processed")
    
    # 5. Collect metrics
    elapsed_time = time.time() - start_time
    
    # Get streaming metrics
    if spark.streams.active:
        last_progress = spark.streams.active[0].lastProgress
        if last_progress:
            input_rows = last_progress.get("numInputRows", 0)
            processed_rows = last_progress.get("processedRowsPerSecond", 0)
            latency = last_progress.get("latestOffsets", {}).get("rate", {}).get("latestOffset", 0)
        else:
            input_rows = processed_rows = latency = 0
    else:
        input_rows = processed_rows = latency = 0
    
    # 6. Query results from memory table
    try:
        results_df = spark.sql(f"SELECT * FROM {query_name}")
        result_count = results_df.count()
        result_sample = results_df.limit(3).collect()
    except:
        result_count = 0
        result_sample = []
    
    # 7. Stop the query
    streaming_query.stop()
    
    # 8. Cleanup checkpoint
    import shutil
    try:
        shutil.rmtree(checkpoint_location)
    except:
        pass
    
    # 9. Measure state store usage (simulated)
    state_store_size = 0.0
    if result_count > 0:
        # Estimate state store size (in practice, check Spark UI)
        state_store_size = result_count * 100 / 1024 / 1024  # MB estimate
    
    return {
        "streaming_latency_ms": latency,
        "processing_rate_rows_per_second": processed_rows,
        "total_rows_processed": input_rows,
        "watermark_delay_seconds": 10,
        "state_store_size_mb": state_store_size,
        "windowed_aggregation_count": result_count,
        "checkpoint_usage": {"location": checkpoint_location, "cleaned_up": True},
        "sample_results": [str(row) for row in result_sample[:2]]
    }

# ============================================================================
# Exercise 6: PySpark-FastAPI Integration - SOLUTION
# ============================================================================

# FastAPI application setup
spark_manager = None
executor = ThreadPoolExecutor(max_workers=2)

class SparkManager:
    """Singleton SparkSession manager for FastAPI."""
    _instance = None
    _spark = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_spark(self):
        if self._spark is None:
            self._spark = create_optimized_spark_session()
        return self._spark
    
    def stop_spark(self):
        if self._spark:
            self._spark.stop()
            self._spark = None

def exercise_6_fastapi_integration_solution(spark: SparkSession) -> Dict[str, Any]:
    """
    Solution for Exercise 6: Integrating PySpark with FastAPI REST API
    """
    print("\n=== Exercise 6: PySpark-FastAPI Integration ===")
    print("Building integrated PySpark-FastAPI application...")
    
    # Note: We'll simulate FastAPI behavior without actually starting a server
    # for the purpose of this exercise solution.
    
    # 1. Create sample data for API endpoints
    sample_data = generate_sample_data(spark, 1000)
    sample_data.createOrReplaceTempView("api_data")
    
    # 2. Implement API endpoint functions
    api_metrics = {
        "response_times": [],
        "cache_hits": 0,
        "cache_misses": 0,
        "concurrent_requests": 0
    }
    
    # Simple cache simulation
    query_cache = {}
    
    def execute_query(query: str, use_cache: bool = True) -> Dict:
        """Execute Spark SQL query with optional caching."""
        start_time = time.time()
        
        # Check cache
        cache_key = hash(query)
        if use_cache and cache_key in query_cache:
            api_metrics["cache_hits"] += 1
            result = query_cache[cache_key]
            cache_status = "HIT"
        else:
            api_metrics["cache_misses"] += 1
            result_df = spark.sql(query)
            
            # Convert to JSON-serializable format
            result = {
                "columns": result_df.columns,
                "data": [row.asDict() for row in result_df.limit(100).collect()],
                "count": result_df.count()
            }
            
            # Cache result (with size limit)
            if len(query_cache) < 10:  # Limit cache size
                query_cache[cache_key] = result
            cache_status = "MISS"
        
        response_time = (time.time() - start_time) * 1000  # ms
        
        api_metrics["response_times"].append(response_time)
        
        return {
            "result": result,
            "response_time_ms": response_time,
            "cache_status": cache_status,
            "cached_items": len(query_cache)
        }
    
    # 3. Test concurrent request handling
    print("Testing concurrent request handling...")
    
    def simulate_api_request(query_idx: int):
        """Simulate an API request."""
        api_metrics["concurrent_requests"] += 1
        
        queries = [
            "SELECT category, COUNT(*) as count FROM api_data GROUP BY category",
            "SELECT user_id, SUM(amount) as total FROM api_data GROUP BY user_id ORDER BY total DESC LIMIT 10",
            "SELECT AVG(amount) as avg_amount, AVG(rating) as avg_rating FROM api_data",
            "SELECT category, user_id, amount FROM api_data WHERE amount > 500"
        ]
        
        query = queries[query_idx % len(queries)]
        result = execute_query(query, use_cache=True)
        
        api_metrics["concurrent_requests"] -= 1
        return result
    
    # Simulate concurrent requests
    import concurrent.futures
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(simulate_api_request, i) for i