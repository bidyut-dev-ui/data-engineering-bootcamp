# PySpark Gotchas & Best Practices for 8GB RAM

## ⚠️ Common Gotchas (and How to Avoid Them)

### 1. **Memory Issues on 8GB RAM**
**Problem**: `java.lang.OutOfMemoryError` or slow performance
**Solution**:
```python
# Configure for 8GB RAM
SparkSession.builder \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "1g") \
    .config("spark.memory.fraction", "0.6") \
    .config("spark.sql.shuffle.partitions", "8")  # Reduce from default 200
```
**Additional tips**:
- Monitor with `htop` in another terminal
- Use Spark UI (`http://localhost:4040`) to check memory usage
- If OOM persists, reduce to `1g` driver memory

### 2. **`.collect()` on Large Datasets**
**Problem**: `.collect()` brings all data to driver, causing OOM
**Solution**:
- Use `.take(100)` or `.limit(1000).collect()` for sampling
- Write to disk instead: `.write.parquet("output.parquet")`
- Use `.toPandas()` cautiously (converts to Pandas, uses more memory)

### 3. **Schema Inference on Large CSV Files**
**Problem**: `inferSchema=True` reads entire file, slow for large files
**Solution**:
```python
# Define schema explicitly
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    # ...
])

df = spark.read.schema(schema).csv("file.csv")
```
- Or sample first: `spark.read.option("samplingRatio", 0.01).csv(...)`

### 4. **Cartesian Product (Cross Join) by Mistake**
**Problem**: Missing join condition creates huge result
**Solution**:
- Always specify join condition explicitly
- Enable check: `spark.sql.crossJoin.enabled = false` (Spark 2.x+)
- Monitor join output size: if `n*m` rows, you have cross join

### 5. **Not Stopping SparkSession**
**Problem**: Memory leak, ports remain open
**Solution**:
```python
try:
    spark = SparkSession.builder.getOrCreate()
    # Your code
finally:
    spark.stop()  # Always stop!
```
- Use context manager pattern if possible
- Check for orphaned processes: `ps aux | grep spark`

### 6. **Skewed Data Causing Slow Joins**
**Problem**: One key has millions of rows, others have few
**Solution**:
1. **Identify**: `df.groupBy("key").count().orderBy(col("count").desc())`
2. **Salting**: Add random suffix to skewed keys
3. **Two-phase aggregation**: Local then global aggregate
4. **Broadcast**: If small dimension table

### 7. **Forgetting Lazy Evaluation**
**Problem**: Code runs slow because transformations chained unnecessarily
**Solution**:
- Use `.cache()` for DataFrames used multiple times
- Break long chains: Write intermediate results
- Check execution plan with `.explain()`

### 8. **Date/Time Parsing Performance**
**Problem**: `to_date()` on string column is slow
**Solution**:
- Parse during read: `.option("timestampFormat", "yyyy-MM-dd")`
- Use `from_unixtime()` if you have Unix timestamps
- Store as proper date type, not string

## ✅ Best Practices for 8GB RAM

### 1. **Memory-Efficient Configuration**
```python
# Optimal settings for 8GB RAM
config = {
    "spark.driver.memory": "2g",
    "spark.executor.memory": "1g", 
    "spark.driver.maxResultSize": "1g",
    "spark.sql.shuffle.partitions": "8",
    "spark.sql.autoBroadcastJoinThreshold": "10485760",  # 10MB
    "spark.memory.fraction": "0.6",
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
}
```

### 2. **Data Reading Optimization**
```python
# Read only needed columns
df = spark.read.parquet("data.parquet").select("col1", "col2", "col3")

# Filter early
df_filtered = df.filter(col("date") > "2024-01-01")

# Use Parquet over CSV (compressed, columnar)
# CSV: 100MB → Parquet: ~25MB (75% compression)
```

### 3. **Join Optimization**
```python
# Broadcast small tables (<10MB)
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# Ensure join keys have same type
df1 = df1.withColumn("key", col("key").cast("int"))
df2 = df2.withColumn("key", col("key").cast("int"))
```

### 4. **Write Optimization**
```python
# Write partitioned data
df.write.partitionBy("year", "month").parquet("output/")

# Control file size
df.coalesce(4).write.parquet("output/")  # 4 files

# Use overwrite mode carefully
df.write.mode("overwrite").parquet("output/")
```

### 5. **Monitoring & Debugging**
```bash
# Monitor system resources
htop  # CPU/Memory
df -h  # Disk space

# Spark UI
http://localhost:4040  # Jobs, stages, storage
http://localhost:4041  # If 4040 busy
```

