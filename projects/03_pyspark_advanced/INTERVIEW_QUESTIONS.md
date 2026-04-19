# Advanced PySpark Interview Questions

## 🎯 Senior Data Engineer / PySpark Specialist Questions

### 1. **Explain Catalyst Optimizer's Rule-Based and Cost-Based Optimization**

**Question:** How does Spark's Catalyst optimizer work, and what's the difference between rule-based and cost-based optimization?

**Answer:**
Catalyst is Spark's query optimization framework with two phases:

1. **Rule-Based Optimization (RBO):**
   - Applies heuristic rules regardless of data statistics
   - Examples: predicate pushdown, constant folding, column pruning
   - Works on logical plan before execution

2. **Cost-Based Optimization (CBO):**
   - Uses data statistics (size, cardinality, histograms) to choose optimal plans
   - Examples: join reordering, broadcast join selection
   - Requires `ANALYZE TABLE` or `spark.sql.statistics` collection

**Example:**
```python
# Enable CBO and collect statistics
spark.conf.set("spark.sql.cbo.enabled", "true")
spark.conf.set("spark.sql.statistics.histogram.enabled", "true")

df = spark.read.parquet("data.parquet")
df.createOrReplaceTempView("table")

# Collect statistics for CBO
spark.sql("ANALYZE TABLE table COMPUTE STATISTICS")

# Catalyst will use stats for optimization
result = spark.sql("""
    SELECT a.id, b.name 
    FROM table a 
    JOIN table b ON a.id = b.id 
    WHERE a.value > 100
""")
```

### 2. **Memory Management in PySpark for 8GB RAM Systems**

**Question:** How would you configure PySpark memory settings for an 8GB RAM machine running both driver and executor?

**Answer:**
For 8GB RAM with single node (local mode):

```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.memory.fraction", "0.6") \
    .config("spark.memory.storageFraction", "0.3") \
    .config("spark.sql.shuffle.partitions", "50") \
    .config("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10MB \
    .config("spark.executor.extraJavaOptions", 
            "-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=35") \
    .config("spark.driver.extraJavaOptions",
            "-XX:+UseG1GC -XX:MaxGCPauseMillis=200") \
    .getOrCreate()
```

**Key Considerations:**
- Leave 2-3GB for OS and other processes
- Use G1GC for better pause times
- Monitor spill to disk with `spark.sql.shuffle.spill.numElementsForceSpillThreshold`
- Consider `MEMORY_AND_DISK_SER` for caching to reduce memory footprint

### 3. **Handling Extreme Data Skew in Joins**

**Question:** You have a join where 90% of records have the same key value. How would you handle this skew?

**Answer:**
Multiple strategies:

**1. Salting Technique:**
```python
from pyspark.sql.functions import concat, lit, rand, explode, array

# Add random salt to skewed keys
df1_salted = df1.withColumn("salted_key", 
                             concat(col("skewed_key"), lit("_"), 
                                    (rand() * 100).cast("int")))

# Explode small table to match all salt values
salt_values = [lit(i) for i in range(100)]
df2_exploded = df2.withColumn("salted_key", explode(array(salt_values)))

result = df1_salted.join(df2_exploded, "salted_key")
```

**2. Split and Union:**
```python
# Identify skewed keys
skewed_keys = ["key_value_1", "key_value_2"]

# Process skewed and non-skewed separately
df1_skewed = df1.filter(col("key").isin(skewed_keys))
df1_normal = df1.filter(~col("key").isin(skewed_keys))

df2_skewed = df2.filter(col("key").isin(skewed_keys))
df2_normal = df2.filter(~col("key").isin(skewed_keys))

# Use broadcast for skewed (small after filtering)
result_skewed = df1_skewed.join(broadcast(df2_skewed), "key")
result_normal = df1_normal.join(df2_normal, "key")

result = result_skewed.union(result_normal)
```

**3. Adaptive Query Execution (AQE):**
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

