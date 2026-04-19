# Advanced PySpark Gotchas & Best Practices for 8GB RAM

## 🚨 Critical Gotchas in Advanced PySpark

### 1. **Catalyst Optimizer Over-Optimization**
**Problem:** Catalyst may over-optimize complex queries, leading to unexpected execution plans or performance degradation.

**Symptoms:**
- Query runs slower after adding "optimizations"
- `explain()` shows unexpected plan changes
- Memory usage spikes during certain operations

**Solutions:**
```python
# Disable specific optimizations if needed
spark.conf.set("spark.sql.optimizer.excludedRules", "")

# Force specific join strategy
df1.hint("broadcast").join(df2, "key")

# Use .cache() strategically to break optimization chains
intermediate_df = df.filter(...).select(...).cache()
result = intermediate_df.groupBy(...).agg(...)
```

### 2. **Memory Management Pitfalls on 8GB RAM**

#### **2.1 Garbage Collection Thrashing**
**Problem:** Frequent GC pauses slow down Spark jobs on memory-constrained systems.

**Detection:**
```bash
# Check GC logs
spark-submit --conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps"
```

**Optimization for 8GB RAM:**
```python
# Optimal JVM settings for 8GB
spark = SparkSession.builder \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.memory.fraction", "0.6") \
    .config("spark.memory.storageFraction", "0.3") \
    .config("spark.executor.extraJavaOptions", 
            "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:ConcGCThreads=4") \
    .getOrCreate()
```

#### **2.2 Off-Heap Memory Leaks**
**Problem:** Off-heap memory not properly released, causing gradual memory exhaustion.

**Best Practices:**
```python
# Monitor off-heap usage
spark.sparkContext.uiWebUrl  # Check Spark UI memory tab

# Explicitly unpersist DataFrames
df.unpersist(blocking=True)

# Use storage level wisely
df.persist(StorageLevel.MEMORY_AND_DISK_SER)  # Serialized to save memory
```

### 3. **Join Strategy Selection Gone Wrong**

#### **3.1 Broadcast Join on Moderately Large Tables**
**Problem:** Broadcasting tables that are too large (e.g., 50MB+) causes driver OOM.

**Rule of Thumb for 8GB RAM:**
- **Broadcast:** < 10MB (safe), < 30MB (risky), > 30MB (avoid)
- **Sort Merge:** 30MB - 500MB
- **Shuffle Hash:** > 500MB (with proper partitioning)

**Safe broadcast implementation:**
```python
def safe_broadcast_join(df1, df2, join_key, max_broadcast_size_mb=30):
    """Safely apply broadcast join only if table size is appropriate."""
    # Estimate DataFrame size
    df2_size_mb = df2.rdd.map(lambda x: len(str(x))).sum() / (1024 * 1024)
    
    if df2_size_mb < max_broadcast_size_mb:
        return df1.join(broadcast(df2), join_key)
    else:
        # Ensure proper partitioning for sort merge
        df1 = df1.repartition(100, join_key)
        df2 = df2.repartition(100, join_key)
        return df1.join(df2, join_key)
```

#### **3.2 Data Skew in Joins**
**Problem:** A few keys have disproportionately large data, causing straggler tasks.

**Skew Handling Techniques:**
```python
# Technique 1: Salting
def salt_skewed_join(df1, df2, join_key, salt_buckets=10):
    """Add random salt to distribute skewed keys."""
    from pyspark.sql.functions import concat, lit, rand
    
    # Add salt to skewed DataFrame
    df1_salted = df1.withColumn("salted_key", 
                                 concat(col(join_key), lit("_"), 
                                        (rand() * salt_buckets).cast("int")))
    df2_exploded = df2.withColumn("salted_key", 
                                   explode(array([lit(f"{i}") for i in range(salt_buckets)])))
    
    return df1_salted.join(df2_exploded, "salted_key")

# Technique 2: Split and Union
def split_skewed_join(df1, df2, join_key, skewed_keys):
    """Handle known skewed keys separately."""
    # Split data
    df1_skewed = df1.filter(col(join_key).isin(skewed_keys))
    df1_normal = df1.filter(~col(join_key).isin(skewed_keys))
    
    df2_skewed = df2.filter(col(join_key).isin(skewed_keys))
    df2_normal = df2.filter(~col(join_key).isin(skewed_keys))
    
    # Join separately with different strategies
    result_skewed = df1_skewed.join(broadcast(df2_skewed), join_key)  # Broadcast for small skewed
    result_normal = df1_normal.join(df2_normal, join_key)  # Sort merge for normal
    
    return result_skewed.union(result_normal)
```

