# Warehouse Builder: Gotchas & Best Practices

This guide covers common pitfalls and best practices for building ETL pipelines, data warehouses, and working with PostgreSQL for analytical workloads in memory-constrained environments (8GB RAM).

## 🚨 Critical Gotchas

### 1. **Memory Explosion with Large CSV Files**
```python
# WRONG: Loading entire CSV into memory
df = pd.read_csv('large_sales.csv')  # Can crash with 8GB RAM!

# CORRECT: Chunked processing
chunk_size = 100000
chunks = []
for chunk in pd.read_csv('large_sales.csv', chunksize=chunk_size):
    processed_chunk = process_chunk(chunk)
    chunks.append(processed_chunk)
    
    # Monitor memory
    if get_memory_usage_mb() > 6000:
        chunk_size = max(10000, chunk_size // 2)
```

### 2. **Inefficient Database Loading**
```python
# WRONG: Row-by-row insertion
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO fact_sales VALUES (%s, %s, %s, %s)",
        (row['product_key'], row['customer_key'], row['quantity'], row['amount'])
    )  # Extremely slow!

# CORRECT: Bulk copy with COPY command
from io import StringIO
output = StringIO()
df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
cursor.copy_from(output, 'fact_sales', sep='\t')
```

### 3. **Missing Surrogate Key Management**
```sql
-- WRONG: Using natural keys as primary keys
CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY,  -- Business key
    name TEXT,
    price DECIMAL
);

-- CORRECT: Surrogate key + natural key
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,  -- Surrogate key
    product_id INTEGER UNIQUE,       -- Business key
    name TEXT,
    price DECIMAL,
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);
```

### 4. **Poor Error Handling in ETL**
```python
# WRONG: No error handling
def load_data(df, table_name):
    df.to_sql(table_name, engine, if_exists='append')

# CORRECT: Comprehensive error handling
def load_data_safely(df, table_name, batch_size=10000):
    try:
        # Validate data before loading
        validate_data(df, table_name)
        
        # Load in batches with transaction
        with engine.begin() as connection:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch.to_sql(table_name, connection, 
                           if_exists='append', index=False)
                
                # Checkpoint progress
                save_checkpoint(table_name, i + len(batch))
                
    except Exception as e:
        logger.error(f"Failed to load {table_name}: {e}")
        # Rollback transaction, quarantine bad data, alert
        handle_etl_failure(e, df, table_name)
        raise
```

### 5. **Ignoring Data Type Optimization**
```python
# WRONG: Default pandas dtypes (memory intensive)
df = pd.read_csv('sales.csv')  # All columns become object dtype

# CORRECT: Specify optimal dtypes
dtype_spec = {
    'product_id': 'int32',
    'customer_id': 'int32',
    'quantity': 'int16',
    'unit_price': 'float32',
    'sale_date': 'str'  # Parse later
}
df = pd.read_csv('sales.csv', dtype=dtype_spec)
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['region'] = df['region'].astype('category')  # Low cardinality
```

## 🏆 Best Practices

### 1. **Memory-Efficient ETL for 8GB RAM**

#### Chunked Processing Strategy
```python
def process_large_file_memory_efficient(file_path, process_func, chunk_size=50000):
    """Process large files in chunks to stay under memory limits."""
    
    processed_chunks = []
    chunk_counter = 0
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        processed_chunk = process_func(chunk)
        processed_chunks.append(processed_chunk)
        chunk_counter += 1
        
        # Monitor and adjust
        memory_usage = get_memory_usage_mb()
        if memory_usage > 6000:  # 6GB threshold
            # Reduce chunk size
            new_chunk_size = max(10000, chunk_size // 2)
            logger.warning(f"Memory high ({memory_usage}MB), reducing chunk size to {new_chunk_size}")
            chunk_size = new_chunk_size
            
            # Write intermediate results to disk
            if len(processed_chunks) > 10:
                save_to_disk(processed_chunks)
                processed_chunks = []
                gc.collect()
        
        # Log progress
        if chunk_counter % 10 == 0:
            logger.info(f"Processed {chunk_counter * chunk_size:,} rows")
    
    # Combine results
    if processed_chunks:
        return pd.concat(processed_chunks, ignore_index=True)
    return pd.DataFrame()
```

