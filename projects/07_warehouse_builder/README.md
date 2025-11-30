# Week 8: Mini-Project 2 - Warehouse Builder

**Goal**: Build a complete ETL pipeline that takes raw CSV files, transforms them, and loads them into a Postgres Data Warehouse using a Star Schema.

## Scenario
You have received data dumps from 3 different systems:
1. `products.csv` (Inventory System)
2. `customers.csv` (CRM System)
3. `sales.csv` (POS System)

Your job is to consolidate this into a central Data Warehouse so the BI team can run reports.

## Structure
- `data/`: Contains the generated CSVs.
- `schema.sql`: Defines the Star Schema (`dim_product`, `dim_customer`, `fact_sales`).
- `etl_loader.py`: The Python script that performs the Extract, Transform, and Load.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../07_warehouse_builder
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Start Database
We use port **5434** for the Warehouse.
```bash
docker compose up -d
```

### 3. Generate Source Data
Create the raw CSV files:
```bash
python generate_data.py
```

### 4. Run the ETL
Run the loader script. This will:
1. Connect to Postgres.
2. Create the tables defined in `schema.sql`.
3. Read the CSVs.
4. **Transform**: Look up surrogate keys, calculate total amounts, format dates.
5. **Load**: Insert data into the Fact and Dimension tables.
```bash
python etl_loader.py
```

### 5. Verify
Connect to the DB and check the results:
```bash
docker exec -it warehouse_postgres psql -U user -d warehouse_db -c "SELECT * FROM fact_sales LIMIT 5;"
```

### 6. Cleanup
```bash
docker compose down
```

## Homework / Challenge
Create `02_analytics.py`:
1. Connect to the Warehouse.
2. Write a SQL query to find the **Top 3 Customers by Total Spend**.
3. Write a SQL query to find the **Total Revenue per Region**.
4. Print the results using Pandas.
