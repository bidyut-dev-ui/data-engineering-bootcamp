# Warehouse Builder Interview Questions

Comprehensive interview questions covering ETL pipeline design, data warehouse architecture, PostgreSQL optimization, star schema implementation, and production deployment for analytical workloads.

## 📊 Core Concepts

### 1. **What is a data warehouse and how does it differ from a transactional database?**
- **Expected Answer**: A data warehouse is a centralized repository optimized for analytical queries, using denormalized schemas (star/snowflake) for read performance. Transactional databases (OLTP) are optimized for CRUD operations with normalized schemas for data integrity. Key differences: workload (analytical vs transactional), schema design (denormalized vs normalized), data characteristics (historical vs current), and performance goals (query speed vs transaction speed).
- **Follow-up**: When would you use a data warehouse vs a data lake?

### 2. **Explain the ETL (Extract, Transform, Load) process.**
- **Expected Answer**: ETL is the process of moving data from source systems to a data warehouse. Extract: read data from various sources (databases, APIs, files). Transform: clean, validate, aggregate, and structure data for analytical use. Load: insert transformed data into target tables. Modern variations include ELT (Extract, Load, Transform) where transformation happens after loading.
- **Follow-up**: What are the advantages of ELT over ETL?

### 3. **What is a star schema and why is it used in data warehousing?**
- **Expected Answer**: A star schema consists of a central fact table connected to multiple dimension tables. Facts contain numeric measures (sales, quantity), dimensions contain descriptive attributes (product, customer, time). Benefits: simplified queries, improved performance, intuitive design for business users, and optimized for aggregations.
- **Follow-up**: Compare star schema with snowflake schema.

### 4. **Explain the difference between fact tables and dimension tables.**
- **Expected Answer**: Fact tables contain quantitative data about business processes (measures) and foreign keys to dimensions. They're typically large and grow quickly. Dimension tables contain descriptive attributes that provide context for facts. They're smaller, change slowly, and are heavily indexed for join performance.
- **Follow-up**: What are degenerate dimensions?

## 🔧 ETL Pipeline Design

### 5. **How would you design an ETL pipeline for loading CSV files into a data warehouse?**
- **Expected Answer**: 
  1. Extraction: Read CSV files with error handling for malformed data
  2. Validation: Check data types, required fields, business rules
  3. Cleaning: Handle missing values, standardize formats, remove duplicates
  4. Transformation: Join with dimensions, calculate derived measures
  5. Loading: Bulk insert into PostgreSQL with proper indexing
  6. Verification: Validate loaded data, update statistics
- **Follow-up**: How would you handle incremental vs full loads?

### 6. **What strategies would you use for handling large CSV files on 8GB RAM?**
- **Expected Answer**: 
  1. Chunked reading (pandas `chunksize` parameter)
  2. Selective column loading (`usecols` parameter)
  3. Optimal data types (categorical, int8, float32)
  4. Disk spilling for intermediate results
  5. Streaming processing line by line
  6. Monitor memory usage and adjust chunk size dynamically
- **Follow-up**: What chunk size would you start with and why?

### 7. **Explain how you would implement incremental loading in an ETL pipeline.**
- **Expected Answer**: 
  1. Track last successful load timestamp
  2. Extract only records modified since last load
  3. Handle new, updated, and deleted records
  4. Use change data capture (CDC) techniques
  5. Maintain metadata about load operations
  6. Support backfilling historical data
- **Follow-up**: How would you detect deleted records in source systems?

### 8. **What error handling strategies are essential for production ETL pipelines?**
- **Expected Answer**: 
  1. Comprehensive logging at different levels
  2. Graceful degradation (skip bad records, continue processing)
  3. Retry logic for transient failures
  4. Dead letter queues for problematic data
  5. Alerting for critical failures
  6. Idempotent design (safe to rerun)
  7. Rollback capability for partial failures
- **Follow-up**: How would you handle data that fails validation?

## 🏗️ Data Warehouse Architecture

### 9. **Compare Kimball vs Inmon approaches to data warehousing.**
- **Expected Answer**: Kimball (bottom-up): Start with data marts using dimensional modeling, then integrate. Faster time-to-value, business-focused. Inmon (top-down): Build normalized enterprise data warehouse first, then create data marts. Better enterprise consistency, more complex. Hybrid approaches are common.
- **Follow-up**: Which approach would you recommend for a startup and why?

