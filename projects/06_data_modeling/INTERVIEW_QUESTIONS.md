# Data Modeling Interview Questions

Comprehensive interview questions covering data modeling concepts, OLTP vs OLAP systems, normalization, dimensional modeling, star/snowflake schemas, and data warehouse design.

## 📊 Core Concepts

### 1. **Explain the difference between OLTP and OLAP systems.**
- **Expected Answer**: OLTP (Online Transaction Processing) systems are optimized for transactional operations with many short transactions (inserts, updates, deletes). They use normalized schemas for data integrity. OLAP (Online Analytical Processing) systems are optimized for complex queries and aggregations on large datasets. They use denormalized schemas (star/snowflake) for query performance.
- **Follow-up**: When would you choose one over the other for a new project?

### 2. **What is data normalization and why is it important?**
- **Expected Answer**: Normalization is the process of organizing data to reduce redundancy and improve data integrity. It involves dividing tables and defining relationships. Normal forms (1NF, 2NF, 3NF, BCNF) provide guidelines. Important for OLTP systems to maintain consistency and avoid update anomalies.
- **Follow-up**: Explain the first three normal forms with examples.

### 3. **What is denormalization and when should you use it?**
- **Expected Answer**: Denormalization is the process of combining tables to reduce the number of JOINs needed for queries. It improves read performance at the cost of write performance and data redundancy. Used in OLAP systems, data warehouses, and reporting databases where read performance is critical.
- **Follow-up**: What are the trade-offs of denormalization?

### 4. **Explain the concept of dimensional modeling.**
- **Expected Answer**: Dimensional modeling is a design technique for data warehouses that organizes data into fact and dimension tables. Facts are numeric measurements (sales, quantity), dimensions are descriptive context (time, product, customer). The goal is to simplify queries and improve performance for analytical workloads.
- **Follow-up**: How does dimensional modeling differ from normalized modeling?

## 🔧 Star Schema & Snowflake Schema

### 5. **What is a star schema and what are its components?**
- **Expected Answer**: A star schema consists of a central fact table connected to multiple dimension tables. Components: Fact table (measures/metrics), Dimension tables (descriptive attributes), Foreign keys (connecting facts to dimensions). The schema resembles a star with the fact table at the center.
- **Follow-up**: Draw a simple star schema for an e-commerce system.

### 6. **Compare star schema vs snowflake schema.**
- **Expected Answer**: Star schema has fully denormalized dimensions (all attributes in one table). Snowflake schema normalizes dimensions into multiple tables (hierarchies are separate). Star is simpler for queries but uses more storage. Snowflake saves storage but requires more JOINs.
- **Follow-up**: When would you choose snowflake over star schema?

### 7. **What are fact tables and dimension tables?**
- **Expected Answer**: Fact tables contain quantitative data (measures) about business processes. They have foreign keys to dimensions and numeric measures. Dimension tables contain descriptive attributes that provide context for facts (who, what, where, when, why).
- **Follow-up**: Give examples of fact and dimension tables for a retail business.

### 8. **Explain the different types of fact tables.**
- **Expected Answer**: 
  - Transaction fact tables: One row per transaction (e.g., sales)
  - Periodic snapshot fact tables: One row per period (e.g., daily account balance)
  - Accumulating snapshot fact tables: Tracks process milestones (e.g., order fulfillment)
  - Factless fact tables: Captures events without measures (e.g., attendance)
- **Follow-up**: When would you use a periodic snapshot vs transaction fact table?

### 9. **What are conformed dimensions?**
- **Expected Answer**: Conformed dimensions are dimensions that are consistent across multiple fact tables or data marts. They have the same meaning, values, and attributes wherever used. Essential for integrated data warehouses to enable cross-functional analysis.
- **Follow-up**: Why are conformed dimensions important for enterprise data warehouses?

### 10. **Explain slowly changing dimensions (SCD) and their types.**
- **Expected Answer**: SCD handles changes to dimension attributes over time. Types:
  - Type 1: Overwrite (no history)
  - Type 2: Add new row (full history)
  - Type 3: Add new column (limited history)
  - Type 4: History table (separate history)
  - Type 6: Hybrid (1+2+3)
