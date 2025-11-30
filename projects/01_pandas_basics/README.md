# Week 2: Pandas Basics & Data Cleaning

**Goal**: Learn how to ingest, inspect, clean, and aggregate data using Pandas. This is the bread and butter of Data Engineering.

## Concepts Covered
1. **Loading Data**: Reading CSV, JSON, and Parquet files.
2. **Inspection**: Checking data types, missing values, and statistics.
3. **Cleaning**: Handling missing values (`dropna`, `fillna`), fixing strings, correcting invalid numbers.
4. **Transformation**: Creating new columns based on logic.
5. **Aggregation**: `groupby`, `sum`, `mean`, and time-based grouping.

## Instructions

### 1. Setup
Activate your environment if not already active:
```bash
cd ../01_pandas_basics
source ../00_setup_and_refresher/venv/bin/activate
pip install pandas pyarrow fastparquet
```
*(Note: `pyarrow` or `fastparquet` is needed for Parquet files)*

### 2. Generate Data
We need some messy data to practice on. Run the generator:
```bash
python generate_data.py
```
This creates `sales_data.csv` with intentional errors (missing values, bad casing, negative numbers).

### 3. Run Tutorial 1: Basics & Cleaning
Read through the code in `01_basics_tutorial.py` first, then run it:
```bash
python 01_basics_tutorial.py
```
This script will clean the data and save it as `sales_clean.parquet`.

### 4. Run Tutorial 2: Aggregation
Read through `02_aggregation_tutorial.py`, then run it:
```bash
python 02_aggregation_tutorial.py
```
This uses the cleaned parquet file to generate reports.

## Homework / Challenge
Create a new script called `03_challenge.py` that answers these questions:
1. Which **Region** sold the most **Laptops** (by quantity)?
2. What is the average order value (total_sales) for each month?
3. Find the top 3 days with the highest total sales.