### 4. **PySpark MLlib Pipeline Optimization for Limited Memory**

**Question:** How would you optimize a PySpark ML pipeline for an 8GB RAM system?

**Answer:**

**Memory-Efficient Pipeline Design:**
```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, MinMaxScaler
from pyspark.ml.classification import LogisticRegression

# 1. Reduce feature dimension early
df = df.select("important_features", "label")

# 2. Use frequency encoding instead of one-hot for high-cardinality
from pyspark.sql import Window
df = df.withColumn("category_freq", 
                   count("*").over(Window.partitionBy("category")) / 
                   count("*").over())

# 3. Pipeline with memory-aware stages
pipeline = Pipeline(stages=[
    StringIndexer(inputCol="category", outputCol="category_index"),
    VectorAssembler(inputCols=["numerical_features"], outputCol="features"),
    MinMaxScaler(inputCol="features", outputCol="scaled_features"),  # Less memory than StandardScaler
    LogisticRegression(featuresCol="scaled_features", labelCol="label",
                      maxIter=10,  # Fewer iterations
                      regParam=0.01)
])

# 4. Cross-validation with reduced parallelism
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid = ParamGridBuilder() \
    .addGrid(LogisticRegression.regParam, [0.01, 0.1]) \
    .build()

crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=3,  # Reduced from 5
                          parallelism=2)  # Limit parallel execution
```

### 5. **Structured Streaming with Watermark and State Management**

**Question:** Explain how watermarking works in Structured Streaming and how you'd handle late-arriving data.

**Answer:**
Watermarking defines how long to wait for late data before considering a window complete:

```python
from pyspark.sql.functions import window, col

streaming_df = spark \
    .readStream \
    .schema(schema) \
    .json("streaming_data/")

# 10 minute watermark, 5 minute windows
windowed_counts = streaming_df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("user_id")
    ) \
    .count()

# Output modes:
# - Append: Only new rows (requires watermark)
# - Update: Updated aggregates
# - Complete: Full result set (state grows indefinitely)

query = windowed_counts \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .trigger(processingTime="30 seconds") \
    .start()
```

**Handling Late Data:**
- Data arriving within watermark is processed
- Data arriving after watermark is dropped
- State is automatically cleaned up after watermark + allowed lateness
- Use `withWatermark` and monitor state store metrics

### 6. **FastAPI Integration with PySpark Singleton Pattern**

**Question:** How would you integrate PySpark with FastAPI in a production environment?

**Answer:**
**Singleton Pattern with Connection Pooling:**

```python
# spark_manager.py
from pyspark.sql import SparkSession
import atexit
from contextlib import contextmanager

class SparkManager:
    _spark_session = None
    _lock = threading.Lock()
    
    @classmethod
    def get_spark_session(cls):
        with cls._lock:
            if cls._spark_session is None:
                cls._spark_session = SparkSession.builder \
                    .appName("FastAPI-Spark") \
                    .config("spark.driver.memory", "2g") \
                    .config("spark.executor.memory", "2g") \
                    .config("spark.sql.shuffle.partitions", "50") \
                    .config("spark.sql.adaptive.enabled", "true") \
                    .getOrCreate()
                
                # Register cleanup
                atexit.register(cls._cleanup)
            
            return cls._spark_session
    
    @classmethod
    def _cleanup(cls):
        if cls._spark_session:
            cls._spark_session.stop()
            cls._spark_session = None

# FastAPI application
from fastapi import FastAPI, BackgroundTasks
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

@app.post("/process-batch")
async def process_batch(request: Request, background_tasks: BackgroundTasks):
    """Process data asynchronously"""
    data = await request.json()
    
    # Submit to thread pool to avoid blocking event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: process_spark_job(data)
    )
    
    return {"status": "completed", "result": result}

def process_spark_job(data):
    spark = SparkManager.get_spark_session()
    # Process data with Spark
    df = spark.createDataFrame(data)
    return df.count()
```