- **Follow-up**: When would you use Type 2 vs Type 3?

## 🏗️ Data Warehouse Design

### 11. **What is the difference between a data warehouse and a data mart?**
- **Expected Answer**: A data warehouse is an enterprise-wide repository of integrated data from multiple sources. A data mart is a subset of a data warehouse focused on a specific business unit or function. Data marts are smaller, more focused, and often built from the warehouse.
- **Follow-up**: When would you build a data mart instead of a full data warehouse?

### 12. **Explain the Kimball vs Inmon approaches to data warehousing.**
- **Expected Answer**: Kimball (bottom-up): Start with data marts using dimensional modeling, then integrate into a warehouse. Inmon (top-down): Build a normalized enterprise data warehouse first, then create data marts. Kimball is faster to deliver, Inmon provides better enterprise consistency.
- **Follow-up**: Which approach would you recommend for a startup and why?

### 13. **What is a data vault and when would you use it?**
- **Expected Answer**: Data Vault is a modeling technique for agile data warehousing. Components: Hubs (business keys), Links (relationships), Satellites (descriptive attributes). Advantages: Scalability, auditability, flexibility for changing requirements. Used when requirements are volatile or for historical tracking.
- **Follow-up**: Compare Data Vault with dimensional modeling.

### 14. **Explain the concept of data mesh.**
- **Expected Answer**: Data mesh is a decentralized architecture where data is treated as a product, owned by domain teams. Principles: Domain-oriented ownership, data as a product, self-serve infrastructure, federated governance. Addresses scalability issues of centralized data warehouses.
- **Follow-up**: How does data mesh change the role of data modeling?

### 15. **What are surrogate keys and why are they used?**
- **Expected Answer**: Surrogate keys are artificial primary keys (usually integers) generated by the system. Used instead of natural/business keys because: Business keys can change, composite keys are inefficient, performance benefits (smaller indexes), separation of concerns.
- **Follow-up**: When would you use natural keys instead of surrogate keys?

## 🔍 Advanced Concepts

### 16. **What are degenerate dimensions?**
- **Expected Answer**: Degenerate dimensions are dimension attributes stored in the fact table because they don't belong to a separate dimension table. Typically transaction identifiers (order number, invoice number, ticket number). They have no other attributes besides the key.
- **Follow-up**: Give an example of a degenerate dimension.

### 17. **Explain the concept of grain in fact tables.**
- **Expected Answer**: Grain is the level of detail or granularity of a fact table. It defines what one row in the fact table represents (e.g., one sales transaction line item, daily store sales, monthly customer summary). Must be clearly defined before designing the fact table.
- **Follow-up**: How does grain affect query performance and storage?

### 18. **What are additive, semi-additive, and non-additive measures?**
- **Expected Answer**: 
  - Additive: Can be summed across all dimensions (e.g., sales quantity)
  - Semi-additive: Can be summed across some dimensions but not others (e.g., account balance across accounts but not across time)
  - Non-additive: Cannot be summed (e.g., unit price, temperature)
- **Follow-up**: How would you handle non-additive measures in aggregations?

### 19. **Explain the concept of bridge tables.**
- **Expected Answer**: Bridge tables resolve many-to-many relationships between dimensions and facts. They sit between the fact table and dimension table. Common for scenarios like multiple customers per account or multiple diagnoses per patient visit.
- **Follow-up**: When would you need a bridge table in a sales schema?

### 20. **What are junk dimensions?**
- **Expected Answer**: Junk dimensions combine low-cardinality flags, indicators, and attributes into a single dimension table. Reduces the number of foreign keys in the fact table. Created by cross-joining all possible combinations of attributes.
- **Follow-up**: What are the advantages and disadvantages of junk dimensions?

## 🛠️ Implementation & Optimization

### 21. **How would you design a star schema for an e-commerce platform?**
- **Expected Answer**: 
  - Fact tables: fact_sales (transaction), fact_inventory (snapshot)
  - Dimensions: dim_customer, dim_product, dim_date, dim_time, dim_store, dim_payment
  - Measures: quantity, unit_price, discount, tax, shipping_cost
  - Granularity: One row per order line item
