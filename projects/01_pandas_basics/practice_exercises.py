"""
Pandas Basics Practice Exercises
================================

This file contains hands-on exercises to reinforce Pandas fundamentals for data engineering.
Focus on memory-efficient operations suitable for 8GB RAM systems.

Each exercise builds on real-world data engineering scenarios with increasing complexity.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import os
import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Exercise 1: Data Loading and Inspection
def exercise_1_data_loading_inspection() -> pd.DataFrame:
    """
    Exercise 1: Data Loading and Basic Inspection
    
    Scenario: You're given a messy CSV file with sales data. Your task is to:
    1. Load the data efficiently (consider memory usage)
    2. Perform basic inspection
    3. Identify data quality issues
    
    Tasks:
    1. Load 'sales_data.csv' with appropriate parameters for memory efficiency
    2. Print shape, column names, and data types
    3. Check for missing values in each column
    4. Identify columns with inconsistent data types
    5. Calculate memory usage of the DataFrame
    
    Returns:
        pd.DataFrame: The loaded DataFrame
    """
    print("=== Exercise 1: Data Loading and Inspection ===")
    
    # Task 1: Load the CSV file with memory-efficient parameters
    # Hint: Use pd.read_csv() with appropriate parameters like dtype, usecols, nrows for testing
    # TODO: Implement loading with memory optimization
    
    # Task 2: Print basic information
    # TODO: Print shape, columns, dtypes
    
    # Task 3: Check for missing values
    # TODO: Calculate and print missing values per column
    
    # Task 4: Identify inconsistent data types
    # TODO: Check for columns that should be numeric but are object type
    
    # Task 5: Calculate memory usage
    # TODO: Use df.memory_usage(deep=True) and print total memory
    
    # Placeholder return - replace with actual implementation
    return pd.DataFrame()

# Exercise 2: Data Cleaning and Transformation
def exercise_2_data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exercise 2: Data Cleaning and Transformation
    
    Scenario: Clean the sales data by handling:
    1. Missing values
    2. Inconsistent formatting
    3. Invalid data
    4. Data type conversions
    
    Tasks:
    1. Handle missing values in 'product' column (drop or fill appropriately)
    2. Standardize 'region' column (title case, remove extra spaces)
    3. Fix 'quantity' column (convert negative values to positive, handle zeros)
    4. Convert 'order_date' to datetime format
    5. Create a new column 'total_sales' = quantity * unit_price
    6. Remove duplicate rows based on order_id
    
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("\n=== Exercise 2: Data Cleaning and Transformation ===")
    
    # Task 1: Handle missing values in 'product' column
    # TODO: Decide whether to drop or fill missing product values
    
    # Task 2: Standardize 'region' column
    # TODO: Convert to title case, strip whitespace
    
    # Task 3: Fix 'quantity' column
    # TODO: Handle negative values and zeros appropriately
    
    # Task 4: Convert 'order_date' to datetime
    # TODO: Use pd.to_datetime() with error handling
    
    # Task 5: Create 'total_sales' column
    # TODO: Calculate total_sales = quantity * unit_price
    
    # Task 6: Remove duplicate rows
    # TODO: Drop duplicates based on order_id
    
    # Placeholder return - replace with actual implementation
    return df.copy()

# Exercise 3: Memory-Efficient Operations
def exercise_3_memory_efficient_operations(df: pd.DataFrame) -> Dict[str, any]:
    """
    Exercise 3: Memory-Efficient Operations for 8GB RAM
    
    Scenario: You need to process large datasets on a system with 8GB RAM.
    Implement memory optimization techniques.
    
    Tasks:
    1. Downcast numeric columns to smallest appropriate dtype
    2. Convert object columns to categorical where appropriate
    3. Process data in chunks if DataFrame is too large
    4. Use efficient aggregation methods
    5. Monitor memory usage before and after optimizations
    
    Returns:
        Dict: Dictionary containing optimization results and memory savings
    """
    print("\n=== Exercise 3: Memory-Efficient Operations ===")
    
    # Task 1: Downcast numeric columns
    # TODO: Use pd.to_numeric() with downcast parameter
    
    # Task 2: Convert object columns to categorical
    # TODO: Identify low-cardinality columns and convert to category dtype
    
    # Task 3: Implement chunk processing
    # TODO: Create a function that processes DataFrame in chunks
    
    # Task 4: Efficient aggregation
    # TODO: Compare memory usage of different aggregation methods
    
    # Task 5: Monitor memory usage
    # TODO: Calculate memory before/after optimizations
    
    return {
        "original_memory_mb": 0,
        "optimized_memory_mb": 0,
        "savings_percent": 0,
        "downcasted_columns": [],
        "categorical_columns": []
    }

# Exercise 4: Aggregation and GroupBy Operations
def exercise_4_aggregation_groupby(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Exercise 4: Aggregation and GroupBy Operations
    
    Scenario: Generate business reports from cleaned sales data.
    
    Tasks:
    1. Calculate total sales by region
    2. Find average order value by product category
    3. Identify top 5 selling products by quantity
    4. Calculate monthly sales trends
    5. Create a pivot table showing sales by region and product
    
    Returns:
        Dict: Dictionary containing various aggregated DataFrames
    """
    print("\n=== Exercise 4: Aggregation and GroupBy ===")
    
    # Task 1: Total sales by region
    # TODO: Group by region and sum total_sales
    
    # Task 2: Average order value by product
    # TODO: Group by product and calculate mean of total_sales
    
    # Task 3: Top 5 selling products
    # TODO: Sort by quantity sold and get top 5
    
    # Task 4: Monthly sales trends
    # TODO: Resample by month and calculate total sales
    
    # Task 5: Pivot table
    # TODO: Create pivot table region vs product
    
    return {
        "sales_by_region": pd.DataFrame(),
        "avg_order_by_product": pd.DataFrame(),
        "top_products": pd.DataFrame(),
        "monthly_trends": pd.DataFrame(),
        "pivot_table": pd.DataFrame()
    }

