# PySpark Interview Questions & Answers

## 📋 Basic Level

### 1. What is PySpark and how does it differ from Pandas?
**Answer**: PySpark is the Python API for Apache Spark, a distributed computing framework. Key differences:
- **Pandas**: Single-node, in-memory processing (limited by RAM)
- **PySpark**: Distributed, can process data larger than RAM using multiple nodes
- **Pandas**: Rich API but limited scalability
- **PySpark**: Designed for big data, fault-tolerant, supports streaming

**For 8GB RAM**: Mention that PySpark can run in local mode on a single machine, using partitioning to handle data larger than RAM.

### 2. Explain Spark Architecture (Driver, Executor, Cluster Manager)
**Answer**:
- **Driver Program**: Runs `main()` function, creates SparkContext, schedules tasks
- **Executor**: Worker nodes that run tasks and store data
- **Cluster Manager**: Manages resources (YARN, Mesos, Kubernetes, or Standalone)
- **In local mode**: All run on single machine, but same architecture applies

### 3. What is a DataFrame in PySpark vs RDD?
**Answer**:
- **RDD (Resilient Distributed Dataset)**: Low-level API, immutable distributed collection
- **DataFrame**: Higher-level API built on RDDs, with schema and Catalyst optimizer
- **Dataset**: Type-safe extension of DataFrame (Scala/Java only)
- **Prefer DataFrame** for most use cases due to optimization benefits

## 📊 Intermediate Level

### 4. How does Spark handle data larger than RAM?
**Answer**: Through partitioning and spilling to disk:
1. **Partitioning**: Data split into chunks across nodes/partitions
2. **Lazy Evaluation**: Operations build DAG, not executed immediately
3. **Spill to Disk**: When memory full, spills to disk (configurable)
4. **Checkpointing**: Saves intermediate results to break lineage

**For 8GB RAM**: Configure `spark.sql.shuffle.partitions` and `spark.memory.fraction` appropriately.

### 5. Explain transformations vs actions
**Answer**:
- **Transformations**: Lazy operations that create new RDD/DataFrame (map, filter, join)
- **Actions**: Trigger computation and return results (count, collect, save)
- **Example**: `df.filter()` is transformation, `df.count()` is action
- **Key point**: Transformations build execution plan, actions execute it

### 6. What is Catalyst Optimizer?
**Answer**: Spark SQL's query optimization framework:
1. **Logical Plan**: Initial query representation
2. **Logical Optimization**: Apply rule-based optimizations (predicate pushdown, constant folding)
3. **Physical Planning**: Convert to physical execution plan
4. **Code Generation**: Generate Java bytecode for execution
- **Benefits**: Automatic optimization without manual tuning

### 7. How to handle data skew in PySpark?
**Answer**:
1. **Identify**: Check key distribution with `groupBy().count()`
2. **Salting**: Add random prefix to skewed keys
3. **Two-Phase Aggregation**: Local then global aggregation
4. **Broadcast Join**: For small skewed dimension tables
5. **AQE**: Use Adaptive Query Execution (Spark 3.0+)
6. **Increase Partitions**: `repartition()` before operations

## 🚀 Advanced Level

### 8. Optimize PySpark job for 8GB RAM machine
**Answer**:
```python
SparkSession.builder \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.sql.autoBroadcastJoinThreshold", "10m") \
    .config("spark.memory.fraction", "0.6") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```
**Additional tips**:
- Use `.select()` to keep only needed columns
- Filter early with `.filter()`
- Use broadcast joins for small tables
- Write intermediate results to disk

### 9. Explain broadcast join vs sort merge join
**Answer**:
- **Broadcast Join**: Small table sent to all executors, no shuffle
  - Use when one table < `spark.sql.autoBroadcastJoinThreshold` (default 10MB)
  - Syntax: `df1.join(broadcast(df2), "key")`
- **Sort Merge Join**: Both tables sorted and merged, requires shuffle
  - Default for large tables
  - More expensive but scalable
- **Choice**: Broadcast for small dimension tables, sort merge for large fact tables

### 10. How to monitor and debug PySpark jobs?
**Answer**:
1. **Spark UI**: `http://localhost:4040` (jobs, stages, storage, executors)
2. **Logs**: Check driver/executor logs for errors
3. **Metrics**: `spark.sparkContext.uiWebUrl`
4. **Debug tips**:
   - Check partition skew in Spark UI
   - Monitor GC time (high = memory pressure)
   - Check shuffle spill (memory vs disk)
   - Use `.explain()` to see execution plan

### 11. What is Tungsten optimization?
**Answer**: Project Tungsten improves Spark's execution engine:
1. **Whole-Stage Code Generation**: Generates optimized Java bytecode
2. **Memory Management**: Off-heap memory, binary data format
3. **Cache-aware Computation**: Optimizes for CPU caches
4. **Benefits**: Faster execution, less memory overhead

## 🎯 Scenario-Based Questions

### 12. You have 10GB CSV file, 8GB RAM machine. How to process?
**Answer**:
1. **Read with partitioning**: `spark.read.csv(..., inferSchema=True)`
2. **Process in chunks**: Use `repartition()` for better parallelism
3. **Write intermediate results**: Use Parquet format (compressed, columnar)
4. **Monitor memory**: Watch for spill to disk in Spark UI
5. **Optimize**: Filter early, select only needed columns

