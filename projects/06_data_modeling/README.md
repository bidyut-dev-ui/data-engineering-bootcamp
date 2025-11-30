# Week 7: Data Modeling (Star Schema vs 3NF)

**Goal**: Understand why Data Engineers prefer Dimensional Modeling (Star Schema) for analytics over Normalized (3NF) schemas.

## Concepts Covered
1. **OLTP vs OLAP**: Transactional systems (3NF) vs Analytical systems (Star).
2. **Normalization**: Reducing redundancy (e.g., separating Country/Region).
3. **Denormalization**: Increasing redundancy for read speed (e.g., flattening Customer/Country/Region into `dim_customer`).
4. **Fact vs Dimension**: 
   - **Fact**: Events (Sales, Logs) -> High volume, numeric.
   - **Dimension**: Context (Who, What, Where, When) -> Descriptive.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../06_data_modeling
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Create Schemas
Run the script to create both database structures in a local SQLite file (`modeling_demo.db`).
```bash
python 01_create_schemas.py
```

### 3. Run ETL
Populate the 3NF tables with random data, then run a mini-ETL process to transform and load that data into the Star Schema.
```bash
python 02_etl_pipeline.py
```

### 4. Compare Queries
Run the comparison script to see the difference in SQL complexity.
```bash
python 03_compare_queries.py
```
*Notice how the Star Schema query is much simpler to write and read.*

## Homework / Challenge
Create `04_challenge.py`:
1. Add a new Dimension: `dim_time` (Hour of day).
2. Update the ETL to extract the hour from `orders` and populate `fact_sales`.
3. Query: "What is the peak sales hour?" using the Star Schema.