### 7. **Debugging Slow PySpark Jobs**

**Question:** A PySpark job is running slowly. What steps would you take to diagnose and fix it?

**Answer:**

**Diagnostic Steps:**

1. **Check Spark UI:**
   - Task execution times and skew
   - Shuffle read/write sizes
   - GC time and frequency
   - Storage memory usage

2. **Analyze Query Plan:**
   ```python
   df.explain(extended=True)  # Show logical, analyzed, optimized, and physical plans
   ```

3. **Monitor Key Metrics:**
   ```python
   # Enable detailed logging
   spark.sparkContext.setLogLevel("INFO")
   
   # Check for spills
   spark.conf.set("spark.sql.adaptive.shuffle.targetPostShuffleInputSize", "67108864")  # 64MB
   ```

4. **Common Issues and Fixes:**
   - **Data Skew:** Use salting or AQE skew join
   - **Too Many Partitions:** Reduce `spark.sql.shuffle.partitions`
   - **Small Files:** Coalesce or repartition
   - **GC Overhead:** Tune G1GC settings
   - **Broadcast Join Issues:** Adjust `spark.sql.autoBroadcastJoinThreshold`

### 8. **Comparing Broadcast vs Sort Merge vs Shuffle Hash Joins**

**Question:** When would you use each join strategy in PySpark?

**Answer:**

| Join Type | When to Use | Memory Impact | Performance |
|-----------|-------------|---------------|-------------|
| **Broadcast** | Small table (< 10MB for 8GB RAM) | High (driver memory) | Fastest (no shuffle) |
| **Sort Merge** | Medium to large tables, sorted/partitioned | Medium (shuffle + sort) | Good for large datasets |
| **Shuffle Hash** | Medium tables, unsorted | High (build hash table) | Fast if fits in memory |

**Decision Tree:**
```python
def choose_join_strategy(df1, df2, join_key):
    # Estimate size
    df2_size_mb = df2.rdd.map(lambda x: len(str(x))).sum() / (1024 * 1024)
    
    if df2_size_mb < 10:  # 10MB threshold for 8GB RAM
        return "BROADCAST"
    elif df2_size_mb < 500:
        # Ensure proper partitioning for sort merge
        df1 = df1.repartition(100, join_key)
        df2 = df2.repartition(100, join_key)
        return "SORT_MERGE"
    else:
        # Large dataset, use shuffle hash with spill
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
        return "SHUFFLE_HASH"
```

### 9. **PySpark on Kubernetes vs YARN vs Standalone**

**Question:** What are the trade-offs between different cluster managers for PySpark?

**Answer:**

| Manager | Pros | Cons | Best For |
|---------|------|------|----------|
| **Standalone** | Simple setup, good for single node | Limited resource management | Development, small deployments |
| **YARN** | Mature, Hadoop integration, fine-grained | Complex configuration, overhead | Hadoop ecosystems, enterprise |
| **K8s** | Containerization, scaling, isolation | Spark-K8s operator needed | Cloud-native, microservices |
| **Mesos** | Fine-grained sharing, Docker support | Declining community support | Mixed workloads |

**For 8GB RAM Development:**
```bash
# Standalone is simplest
./bin/spark-submit \
  --master local[4] \
  --driver-memory 2g \
  --executor-memory 2g \
  your_script.py
```

### 10. **Optimizing PySpark for CSV vs Parquet vs Delta**

**Question:** How do storage formats affect PySpark performance on 8GB RAM?

**Answer:**

**CSV:**
- **Pros:** Human readable, widely supported
- **Cons:** No schema, no compression, slow reads
- **Optimization:** Use schema inference once, then cache

**Parquet:**
- **Pros:** Columnar, compression, predicate pushdown
- **Cons:** Write overhead, not mutable
- **Best for:** Analytical queries, 8GB RAM (reduces memory pressure)

