# Data Engineer Interview Questions & Answers

## Category 1: SQL & Databases (Most Common)

### Q1: Explain the difference between INNER JOIN and LEFT JOIN.
**Answer**: 
- INNER JOIN returns only matching rows from both tables
- LEFT JOIN returns all rows from the left table and matching rows from right 
  (NULL for non-matches)

**Example**: "In a customer-orders scenario, INNER JOIN shows only customers 
with orders, while LEFT JOIN shows all customers, including those without orders."

### Q2: How would you optimize a slow SQL query?
**Answer**:
1. Check EXPLAIN plan to identify bottlenecks
2. Add indexes on frequently filtered/joined columns
3. Avoid SELECT *, specify needed columns
4. Use WHERE instead of HAVING when possible
5. Consider partitioning for large tables
6. Use CTEs for complex queries (readability + optimization)

### Q3: What is a star schema? Why use it?
**Answer**: 
Star schema has a central fact table connected to dimension tables. Benefits:
- Simpler queries (fewer joins)
- Better query performance
- Easier for business users to understand
- Optimized for analytical workloads (OLAP)

### Q4: Difference between DELETE, TRUNCATE, and DROP?
**Answer**:
- DELETE: Removes rows, can use WHERE, can rollback, slower
- TRUNCATE: Removes all rows, faster, can't rollback (usually), resets identity
- DROP: Removes entire table structure

### Q5: What are indexes? When would you not use them?
**Answer**: 
Indexes speed up reads by creating a sorted data structure. Don't use when:
- Table has frequent writes (indexes slow down INSERT/UPDATE)
- Column has low cardinality (e.g., gender: M/F)
- Table is very small

## Category 2: Python & Data Processing

### Q6: How do you handle large files that don't fit in memory?
**Answer**:
- Use chunking: `pd.read_csv(file, chunksize=10000)`
- Process iteratively, aggregate results
- Use Dask or PySpark for distributed processing
- Optimize dtypes (int32 vs int64, category for strings)

### Q7: Explain the difference between list and tuple in Python.
**Answer**:
- List: Mutable, slower, uses more memory, syntax: [1, 2, 3]
- Tuple: Immutable, faster, less memory, syntax: (1, 2, 3)
Use tuples for fixed data (coordinates, RGB values)

### Q8: What is the difference between .loc and .iloc in Pandas?
**Answer**:
- .loc: Label-based indexing (df.loc['row_name', 'column_name'])
- .iloc: Integer position-based (df.iloc[0, 1])

### Q9: How do you handle missing data in Pandas?
**Answer**:
1. Identify: `df.isnull().sum()`
2. Strategies:
   - Drop: `df.dropna()` (if < 5% missing)
   - Fill: `df.fillna(value)` or `df.fillna(method='ffill')`
   - Impute: Use mean/median for numerical, mode for categorical

## Category 3: ETL & Airflow

### Q10: What is idempotency in ETL? Why is it important?
**Answer**: 
Idempotency means running the same operation multiple times produces the same 
result. Important because:
- Pipelines may need to be re-run due to failures
- Prevents data duplication
- Ensures data consistency

**Example**: Use UPSERT instead of INSERT, or check if data exists before loading.

### Q11: How do you handle failures in Airflow DAGs?
**Answer**:
1. Set retries and retry_delay in default_args
2. Use on_failure_callback for alerts
3. Implement data quality checks before loading
4. Use sensors to wait for dependencies
5. Log errors comprehensively

### Q12: Explain XComs in Airflow.
**Answer**: 
XComs (cross-communications) allow tasks to exchange small amounts of data. 
Use `ti.xcom_push(key, value)` to send and `ti.xcom_pull(task_ids, key)` to receive.

**Limitation**: Not for large data (use external storage like S3)

### Q13: What is the difference between ETL and ELT?
**Answer**:
- ETL: Extract, Transform, Load - Transform before loading (traditional)
- ELT: Extract, Load, Transform - Load raw data first, transform in warehouse 
  (modern, cloud-based)

ELT is better for:
- Cloud data warehouses (Snowflake, BigQuery)
- Preserving raw data
- Flexibility in transformations

## Category 4: Data Warehousing