# Exercise 5: File I/O with Different Formats
def exercise_5_file_io_optimization(df: pd.DataFrame) -> Dict[str, float]:
    """
    Exercise 5: File I/O Optimization for Different Formats
    
    Scenario: Compare performance and memory usage of different file formats.
    
    Tasks:
    1. Save DataFrame to CSV, Parquet, and Feather formats
    2. Measure file sizes and write times
    3. Load each file back and measure read times
    4. Compare memory usage of loaded DataFrames
    5. Recommend best format for different use cases
    
    Returns:
        Dict: Performance metrics for each format
    """
    print("\n=== Exercise 5: File I/O Optimization ===")
    
    # Task 1: Save to different formats
    # TODO: Save to CSV, Parquet, and Feather
    
    # Task 2: Measure file sizes and write times
    # TODO: Use time.time() to measure performance
    
    # Task 3: Load files and measure read times
    # TODO: Load each format and time the operation
    
    # Task 4: Compare memory usage
    # TODO: Calculate memory usage of each loaded DataFrame
    
    # Task 5: Provide recommendations
    # TODO: Based on metrics, recommend best format for different scenarios
    
    return {
        "csv_size_mb": 0,
        "parquet_size_mb": 0,
        "feather_size_mb": 0,
        "csv_write_time": 0,
        "parquet_write_time": 0,
        "feather_write_time": 0,
        "csv_read_time": 0,
        "parquet_read_time": 0,
        "feather_read_time": 0
    }

# Exercise 6: Handling Large Datasets with Chunking
def exercise_6_chunking_large_datasets() -> pd.DataFrame:
    """
    Exercise 6: Handling Large Datasets with Chunking
    
    Scenario: Process a dataset that's too large to fit in memory.
    Use chunking techniques to process in batches.
    
    Tasks:
    1. Read CSV in chunks with pd.read_csv(chunksize=...)
    2. Clean each chunk independently
    3. Aggregate results across chunks
    4. Merge cleaned chunks into final DataFrame
    5. Handle edge cases (data spanning chunks)
    
    Returns:
        pd.DataFrame: Final aggregated DataFrame
    """
    print("\n=== Exercise 6: Chunking Large Datasets ===")
    
    # Task 1: Read in chunks
    # TODO: Use pd.read_csv with chunksize parameter
    
    # Task 2: Clean each chunk
    # TODO: Apply cleaning operations to each chunk
    
    # Task 3: Aggregate across chunks
    # TODO: Maintain running totals or collect results
    
    # Task 4: Merge chunks
    # TODO: Combine cleaned chunks into final DataFrame
    
    # Task 5: Handle edge cases
    # TODO: Consider records that might be split across chunks
    
    return pd.DataFrame()