#### Selective Column Loading
```python
# Only load needed columns to save memory
columns_needed = ['product_id', 'customer_id', 'quantity', 'sale_date', 'amount']
df = pd.read_csv('sales.csv', usecols=columns_needed, dtype={
    'product_id': 'int32',
    'customer_id': 'int32',
    'quantity': 'int16',
    'amount': 'float32'
})
```

### 2. **PostgreSQL Optimization for Data Warehousing**

#### Table Partitioning
```sql
-- Partition fact table by date for better performance
CREATE TABLE fact_sales (
    sale_id SERIAL,
    product_key INTEGER,
    customer_key INTEGER,
    date_key INTEGER,
    quantity INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (date_key);

-- Create monthly partitions
CREATE TABLE fact_sales_2024_01 PARTITION OF fact_sales
FOR VALUES FROM (20240101) TO (20240201);

CREATE TABLE fact_sales_2024_02 PARTITION OF fact_sales
FOR VALUES FROM (20240201) TO (20240301);
```

#### Indexing Strategy
```sql
-- Essential indexes for star schema queries
CREATE INDEX idx_fact_sales_date_product ON fact_sales(date_key, product_key);
CREATE INDEX idx_fact_sales_customer_date ON fact_sales(customer_key, date_key);
CREATE INDEX idx_dim_product_category ON dim_product(category) WHERE is_current = TRUE;

-- Covering indexes for common queries
CREATE INDEX idx_fact_sales_date_amount 
ON fact_sales(date_key, amount) 
INCLUDE (product_key, customer_key);
```

#### Vacuum and Analyze
```python
# Regular maintenance for PostgreSQL performance
def perform_database_maintenance(connection):
    """Run maintenance tasks for optimal performance."""
    
    # Update statistics for query planner
    connection.execute("ANALYZE fact_sales")
    connection.execute("ANALYZE dim_product")
    connection.execute("ANALYZE dim_customer")
    
    # Vacuum to reclaim space and update visibility map
    connection.execute("VACUUM ANALYZE fact_sales")
    
    # Reindex if needed (during maintenance window)
    if needs_reindexing(connection, 'fact_sales'):
        connection.execute("REINDEX TABLE fact_sales")
    
    logger.info("Database maintenance completed")
```

### 3. **Robust ETL Pipeline Design**

#### Idempotent ETL Design
```python
def run_idempotent_etl(config, execution_id=None):
    """Design ETL to be safely rerunnable."""
    
    # Generate execution ID if not provided
    if not execution_id:
        execution_id = generate_execution_id()
    
    # Check if already completed
    if is_execution_complete(execution_id):
        logger.info(f"Execution {execution_id} already completed, skipping")
        return {"status": "already_complete"}
    
    try:
        # Start execution tracking
        start_execution(execution_id, config)
        
        # Extract with checkpointing
        raw_data = extract_data(config['sources'])
        save_checkpoint(execution_id, 'extract_complete', raw_data.shape)
        
        # Transform with rollback capability
        transformed_data = transform_data(raw_data)
        save_checkpoint(execution_id, 'transform_complete', transformed_data.keys())
        
        # Load with transaction
        with get_database_connection() as conn:
            load_results = load_data(conn, transformed_data)
            save_checkpoint(execution_id, 'load_complete', load_results)
        
        # Mark execution as complete
        complete_execution(execution_id, load_results)
        
        return {"status": "success", "execution_id": execution_id}
        
    except Exception as e:
        # Log failure and allow retry
        fail_execution(execution_id, str(e))
        logger.error(f"ETL failed: {e}")
        
        # Quarantine problematic data
        quarantine_failed_data(execution_id, locals())
        
        raise
```

#### Incremental Loading Pattern
```python
def incremental_load(source_data, target_table, natural_key, timestamp_column):
    """Load only new or changed records efficiently."""
    
    # Get last load timestamp
    last_load = get_last_load_timestamp(target_table)
    
    # Filter new/changed records
    new_records = source_data[
        source_data[timestamp_column] > last_load
    ].copy()
    
    if len(new_records) == 0:
        logger.info("No new records to load")
        return {"loaded": 0, "skipped": len(source_data)}
    
    # Handle SCD Type 2 for dimensions
    if target_table.startswith('dim_'):
        return handle_scd_type2_load(new_records, target_table, natural_key)
    
    # Simple append for facts
    else:
        loaded = load_new_facts(new_records, target_table)
        update_last_load_timestamp(target_table, new_records[timestamp_column].max())
        
        return {"loaded": loaded, "skipped": len(source_data) - loaded}
```

