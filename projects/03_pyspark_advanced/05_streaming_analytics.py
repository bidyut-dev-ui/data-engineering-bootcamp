#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 5: Streaming Analytics with Structured Streaming

This tutorial covers PySpark Structured Streaming for real-time data processing
on 8GB RAM systems, including window operations, watermarking, and integration
with Kafka/Redpanda.

Key Concepts:
- Structured Streaming fundamentals
- Window operations and watermarking
- Stateful processing with 8GB RAM constraints
- Output modes and sinks
- Fault tolerance and checkpointing

Optimized for 8GB RAM with simulated streaming data.
"""

import time
import json
import tempfile
import os
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, count, sum as spark_sum, avg, from_json, to_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.streaming import StreamingQuery

def create_streaming_spark_session():
    """Create a SparkSession optimized for streaming on 8GB RAM"""
    return SparkSession.builder \
        .appName("Streaming-Analytics-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.streaming.schemaInference", "true") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/streaming-checkpoints") \
        .config("spark.sql.streaming.metricsEnabled", "true") \
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
        .getOrCreate()

def generate_streaming_data(output_dir, num_files=10, events_per_file=100):
    """Generate simulated streaming data files"""
    print(f"Generating {num_files} streaming data files in {output_dir}...")
    
    # Create schema for streaming data
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("device", StringType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Event types and devices for variety
    event_types = ["click", "purchase", "view", "login", "logout", "search"]
    devices = ["mobile", "desktop", "tablet"]
    locations = ["US", "UK", "DE", "FR", "IN", "JP", "BR", "AU"]
    
    # Generate files with timestamped events
    for file_num in range(num_files):
        file_path = os.path.join(output_dir, f"events_{file_num:03d}.json")
        events = []
        
        # Generate events with increasing timestamps
        base_time = datetime.now() - timedelta(minutes=num_files - file_num)
        
        for i in range(events_per_file):
            event_time = base_time + timedelta(seconds=i)
            event = {
                "event_id": f"evt_{file_num:03d}_{i:04d}",
                "user_id": f"user_{i % 1000:04d}",
                "event_type": event_types[i % len(event_types)],
                "amount": round((i % 100) * 1.5, 2) if event_types[i % len(event_types)] == "purchase" else 0.0,
                "timestamp": event_time.isoformat(),
                "device": devices[i % len(devices)],
                "location": locations[i % len(locations)]
            }
            events.append(json.dumps(event))
        
        # Write events to file
        with open(file_path, 'w') as f:
            f.write("\n".join(events))
        
        print(f"  Created {file_path} with {events_per_file} events")
    
    print(f"Total: {num_files * events_per_file} events generated")
    return output_dir

def demonstrate_basic_streaming(spark, data_dir):
    """Show basic structured streaming concepts"""
    print("\n" + "="*80)
    print("BASIC STRUCTURED STREAMING")
    print("="*80)
    
    # Define schema for JSON data
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("device", StringType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Read streaming data
    print("\n1. Reading streaming data from directory...")
    streaming_df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(data_dir)
    
    print("Streaming DataFrame schema:")
    streaming_df.printSchema()
    
    # Basic transformations
    print("\n2. Applying transformations...")
    transformed_df = streaming_df \
        .filter(col("event_type").isin(["click", "purchase", "view"])) \
        .select("event_id", "user_id", "event_type", "amount", "timestamp", "device") \
        .withWatermark("timestamp", "5 minutes")  # 5-minute watermark
    
    # Simple aggregation
    print("\n3. Aggregating events by type...")
    aggregated_df = transformed_df \
        .groupBy("event_type") \
        .agg(
            count("*").alias("event_count"),
            spark_sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount")
        )
    
    # Start streaming query
    print("\n4. Starting streaming query (memory sink)...")
    query = aggregated_df.writeStream \
        .outputMode("complete") \
        .format("memory") \
        .queryName("event_aggregations") \
        .start()
    
    # Wait for some data to be processed
    print("Processing streaming data...")
    time.sleep(5)  # Give time to process some files
    
    # Show results
    print("\n5. Query results in memory table:")
    try:
        spark.sql("SELECT * FROM event_aggregations").show(truncate=False)
    except:
        print("No data processed yet - waiting a bit more...")
        time.sleep(3)
        spark.sql("SELECT * FROM event_aggregations").show(truncate=False)
    
    # Stop the query
    query.stop()
    print("\nStreaming query stopped.")
    
    return streaming_df

def demonstrate_window_operations(spark, data_dir):
    """Show window-based aggregations"""
    print("\n" + "="*80)
    print("WINDOW OPERATIONS & WATERMARKING")
    print("="*80)
    
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("device", StringType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Read streaming data
    streaming_df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(data_dir)
    
    # Apply watermark for late data handling
    watermarked_df = streaming_df.withWatermark("timestamp", "10 minutes")
    
    # Window-based aggregation
    print("\n1. Tumbling window (5-minute windows):")
    windowed_df = watermarked_df \
        .groupBy(
            window(col("timestamp"), "5 minutes"),
            "event_type"
        ) \
        .agg(
            count("*").alias("event_count"),
            spark_sum("amount").alias("total_amount")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "event_type",
            "event_count",
            "total_amount"
        )
    
    # Start windowed query
    print("Starting windowed aggregation query...")
    query = windowed_df.writeStream \
        .outputMode("append") \
        .format("memory") \
        .queryName("windowed_events") \
        .start()
    
    time.sleep(8)  # Process more data
    
    print("\nWindowed aggregation results:")
    try:
        spark.sql("SELECT * FROM windowed_events ORDER BY window_start DESC").show(truncate=False)
    except:
        print("Waiting for windowed data...")
        time.sleep(5)
        spark.sql("SELECT * FROM windowed_events ORDER BY window_start DESC").show(truncate=False)
    
    # Sliding window example
    print("\n2. Sliding window (5-minute window, sliding every 1 minute):")
    sliding_df = watermarked_df \
        .groupBy(
            window(col("timestamp"), "5 minutes", "1 minute"),
            "device"
        ) \
        .agg(count("*").alias("event_count"))
    
    # Start sliding window query
    sliding_query = sliding_df.writeStream \
        .outputMode("update") \
        .format("memory") \
        .queryName("sliding_window") \
        .start()
    
    time.sleep(5)
    
    print("Sliding window results (sample):")
    try:
        spark.sql("SELECT * FROM sliding_window LIMIT 10").show(truncate=False)
    except:
        print("No sliding window data yet")
    
    # Stop queries
    query.stop()
    sliding_query.stop()
    print("\nWindow queries stopped.")
    
    return windowed_df

def demonstrate_stateful_processing(spark, data_dir):
    """Show stateful operations with 8GB RAM constraints"""
    print("\n" + "="*80)
    print("STATEFUL PROCESSING WITH 8GB RAM CONSTRAINTS")
    print("="*80)
    
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("device", StringType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Read streaming data
    streaming_df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(data_dir)
    
    # Stateful operation: User session tracking
    print("\n1. User session tracking with state:")
    
    # Filter for user actions and add watermark
    user_actions = streaming_df \
        .filter(col("event_type").isin(["click", "view", "purchase"])) \
        .withWatermark("timestamp", "15 minutes") \
        .select("user_id", "event_type", "timestamp", "amount")
    
    # Count events per user with state
    user_event_counts = user_actions \
        .groupBy("user_id") \
        .agg(
            count("*").alias("total_events"),
            spark_sum("amount").alias("total_spent")
        )
    
    # Start stateful query
    print("Starting stateful aggregation (complete output mode)...")
    stateful_query = user_event_counts.writeStream \
        .outputMode("complete") \
        .format("memory") \
        .queryName("user_state") \
        .option("checkpointLocation", "/tmp/user-state-checkpoint") \
        .start()
    
    time.sleep(10)  # Process data
    
    print("\nUser state (top 10 users by events):")
    try:
        spark.sql("SELECT * FROM user_state ORDER BY total_events DESC LIMIT 10").show(truncate=False)
    except:
        print("Processing stateful data...")
        time.sleep(5)
        spark.sql("SELECT * FROM user_state ORDER BY total_events DESC LIMIT 10").show(truncate=False)
    
    # Memory management for stateful operations
    print("\n2. Memory Management for Stateful Operations:")
    print("""
