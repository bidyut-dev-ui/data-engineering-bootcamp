# Data Modeling: Gotchas & Best Practices

This guide covers common pitfalls and best practices for data modeling, focusing on OLTP vs OLAP systems, normalization vs denormalization, star schema design, and dimensional modeling.

## 🚨 Critical Gotchas

### 1. **Over-Normalization for Analytics**
```sql
-- WRONG: Too many JOINs for analytical queries
SELECT 
    d.department_name,
    SUM(oi.quantity * oi.unit_price) as total_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN departments d ON c.department_id = d.department_id
JOIN customers cu ON o.customer_id = cu.customer_id
JOIN addresses a ON cu.customer_id = a.customer_id AND a.address_type = 'billing'
WHERE o.order_date BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY d.department_name;

-- CORRECT: Star schema with denormalized dimensions
SELECT 
    d.department_name,
    SUM(fs.total_amount) as total_sales
FROM fact_sales fs
JOIN dim_product dp ON fs.product_key = dp.product_key
JOIN dim_department d ON dp.department_key = d.department_key
JOIN dim_date dd ON fs.date_key = dd.date_key
WHERE dd.quarter = 'Q1' AND dd.year = 2024
GROUP BY d.department_name;
```

### 2. **Ignoring Slowly Changing Dimensions (SCD)**
```sql
-- WRONG: Overwriting customer history
UPDATE dim_customer 
SET city = 'New City', email = 'new@email.com'
WHERE customer_id = 123;

-- CORRECT: SCD Type 2 - preserve history
UPDATE dim_customer 
SET valid_to = CURRENT_DATE, is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE;

INSERT INTO dim_customer (customer_id, name, email, city, valid_from, valid_to, is_current)
VALUES (123, 'John Doe', 'new@email.com', 'New City', CURRENT_DATE, NULL, TRUE);
```

### 3. **Fact Table Design Mistakes**
```sql
-- WRONG: Mixing granularities in fact table
CREATE TABLE fact_sales (
    sale_id INTEGER PRIMARY KEY,
    daily_total DECIMAL(10,2),  -- WRONG: Aggregated measure
    monthly_total DECIMAL(10,2), -- WRONG: Another aggregation level
    product_id INTEGER,
    date_id INTEGER
);

-- CORRECT: Single granularity with additive measures
CREATE TABLE fact_sales (
    sale_id INTEGER PRIMARY KEY,
    quantity INTEGER,           -- Additive
    unit_price DECIMAL(10,2),   -- Semi-additive
    discount_amount DECIMAL(10,2), -- Additive
    product_key INTEGER,
    date_key INTEGER,
    customer_key INTEGER
);
```

### 4. **Missing Surrogate Keys**
```sql
-- WRONG: Using business keys as primary keys in dimensions
CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,  -- Business key
    name TEXT,
    email TEXT
);

-- CORRECT: Surrogate key + business key
CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,  -- Surrogate key
    customer_id INTEGER,                             -- Business key
    name TEXT,
    email TEXT,
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN,
    UNIQUE(customer_id, valid_from)  -- Natural key for SCD
);
```

### 5. **Poor Indexing Strategy**
```sql
-- WRONG: No indexes or wrong column order
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
-- Only helps queries filtering by date_key alone

-- CORRECT: Composite indexes for common query patterns
CREATE INDEX idx_fact_sales_date_product ON fact_sales(date_key, product_key);
CREATE INDEX idx_fact_sales_customer_date ON fact_sales(customer_key, date_key);
```

## 🏆 Best Practices

### 1. **Choose the Right Model for the Workload**

#### OLTP Systems (Transactional)
```sql
-- Normalized 3NF for transactional systems
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TIMESTAMP,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

#### OLAP Systems (Analytical)
```sql
-- Denormalized star schema for analytics
CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id INTEGER,
    name TEXT,
    email TEXT,
    city TEXT,
    state TEXT,
    registration_date DATE
);

CREATE TABLE fact_sales (
    sale_key INTEGER PRIMARY KEY,
    customer_key INTEGER,
    product_key INTEGER,
    date_key INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
```

### 2. **Design Effective Dimensions**

#### Conformed Dimensions
```sql
-- Design dimensions to be reusable across multiple fact tables
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE UNIQUE,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Same dim_date can be used for:
-- fact_sales, fact_inventory, fact_returns, etc.
```

#### Hierarchical Dimensions
```sql
-- Support drill-down paths
CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT,
    category_name TEXT,
    department_name TEXT,
    -- Hierarchy: product → category → department
    category_key INTEGER,
    department_key INTEGER
);

-- Alternative: Snowflake for better normalization
CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT,
    category_key INTEGER,
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key)
);