### 4. **Data Quality Assurance**

#### Comprehensive Validation
```python
class DataQualityValidator:
    """Validate data quality at each stage of ETL."""
    
    def __init__(self, rules):
        self.rules = rules
        self.violations = []
    
    def validate_extraction(self, raw_data):
        """Validate raw extracted data."""
        checks = [
            self._check_completeness(raw_data),
            self._check_file_format(raw_data),
            self._check_encoding(raw_data),
            self._check_row_count(raw_data)
        ]
        return self._aggregate_results(checks)
    
    def validate_transformation(self, transformed_data):
        """Validate transformed data."""
        checks = [
            self._check_referential_integrity(transformed_data),
            self._check_business_rules(transformed_data),
            self._check_data_types(transformed_data),
            self._check_value_ranges(transformed_data)
        ]
        return self._aggregate_results(checks)
    
    def validate_loading(self, load_results):
        """Validate loaded data."""
        checks = [
            self._check_row_counts_match(load_results),
            self._check_constraints(load_results),
            self._check_duplicates(load_results),
            self._check_aggregates(load_results)
        ]
        return self._aggregate_results(checks)
    
    def _check_completeness(self, data):
        """Check for missing values in required columns."""
        required_cols = self.rules.get('required_columns', [])
        missing_counts = data[required_cols].isnull().sum()
        
        violations = missing_counts[missing_counts > 0].to_dict()
        if violations:
            self.violations.append({
                'check': 'completeness',
                'violations': violations
            })
        
        return len(violations) == 0
```

#### Automated Quality Monitoring
```python
def monitor_data_quality_continuously(db_config, quality_rules):
    """Continuous data quality monitoring."""
    
    # Schedule regular quality checks
    scheduler = BackgroundScheduler()
    
    # Daily completeness check
    scheduler.add_job(
        check_completeness,
        'cron', hour=2,
        args=[db_config, quality_rules]
    )
    
    # Weekly accuracy check
    scheduler.add_job(
        check_accuracy,
        'cron', day_of_week='mon', hour=3,
        args=[db_config, quality_rules]
    )
    
    # Real-time anomaly detection
    scheduler.add_job(
        detect_anomalies,
        'interval', minutes=30,
        args=[db_config, quality_rules]
    )
    
    scheduler.start()
    
    # Set up alerting
    alert_config = {
        'email': quality_rules.get('alert_email'),
        'slack_webhook': quality_rules.get('slack_webhook'),
        'pagerduty_key': quality_rules.get('pagerduty_key')
    }
    
    return scheduler, alert_config
```

### 5. **Performance Optimization Techniques**

#### Query Optimization
```sql
-- Use EXPLAIN ANALYZE to understand query performance
EXPLAIN ANALYZE
SELECT 
    d.category,
    SUM(f.amount) as total_sales
FROM fact_sales f
JOIN dim_product d ON f.product_key = d.product_key
WHERE f.date_key BETWEEN 20240101 AND 20240131
GROUP BY d.category
ORDER BY total_sales DESC;

-- Optimize with:
-- 1. Appropriate indexes
-- 2. Partition pruning
-- 3. Materialized views for frequent queries
-- 4. Query rewriting for better plans
```

#### Materialized Views for Common Queries
```sql
-- Create materialized view for daily sales summary
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
    date_key,
    product_key,
    COUNT(*) as transaction_count,
    SUM(quantity) as total_quantity,
    SUM(amount) as total_amount
FROM fact_sales
GROUP BY date_key, product_key;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;

-- Index for fast querying
CREATE INDEX idx_mv_daily_sales_date 
ON mv_daily_sales(date_key, product_key);
```

### 6. **Monitoring and Observability**