For 8GB RAM systems:
- Use withWatermark() to limit state retention
- Set appropriate watermark intervals (e.g., 10-30 minutes)
- Use .option("checkpointLocation", "...") for fault tolerance
- Monitor state store size in Spark UI
- Consider reducing state TTL for long-running queries
""")
    
    # Stop query
    stateful_query.stop()
    print("\nStateful query stopped.")
    
    return user_event_counts

def demonstrate_output_modes(spark, data_dir):
    """Show different output modes"""
    print("\n" + "="*80)
    print("OUTPUT MODES COMPARISON")
    print("="*80)
    
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("device", StringType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Read streaming data
    streaming_df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(data_dir)
    
    # Prepare data for output mode comparison
    purchase_events = streaming_df \
        .filter(col("event_type") == "purchase") \
        .withWatermark("timestamp", "5 minutes")
    
    # Output Mode 1: Append (only new rows)
    print("\n1. Append Mode (only new rows):")
    print("   - Suitable for queries with watermark")
    print("   - Only outputs rows that won't be updated")
    
    append_query = purchase_events \
        .groupBy("device") \
        .agg(spark_sum("amount").alias("total_sales")) \
        .writeStream \
        .outputMode("append") \
        .format("memory") \
        .queryName("append_output") \
        .start()
    
    # Output Mode 2: Complete (all rows every trigger)
    print("\n2. Complete Mode (all rows every trigger):")
    print("   - Outputs entire result table each time")
    print("   - Suitable for aggregated queries")
    print("   - Requires unbounded state retention")
    
    complete_query = purchase_events \
        .groupBy("location") \
        .agg(count("*").alias("purchase_count")) \
        .writeStream \
        .outputMode("complete") \
        .format("memory") \
        .queryName("complete_output") \
        .start()
    
    # Output Mode 3: Update (only changed rows)
    print("\n3. Update Mode (only changed rows):")
    print("   - Outputs only rows that were updated")
    print("   - Most efficient for many updates")
    print("   - Requires aggregations with watermark")
    
    update_query = purchase_events \
        .groupBy(window(col("timestamp"), "5 minutes"), "event_type") \
        .agg(spark_sum("amount").alias("window_sales")) \
        .writeStream \
        .outputMode("update") \
        .format("memory") \
        .queryName("update_output") \
        .start()
    
    # Let queries run for a bit
    print("\nRunning all output mode queries for 10 seconds...")
    time.sleep(10)
    
    # Show results
    print("\nAppend Mode Results:")
    try:
        spark.sql("SELECT * FROM append_output").show(truncate=False)
    except:
        print("No append output yet")
    
    print("\nComplete Mode Results:")
    try:
        spark.sql("SELECT * FROM complete_output").show(truncate=False)
    except:
        print("No complete output yet")
    
    print("\nUpdate Mode Results:")
    try:
        spark.sql("SELECT * FROM update_output").show(truncate=False)
    except:
        print("No update output yet")
    
    # Stop queries
    append_query.stop()
    complete_query.stop()
    update_query.stop()
    print("\nAll output mode queries stopped.")

def demonstrate_fault_tolerance():
    """Show fault tolerance and checkpointing"""
    print("\n" + "="*80)
    print("FAULT TOLERANCE & CHECKPOINTING")
    print("="*80)
    
    print("""
