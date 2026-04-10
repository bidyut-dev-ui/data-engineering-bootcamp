# Week 2.5: PySpark Basics for 8GB RAM

**Goal**: Learn Apache Spark (PySpark) on a laptop with 8GB RAM, focusing on practical data engineering tasks.

## 🎯 Learning Objectives

By completing this module, you'll be able to:
1. Set up PySpark in local mode with memory constraints
2. Perform basic DataFrame operations (filtering, aggregation, joins)
3. Process large datasets using partitioning and chunking
4. Optimize PySpark jobs for low-memory environments
5. Integrate PySpark with existing ETL pipelines

## 🖥️ Hardware Constraints & Configuration

Your environment:
- **RAM**: 8GB total
- **CPU**: Intel i5 (no GPU)
- **OS**: WSL2 Ubuntu 22.04
- **Storage**: SSD

PySpark configuration optimized for these constraints:
- Driver memory: 2GB
- Executor memory: 1GB  
- Cores: 2 (local[2])
- Shuffle partitions: 2
- Memory fraction: 0.6

## 📁 Project Structure

```
02_5_pyspark_basics/
├── README.md                          # This file
├── requirements.txt                   # PySpark dependencies
├── 01_pyspark_setup.py               # Minimal configuration for 8GB RAM
├── 02_dataframe_basics.py            # PySpark vs Pandas comparison
├── 03_chunking_pyspark.py            # Processing large files
├── 04_optimization_techniques.py     # Memory & performance optimization
├── 05_etl_pipeline.py                # Complete ETL example
├── generate_sample_data.py           # Create test datasets
├── INTERVIEW_QUESTIONS.md            # PySpark interview prep
├── GOTCHAS_BEST_PRACTICES.md         # Common pitfalls & solutions
└── data/                             # Sample data directory
```

## 🚀 Getting Started

### 1. Activate Virtual Environment
```bash
cd projects/02_5_pyspark_basics
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Sample Data
```bash
python generate_sample_data.py
```
This creates:
- `data/sales_small.csv` (10,000 rows) - for quick testing
- `data/sales_large.csv` (500,000 rows) - for performance testing
- `data/customers.csv` (5,000 rows) - for join operations

### 4. Run Tutorials in Order
```bash
# 1. Setup and configuration
python 01_pyspark_setup.py

# 2. DataFrame basics
python 02_dataframe_basics.py

# 3. Chunking large files
python 03_chunking_pyspark.py

# 4. Optimization techniques
python 04_optimization_techniques.py

# 5. Complete ETL pipeline
python 05_etl_pipeline.py
```

## 📊 What You'll Learn

### Tutorial 1: PySpark Setup for 8GB RAM
- Configuring SparkSession with memory limits
- Understanding Spark UI for monitoring
- Testing basic operations

### Tutorial 2: DataFrame Basics
- Creating DataFrames from CSV/Parquet
- Filtering, selecting, and aggregating
- Comparing PySpark vs Pandas syntax
- Handling missing data

### Tutorial 3: Processing Large Files
- Reading files in chunks/partitions
- Repartitioning for better performance
- Writing optimized output (Parquet format)
- Monitoring memory usage

### Tutorial 4: Optimization Techniques
- Caching strategies for iterative operations
- Broadcast joins for small lookup tables
- Data skew handling
- Partition pruning

### Tutorial 5: ETL Pipeline
- End-to-end data pipeline
- Reading from multiple sources
- Transformations and business logic
- Writing to analytical format

## 🎯 Real-World Application

This module prepares you for:
1. **Data Engineering Interviews**: PySpark is a must-have skill
2. **Big Data Processing**: Handle datasets larger than RAM
3. **ETL Pipeline Development**: Build scalable data pipelines
4. **Performance Tuning**: Optimize for constrained environments

## 📈 Expected Outcomes

After completing this module, you should:
- ✅ Have PySpark running on your 8GB laptop
- ✅ Understand PySpark DataFrame API
- ✅ Process 500K+ row datasets efficiently
- ✅ Optimize memory usage for low-RAM environments
- ✅ Be ready to add "PySpark" to your resume

## 🚨 Important Notes for 8GB RAM

1. **Start Small**: Begin with 10K rows, then scale to 500K
2. **Monitor Memory**: Watch `htop` or Spark UI during execution
3. **Use Parquet**: Always write intermediate results in Parquet format
4. **Clean Up**: Call `spark.stop()` and `del` variables when done
5. **Restart Kernel**: If memory leaks occur, restart Python

## 🔗 Integration with Other Projects

This PySpark module connects to:
- **Month 2, Week 8**: Warehouse Builder (replace Pandas ETL with PySpark)
- **Month 3, Week 12**: Airflow DAGs (orchestrate PySpark jobs)
- **Month 4, Week 16**: Data API Service (serve PySpark-processed data)

## 📚 Further Learning

After mastering these basics:
1. **Spark SQL**: Advanced querying capabilities
2. **Structured Streaming**: Real-time data processing
3. **MLlib**: Machine learning with Spark
4. **Delta Lake**: ACID transactions on data lakes

---

**Next Step**: Install dependencies and run `01_pyspark_setup.py`