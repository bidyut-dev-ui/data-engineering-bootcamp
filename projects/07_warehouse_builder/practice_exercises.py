#!/usr/bin/env python3
"""
Practice Exercises for Warehouse Builder Project

This module contains exercises for building a complete ETL pipeline:
- Extracting data from CSV files
- Transforming data for dimensional modeling
- Loading into PostgreSQL data warehouse
- Building star schema with fact and dimension tables

IMPORTANT: Do NOT provide solutions in this file. The exercises should contain
TODO placeholders where learners will implement their own solutions.
"""

import pandas as pd
import psycopg2
from typing import Dict, Any, List, Tuple
import csv
from datetime import datetime
import os
from pathlib import Path


def exercise_1_extract_csv_data() -> Dict[str, Any]:
    """
    Exercise 1: Extract CSV Data
    
    Read and validate CSV files from multiple sources with different formats.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Extract data from three CSV files with different formats and schemas.
        
        Files:
        1. products.csv: Product inventory data (product_id, name, category, price, stock)
        2. customers.csv: Customer relationship data (customer_id, name, email, region, signup_date)
        3. sales.csv: Point-of-sale transaction data (sale_id, customer_id, product_id, quantity, sale_date, unit_price)
        
        Requirements:
        1. Read each CSV file using appropriate method (pandas, csv module, or Dask for large files)
        2. Handle different delimiters, encodings, and missing headers
        3. Validate data types and required columns
        4. Log extraction statistics (row count, missing values, data types)
        5. Return DataFrames or dictionaries for further processing
        
        The goal is to build robust extraction that handles real-world data inconsistencies.
        """,
        "hint": "Use pandas.read_csv() with dtype parameter for type specification. Check for required columns before processing.",
        "function_name": "extract_csv_data",
        "parameters": ["data_dir: str = './data'"],
        "returns": "Dict[str, pd.DataFrame] (dictionary of DataFrames)"
    }


def exercise_2_data_validation_and_cleaning() -> Dict[str, Any]:
    """
    Exercise 2: Data Validation and Cleaning
    
    Implement comprehensive data validation and cleaning rules.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Validate and clean extracted data according to business rules.
        
        Validation Rules:
        1. Products: price > 0, stock >= 0, category in allowed list
        2. Customers: valid email format, region in valid regions, signup_date not in future
        3. Sales: quantity > 0, unit_price > 0, sale_date within valid range
        
        Cleaning Operations:
        1. Handle missing values (impute, drop, or flag)
        2. Standardize formats (dates, strings, numbers)
        3. Remove duplicates
        4. Fix data type issues
        5. Handle outliers (e.g., extremely high prices)
        
        Requirements:
        1. Create validation report with counts of issues by type
        2. Implement configurable cleaning rules
        3. Support both automatic and manual cleaning decisions
        4. Preserve original data for audit trail
        
        The goal is to ensure data quality before loading into warehouse.
        """,
        "hint": "Create a DataValidator class with rule-based validation. Use pandas operations for efficient cleaning.",
        "function_name": "validate_and_clean_data",
        "parameters": ["data_dict: Dict[str, pd.DataFrame]", "validation_rules: Dict[str, Any]"],
        "returns": "Tuple[Dict[str, pd.DataFrame], Dict[str, Any]] (cleaned_data, validation_report)"
    }


def exercise_3_dimension_table_processing() -> Dict[str, Any]:
    """
    Exercise 3: Dimension Table Processing
    
    Process dimension tables with surrogate keys and SCD Type 2 support.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Process dimension tables for star schema with proper surrogate keys and SCD handling.
        
        Dimension Tables to Create:
        1. dim_product: product_key (surrogate), product_id (natural), name, category, price, valid_from, valid_to, is_current
        2. dim_customer: customer_key (surrogate), customer_id (natural), name, email, region, signup_date, valid_from, valid_to, is_current
        3. dim_date: date_key (surrogate), date, year, month, day, quarter, day_of_week, is_weekend, is_holiday
        
        Requirements:
        1. Generate surrogate keys (sequential integers)
        2. Implement SCD Type 2 for product and customer dimensions
        3. Create date dimension for entire date range in sales data
        4. Handle dimension updates (new, changed, deleted records)
        5. Maintain dimension history for auditing
        
        Additional Challenge:
        - Implement SCD Type 1 for some attributes (overwrite)
        - Add junk dimension for flags and indicators
        
        The goal is to build production-ready dimension tables.
        """,
        "hint": "Use pandas to generate surrogate keys. For SCD Type 2, compare current vs new records and insert new versions for changes.",
        "function_name": "process_dimensions",
        "parameters": ["cleaned_data: Dict[str, pd.DataFrame]", "existing_dimensions: Dict[str, pd.DataFrame] = None"],
        "returns": "Dict[str, pd.DataFrame] (processed dimension tables)"
    }