# Exercise 7: Real-World Data Engineering Pipeline
def exercise_7_complete_pipeline() -> Dict[str, any]:
    """
    Exercise 7: Complete Data Engineering Pipeline
    
    Scenario: Implement an end-to-end data pipeline from raw data to insights.
    
    Tasks:
    1. Load raw data with error handling
    2. Perform data validation and quality checks
    3. Clean and transform data
    4. Optimize memory usage
    5. Generate business insights
    6. Export results in optimized format
    7. Create a summary report
    
    Returns:
        Dict: Pipeline results including metrics and output files
    """
    print("\n=== Exercise 7: Complete Data Engineering Pipeline ===")
    
    # Task 1: Load with error handling
    # TODO: Implement robust loading with try-except
    
    # Task 2: Data validation
    # TODO: Check for required columns, data types, value ranges
    
    # Task 3: Clean and transform
    # TODO: Apply all cleaning operations from previous exercises
    
    # Task 4: Memory optimization
    # TODO: Apply downcasting and categorical conversion
    
    # Task 5: Generate insights
    # TODO: Calculate key business metrics
    
    # Task 6: Export results
    # TODO: Save cleaned data and insights to files
    
    # Task 7: Create summary report
    # TODO: Generate a text report with pipeline statistics
    
    return {
        "success": True,
        "rows_processed": 0,
        "cleaning_issues_fixed": 0,
        "memory_savings_mb": 0,
        "output_files": [],
        "insights": {}
    }

# Main function to run all exercises
def main():
    """Run all practice exercises in sequence."""
    print("=" * 60)
    print("PANDAS BASICS PRACTICE EXERCISES")
    print("=" * 60)
    
    # Check if data file exists
    if not os.path.exists('sales_data.csv'):
        print("Error: sales_data.csv not found. Run generate_data.py first.")
        return
    
    try:
        # Exercise 1: Data Loading
        print("\n" + "=" * 40)
        print("Starting Exercise 1: Data Loading and Inspection")
        print("=" * 40)
        df_raw = exercise_1_data_loading_inspection()
        
        # Exercise 2: Data Cleaning
        print("\n" + "=" * 40)
        print("Starting Exercise 2: Data Cleaning")
        print("=" * 40)
        df_clean = exercise_2_data_cleaning(df_raw)
        
        # Exercise 3: Memory Optimization
        print("\n" + "=" * 40)
        print("Starting Exercise 3: Memory Optimization")
        print("=" * 40)
        optimization_results = exercise_3_memory_efficient_operations(df_clean)
        
        # Exercise 4: Aggregation
        print("\n" + "=" * 40)
        print("Starting Exercise 4: Aggregation")
        print("=" * 40)
        aggregation_results = exercise_4_aggregation_groupby(df_clean)
        
        # Exercise 5: File I/O
        print("\n" + "=" * 40)
        print("Starting Exercise 5: File I/O Optimization")
        print("=" * 40)
        io_results = exercise_5_file_io_optimization(df_clean)
        
        # Exercise 6: Chunking
        print("\n" + "=" * 40)
        print("Starting Exercise 6: Chunking Large Datasets")
        print("=" * 40)
        chunked_results = exercise_6_chunking_large_datasets()
        
        # Exercise 7: Complete Pipeline
        print("\n" + "=" * 40)
        print("Starting Exercise 7: Complete Pipeline")
        print("=" * 40)
        pipeline_results = exercise_7_complete_pipeline()
        
        print("\n" + "=" * 60)
        print("ALL EXERCISES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Summary
        print("\nSummary of Exercises Completed:")
        print("1. Data Loading and Inspection")
        print("2. Data Cleaning and Transformation")
        print("3. Memory-Efficient Operations")
        print("4. Aggregation and GroupBy")
        print("5. File I/O Optimization")
        print("6. Chunking Large Datasets")
        print("7. Complete Data Engineering Pipeline")
        
    except Exception as e:
        print(f"\nError during exercises: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()