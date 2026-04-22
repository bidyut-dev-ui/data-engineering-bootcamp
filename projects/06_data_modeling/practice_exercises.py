#!/usr/bin/env python3
"""
Practice Exercises for Data Modeling Project

This module contains exercises for understanding data modeling concepts:
- OLTP vs OLAP systems
- Normalization (3NF) vs Denormalization
- Star Schema vs Snowflake Schema design
- Fact and Dimension tables
- ETL for dimensional modeling

IMPORTANT: Do NOT provide solutions in this file. The exercises should contain
TODO placeholders where learners will implement their own solutions.
"""

import sqlite3
from typing import Dict, Any, List, Tuple
import pandas as pd
from datetime import datetime
import random


def exercise_1_create_3nf_schema() -> Dict[str, Any]:
    """
    Exercise 1: Create 3NF (Normalized) Schema
    
    Design and implement a fully normalized 3NF schema for an e-commerce system.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Create a fully normalized 3NF schema for an e-commerce system with the following entities:
        
        Entities:
        1. Customers (customer_id, name, email, registration_date)
        2. Products (product_id, name, category_id, price)
        3. Categories (category_id, category_name, department_id)
        4. Departments (department_id, department_name)
        5. Orders (order_id, customer_id, order_date, total_amount)
        6. Order_Items (order_item_id, order_id, product_id, quantity, unit_price)
        7. Addresses (address_id, customer_id, address_type, street, city, state, zip_code)
        
        Requirements:
        1. Design tables with appropriate primary keys and foreign keys
        2. Ensure 3NF compliance (no transitive dependencies)
        3. Create the schema in SQLite
        4. Insert sample data for testing
        
        The goal is to understand normalization principles and trade-offs.
        """,
        "hint": "Use CREATE TABLE statements with FOREIGN KEY constraints. Consider using ON DELETE CASCADE for referential integrity.",
        "function_name": "create_3nf_schema",
        "parameters": ["db_path: str = 'ecommerce_3nf.db'"],
        "returns": "sqlite3.Connection"
    }


def exercise_2_create_star_schema() -> Dict[str, Any]:
    """
    Exercise 2: Create Star Schema
    
    Design and implement a star schema for the same e-commerce system optimized for analytics.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Create a star schema (dimensional model) for the e-commerce system optimized for analytics.
        
        Dimension Tables:
        1. dim_customer (customer_key, customer_id, name, email, registration_date, city, state)
        2. dim_product (product_key, product_id, name, category_name, department_name, price)
        3. dim_date (date_key, date, day, month, year, quarter, day_of_week, is_weekend)
        4. dim_time (time_key, hour, minute, period_of_day)
        
        Fact Table:
        1. fact_sales (sale_key, customer_key, product_key, date_key, time_key, 
                      quantity, unit_price, total_amount, discount_amount)
        
        Requirements:
        1. Denormalize dimensions for faster queries
        2. Include surrogate keys (auto-increment) for dimensions
        3. Add slowly changing dimension (SCD) Type 2 support for dim_customer
        4. Create appropriate indexes for query performance
        
        The goal is to understand denormalization for analytical workloads.
        """,
        "hint": "Design dimensions with descriptive attributes and facts with numeric measures. Use INTEGER PRIMARY KEY for surrogate keys.",
        "function_name": "create_star_schema",
        "parameters": ["db_path: str = 'ecommerce_star.db'"],
        "returns": "sqlite3.Connection"
    }


def exercise_3_etl_3nf_to_star() -> Dict[str, Any]:
    """
    Exercise 3: ETL from 3NF to Star Schema
    
    Build an ETL pipeline that extracts data from 3NF schema, transforms it, and loads into star schema.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Build an ETL pipeline that transforms data from 3NF schema to star schema.
        
        ETL Steps:
        1. Extract: Read data from 3NF tables (customers, products, orders, order_items)
        2. Transform:
           - Flatten customer with address information
           - Flatten product with category and department
           - Create date dimension from order dates
           - Create time dimension from order timestamps
           - Calculate derived measures (total_amount = quantity * unit_price - discount)
        3. Load: Insert transformed data into star schema tables
        
        Requirements:
        1. Handle incremental updates (only process new/changed records)
        2. Implement error handling and logging
        3. Add data quality checks
        4. Generate ETL execution report
        
        The goal is to understand the transformation process in dimensional modeling.
        """,
        "hint": "Use SQL JOINs for extraction, pandas for transformation (or pure SQL), and batch inserts for loading.",
        "function_name": "run_etl_pipeline",
        "parameters": ["source_db: str", "target_db: str", "incremental: bool = True"],
        "returns": "Dict[str, Any] (etl statistics)"
    }