def exercise_4_fact_table_processing() -> Dict[str, Any]:
    """
    Exercise 4: Fact Table Processing
    
    Process fact table with proper foreign keys and additive measures.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Process fact table by joining dimension keys and calculating measures.
        
        Fact Table to Create:
        fact_sales: sale_key, product_key, customer_key, date_key, quantity, unit_price, total_amount, discount_amount
        
        Processing Steps:
        1. Join sales data with dimension tables to get surrogate keys
        2. Calculate derived measures (total_amount = quantity * unit_price - discount)
        3. Handle missing dimension keys (orphaned facts)
        4. Validate referential integrity
        5. Add degenerate dimensions (sale_id as transaction identifier)
        
        Requirements:
        1. Ensure all facts have valid dimension keys
        2. Handle type 2 dimensions correctly (use appropriate valid_from/valid_to)
        3. Calculate and validate business metrics
        4. Support incremental fact loading
        5. Generate fact loading statistics
        
        The goal is to build accurate and query-optimized fact tables.
        """,
        "hint": "Use pandas merge() to join facts with dimensions. For SCD Type 2, join on natural key and date between valid_from and valid_to.",
        "function_name": "process_facts",
        "parameters": ["sales_data: pd.DataFrame", "dimensions: Dict[str, pd.DataFrame]"],
        "returns": "pd.DataFrame (processed fact table)"
    }


def exercise_5_postgres_database_operations() -> Dict[str, Any]:
    """
    Exercise 5: PostgreSQL Database Operations
    
    Implement database operations for creating schema and loading data.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement PostgreSQL database operations for the data warehouse.
        
        Operations Required:
        1. Create database connection with connection pooling
        2. Execute DDL statements from schema.sql
        3. Load dimension tables with efficient bulk insert
        4. Load fact tables with batch processing
        5. Create indexes and constraints
        6. Update statistics
        
        Requirements:
        1. Use connection pooling for performance
        2. Implement retry logic for transient failures
        3. Use COPY command for bulk loading (fastest method)
        4. Handle large datasets with batch processing
        5. Maintain transaction integrity
        6. Log all database operations
        
        Additional Challenge:
        - Implement parallel loading for independent tables
        - Add progress tracking for long-running loads
        
        The goal is to build efficient and reliable database operations.
        """,
        "hint": "Use psycopg2 for PostgreSQL connection. For bulk loading, use copy_from() or COPY command with StringIO.",
        "function_name": "load_to_postgres",
        "parameters": ["data_dict: Dict[str, pd.DataFrame]", "db_config: Dict[str, str]", "schema_file: str = 'schema.sql'"],
        "returns": "Dict[str, int] (load statistics)"
    }


def exercise_6_etl_orchestration() -> Dict[str, Any]:
    """
    Exercise 6: ETL Orchestration
    
    Build a complete ETL pipeline with error handling and monitoring.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Orchestrate the complete ETL pipeline from extraction to loading.
        
        Pipeline Steps:
        1. Extract: Read CSV files
        2. Validate: Check data quality
        3. Clean: Fix data issues
        4. Transform: Process dimensions and facts
        5. Load: Insert into PostgreSQL
        6. Verify: Validate loaded data
        
        Requirements:
        1. Implement comprehensive error handling and logging
        2. Support incremental and full refresh modes
        3. Add monitoring and alerting
        4. Generate ETL execution report
        5. Implement idempotency (can be rerun safely)
        6. Support configuration-driven execution
        
        Additional Features:
        - Dependency management between tasks
        - Parallel execution where possible
        - Resource usage monitoring
        - Rollback on failure
        
        The goal is to build a production-ready ETL orchestration framework.
        """,
        "hint": "Use a pipeline pattern with discrete steps. Implement checkpointing for resumable execution.",
        "function_name": "run_etl_pipeline",
        "parameters": ["config: Dict[str, Any]", "incremental: bool = True"],
        "returns": "Dict[str, Any] (pipeline execution report)"
    }


def exercise_7_performance_optimization() -> Dict[str, Any]:
    """
    Exercise 7: Performance Optimization
    
    Optimize ETL pipeline for speed and memory efficiency.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Optimize the ETL pipeline for performance on 8GB RAM machine.
        
        Optimization Areas:
        1. Memory usage: Process data in chunks, use efficient dtypes
        2. CPU usage: Parallel processing, vectorized operations
        3. I/O: Batch database operations, compression
        4. Algorithmic: Efficient joins, indexing strategies
        
        Requirements:
        1. Implement chunked processing for large files
        2. Use appropriate pandas dtypes (category, int8, float32)
        3. Parallelize independent operations
        4. Optimize database operations (bulk insert, prepared statements)
        5. Profile and identify bottlenecks
        6. Compare performance before/after optimization
        
        Metrics to Track:
        - Memory usage peak
        - Total execution time
        - CPU utilization
        - I/O operations
        
        The goal is to make ETL pipeline efficient for production workloads.
        """,
        "hint": "Use pandas read_csv() with chunksize for large files. For parallel processing, consider multiprocessing or concurrent.futures.",
        "function_name": "optimize_etl_performance",
        "parameters": ["pipeline_func: callable", "test_data: Dict[str, Any]", "iterations: int = 3"],
        "returns": "Dict[str, Any] (optimization results)"
    }


