# Week 14.5: Hadoop Fundamentals for 8GB RAM

**Goal**: Learn Apache Hadoop ecosystem on a laptop with 8GB RAM, focusing on practical big data processing tasks.

## 🎯 Learning Objectives

By completing this module, you'll be able to:
1. Set up a single-node Hadoop cluster in Docker with memory constraints
2. Understand HDFS architecture and perform basic file operations
3. Write and run MapReduce jobs in Python using MRJob
4. Process data with Apache Hive for SQL-like queries
5. Optimize Hadoop jobs for low-memory environments
6. Integrate Hadoop with existing PySpark workflows

## 🖥️ Hardware Constraints & Configuration

Your environment:
- **RAM**: 8GB total
- **CPU**: Intel i5 (no GPU)
- **OS**: WSL2 Ubuntu 22.04
- **Storage**: SSD

Hadoop configuration optimized for these constraints:
- HDFS block size: 64MB (reduced from 128MB)
- YARN container memory: 512MB
- MapReduce heap size: 256MB
- Number of reducers: 1
- Replication factor: 1 (single node)

## 📁 Project Structure

```
14_5_hadoop_basics/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── 01_hadoop_docker_setup.py         # Tutorial 1: Hadoop in Docker
├── 02_hdfs_basics.py                 # Tutorial 2: HDFS operations
├── 03_mapreduce_wordcount.py         # Tutorial 3: MapReduce with MRJob
├── 04_hive_basics.py                 # Tutorial 4: Hive integration
├── 05_hadoop_spark_integration.py    # Tutorial 5: Spark on Hadoop
├── generate_sample_data.py           # Generate test data
├── docker-compose.yml                # Hadoop single-node cluster
├── GOTCHAS_BEST_PRACTICES.md         # Common pitfalls & solutions
└── INTERVIEW_QUESTIONS.md            # Hadoop interview questions
```

## 🚀 Getting Started

### 1. Start Hadoop Cluster
```bash
# Start single-node Hadoop cluster in Docker
docker-compose up -d

# Check if services are running
docker-compose ps

# Access Hadoop Web UI (if enabled):
# - Namenode: http://localhost:9870
# - ResourceManager: http://localhost:8088
```

### 2. Install Dependencies
```bash
# Create virtual environment (if not already active)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Generate Sample Data
```bash
# Generate sample log files for processing
python generate_sample_data.py
```

## 📚 Tutorials

### Tutorial 1: Hadoop Docker Setup for 8GB RAM
Learn to run Hadoop in Docker with memory limits suitable for 8GB systems.
- Docker Compose configuration with memory constraints
- HDFS initialization and health checks
- YARN resource manager configuration

### Tutorial 2: HDFS Basics
Master HDFS operations for constrained environments.
- Uploading/downloading files to HDFS
- Directory operations and permissions
- Checking disk usage and replication

### Tutorial 3: MapReduce with Python (MRJob)
Write and run MapReduce jobs using Python.
- WordCount example with MRJob
- Custom mapper and reducer functions
- Running jobs locally and on Hadoop cluster

### Tutorial 4: Hive for Data Warehousing
Use Hive for SQL-like queries on HDFS data.
- Creating external and managed tables
- Basic HiveQL queries
- Partitioning and bucketing strategies

### Tutorial 5: Spark on Hadoop Integration
Integrate Spark with Hadoop ecosystem.
- Reading data from HDFS with Spark
- Writing results back to HDFS
- YARN resource management for Spark

## 🎯 Real-World Application

This module prepares you for:
- **Legacy Hadoop systems**: Many enterprises still use Hadoop for batch processing
- **Data Lake foundations**: HDFS is the backbone of many data lakes
- **Big Data interviews**: Hadoop knowledge is frequently tested
- **Hybrid architectures**: Understanding where Hadoop fits vs. Spark

## 📈 Expected Outcomes

After completing this module, you should be able to:
- ✅ Run a functional Hadoop cluster on your 8GB laptop
- ✅ Process 100MB-1GB datasets with MapReduce
- ✅ Query data using Hive SQL
- ✅ Explain Hadoop architecture in interviews
- ✅ Make informed decisions about Hadoop vs. Spark for different use cases

## 🚨 Important Notes for 8GB RAM

1. **Memory Management**: Hadoop services are memory-hungry. We configure minimal memory settings.
2. **Dataset Size**: Use small datasets (100MB range) that demonstrate concepts without exhausting memory.
3. **One Service at a Time**: Consider stopping other Docker containers (PostgreSQL, Airflow) when running Hadoop.
4. **Swap Space**: Ensure you have adequate swap space configured in WSL2.

## 🔗 Integration with Other Projects

- **PySpark**: Use Spark to read data from HDFS (Tutorial 5)
- **Airflow**: Schedule Hadoop jobs as Airflow tasks
- **FastAPI**: Build APIs that trigger Hadoop processing
- **Data Warehouse**: Load Hive query results into PostgreSQL

## 📚 Further Learning

1. **Official Documentation**: [Apache Hadoop](https://hadoop.apache.org/docs/)
2. **MRJob Documentation**: [Yelp MRJob](https://mrjob.readthedocs.io/)
3. **Hive Documentation**: [Apache Hive](https://hive.apache.org/)
4. **Docker Hadoop**: [Big Data Europe](https://github.com/big-data-europe/docker-hadoop)

---

**Next**: Complete each tutorial in order, then move to FastAPI fundamentals (Week 15).