### 10. **What are conformed dimensions and why are they important?**
- **Expected Answer**: Conformed dimensions are dimensions that are consistent across multiple fact tables or data marts. They have the same meaning, values, and attributes wherever used. Critical for integrated reporting and cross-functional analysis. Examples: date dimension, product dimension, customer dimension.
- **Follow-up**: How would you ensure dimensions remain conformed as the warehouse evolves?

### 11. **Explain slowly changing dimensions (SCD) and their types.**
- **Expected Answer**: SCD handles changes to dimension attributes over time. Types: Type 1 (overwrite), Type 2 (add new row), Type 3 (add new column), Type 4 (history table), Type 6 (hybrid). Type 2 is most common for preserving historical accuracy.
- **Follow-up**: When would you use Type 3 instead of Type 2?

### 12. **What is a data vault and when would you use it?**
- **Expected Answer**: Data Vault is a modeling technique for agile data warehousing. Components: Hubs (business keys), Links (relationships), Satellites (descriptive attributes). Advantages: scalability, auditability, flexibility for changing requirements. Used when requirements are volatile or for historical tracking.
- **Follow-up**: Compare Data Vault with dimensional modeling.

## 🐘 PostgreSQL Optimization

### 13. **How would you optimize PostgreSQL for data warehouse workloads?**
- **Expected Answer**: 
  1. Table partitioning by date
  2. Appropriate indexing (B-tree, BRIN, covering indexes)
  3. Query optimization (EXPLAIN ANALYZE, query rewriting)
  4. Configuration tuning (shared_buffers, work_mem, maintenance_work_mem)
  5. Materialized views for common aggregations
  6. Parallel query execution
  7. Columnar storage extensions (cstore_fdw, Citus)
- **Follow-up**: What PostgreSQL configuration parameters are most important for analytical queries?

### 14. **Explain different PostgreSQL index types and when to use each.**
- **Expected Answer**: 
  - B-tree: Default, good for equality and range queries
  - Hash: Faster for equality, no range queries
  - GIN: For array, JSON, full-text search
  - GiST: For geometric data, full-text search
  - BRIN: For large tables with sorted data (e.g., time series)
  - SP-GiST: For clustered data like phone numbers, IP addresses
- **Follow-up**: When would you choose BRIN over B-tree for a fact table?

### 15. **What is table partitioning and how does it improve performance?**
- **Expected Answer**: Partitioning splits a large table into smaller physical tables (partitions) based on a key (e.g., date). Benefits: faster queries (partition pruning), easier maintenance (drop old partitions), parallel operations, better index performance. Implemented via inheritance or declarative partitioning.
- **Follow-up**: How would you handle queries that don't include the partition key?

### 16. **How would you implement bulk loading in PostgreSQL for maximum performance?**
- **Expected Answer**: 
  1. Use COPY command (fastest method)
  2. Disable indexes during load, rebuild after
  3. Use UNLOGGED tables for intermediate staging
  4. Batch inserts with prepared statements
  5. Parallel loading with multiple connections
  6. Adjust autovacuum settings for large loads
- **Follow-up**: What are the trade-offs of using UNLOGGED tables?

## 📈 Performance & Scalability

### 17. **How would you optimize query performance in a star schema?**
- **Expected Answer**: 
  1. Proper indexing (composite indexes on fact table)
  2. Partitioning fact table by date
  3. Materialized views for common aggregations
  4. Query optimization (avoid SELECT *, use WHERE efficiently)
  5. Columnar storage for analytical workloads
  6. Statistics collection and query plan analysis
- **Follow-up**: How would you identify slow queries in production?

### 18. **What strategies would you use for scaling a data warehouse?**
- **Expected Answer**: 
  1. Vertical scaling: More RAM, CPU, faster storage
  2. Horizontal scaling: Sharding, distributed databases
  3. Query optimization: Reduce data scanned, efficient joins
  4. Caching: Materialized views, Redis for frequent queries
  5. Data lifecycle management: Archive old data
  6. Workload management: Separate analytical vs reporting queries
- **Follow-up**: When would you consider moving from PostgreSQL to a distributed database?