def exercise_4_query_comparison() -> Dict[str, Any]:
    """
    Exercise 4: Query Complexity Comparison
    
    Write equivalent queries in 3NF and star schema and compare their complexity and performance.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Write and compare queries for both 3NF and star schema to demonstrate the benefits of dimensional modeling.
        
        Query Requirements:
        1. Total sales by department for Q1 2024
        2. Top 10 customers by purchase amount
        3. Monthly sales trend for the past year
        4. Average order value by customer city
        5. Product category performance by quarter
        
        For each query:
        - Write the 3NF version (multiple JOINs)
        - Write the star schema version (simpler JOINs)
        - Compare execution time
        - Compare query complexity (lines of SQL)
        
        Requirements:
        1. Use EXPLAIN QUERY PLAN to analyze query execution
        2. Measure execution time for both schemas
        3. Document the complexity difference
        
        The goal is to quantitatively demonstrate the advantages of star schema for analytics.
        """,
        "hint": "For timing, use time.time() before and after query execution. For complexity, count JOIN operations and WHERE conditions.",
        "function_name": "compare_queries",
        "parameters": ["query_id: int", "nf_db: sqlite3.Connection", "star_db: sqlite3.Connection"],
        "returns": "Dict[str, Any] (comparison results)"
    }


def exercise_5_slowly_changing_dimensions() -> Dict[str, Any]:
    """
    Exercise 5: Slowly Changing Dimensions (SCD)
    
    Implement SCD Type 2 for customer dimension to track historical changes.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement Slowly Changing Dimension (SCD) Type 2 for customer dimension to track historical changes.
        
        SCD Type 2 Requirements:
        1. When a customer attribute changes (e.g., city), create a new version
        2. Maintain effective date range (valid_from, valid_to)
        3. Set current version flag (is_current = True/False)
        4. Handle updates, inserts, and deletions
        
        Implementation Steps:
        1. Modify dim_customer table to include SCD columns
        2. Create SCD detection logic (compare current vs new)
        3. Implement SCD Type 2 update process
        4. Test with customer address changes
        
        Additional Challenge:
        - Implement SCD Type 1 (overwrite) for some attributes
        - Implement SCD Type 3 (add previous value column) for critical attributes
        
        The goal is to understand dimension management in data warehouses.
        """,
        "hint": "Add columns: valid_from DATE, valid_to DATE, is_current BOOLEAN. Use NULL for valid_to of current records.",
        "function_name": "implement_scd_type2",
        "parameters": ["customer_updates: List[Dict[str, Any]]", "dim_connection: sqlite3.Connection"],
        "returns": "Dict[str, int] (update statistics)"
    }


def exercise_6_snowflake_schema_design() -> Dict[str, Any]:
    """
    Exercise 6: Snowflake Schema Design
    
    Design and implement a snowflake schema as a compromise between 3NF and star schema.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Design and implement a snowflake schema for the e-commerce system.
        
        Snowflake Schema Requirements:
        1. Normalize some dimensions (e.g., product → category → department)
        2. Maintain star schema fact table
        3. Balance between normalization and query performance
        4. Compare with star schema on storage and query performance
        
        Design:
        1. dim_product (product_key, product_id, name, price, category_key)
        2. dim_category (category_key, category_id, category_name, department_key)
        3. dim_department (department_key, department_id, department_name)
        4. fact_sales (connects to dim_product, not to dim_category/dim_department)
        
        Requirements:
        1. Create the snowflake schema
        2. Load data from 3NF
        3. Write queries and compare with star schema
        4. Analyze trade-offs (storage vs query complexity)
        
        The goal is to understand when snowflake schema is appropriate.
        """,
        "hint": "Snowflake schema is partially normalized star schema. Queries will need more JOINs but storage may be smaller.",
        "function_name": "create_snowflake_schema",
        "parameters": ["db_path: str = 'ecommerce_snowflake.db'"],
        "returns": "sqlite3.Connection"
    }


def exercise_7_data_vault_modeling() -> Dict[str, Any]:
    """
    Exercise 7: Data Vault Modeling
    
    Implement basic Data Vault 2.0 concepts for agile data warehouse design.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement basic Data Vault 2.0 modeling concepts for the e-commerce system.
        
        Data Vault Components:
        1. Hubs: Business keys (customer_id, product_id, order_id)
        2. Links: Relationships between hubs (customer_order_link, order_product_link)
        3. Satellites: Descriptive attributes for hubs/links (sat_customer, sat_product)
        
        Design Requirements:
        1. Create hub_customer, hub_product, hub_order
        2. Create link_customer_order, link_order_product
        3. Create sat_customer_details, sat_product_details, sat_order_details
        4. Load data from 3NF source
        5. Demonstrate querying from Data Vault
        
        Additional Concepts:
        - Add load date and record source to all tables
        - Implement hash keys for primary keys
        - Show how to build star schema from Data Vault
        
        The goal is to understand agile data warehouse design patterns.
        """,
        "hint": "Data Vault uses hash keys (MD5/SHA) for primary keys. Hubs contain business keys, links contain hash key relationships.",
        "function_name": "create_data_vault",
        "parameters": ["db_path: str = 'ecommerce_datavault.db'"],
        "returns": "sqlite3.Connection"
    }