- **Follow-up**: What dimensions would be conformed across multiple fact tables?

### 22. **How do you handle hierarchical dimensions (e.g., product category hierarchy)?**
- **Expected Answer**: Options: 
  1. Flatten in star schema (category, subcategory, department columns)
  2. Snowflake schema (separate tables for each level)
  3. Bridge table for ragged/variable-depth hierarchies
  4. Path enumeration (materialized path)
- **Follow-up**: Which approach is best for query performance?

### 23. **What indexing strategies would you use for a star schema?**
- **Expected Answer**: 
  - Fact table: Composite indexes on (date_key, product_key), (customer_key, date_key)
  - Dimension tables: Index on surrogate key, indexes on frequently filtered attributes
  - Covering indexes for common query patterns
  - Bitmap indexes for low-cardinality columns (where supported)
- **Follow-up**: How would index strategy differ for snowflake schema?

### 24. **How would you optimize query performance in a large data warehouse?**
- **Expected Answer**: 
  1. Proper indexing strategy
  2. Partitioning fact tables by date
  3. Materialized views for common aggregations
  4. Query optimization (avoid SELECT *, use WHERE efficiently)
  5. Columnar storage for analytical workloads
  6. Appropriate hardware (SSDs, memory)
- **Follow-up**: What would you do if queries are still slow after indexing?

### 25. **Explain how to implement incremental loading in a data warehouse.**
- **Expected Answer**: 
  1. Identify new/changed records using timestamps, change data capture, or checksums
  2. Extract only delta since last load
  3. Transform and validate delta
  4. Load to staging area
  5. Apply to target tables (MERGE or INSERT/UPDATE)
  6. Update load metadata
- **Follow-up**: How would you handle deleted records in incremental loading?

## 📈 Scenario-Based Questions

### 26. **You're designing a data warehouse for a retail chain. What dimensions and facts would you include?**
- **Expected Answer**: 
  - Dimensions: Store, Product, Date, Time, Customer, Promotion, Employee
  - Facts: Sales (transactions), Inventory (snapshots), Returns, Purchasing, Customer visits
  - Conformed dimensions: Date, Product, Store, Customer
  - Granularity: Sales at transaction line item level, Inventory daily snapshot
- **Follow-up**: How would you handle seasonal products that are only sold part of the year?

### 27. **How would you model a customer dimension that includes both B2C and B2B customers?**
- **Expected Answer**: 
  - Common attributes in base dimension: customer_key, customer_id, name, created_date
  - Role-playing views or separate columns for B2C vs B2B attributes
  - Junk dimension for customer type flags
  - Consider separate dimensions if attributes are very different
  - SCD Type 2 for customer attribute changes
- **Follow-up**: How would you handle a customer that transitions from B2C to B2B?

### 28. **You need to track product price changes over time. How would you model this?**
- **Expected Answer**: 
  - Option 1: SCD Type 2 in dim_product (price as attribute)
  - Option 2: Separate fact_product_price with effective dates
  - Option 3: Bridge table between product and price dimensions
  - Recommendation: SCD Type 2 if price changes infrequently, separate fact if price changes frequently
- **Follow-up**: How would you query the price at the time of a specific sale?

### 29. **How would you design a schema for analyzing website clickstream data?**
- **Expected Answer**: 
  - Fact table: fact_page_views (timestamp, session_id, user_id, page_id, time_on_page)
  - Dimensions: dim_user, dim_page, dim_date, dim_time, dim_session, dim_referrer
  - Degenerate dimension: session_id
  - Measures: page_view_count, time_on_page, bounce_flag
  - Granularity: One row per page view
- **Follow-up**: How would you track user paths through the website?

### 30. **You're building a data warehouse for a healthcare provider. What special considerations apply?**
- **Expected Answer**: 
  - HIPAA compliance and data security
  - Complex many-to-many relationships (patients-doctors-diagnoses)
  - Temporal data (changing diagnoses, treatments)
  - Hierarchical dimensions (ICD codes, medical specialties)
  - Factless fact tables for appointments, diagnoses
  - Bridge tables for patient encounters with multiple diagnoses