### 4. **ML Pipeline Memory Explosion**

#### **4.1 Feature Vector Size**
**Problem:** One-hot encoding on high-cardinality columns creates massive feature vectors.

**Memory-Efficient Alternatives:**
```python
# Instead of OneHotEncoder for high-cardinality (>1000 categories)
from pyspark.ml.feature import StringIndexer, TargetEncoder

# Use target encoding (mean encoding) for high-cardinality
# Or use frequency-based encoding
df = df.withColumn("category_freq", 
                   count("*").over(Window.partitionBy("category")) / count("*").over())
```

#### **4.2 Cross-Validation Memory Issues**
**Problem:** `CrossValidator` creates multiple copies of data, exhausting memory.

**Optimization:**
```python
# Reduce number of folds for 8GB RAM
paramGrid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.01, 0.1]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5]) \
    .build()

# Use 3-fold instead of 5-fold
crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=3,  # Reduced for memory
                          parallelism=2)  # Limit parallel execution
```

### 5. **Structured Streaming Memory Traps**

#### **5.1 Watermark and State Size**
**Problem:** Incorrect watermark leads to unbounded state growth.

**Correct Configuration:**
```python
# For 8GB RAM, limit state retention
streaming_query = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(window("event_time", "5 minutes"), "user_id") \
    .agg(count("*").alias("events")) \
    .writeStream \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .trigger(processingTime="30 seconds") \  # Micro-batches
    .start()

# Monitor state store size
spark.streams.active[0].recentProgress  # Check numInputRows, stateOperators
```

#### **5.2 Sink Backpressure**
**Problem:** Slow sink causes memory buildup in streaming buffers.

**Backpressure Management:**
```python
# Configure max offsets per trigger
spark.conf.set("spark.sql.streaming.maxOffsetsPerTrigger", 10000)

# Use foreachBatch for better control
def process_batch(batch_df, batch_id):
    # Process in smaller chunks
    for chunk in np.array_split(batch_df.toPandas(), 4):
        # Process chunk
        pass

streaming_query = df.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()
```

### 6. **FastAPI Integration Issues**

#### **6.1 SparkSession Singleton Problems**
**Problem:** Multiple SparkSessions in FastAPI workers cause resource contention.

**Proper Singleton Pattern:**
```python
# spark_session.py
from pyspark.sql import SparkSession
import atexit

_spark = None

def get_spark_session():
    global _spark
    if _spark is None:
        _spark = SparkSession.builder \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "2g") \
            .config("spark.sql.shuffle.partitions", "50") \
            .getOrCreate()
        
        # Register cleanup
        atexit.register(lambda: _spark.stop() if _spark else None)
    
    return _spark

# In FastAPI route
@app.post("/process")
async def process_data(request: Request):
    spark = get_spark_session()  # Reuse singleton
    # Process data
```

#### **6.2 Async Job Submission Deadlocks**
**Problem:** Blocking Spark operations in async endpoints block the entire event loop.

**Solution: Use ThreadPoolExecutor:**
```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor(max_workers=2)

@app.post("/async-process")
async def async_process(request: Request):
    loop = asyncio.get_event_loop()
    
    # Run Spark job in thread pool
    result = await loop.run_in_executor(
        executor, 
        lambda: spark.sql("SELECT * FROM large_table").count()
    )
    
    return {"count": result}
```

## 🛠️ Best Practices for 8GB RAM Production

### 1. **Monitoring and Alerting**

```python
def monitor_resources(spark):
    """Monitor Spark job resources for 8GB constraints."""
    import psutil
    
    metrics = {
        "driver_memory_mb": psutil.Process().memory_info().rss / 1024 / 1024,
        "system_memory_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=1),
    }
    
    # Alert if approaching limits
    if metrics["driver_memory_mb"] > 1500:  # 1.5GB threshold
        print("WARNING: Driver memory approaching limit")
        # Trigger spill to disk
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
    
    return metrics
```

### 2. **Progressive Optimization Strategy**

**Step 1: Baseline (Always start here)**
```python
# Minimal configuration for 8GB
spark = SparkSession.builder \
    .config("spark.driver.memory", "1g") \
    .config("spark.executor.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "50") \
    .getOrCreate()
```