#### ETL Pipeline Metrics
```python
def collect_etl_metrics(pipeline_name, start_time, end_time, stats):
    """Collect comprehensive ETL metrics."""
    
    metrics = {
        'pipeline': pipeline_name,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_seconds': (end_time - start_time).total_seconds(),
        'records_processed': stats.get('records_processed', 0),
        'records_loaded': stats.get('records_loaded', 0),
        'records_failed': stats.get('records_failed', 0),
        'memory_peak_mb': stats.get('memory_peak_mb', 0),
        'database_connections': stats.get('database_connections', 0),
        'error_count': stats.get('error_count', 0),
        'success_rate': calculate_success_rate(stats)
    }
    
    # Send to monitoring system
    send_to_prometheus(metrics)
    send_to_datadog(metrics)
    store_in_database(metrics)
    
    # Alert if thresholds exceeded
    check_metric_thresholds(metrics)
    
    return metrics
```

#### Dashboard Creation
```python
def create_etl_dashboard(metrics_db):
    """Create monitoring dashboard for ETL pipelines."""
    
    # Query recent metrics
    query = """
    SELECT 
        pipeline,
        DATE(start_time) as date,
        AVG(duration_seconds) as avg_duration,
        AVG(success_rate) as avg_success_rate,
        SUM(records_processed) as total_records
    FROM etl_metrics
    WHERE start_time > NOW() - INTERVAL '7 days'
    GROUP BY pipeline, DATE(start_time)
    ORDER BY date DESC, pipeline
    """
    
    df = pd.read_sql_query(query, metrics_db)
    
    # Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Duration Trend', 'Success Rate', 'Volume Trend', 'Alerts')
    )
    
    # Add traces
    for pipeline in df['pipeline'].unique():
        pipeline_data = df[df['pipeline'] == pipeline]
        fig.add_trace(
            go.Scatter(x=pipeline_data['date'], y=pipeline_data['avg_duration'],
                      name=pipeline, mode='lines+markers'),
            row=1, col=1
        )
    
    # Update layout
    fig.update_layout(height=800, title_text="ETL Pipeline Dashboard")
    
    return fig
```

## 📊 Performance Benchmarks

### Expected Performance on 8GB RAM:
- **1GB CSV file processing**: 2-5 minutes with chunked processing
- **PostgreSQL bulk loading**: 50,000-100,000 rows/second with COPY
- **Memory usage**: Should stay under 6GB peak
- **Query performance**: Sub-second for simple aggregates, 2-10 seconds for complex joins

### Optimization Impact:
| Technique | Memory Reduction | Speed Improvement |
|-----------|------------------|-------------------|
| Chunked CSV reading | 80% | -10% |
| Optimal dtypes | 60% | +5% |
| Bulk COPY loading | 0% | +500% |
| Partitioning | 0% | +200% for date-range queries |
| Materialized views | 20% (storage) | +1000% for repeated queries |

## 🚀 Deployment Checklist

### Before Production:
- [ ] Memory profiling completed for 8GB constraint
- [ ] Performance benchmarks with production-sized data
- [ ] Error handling and recovery tested
- [ ] Data quality monitoring implemented
- [ ] Alerting configured for failures
- [ ] Backup and restore procedures tested
- [ ] Documentation complete (runbooks, schemas)
- [ ] Rollback plan documented and tested
- [ ] Security review completed
- [ ] Load testing with concurrent users

### Monitoring to Implement:
- **Pipeline Health**: Success/failure rates, duration, lag
- **Data Quality**: Completeness, accuracy, freshness
- **Resource Usage**: Memory, CPU, disk I/O, database connections
- **Business Metrics**: Record counts, aggregation accuracy
- **Alerting**: SLA violations, quality breaches, failures

## 🎯 Key Takeaways

1. **Always process large files in chunks** - Critical for 8GB RAM environments
2. **Use PostgreSQL COPY for bulk loading** - Orders of magnitude faster than INSERT
3. **Implement comprehensive error handling** - ETL pipelines must be robust
4. **Monitor data quality continuously** - Bad data is worse than no data
5. **Design for idempotency** - Pipelines should be safely rerunnable
6. **Optimize for your specific workload** - Test with real data volumes
7. **Implement proper indexing and partitioning** - Essential for query performance
8. **Create observability from day one** - You can't optimize what you can't measure

By following these best practices, you'll build a production-ready data warehouse ETL pipeline that performs well within 8GB RAM constraints and delivers reliable, high-quality data for analytics.