**Delta:**
- **Pros:** ACID transactions, time travel, schema evolution
- **Cons:** Slightly larger footprint
- **Best for:** Production pipelines with updates

**Comparison Code:**
```python
# CSV with optimization
df_csv = spark.read \
    .option("inferSchema", "true") \
    .option("header", "true") \
    .csv("data.csv") \
    .cache()  # Cache after schema inference

# Parquet (better for 8GB RAM)
df_parquet = spark.read.parquet("data.parquet")
# Automatic predicate pushdown, column pruning

# Delta with optimizations
df_delta = spark.read.format("delta").load("data.delta")
# Z-ordering for better performance
df_delta.optimize().executeZOrderBy("date_column")
```

### 11. **Implementing Incremental Processing in PySpark**

**Question:** How would you design an incremental ETL pipeline in PySpark?

**Answer:**

**Watermark-based Incremental Processing:**
```python
from pyspark.sql.functions import max as spark_max

def incremental_load(spark, table_path, checkpoint_path):
    """Load only new data since last run."""
    
    # Read checkpoint
    try:
        last_processed = spark.read.parquet(checkpoint_path) \
            .agg(spark_max("last_processed_timestamp")) \
            .collect()[0][0]
    except:
        last_processed = "1900-01-01"
    
    # Incremental query
    new_data = spark.read.parquet(table_path) \
        .filter(f"timestamp > '{last_processed}'")
    
    if new_data.count() > 0:
        # Process new data
        processed = transform_data(new_data)
        
        # Update checkpoint
        new_checkpoint = processed.agg(spark_max("timestamp")) \
            .withColumnRenamed("max(timestamp)", "last_processed_timestamp")
        new_checkpoint.write.mode("overwrite").parquet(checkpoint_path)
        
        return processed
    else:
        print("No new data to process")
        return spark.createDataFrame([], schema)
```

### 12. **PySpark Unit Testing Best Practices**

**Question:** How do you write effective unit tests for PySpark code?

**Answer:**

**Using pytest and chispa for Spark testing:**
```python
import pytest
from chispa.dataframe_comparer import assert_df_equality
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local[2]") \
        .appName("test") \
        .getOrCreate()

def test_dataframe_transformation(spark):
    # Create test data
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    
    input_data = [(1, "Alice"), (2, "Bob")]
    input_df = spark.createDataFrame(input_data, schema)
    
    # Apply transformation
    result_df = transform_function(input_df)
    
    # Expected output
    expected_data = [(1, "ALICE"), (2, "BOB")]
    expected_df = spark.createDataFrame(expected_data, schema)
    
    # Compare dataframes
    assert_df_equality(result_df, expected_df, ignore_nullable=True)

def test_edge_cases(spark):
    # Test empty dataframe
    empty_df = spark.createDataFrame([], schema)
    result = transform_function(empty_df)
    assert result.count() == 0
    
    # Test null values
    null_data = [(1, None), (2, "Bob")]
    null_df = spark.createDataFrame(null_data, schema)
    result = transform_function(null_df)
    assert result.filter(col("name").isNull()).count() == 1
```

### 13. **Memory Leak Detection in PySpark Applications**

**Question:** How would you detect and fix memory leaks in a long-running PySpark application?

**Answer:**

**Detection Techniques:**
```python
import psutil
import gc

def monitor_memory(spark):
    """Monitor memory usage and detect leaks."""
    process = psutil.Process()
    
    metrics = {
        "driver_rss_mb": process.memory_info().rss / 1024 / 1024,
        "driver_vms_mb": process.memory_info().vms / 1024 / 1024,
        "system_memory_percent": psutil.virtual_memory().percent,
        "spark_storage_memory": spark.sparkContext.getExecutorMemoryStatus()
    }
    
    # Check for memory growth
    if metrics["driver_rss_mb"] > 1500:  # 1.5GB threshold for 8GB
        print("WARNING: High memory usage detected")
        
        # Force garbage collection
        gc.collect()
        
        # Unpersist unused DataFrames
        for (id, rdd) in spark.sparkContext._jsc.getPersistentRDDs().items():
            if rdd.is_cached:
                rdd.unpersist()
    
    return metrics

# Common leak sources and fixes:
# 1. Unclosed SparkSessions -> Use context managers
# 2. Accumulators not cleared -> spark.sparkContext.clearAccumulators()
# 3. Cached DataFrames not unpersisted -> df.unpersist()
# 4. Broadcast variables not destroyed -> bc.destroy()
```