Structured Streaming provides fault tolerance through:
1. **Checkpointing**: Saves query progress and intermediate state
2. **Write-Ahead Logs**: Ensures exactly-once processing
3. **Watermarking**: Limits state size for 8GB RAM

Checkpoint Location Configuration:
```python
query = df.writeStream \\
    .outputMode("append") \\
    .format("parquet") \\
    .option("checkpointLocation", "/tmp/streaming-checkpoints") \\
    .start("/tmp/output")
```

Recovery Process:
1. On failure, Spark reads checkpoint metadata
2. Restores state from checkpoint
3. Resumes processing from last committed offset
4. Ensures exactly-once semantics

Memory Considerations for 8GB RAM:
- Use watermark to bound state size
- Set reasonable trigger intervals (e.g., 1 minute)
- Monitor state store metrics in Spark UI
- Use disk-based checkpoints, not memory
""")

def streaming_exercises(data_dir):
    """Provide hands-on streaming exercises"""
    print("\n" + "="*80)
    print("STREAMING ANALYTICS EXERCISES")
    print("="*80)
    
    print("""
Exercise 1: Basic Streaming Pipeline
------------------------------------------------
1. Read JSON files from a directory as a stream
2. Filter for specific event types (e.g., "purchase")
3. Calculate real-time metrics (count, sum, average)
4. Write results to memory sink and query them