### 19. **How would you handle memory constraints (8GB RAM) in a data warehouse?**
- **Expected Answer**: 
  1. Chunked processing for large operations
  2. Efficient data types (categorical, smaller numerics)
  3. Disk-based operations when memory insufficient
  4. Query optimization to reduce intermediate results
  5. Monitoring and alerting for memory usage
  6. Resource limits for concurrent queries
- **Follow-up**: What tools would you use to monitor memory usage?

### 20. **Explain how to implement data compression in a data warehouse.**
- **Expected Answer**: 
  1. Columnar storage (native compression)
  2. PostgreSQL TOAST compression for large values
  3. Application-level compression before storage
  4. Archive compression for historical data
  5. Choose appropriate compression algorithms (gzip, snappy, lz4)
  6. Balance compression ratio vs query performance
- **Follow-up**: How does compression affect query performance?

## 🛠️ Production Deployment

### 21. **What monitoring would you implement for a production data warehouse?**
- **Expected Answer**: 
  1. Pipeline health: Success/failure rates, duration, lag
  2. Data quality: Completeness, accuracy, freshness
  3. Resource usage: Memory, CPU, disk I/O, database connections
  4. Business metrics: Record counts, aggregation accuracy
  5. Alerting: SLA violations, quality breaches, failures
  6. Performance: Query response times, load times
- **Follow-up**: How would you set up alerting for data quality issues?

### 22. **How would you ensure data quality in a data warehouse?**
- **Expected Answer**: 
  1. Validation rules at ingestion
  2. Automated data profiling
  3. Anomaly detection for key metrics
  4. Data lineage tracking
  5. Regular data quality audits
  6. SLA tracking for data delivery
  7. Root cause analysis for quality issues
- **Follow-up**: How would you handle data that fails quality checks?

### 23. **What backup and recovery strategies would you use for a data warehouse?**
- **Expected Answer**: 
  1. Regular full backups (pg_dump, physical backups)
  2. Incremental backups (WAL archiving)
  3. Point-in-time recovery capability
  4. Test recovery procedures regularly
  5. Geographic redundancy for disaster recovery
  6. Backup validation and integrity checks
- **Follow-up**: How would you handle a data corruption incident?

### 24. **How would you implement security in a data warehouse?**
- **Expected Answer**: 
  1. Authentication: Role-based access control
  2. Authorization: Fine-grained permissions
  3. Encryption: Data at rest and in transit
  4. Auditing: Log all access and modifications
  5. Data masking for sensitive information
  6. Compliance with regulations (GDPR, HIPAA)
- **Follow-up**: How would you handle PII (Personally Identifiable Information) in the warehouse?

## 🔍 Advanced Topics

### 25. **Explain how to implement real-time data warehousing.**
- **Expected Answer**: 
  1. Change data capture (CDC) from source systems
  2. Streaming ETL with tools like Kafka, Spark Streaming
  3. Micro-batch processing for near-real-time updates
  4. Lambda architecture for batch and streaming
  5. Use of materialized views for real-time aggregations
  6. Trade-offs: complexity vs freshness requirements
- **Follow-up**: How would you handle late-arriving data in a real-time pipeline?

### 26. **What is data mesh and how does it affect data warehouse design?**
- **Expected Answer**: Data mesh is a decentralized architecture where data is treated as a product, owned by domain teams. Principles: domain-oriented ownership, data as a product, self-serve infrastructure, federated governance. Affects warehouse design: shift from centralized to federated, focus on interoperability, domain-specific data products.
- **Follow-up**: How would you implement a data mesh with existing data warehouse infrastructure?

### 27. **How would you implement data lineage tracking in a data warehouse?**
- **Expected Answer**: 
  1. Capture metadata at each ETL step
  2. Track transformations and dependencies
  3. Use specialized tools (OpenLineage, Marquez)
  4. Integrate with CI/CD for pipeline changes
  5. Provide lineage visualization for users
  6. Support impact analysis and root cause investigation
- **Follow-up**: How would you handle lineage for ad-hoc queries and transformations?

### 28. **Explain how to implement A/B testing data in a data warehouse.**
- **Expected Answer**: 
  1. Design fact table for experiment events
  2. Include dimensions: experiment, variant, user, date
  3. Track metrics: conversions, engagement, revenue
  4. Support statistical analysis (significance testing)
  5. Handle user assignment and experiment configuration
  6. Integrate with experiment management systems
- **Follow-up**: How would you ensure data consistency for experiment analysis?

## 🧪 Practical & Technical Questions