def exercise_8_data_quality_monitoring() -> Dict[str, Any]:
    """
    Exercise 8: Data Quality Monitoring
    
    Implement data quality monitoring and alerting system.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement comprehensive data quality monitoring for the data warehouse.
        
        Monitoring Areas:
        1. Completeness: Missing values, null rates
        2. Accuracy: Business rule violations, outlier detection
        3. Consistency: Cross-table referential integrity
        4. Timeliness: Data freshness, latency metrics
        5. Validity: Data type compliance, format validation
        
        Requirements:
        1. Define data quality rules and thresholds
        2. Implement automated quality checks
        3. Generate quality scorecards and dashboards
        4. Set up alerting for quality violations
        5. Track quality trends over time
        6. Support ad-hoc quality investigations
        
        Additional Features:
        - Automated data profiling
        - Anomaly detection for quality metrics
        - Root cause analysis for quality issues
        - SLA tracking for data delivery
        
        The goal is to ensure ongoing data quality in the warehouse.
        """,
        "hint": "Create a DataQualityMonitor class with rule-based checks. Store quality metrics in a database for trend analysis.",
        "function_name": "monitor_data_quality",
        "parameters": ["db_config: Dict[str, str]", "quality_rules: Dict[str, Any]", "alert_thresholds: Dict[str, float]"],
        "returns": "Dict[str, Any] (quality report)"
    }


def exercise_9_incremental_etl_processing() -> Dict[str, Any]:
    """
    Exercise 9: Incremental ETL Processing
    
    Implement incremental ETL processing for daily updates.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement incremental ETL processing to handle daily data updates efficiently.
        
        Incremental Processing Requirements:
        1. Identify new and changed records since last run
        2. Process only delta data (not full refresh)
        3. Handle dimension updates with SCD Type 2
        4. Append new facts to existing fact tables
        5. Maintain change data capture (CDC) metadata
        
        Challenges:
        1. Detect deleted records in source systems
        2. Handle late-arriving facts and dimensions
        3. Maintain consistency during incremental updates
        4. Support backfilling historical data
        
        Requirements:
        1. Implement CDC using timestamps, checksums, or database triggers
        2. Create metadata tables to track ETL execution
        3. Support reprocessing of specific date ranges
        4. Handle partial failures and resume capability
        
        The goal is to build efficient daily ETL processes.
        """,
        "hint": "Use last_updated timestamp columns for CDC. Maintain an ETL metadata table to track last successful run.",
        "function_name": "run_incremental_etl",
        "parameters": ["config: Dict[str, Any]", "last_run_date: datetime = None"],
        "returns": "Dict[str, Any] (incremental load statistics)"
    }


def exercise_10_analytics_and_reporting() -> Dict[str, Any]:
    """
    Exercise 10: Analytics and Reporting
    
    Build analytics and reporting on top of the data warehouse.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Build analytical queries and reports on the data warehouse.
        
        Analytical Queries to Implement:
        1. Top N customers by total spend
        2. Revenue by region and time period
        3. Product category performance trends
        4. Customer retention and churn analysis
        5. Sales forecasting based on historical data
        
        Reporting Requirements:
        1. Create parameterized queries for ad-hoc analysis
        2. Generate summary reports (daily, weekly, monthly)
        3. Build data visualizations (charts, dashboards)
        4. Export reports to multiple formats (CSV, Excel, PDF)
        5. Schedule automated report generation
        
        Additional Features:
        - Interactive dashboards with filtering
        - Alerting on business KPI thresholds
        - Comparative analysis (YoY, MoM)
        - What-if analysis scenarios
        
        The goal is to demonstrate business value from the data warehouse.
        """,
        "hint": "Use SQL for complex aggregations, pandas for data manipulation, and matplotlib/plotly for visualizations.",
        "function_name": "generate_analytics",
        "parameters": ["db_config: Dict[str, str]", "report_type: str", "parameters: Dict[str, Any]"],
        "returns": "Dict[str, Any] (analytics results)"
    }


def main():
    """Print all exercise descriptions."""
    exercises = [
        exercise_1_extract_csv_data(),
        exercise_2_data_validation_and_cleaning(),
        exercise_3_dimension_table_processing(),
        exercise_4_fact_table_processing(),
        exercise_5_postgres_database_operations(),
        exercise_6_etl_orchestration(),
        exercise_7_performance_optimization(),
        exercise_8_data_quality_monitoring(),
        exercise_9_incremental_etl_processing(),
        exercise_10_analytics_and_reporting(),
    ]
    
    print("=" * 80)
    print("WAREHOUSE BUILDER PRACTICE EXERCISES")
    print("=" * 80)
    print("\nThese exercises help you build a complete ETL pipeline and data warehouse.")
    print("Implement each function according to the specifications.\n")
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"EXERCISE {i}: {exercise['function_name']}")
        print(f"{'='*60}")
        print(f"Description: {exercise['description'].strip()}")
        print(f"\nFunction: {exercise['function_name']}({', '.join(exercise['parameters'])})")
        print(f"Returns: {exercise['returns']}")
        print(f"Hint: {exercise['hint']}")
        print(f"\nTODO: Implement the function above according to the requirements.")
        print(f"{'-'*60}")


if __name__ == "__main__":
    main()