**Step 2: Monitor and Identify Bottlenecks**
- Check Spark UI for skew, spills, GC
- Use `.explain()` to understand query plans
- Monitor system resources during execution

**Step 3: Apply Targeted Optimizations**
- Add specific configs based on bottlenecks
- Test one change at a time
- Measure before/after performance

### 3. **Memory-Aware Data Processing Patterns**

```python
def process_large_dataset_memory_aware(spark, input_path):
    """Process dataset with memory constraints in mind."""
    
    # 1. Read with schema to avoid inference
    schema = StructType([...])
    df = spark.read.schema(schema).parquet(input_path)
    
    # 2. Early filtering and projection
    df = df.select("essential_cols").filter("important_condition")
    
    # 3. Check estimated size
    row_count = df.count()
    if row_count > 1000000:  # 1M rows threshold
        # Use disk-based processing
        df = df.repartition(100).persist(StorageLevel.DISK_ONLY)
    
    # 4. Process in chunks if needed
    for month in range(1, 13):
        monthly_df = df.filter(f"month = {month}")
        # Process monthly chunk
        process_chunk(monthly_df)
    
    return df
```

### 4. **Disaster Recovery for OOM**

```python
def safe_execution_with_fallback(spark, operation, fallback_operation):
    """Execute with OOM protection and fallback."""
    try:
        # Try with optimal settings
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10MB
        result = operation()
        return result
    except Exception as e:
        if "Java heap space" in str(e) or "OutOfMemory" in str(e):
            print("OOM detected, switching to fallback mode")
            # Apply aggressive memory savings
            spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")  # No broadcast
            spark.conf.set("spark.sql.shuffle.partitions", "200")  # More partitions
            return fallback_operation()
        else:
            raise
```

## 📊 Performance Checklist for 8GB RAM

### Before Running Job:
- [ ] Set `spark.driver.memory` ≤ 2GB
- [ ] Set `spark.executor.memory` ≤ 2GB  
- [ ] Configure `spark.memory.fraction` = 0.6
- [ ] Enable `spark.sql.adaptive.enabled` = true
- [ ] Set `spark.sql.shuffle.partitions` = 50-100
- [ ] Disable broadcast for tables > 30MB

### During Development:
- [ ] Use `.explain()` to verify query plans
- [ ] Monitor Spark UI for spills and skew
- [ ] Test with sample data before full dataset
- [ ] Implement incremental processing for large datasets

### After Job Completes:
- [ ] Check executor/driver logs for GC warnings
- [ ] Verify no data spills to disk (unless intentional)
- [ ] Clean up cached DataFrames with `.unpersist()`
- [ ] Stop SparkSession to release resources

## 🔧 Troubleshooting Common Issues

### 1. **"Java heap space" Error**
```bash
# Immediate actions:
1. Increase partitions: spark.conf.set("spark.sql.shuffle.partitions", "200")
2. Disable broadcast: spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
3. Persist to disk: df.persist(StorageLevel.DISK_ONLY)
4. Reduce executor memory: spark.conf.set("spark.executor.memory", "1g")
```

### 2. **Long GC Pauses**
```python
# Switch to G1GC with optimized settings
spark.conf.set("spark.executor.extraJavaOptions",
               "-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=35")
```

### 3. **Slow Join Performance**
```python
# Diagnostic steps:
1. Check data skew: df.groupBy("join_key").count().orderBy("count", ascending=False).show()
2. Verify join strategy: df.explain()  # Look for "BroadcastHashJoin" vs "SortMergeJoin"
3. Consider salting for skewed keys
```

## 🎯 Key Takeaways for 8GB RAM

1. **Be Conservative:** Start with minimal memory allocation, increase only if needed
2. **Monitor Constantly:** Use Spark UI and system monitoring tools
3. **Design for Spill:** Assume some operations will spill to disk, optimize for it
4. **Batch Processing:** Break large operations into smaller batches
5. **Clean Up:** Always `.unpersist()` cached DataFrames and stop SparkSessions

## 🔗 Integration with Other Projects

- **02_5_pyspark_basics:** Builds on basic optimization techniques
- **05_streaming_analytics:** Applies memory-aware streaming patterns  
- **06_fastapi_integration:** Uses singleton SparkSession pattern
- **14_5_hadoop_basics:** Complementary big data processing techniques

---

*Last Updated: April 2026*  
*Optimized for 8GB RAM systems running PySpark 3.5+*