CREATE TABLE dim_category (
    category_key INTEGER PRIMARY KEY,
    category_name TEXT,
    department_key INTEGER,
    FOREIGN KEY (department_key) REFERENCES dim_department(department_key)
);
```

### 3. **Optimize Fact Tables**

#### Grain Definition
```python
# Clearly define fact table granularity
FACT_TABLE_GRAIN = {
    "description": "One row per sales transaction line item",
    "level": "Transaction line item",
    "dimensions": ["customer", "product", "date", "store"],
    "measures": ["quantity", "unit_price", "discount_amount", "tax_amount"],
    "additivity": {
        "quantity": "fully additive",
        "unit_price": "non-additive", 
        "discount_amount": "fully additive",
        "tax_amount": "fully additive"
    }
}
```

#### Measure Types
```sql
-- Fully additive: Can be summed across all dimensions
quantity INTEGER,
discount_amount DECIMAL(10,2),

-- Semi-additive: Can be summed across some dimensions but not others
account_balance DECIMAL(10,2),  -- Can sum across accounts, not across time

-- Non-additive: Cannot be summed
unit_price DECIMAL(10,2),        -- Average should be used instead
temperature DECIMAL(5,2)         -- Neither sum nor average across dimensions
```

### 4. **Implement Effective ETL Patterns**

#### Incremental Loading
```python
def incremental_load(source_conn, target_conn, last_load_date):
    """Load only new or changed records."""
    
    # Get maximum timestamp from target
    cursor = target_conn.execute(
        "SELECT MAX(last_updated) FROM fact_sales"
    )
    max_target_date = cursor.fetchone()[0] or last_load_date
    
    # Extract new/changed records
    query = """
    SELECT * FROM source_orders 
    WHERE last_updated > ? 
    OR (last_updated = ? AND operation = 'INSERT')
    """
    
    new_records = pd.read_sql_query(
        query, source_conn, params=[max_target_date, max_target_date]
    )
    
    # Transform and load
    transformed = transform_records(new_records)
    load_to_target(transformed, target_conn)
    
    return len(new_records)
```

#### Change Data Capture (CDC)
```python
def capture_changes(source_table, target_table, key_columns):
    """Implement CDC using hash comparison."""
    
    # Get source data
    source_df = get_source_data(source_table)
    
    # Calculate hash for each row
    source_df['hash'] = calculate_hash(source_df)
    
    # Get target data with hashes
    target_df = get_target_data(target_table)
    
    # Identify changes
    new_records = source_df[~source_df[key_columns].isin(target_df[key_columns])]
    changed_records = identify_changed_records(source_df, target_df, key_columns)
    deleted_records = identify_deleted_records(source_df, target_df, key_columns)
    
    return {
        'new': new_records,
        'changed': changed_records,
        'deleted': deleted_records
    }
```

### 5. **Query Optimization Techniques**

#### Pre-Aggregations
```sql
-- Create summary tables for frequent queries
CREATE TABLE agg_daily_sales AS
SELECT 
    date_key,
    product_key,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_sales,
    COUNT(*) as transaction_count
FROM fact_sales
GROUP BY date_key, product_key;

-- Index for fast querying
CREATE INDEX idx_agg_daily_sales_date_product 
ON agg_daily_sales(date_key, product_key);
```

#### Partitioning Strategy
```sql
-- Partition fact table by date (conceptual example for SQLite)
CREATE TABLE fact_sales_2024_q1 (
    CHECK (date_key BETWEEN 20240101 AND 20240331)
) INHERITS (fact_sales);

CREATE TABLE fact_sales_2024_q2 (
    CHECK (date_key BETWEEN 20240401 AND 20240630)
) INHERITS (fact_sales);
```

### 6. **Data Quality & Governance**

#### Dimension Validation
```python
def validate_dimension(dimension_df, rules):
    """Validate dimension data quality."""
    
    violations = []
    
    # Check for duplicates on natural key
    duplicates = dimension_df.duplicated(
        subset=['customer_id', 'valid_from'], 
        keep=False
    )
    if duplicates.any():
        violations.append({
            'rule': 'Unique natural key',
            'count': duplicates.sum(),
            'examples': dimension_df[duplicates].head().to_dict('records')
        })
    
    # Check for NULLs in required columns
    required_cols = ['customer_id', 'name', 'valid_from']
    for col in required_cols:
        null_count = dimension_df[col].isnull().sum()
        if null_count > 0:
            violations.append({
                'rule': f'NonNull {col}',
                'count': null_count
            })
    
    # Check date validity
    date_violations = dimension_df[
        (dimension_df['valid_from'] > dimension_df['valid_to']) &
        dimension_df['valid_to'].notnull()
    ]
    if len(date_violations) > 0:
        violations.append({
            'rule': 'Valid date ranges',
            'count': len(date_violations)
        })
    
    return violations