def exercise_8_performance_benchmarking() -> Dict[str, Any]:
    """
    Exercise 8: Performance Benchmarking
    
    Benchmark different schema designs on various query patterns.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Benchmark and compare performance of different schema designs.
        
        Schemas to Compare:
        1. 3NF (fully normalized)
        2. Star Schema (fully denormalized)
        3. Snowflake Schema (partially normalized)
        4. Data Vault (agile design)
        
        Benchmark Queries:
        1. Simple aggregation (total sales)
        2. Multi-table JOIN (sales by department)
        3. Time-series analysis (monthly trends)
        4. Ad-hoc dimensional query (drill-down)
        
        Metrics to Measure:
        1. Query execution time
        2. Storage space used
        3. Query complexity (lines of SQL)
        4. Memory usage during query
        5. Index size and effectiveness
        
        Requirements:
        1. Generate benchmark report with recommendations
        2. Visualize results (charts if possible)
        3. Provide guidance on schema selection
        
        The goal is to make data-driven schema design decisions.
        """,
        "hint": "Use SQLite's EXPLAIN QUERY PLAN for query analysis. Use time.perf_counter() for precise timing.",
        "function_name": "benchmark_schemas",
        "parameters": ["schemas: Dict[str, sqlite3.Connection]", "query_set: List[str]"],
        "returns": "pd.DataFrame (benchmark results)"
    }


def exercise_9_schema_evolution() -> Dict[str, Any]:
    """
    Exercise 9: Schema Evolution
    
    Handle schema changes in a production data warehouse.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Handle schema evolution scenarios in a production data warehouse.
        
        Evolution Scenarios:
        1. Add new column to dimension (customer loyalty tier)
        2. Remove deprecated column (legacy shipping method)
        3. Change data type (price from INTEGER to DECIMAL)
        4. Split column (full_name to first_name, last_name)
        5. Add new dimension (payment method)
        
        Requirements for Each Scenario:
        1. Plan backward compatibility
        2. Implement migration script
        3. Update ETL processes
        4. Test with existing queries
        5. Document the change
        
        Additional Considerations:
        - Zero-downtime deployment
        - Data validation after migration
        - Rollback strategy
        - Communication plan
        
        The goal is to understand production schema management.
        """,
        "hint": "Use ALTER TABLE ADD COLUMN for additive changes. For breaking changes, create new table and migrate data.",
        "function_name": "handle_schema_evolution",
        "parameters": ["evolution_scenario: str", "db_connection: sqlite3.Connection"],
        "returns": "Dict[str, Any] (migration results)"
    }


def exercise_10_dimensional_modeling_documentation() -> Dict[str, Any]:
    """
    Exercise 10: Dimensional Modeling Documentation
    
    Create comprehensive documentation for a dimensional model.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Create comprehensive documentation for a dimensional model.
        
        Documentation Components:
        1. Business Requirements Document
        2. Data Dictionary (tables, columns, data types, descriptions)
        3. Entity-Relationship Diagram (ERD)
        4. Data Flow Diagram (source → staging → warehouse → marts)
        5. Query Patterns and Examples
        6. ETL Specification
        7. Change Log
        
        Requirements:
        1. Use Markdown for documentation
        2. Generate diagrams using Mermaid or similar
        3. Include sample queries for common business questions
        4. Document data quality rules
        5. Create a data lineage map
        
        Tools to Use:
        - SQL comments for data dictionary
        - Python for automated documentation generation
        - Version control for change tracking
        
        The goal is to understand the importance of documentation in data modeling.
        """,
        "hint": "Use SQLite's pragma table_info() to generate data dictionary. Use graphviz or mermaid for diagrams.",
        "function_name": "generate_documentation",
        "parameters": ["schema_name: str", "db_connection: sqlite3.Connection", "output_dir: str"],
        "returns": "Dict[str, str] (paths to generated documents)"
    }


def main():
    """Print all exercise descriptions."""
    exercises = [
        exercise_1_create_3nf_schema(),
        exercise_2_create_star_schema(),
        exercise_3_etl_3nf_to_star(),
        exercise_4_query_comparison(),
        exercise_5_slowly_changing_dimensions(),
        exercise_6_snowflake_schema_design(),
        exercise_7_data_vault_modeling(),
        exercise_8_performance_benchmarking(),
        exercise_9_schema_evolution(),
        exercise_10_dimensional_modeling_documentation(),
    ]
    
    print("=" * 80)
    print("DATA MODELING PRACTICE EXERCISES")
    print("=" * 80)
    print("\nThese exercises help you understand data modeling concepts and trade-offs.")
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