### Q14: What is data partitioning? When would you use it?
**Answer**: 
Dividing large tables into smaller, manageable pieces. Use when:
- Table has time-series data (partition by date)
- Queries filter on specific columns
- Table size > 100GB

Benefits: Faster queries, easier maintenance, parallel processing

### Q15: Explain slowly changing dimensions (SCD).
**Answer**:
- Type 1: Overwrite old data (no history)
- Type 2: Add new row with version/date (full history)
- Type 3: Add new column (limited history)

**Example**: Customer address changes - Type 2 keeps all addresses with 
effective dates.

### Q16: What is data normalization? Denormalization?
**Answer**:
- Normalization: Reducing redundancy by splitting tables (3NF)
- Denormalization: Adding redundancy for query performance

Use normalization for OLTP (transactions), denormalization for OLAP (analytics).

## Category 5: APIs & Microservices

### Q17: What is REST? What are HTTP methods?
**Answer**: 
REST (Representational State Transfer) is an architectural style for APIs.

HTTP Methods:
- GET: Retrieve data
- POST: Create new resource
- PUT: Update entire resource
- PATCH: Update partial resource
- DELETE: Remove resource

### Q18: How do you handle API rate limiting?
**Answer**:
1. Implement exponential backoff
2. Use retry logic with delays
3. Cache responses when possible
4. Batch requests
5. Monitor rate limit headers

### Q19: What is the difference between synchronous and asynchronous APIs?
**Answer**:
- Sync: Client waits for response (blocking)
- Async: Client continues, gets response later (non-blocking)

Use async for:
- Long-running tasks (ML training)
- High-throughput systems
- I/O-bound operations

## Category 6: Machine Learning (Basic)

### Q20: Explain overfitting and how to prevent it.
**Answer**: 
Overfitting: Model learns training data too well, performs poorly on new data.

Prevention:
1. Use train/test split
2. Cross-validation
3. Regularization (L1/L2)
4. Reduce model complexity
5. Get more training data

### Q21: What is the difference between classification and regression?
**Answer**:
- Classification: Predict categories (churn: yes/no)
- Regression: Predict continuous values (house price: $X)

### Q22: How do you evaluate a classification model?
**Answer**:
- Accuracy: Overall correctness
- Precision: Of predicted positives, how many are correct?
- Recall: Of actual positives, how many did we find?
- F1-Score: Harmonic mean of precision and recall
- ROC-AUC: Trade-off between true/false positive rates

## Category 7: System Design

### Q23: Design a data pipeline for processing user events.
**Answer Structure**:
1. **Requirements**: Volume, latency, data retention
2. **Components**:
   - Ingestion: Kafka/API
   - Processing: Airflow/Spark
   - Storage: Data Lake (S3) + Warehouse (Redshift)
   - Serving: API/Dashboard
3. **Considerations**: Scalability, fault tolerance, monitoring

### Q24: How would you design a real-time analytics system?
**Answer**:
1. Stream ingestion: Kafka/Kinesis
2. Stream processing: Flink/Spark Streaming
3. Storage: Time-series DB (InfluxDB) or fast warehouse (ClickHouse)
4. Caching: Redis for hot data
5. Visualization: Grafana/custom dashboard

## Behavioral Questions

### Q25: Describe a challenging data quality issue you faced.
**Framework** (STAR):
- **Situation**: "In a previous project, we had inconsistent date formats..."
- **Task**: "I needed to standardize and validate all incoming data..."
- **Action**: "I implemented validation checks in the ETL pipeline..."
- **Result**: "Reduced data errors by 80%, saving 5 hours/week of manual fixes"

### Q26: How do you prioritize when multiple stakeholders need data?
**Answer**:
1. Understand business impact of each request
2. Assess technical complexity and time required
3. Communicate timelines clearly
4. Deliver quick wins first if possible
5. Set realistic expectations

## Tips for Answering

1. **Use the STAR method** for behavioral questions
2. **Quantify results** whenever possible
3. **Admit if you don't know**, then explain how you'd find out
4. **Ask clarifying questions** for system design
5. **Think out loud** - show your thought process
6. **Relate to your projects** - use examples from your capstone