### 13. Job is slow due to shuffle. How to optimize?
**Answer**:
1. **Check shuffle partitions**: `spark.sql.shuffle.partitions` (default 200)
2. **Reduce data before shuffle**: Filter, select columns
3. **Use broadcast join** if possible
4. **Handle data skew**: Salting, two-phase aggregation
5. **Check partition size**: Aim for 100-200MB per partition

### 14. OutOfMemoryError in driver/executor. How to fix?
**Answer**:
**Driver OOM**:
- Increase `spark.driver.memory`
- Reduce `spark.driver.maxResultSize`
- Avoid `.collect()` on large datasets

**Executor OOM**:
- Increase `spark.executor.memory`
- Increase partitions (smaller tasks)
- Use `MEMORY_AND_DISK` storage level
- Enable spill with `spark.memory.fraction`

### 15. How to implement incremental load in PySpark?
**Answer**:
1. **Track last processed timestamp/ID**
2. **Filter new data**: `df.filter(col("timestamp") > last_processed)`
3. **Merge with existing**: Use `merge` (Delta Lake) or `insert overwrite partition`
4. **Update metadata**: Store last processed value
5. **Idempotent**: Design to handle reruns safely

## 💼 Resume & Experience Questions

### 16. "You mention PySpark on your resume. What's the largest dataset you've processed?"
**Answer Template**:
"On my 8GB RAM laptop, I've processed 500K+ row datasets using PySpark local mode with optimization techniques like partitioning, broadcast joins, and memory tuning. I understand the principles that would scale to larger datasets in a cluster environment."

### 17. "How do you ensure data quality in PySpark pipelines?"
**Answer**:
1. **Schema validation**: Define and enforce schemas
2. **Null checks**: `.filter(col("key").isNotNull())`
3. **Data profiling**: Summary statistics, value distributions
4. **Unit tests**: Test transformations with sample data
5. **Monitoring**: Track record counts, null percentages

### 18. "Explain a complex PySpark project you've worked on"
**Answer Structure**:
1. **Business problem**: What were you solving?
2. **Data volume**: Size, velocity, variety
3. **Architecture**: Source → Transform → Sink
4. **Challenges**: Memory, performance, data quality
5. **Solutions**: Optimization techniques used
6. **Results**: Performance improvement, business impact

## 🔧 Technical Deep Dive

### 19. How does Spark SQL's query planning work?
**Answer**:
1. **Unresolved Logical Plan**: Parse SQL/DataFrame API
2. **Analyzed Logical Plan**: Resolve references, check schema
3. **Optimized Logical Plan**: Catalyst optimizer applies rules
4. **Physical Plan**: Choose join algorithms, partitioning
5. **RDD Generation**: Convert to RDD operations
6. **Execution**: Run on cluster

### 20. What are accumulator and broadcast variables?
**Answer**:
- **Accumulator**: Distributed counter (only add operation)
  - Use for metrics collection (e.g., count errors)
  - Driver can read final value
- **Broadcast Variable**: Read-only variable cached on each executor
  - Use for large lookup data
  - More efficient than sending with each task

## 📝 Coding Questions

### 21. Write PySpark code to find top 10 customers by revenue
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = SparkSession.builder.getOrCreate()

# Read data
df = spark.read.parquet("sales.parquet")

# Calculate top customers
top_customers = df.groupBy("customer_id") \
    .agg(sum("amount").alias("total_spent")) \
    .orderBy(col("total_spent").desc()) \
    .limit(10)

top_customers.show()
```

### 22. Handle missing values in PySpark DataFrame
```python
# Various strategies
df_clean = df \
    .fillna({"age": 0, "salary": df.agg(avg("salary")).first()[0]}) \
    .dropna(subset=["customer_id"])  # Remove rows with null key

# Or using when/otherwise
from pyspark.sql.functions import when
df_with_default = df.withColumn(
    "category",
    when(col("category").isNull(), "Unknown").otherwise(col("category"))
)
```

## 🎖️ Certification-Style Questions

### 23. What happens when you call `.cache()` on a DataFrame?
**Answer**:
- Marks DataFrame for caching
- Actually cached when action is called
- Default storage level: `MEMORY_AND_DISK`
- Can specify level: `.persist(StorageLevel.MEMORY_ONLY)`
- Must call `.unpersist()` to free memory

### 24. Difference between `coalesce()` and `repartition()`
**Answer**:
- **`coalesce()`**: Reduces partitions without shuffle
  - Use to decrease partitions (e.g., before write)
  - Cannot increase partitions
- **`repartition()`**: Can increase or decrease partitions with shuffle
  - Use for better parallelism or to fix skew
  - More expensive due to shuffle

### 25. When would you use Window functions vs groupBy?
**Answer**:
- **`groupBy()`**: Aggregation that reduces rows (one row per group)
- **Window functions**: Compute across rows while keeping all rows
- **Use Window for**: Running totals, rankings, moving averages
- **Use groupBy for**: Summary statistics per category

---

## 📚 Preparation Tips

1. **Practice coding**: Write actual PySpark code for common tasks
2. **Understand optimization**: Know how to explain performance tuning
3. **Know your projects**: Be ready to discuss your experience in detail
4. **Review architecture**: Understand Spark internals at high level
5. **Prepare examples**: Have specific examples of challenges and solutions

## 🔗 Related Resources in This Repository

- `01_pyspark_setup.py` - Configuration for 8GB RAM
- `02_dataframe_basics.py` - Core operations
- `03_chunking_pyspark.py` - Large file processing
- `04_optimization_techniques.py` - Performance tuning
- `05_etl_pipeline.py` - Complete project example
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and solutions