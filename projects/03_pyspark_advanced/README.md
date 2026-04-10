# Week 13-14: Advanced PySpark for 8GB RAM

## Overview
This module dives deep into PySpark's internals and advanced optimization techniques specifically designed for resource-constrained environments (8GB RAM). You'll learn how to make PySpark work efficiently on limited hardware while mastering concepts that are crucial for production deployments and technical interviews.

## Learning Objectives
By the end of this module, you will be able to:
- Understand and leverage Spark's Catalyst Optimizer for query optimization
- Implement effective memory management and garbage collection tuning
- Master different join strategies and handle data skew
- Build ML pipelines with PySpark MLlib on CPU
- Implement streaming analytics with PySpark Structured Streaming
- Integrate PySpark with FastAPI for REST API endpoints
- Optimize PySpark jobs for production deployment

## Prerequisites
- Completion of `projects/02_5_pyspark_basics/`
- Basic understanding of Spark architecture
- Familiarity with DataFrame operations
- 8GB RAM system with Docker and Python 3.10+

## Project Structure

```
projects/03_pyspark_advanced/
├── README.md                          # This file
├── scope.md                          # Detailed 6-month roadmap
├── integration_plan.md               # Curriculum integration plan
├── 01_catalyst_optimizer.py          # Query optimization techniques
├── 02_memory_management.py           # Memory tuning and GC optimization
├── 03_join_strategies.py             # Join algorithms and skew handling
├── 04_ml_pipeline.py                 # MLlib pipelines and evaluation
├── 05_streaming_analytics.py         # Structured streaming with Redpanda
├── 06_fastapi_integration.py         # REST API integration with PySpark
├── requirements.txt                   # Python dependencies
├── generate_advanced_data.py          # Advanced dataset generation
└── data/                             # Sample datasets
    ├── transactions_large.parquet
    ├── customers_large.parquet
    └── streaming_events.json
```

## Tutorial Files

### 1. Catalyst Optimizer Deep Dive
**File:** `01_catalyst_optimizer.py`
- Understand logical vs physical query plans
- Learn how Catalyst optimizes DataFrame operations
- Explore predicate pushdown and column pruning
- Benchmark optimized vs non-optimized queries
- Use `explain()` to analyze query execution

### 2. Memory Management & Tuning
**File:** `02_memory_management.py`
- Configure Spark memory for 8GB constraints
- Tune garbage collection for better performance
- Implement off-heap memory storage
- Optimize serialization (Kryo vs Java)
- Monitor memory usage with Spark UI

### 3. Join Strategies & Data Skew
**File:** `03_join_strategies.py`
- Compare broadcast vs sort merge joins
- Handle data skew with salting techniques
- Implement adaptive query execution
- Use bucketing for join optimization
- Benchmark join performance on skewed data

### 4. ML Pipelines with MLlib
**File:** `04_ml_pipeline.py`
- Build end-to-end ML pipelines
- Implement feature transformers
- Train classification/regression models
- Evaluate models with cross-validation
- Save and load ML models for production

### 5. Streaming Analytics
**File:** `05_streaming_analytics.py`
- Set up structured streaming with Redpanda
- Implement window operations and watermarking
- Handle late arriving data
- Write streaming aggregations to sinks
- Monitor streaming query progress

### 6. FastAPI Integration
**File:** `06_fastapi_integration.py`
- Create REST API endpoints for PySpark jobs
- Implement async job submission
- Expose DataFrame operations as API
- Add job status tracking
- Integrate with existing FastAPI projects

## Getting Started

### 1. Install Dependencies
```bash
cd projects/03_pyspark_advanced
pip install -r requirements.txt
```

### 2. Generate Sample Data
```bash
python generate_advanced_data.py
```

### 3. Run Tutorials
```bash
# Run each tutorial in order
python 01_catalyst_optimizer.py
python 02_memory_management.py
python 03_join_strategies.py
python 04_ml_pipeline.py
python 05_streaming_analytics.py
python 06_fastapi_integration.py
```

## Configuration for 8GB RAM

All tutorials use this optimized Spark configuration:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PySpark-Advanced-8GB") \
    .master("local[2]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
```

## Integration with Existing Curriculum

This module integrates with the broader bootcamp:

- **Month 4 (API Development):** Use `06_fastapi_integration.py` with Week 13-14 FastAPI projects
- **Month 5 (Machine Learning):** Use `04_ml_pipeline.py` alongside sklearn tutorials
- **Month 6 (Capstone):** Replace Pandas ETL with PySpark for large datasets
- **Streaming:** Connect `05_streaming_analytics.py` with Redpanda projects

## Performance Guidelines

### Memory Optimization
- Use `cache()` judiciously - only for frequently reused DataFrames
- Prefer `persist(StorageLevel.MEMORY_AND_DISK)` for large datasets
- Monitor Spark UI at `http://localhost:4040`
- Use `df.rdd.getNumPartitions()` to check partitioning

### Data Size Limits
- Training: 10K-500K rows per tutorial
- Production simulation: 1M rows with chunking
- Streaming: 100K events/hour simulated
- All data fits within 8GB RAM with proper optimization

## Homework Challenges

1. **Optimization Challenge:** Take a slow PySpark query and optimize it using Catalyst techniques
2. **Integration Challenge:** Create a FastAPI endpoint that processes 1M rows with PySpark
3. **ML Challenge:** Build a PySpark ML pipeline that outperforms sklearn on the same dataset
4. **Streaming Challenge:** Implement a real-time anomaly detection system with PySpark Streaming

## Interview Preparation

This module covers advanced PySpark topics commonly asked in interviews:
- Catalyst Optimizer internals
- Memory management and tuning
- Join strategies and data skew
- MLlib vs sklearn comparison
- Structured streaming concepts
- Integration patterns with REST APIs

## Troubleshooting

### Common Issues
1. **Out of Memory:** Reduce dataset size or increase `spark.sql.shuffle.partitions`
2. **Slow Performance:** Check Spark UI for bottlenecks, enable adaptive query execution
3. **Streaming Stuck:** Check watermark settings and trigger intervals
4. **ML Pipeline Errors:** Ensure feature columns are properly typed

### Debugging Tips
- Use `df.explain()` to see query plans
- Check Spark UI for stage details
- Enable logging with `spark.sparkContext.setLogLevel("INFO")`
- Use `df.printSchema()` to verify data types

## Next Steps

After completing this module, you can:
1. Integrate PySpark into your Month 4 API projects
2. Enhance Month 5 ML projects with distributed processing
3. Upgrade the Capstone project with PySpark for large datasets
4. Prepare for PySpark-focused data engineering interviews

## Resources
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Spark Performance Tuning Guide](https://spark.apache.org/docs/latest/tuning.html)
- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)