- **Follow-up**: How would you handle patient data anonymization?

## 🧪 Practical & Technical Questions

### 31. **Write SQL to create a star schema for sales data.**
```sql
-- TODO: Write CREATE TABLE statements for:
-- 1. dim_date (date_key, date, year, month, day, quarter, day_of_week)
-- 2. dim_product (product_key, product_id, name, category, price)
-- 3. dim_customer (customer_key, customer_id, name, city, state)
-- 4. fact_sales (sale_key, date_key, product_key, customer_key, quantity, amount)
```

### 32. **Write a query to get monthly sales by product category from a star schema.**
```sql
-- TODO: Write query joining fact_sales, dim_product, dim_date
-- Group by year, month, category
-- Order by year, month, sales descending
```

### 33. **Implement SCD Type 2 for customer dimension updates.**
```python
# TODO: Write Python function to handle SCD Type 2 updates
def update_customer_dimension(customer_updates, connection):
    # For each update:
    # 1. Close current record (set valid_to = today, is_current = False)
    # 2. Insert new record (valid_from = today, valid_to = NULL, is_current = True)
    pass
```

### 34. **Design an ETL process to load data from OLTP to star schema.**
```python
# TODO: Design ETL pipeline
# 1. Extract from normalized tables
# 2. Transform (denormalize, calculate measures)
# 3. Load to dimension and fact tables
# 4. Handle incremental updates
```

### 35. **Optimize a slow-running star schema query.**
```sql
-- TODO: Given a slow query, identify optimization opportunities
-- 1. Add missing indexes
-- 2. Rewrite query for better performance
-- 3. Consider materialized views
-- 4. Partition large tables
```

## 📚 Study Resources

### Recommended Books:
1. **The Data Warehouse Toolkit** - Ralph Kimball (dimensional modeling bible)
2. **Building the Data Warehouse** - William Inmon (Inmon approach)
3. **Data Warehouse Design Solutions** - Christopher Adamson
4. **Star Schema: The Complete Reference** - Christopher Adamson

### Online Resources:
- Kimball Group articles (kimballgroup.com)
- Data Warehousing concepts on Wikipedia
- Star vs Snowflake schema comparisons
- Slowly Changing Dimensions tutorials

### Practice Platforms:
- Build sample data warehouses with different schemas
- Practice writing complex analytical queries
- Implement ETL pipelines for sample data
- Benchmark different schema designs

## 🎯 Interview Preparation Tips

### 1. **Understand the fundamentals**:
   - Normalization forms (1NF, 2NF, 3NF, BCNF)
   - Star vs Snowflake vs Galaxy schemas
   - Fact and dimension table design
   - SCD types and implementation

### 2. **Practice drawing schemas**:
   - Draw star schemas for common business domains
   - Convert normalized schemas to dimensional models
   - Design for specific query patterns

### 3. **Be ready for trade-off discussions**:
   - Normalization vs denormalization
   - Storage vs performance
   - Flexibility vs simplicity
   - Development speed vs long-term maintainability

### 4. **Prepare real-world examples**:
   - Projects where you designed data models
   - Performance challenges and solutions
   - Schema evolution experiences
   - Data quality issues addressed

### 5. **Ask insightful questions**:
   - What's the primary use case for the data warehouse?
   - What are the most common query patterns?
   - What are the performance requirements?
   - How frequently does the schema need to change?

## 🔗 Related Resources in This Repository

- `practice_exercises.py` - Hands-on exercises for implementing data models
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and optimization techniques
- `01_create_schemas.py` - Reference implementation for schema creation
- `02_etl_pipeline.py` - ETL process from 3NF to star schema
- `03_compare_queries.py` - Query performance comparison

Remember: Data modeling interviews test both theoretical knowledge and practical application. Be prepared to explain concepts clearly, draw diagrams, write SQL, and discuss trade-offs based on specific business requirements.