Exercise 2: Windowed Aggregations
------------------------------------------------
1. Create tumbling windows of 5 minutes
2. Aggregate events by type within each window
3. Add watermark of 10 minutes for late data
4. Compare append vs update output modes

Exercise 3: Stateful Session Tracking
------------------------------------------------
1. Track user sessions with 30-minute timeouts
2. Calculate session duration and activity count
3. Implement stateful aggregation with checkpointing
4. Test fault tolerance by stopping/restarting query

Exercise 4: Streaming Joins
------------------------------------------------
1. Create a static reference dataset (e.g., user profiles)
2. Join streaming events with static reference data
3. Implement stream-stream join with watermarking
4. Handle late arriving data

Exercise 5: Performance Optimization
------------------------------------------------
1. Monitor streaming query metrics in Spark UI
2. Adjust trigger interval for 8GB RAM constraints
3. Implement backpressure handling
4. Test with different batch sizes
""")

def main():
    """Main execution function"""
    print("="*80)
    print("ADVANCED PYSPARK: STREAMING ANALYTICS ON 8GB RAM")
    print("="*80)
    print("This tutorial covers PySpark Structured Streaming for real-time processing.")
    print("All examples optimized for 8GB RAM systems.\n")
    
    # Create temporary directory for streaming data
    temp_dir = tempfile.mkdtemp(prefix="streaming_data_")
    print(f"Using temporary directory: {temp_dir}")
    
    # Initialize Spark
    spark = create_streaming_spark_session()
    
    try:
        # Generate streaming data
        data_dir = generate_streaming_data(temp_dir, num_files=5, events_per_file=50)
        
        # Run demonstrations
        streaming_df = demonstrate_basic_streaming(spark, data_dir)
        windowed_df = demonstrate_window_operations(spark, data_dir)
        stateful_df = demonstrate_stateful_processing(spark, data_dir)
        demonstrate_output_modes(spark, data_dir)
        demonstrate_fault_tolerance()
        streaming_exercises(data_dir)
        
        print("\n" + "="*80)
        print("TUTORIAL COMPLETE")
        print("="*80)
        print("Key Takeaways:")
        print("1. Structured Streaming provides fault-tolerant real-time processing")
        print("2. Watermarking limits state size for 8GB RAM systems")
        print("3. Window operations enable time-based aggregations")
        print("4. Checkpointing ensures exactly-once processing")
        print("5. Choose output mode based on use case (append/update/complete)")
        print("\nNext: Run 06_fastapi_integration.py for PySpark + FastAPI integration")
        
    finally:
        # Cleanup
        spark.stop()
        
        # Remove temporary directory
        import shutil
        try:
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temporary directory: {temp_dir}")
        except:
            print(f"\nNote: Could not clean up {temp_dir}")
        
        print("Spark session stopped.")

if __name__ == "__main__":
    main()