### 6. **Development Workflow**
```python
# 1. Start small
df_sample = spark.read.parquet("data.parquet").limit(1000)

# 2. Test logic
result_sample = transform(df_sample)

# 3. Scale up
result_full = transform(spark.read.parquet("data.parquet"))

# 4. Optimize based on performance
```

## 🔧 Performance Tuning Checklist

### Before Running Job:
- [ ] Set appropriate memory configuration
- [ ] Check available disk space for spills
- [ ] Review data size vs RAM
- [ ] Plan partition strategy

### During Development:
- [ ] Use `.explain()` to see execution plan
- [ ] Test with sample data first
- [ ] Monitor Spark UI during execution
- [ ] Check for data skew

### After Job Completes:
- [ ] Review execution time in Spark UI
- [ ] Check for spilled data (memory vs disk)
- [ ] Verify output size matches expectations
- [ ] Clean up temporary files

## 🚨 Error Recovery

### 1. **OutOfMemoryError**
**Symptoms**: Job fails with Java heap space error
**Recovery**:
1. Increase `spark.driver.memory` or `spark.executor.memory`
2. Reduce `spark.sql.shuffle.partitions`
3. Add `.coalesce()` before expensive operations
4. Use `MEMORY_AND_DISK` storage level

### 2. **Disk Full Error**
**Symptoms**: `No space left on device`
**Recovery**:
1. Clean up old Spark directories: `rm -rf /tmp/spark-*`
2. Increase `spark.local.dir` to different location
3. Reduce output size: Use compression, select fewer columns

### 3. **Long-Running Job**
**Symptoms**: Job runs for hours without progress
**Recovery**:
1. Check Spark UI for stuck stages
2. Look for data skew in stage details
3. Kill and restart with more partitions
4. Add checkpoint to break lineage

### 4. **Connection Errors**
**Symptoms**: `Connection refused`, `Timeout`
**Recovery**:
1. Check if Spark is running: `ps aux | grep spark`
2. Restart SparkSession
3. Check port conflicts: `netstat -tulpn | grep 4040`
4. Increase timeout: `spark.network.timeout 600s`

## 📊 Memory Management Guide

### For 8GB RAM System:
```
Total RAM: 8GB
- OS & Other: ~3GB
- Spark Driver: 2GB
- Spark Executor: 1GB
- Buffer: ~2GB
```

### Storage Levels (Choose Wisely):
```python
from pyspark.storagelevel import StorageLevel

# MEMORY_ONLY: Fastest, but uses most memory
df.persist(StorageLevel.MEMORY_ONLY)

# MEMORY_AND_DISK: Spills to disk when memory full
df.persist(StorageLevel.MEMORY_AND_DISK)

# DISK_ONLY: Slowest, but saves memory
df.persist(StorageLevel.DISK_ONLY)

# MEMORY_ONLY_SER: Serialized, less memory
df.persist(StorageLevel.MEMORY_ONLY_SER)
```

## 🎯 Pro Tips for Interviews

### When Asked About Experience:
- "I've optimized PySpark for 8GB RAM constraints using partitioning, broadcast joins, and memory tuning"
- "I can process datasets larger than RAM by using Spark's partitioning and spill-to-disk capabilities"
- "I understand the trade-offs and can choose appropriate storage levels and join strategies"

### When Asked About Scaling:
- "The principles I've learned on 8GB RAM apply to clusters: partitioning, data locality, minimizing shuffle"
- "I would use the same optimization techniques but with cluster-specific configurations"

### When Asked About Debugging:
- "I start with Spark UI to identify slow stages, then check for data skew, then examine execution plans"
- "For memory issues, I monitor heap usage and adjust configuration or repartition data"

## 📚 Learning Path from This Module

1. **Start with**: `01_pyspark_setup.py` - Get PySpark running on 8GB RAM
2. **Learn basics**: `02_dataframe_basics.py` - DataFrame operations
3. **Handle large data**: `03_chunking_pyspark.py` - Partitioning strategies
4. **Optimize**: `04_optimization_techniques.py` - Performance tuning
5. **Build complete**: `05_etl_pipeline.py` - End-to-end project
6. **Prepare for interviews**: `INTERVIEW_QUESTIONS.md` - Q&A practice
7. **Avoid pitfalls**: This document - Gotchas and best practices

## 🔗 Integration with Other Projects

This PySpark module connects to:
- **Airflow Orchestration**: Schedule PySpark jobs (Month 3)
- **FastAPI Services**: Serve PySpark-processed data (Month 4)
- **Data Warehouse**: Replace Pandas ETL with PySpark (Month 2, Week 8)
- **Monitoring**: Track PySpark job metrics (Month 7)

---

**Remember**: PySpark on 8GB RAM is about working smarter, not harder. The constraints teach valuable optimization skills that scale to larger environments.