### 14. **Real-time Scenario: 8GB RAM, 100GB Dataset**

**Question:** You need to process a 100GB dataset on an 8GB RAM machine. What's your approach?

**Answer:**

**Chunking Strategy with Disk Spill:**
```python
def process_large_dataset_chunked(spark, input_path, output_path, chunk_size=1000000):
    """Process dataset in chunks to fit 8GB RAM."""
    
    # Read schema without data
    schema = spark.read.parquet(input_path).schema
    
    # Get total rows
    total_rows = spark.read.parquet(input_path).count()
    
    # Process in chunks
    for i in range(0, total_rows, chunk_size):
        print(f"Processing chunk {i//chunk_size + 1}/{(total_rows + chunk_size - 1)//chunk_size}")
        
        # Read chunk
        chunk = spark.read.parquet(input_path) \
            .limit(chunk_size) \
            .offset(i) \
            .persist(StorageLevel.DISK_ONLY)  # Spill to disk if needed
        
        # Process chunk
        processed_chunk = transform_chunk(chunk)
        
        # Write chunk (append mode)
        if i == 0:
            processed_chunk.write.mode("overwrite").parquet(output_path)
        else:
            processed_chunk.write.mode("append").parquet(output_path)
        
        # Cleanup
        chunk.unpersist()
        processed_chunk.unpersist()
        
        # Force garbage collection
        gc.collect()
```

### 15. **Career Advancement: From PySpark Developer to Architect**

**Question:** What skills should a PySpark developer focus on to advance to a data architect role?

**Answer:**

**Technical Skills:**
1. **Distributed Systems:** Understand CAP theorem, consistency models, partitioning strategies
2. **Storage Systems:** Delta Lake, Iceberg, Hudi for data lakehouses
3. **Orchestration:** Airflow, Dagster, Prefect for workflow management
4. **Cloud Platforms:** AWS EMR, Databricks, Azure Synapse optimization
5. **Monitoring:** Prometheus, Grafana, Spark UI deep dive

**Architectural Patterns:**
- Lambda vs Kappa architecture
- Medallion architecture (bronze, silver, gold)
- Data mesh principles
- Cost optimization strategies

**Soft Skills:**
- Cross-team collaboration
- Technical documentation
- Mentoring junior engineers
- Stakeholder communication

## 📚 Preparation Tips for Advanced PySpark Interviews

1. **Understand Internals:** Study Catalyst optimizer, Tungsten execution, and Spark SQL internals
2. **Memory Management:** Be prepared to discuss JVM tuning, GC algorithms, and off-heap memory
3. **Performance Tuning:** Practice with real datasets and measure before/after optimizations
4. **Production Experience:** Discuss actual production issues you've solved (OOM, skew, etc.)
5. **Tool Ecosystem:** Know how PySpark integrates with Airflow, Kafka, Delta Lake, etc.

## 🔗 Related Resources in This Repository

- **02_5_pyspark_basics:** Foundational PySpark concepts
- **05_streaming_analytics:** Structured streaming patterns
- **06_fastapi_integration:** Production API integration
- **GOTCHAS_BEST_PRACTICES.md:** Common pitfalls and solutions
- **practice_exercises.py:** Hands-on coding exercises

---

*Last Updated: April 2026*  
*Target Level: Senior Data Engineer / PySpark Specialist*