### 29. **Write SQL to create a star schema for sales data in PostgreSQL.**
```sql
-- TODO: Write CREATE TABLE statements for:
-- 1. dim_date (date_key, date, year, month, day, quarter, day_of_week)
-- 2. dim_product (product_key, product_id, name, category, price)
-- 3. dim_customer (customer_key, customer_id, name, city, state)
-- 4. fact_sales (sale_key, date_key, product_key, customer_key, quantity, amount)
-- Include appropriate indexes and constraints
```

### 30. **Write a Python function to load CSV data into PostgreSQL using bulk copy.**
```python
# TODO: Write function to load CSV to PostgreSQL
def bulk_load_csv_to_postgres(csv_path, table_name, connection):
    # Use COPY command for maximum performance
    # Handle errors, logging, and validation
    pass
```

### 31. **Implement SCD Type 2 for customer dimension updates.**
```python
# TODO: Write function to handle SCD Type 2 updates
def update_customer_dimension_scd2(customer_updates, connection):
    # For each update:
    # 1. Close current record (set valid_to = today, is_current = False)
    # 2. Insert new record (valid_from = today, valid_to = NULL, is_current = True)
    # Handle inserts, updates, and deletions
    pass
```

### 32. **Design an ETL pipeline for incremental daily loads.**
```python
# TODO: Design ETL pipeline with incremental loading
class IncrementalETLPipeline:
    def __init__(self, config):
        self.config = config
    
    def extract_incremental(self, last_run_date):
        # Extract new/changed records since last run
        pass
    
    def transform(self, raw_data):
        # Transform data for warehouse
        pass
    
    def load_incremental(self, transformed_data):
        # Load data with SCD handling
        pass
    
    def run(self):
        # Orchestrate incremental ETL
        pass
```

### 33. **Optimize a slow-running star schema query.**
```sql
-- TODO: Given a slow query, identify optimization opportunities
-- 1. Add missing indexes
-- 2. Rewrite query for better performance
-- 3. Consider materialized views
-- 4. Partition large tables
-- 5. Update statistics
```

## 📚 Study Resources

### Recommended Books:
1. **The Data Warehouse Toolkit** - Ralph Kimball (dimensional modeling)
2. **Building the Data Warehouse** - William Inmon (Inmon approach)
3. **PostgreSQL Up and Running** - Regina Obe & Leo Hsu (PostgreSQL optimization)
4. **Designing Data-Intensive Applications** - Martin Kleppmann (scalability)

### Online Resources:
- PostgreSQL documentation (performance tuning section)
- Kimball Group articles (kimballgroup.com)
- ETL best practices on Towards Data Science
- Data warehouse design patterns on Medium

### Practice Platforms:
- Build sample data warehouses with different schemas
- Implement ETL pipelines with real-world data
- Optimize PostgreSQL for analytical workloads
- Benchmark different design approaches

## 🎯 Interview Preparation Tips

### 1. **Understand the fundamentals**:
   - Star vs snowflake vs galaxy schemas
   - Fact and dimension table design
   - SCD types and implementation
   - ETL vs ELT architectures

### 2. **Practice designing schemas**:
   - Draw star schemas for common business domains
   - Convert normalized schemas to dimensional models
   - Design for specific query patterns and performance

### 3. **Be ready for trade-off discussions**:
   - Normalization vs denormalization
   - Storage vs performance
   - Flexibility vs simplicity
   - Development speed vs long-term maintainability

### 4. **Prepare real-world examples**:
   - Projects where you designed data warehouses
   - Performance challenges and solutions
   - Data quality issues addressed
   - Production deployment experiences

### 5. **Ask insightful questions**:
   - What's the primary use case for the data warehouse?
   - What are the performance requirements?
   - How frequently does the schema need to change?
   - What are the biggest pain points currently?

## 🔗 Related Resources in This Repository

- `practice_exercises.py` - Hands-on exercises for building ETL pipelines
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and optimization techniques
- `etl_loader.py` - Reference implementation for ETL
- `schema.sql` - Star schema definition for PostgreSQL
- `docker-compose.yml` - PostgreSQL setup for data warehouse

Remember: Data warehouse interviews test both theoretical knowledge and practical application. Be prepared to explain concepts clearly, draw diagrams, write SQL, discuss trade-offs, and demonstrate understanding of production considerations.