```

#### Referential Integrity
```python
def check_referential_integrity(fact_df, dimension_dict):
    """Ensure all foreign keys have corresponding dimension entries."""
    
    issues = []
    
    for dim_name, dim_df in dimension_dict.items():
        fk_column = f"{dim_name}_key"
        
        if fk_column in fact_df.columns:
            # Find foreign keys not in dimension
            invalid_fks = fact_df[~fact_df[fk_column].isin(dim_df['key_column'])]
            
            if len(invalid_fks) > 0:
                issues.append({
                    'dimension': dim_name,
                    'invalid_count': len(invalid_fks),
                    'invalid_keys': invalid_fks[fk_column].unique().tolist()[:10]
                })
    
    return issues
```

## 🔧 Performance Optimization for 8GB RAM

### 1. **Memory-Efficient Schema Design**
```python
# Use appropriate data types to reduce memory
OPTIMAL_DTYPES = {
    'dim_customer': {
        'customer_key': 'int32',
        'customer_id': 'int32',
        'name': 'category',  # Low cardinality
        'email': 'string',
        'city': 'category',  # Medium cardinality
        'registration_date': 'datetime64[ns]'
    },
    'fact_sales': {
        'sale_key': 'int64',
        'customer_key': 'int32',
        'product_key': 'int32',
        'date_key': 'int32',  # YYYYMMDD format
        'quantity': 'int16',  # Small range
        'unit_price': 'float32',
        'total_amount': 'float32'
    }
}
```

### 2. **Chunked Processing for Large Dimensions**
```python
def process_large_dimension_in_chunks(source_data, chunk_size=100000):
    """Process dimension data in chunks to stay under memory limits."""
    
    chunks = []
    for i in range(0, len(source_data), chunk_size):
        chunk = source_data[i:i + chunk_size]
        
        # Process chunk
        processed_chunk = process_dimension_chunk(chunk)
        
        # Write to database
        write_chunk_to_db(processed_chunk)
        
        # Clear memory
        del chunk
        del processed_chunk
        gc.collect()
        
        # Check memory usage
        if get_memory_usage_mb() > 6000:  # 6GB threshold
            chunk_size = max(10000, chunk_size // 2)
```

### 3. **Indexing Strategy for Analytical Queries**
```sql
-- Essential indexes for star schema queries
CREATE INDEX idx_fact_sales_date_product 
ON fact_sales(date_key, product_key) 
INCLUDE (quantity, total_amount);

CREATE INDEX idx_fact_sales_customer_date 
ON fact_sales(customer_key, date_key);

CREATE INDEX idx_dim_product_category 
ON dim_product(category_key) 
WHERE is_current = TRUE;

-- Covering indexes for common aggregates
CREATE INDEX idx_fact_sales_date_amount 
ON fact_sales(date_key, total_amount);
```

## 📊 Schema Design Decision Framework

### When to Use Each Model:

| Scenario | Recommended Model | Reason |
|----------|------------------|--------|
| Transaction processing (OLTP) | 3NF | Minimize redundancy, ensure ACID compliance |
| Business intelligence (OLAP) | Star Schema | Query performance, simplicity |
| Large dimensions with hierarchies | Snowflake | Balance storage vs performance |
| Agile development, historical tracking | Data Vault | Flexibility, auditability |
| Real-time analytics | Wide-table denormalization | Lowest latency |

### Dimension Design Checklist:
- [ ] Surrogate key present
- [ ] Natural key identified
- [ ] SCD strategy defined
- [ ] Hierarchies documented
- [ ] Conformed across facts
- [ ] Appropriate data types
- [ ] Indexes on join columns
- [ ] Descriptive column names

### Fact Table Design Checklist:
- [ ] Grain clearly defined
- [ ] All measures additive or semi-additive
- [ ] Foreign keys to all dimensions
- [ ] Degenerate dimensions identified
- [ ] Transaction vs snapshot fact decided
- [ ] Partitioning strategy defined

## 🚀 Production Deployment Checklist

### Before Go-Live:
- [ ] Data quality tests implemented
- [ ] ETL idempotency verified
- [ ] Performance benchmarks completed
- [ ] Backup/restore procedures tested
- [ ] Monitoring and alerting configured
- [ ] Documentation complete
- [ ] Rollback plan documented
- [ ] User training conducted

### Monitoring Metrics:
- **Data Quality**: Referential integrity, completeness, accuracy
- **Performance**: Query response times, load times
- **Storage**: Table sizes, index sizes, growth rates
- **Usage**: Most queried tables, common query patterns
- **Errors**: ETL failures, constraint violations

## 🎯 Key Takeaways

1. **Choose schema based on workload** - OLTP needs normalization, OLAP needs denormalization
2. **Always use surrogate keys** - Business keys change, surrogate keys are stable
3. **Design for query patterns** - Optimize for how data will be accessed
4. **Implement SCD from day one** - Historical tracking is hard to add later
5. **Document everything** - Data dictionaries, ERDs, and lineage are crucial
6. **Test with real data volumes** - Don't assume performance at scale
7. **Plan for evolution** - Schemas will change, design for flexibility
8. **Monitor and optimize** - Continuously improve based on usage patterns

By following these best practices, you'll create data models that are performant, maintainable, and scalable for both transactional and analytical workloads.