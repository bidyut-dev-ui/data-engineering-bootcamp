#!/usr/bin/env python3
"""
Advanced Pandas Practice Exercises for Memory-Constrained Environments (8GB RAM)

This module provides hands-on exercises for mastering advanced Pandas techniques
focused on memory optimization, chunked processing, and performance tuning.
"""

import pandas as pd
import numpy as np
import os
import sys
from typing import Dict, Any, List, Optional, Generator
import time
import psutil
import gc

def get_memory_usage_mb() -> float:
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def exercise_1_memory_optimization_basics() -> Dict[str, Any]:
    """
    Exercise 1: Memory Optimization Fundamentals
    
    Learn to analyze and reduce Pandas DataFrame memory usage through:
    1. Memory profiling of different data types
    2. Downcasting numeric columns
    3. Converting strings to categoricals
    4. Dropping unnecessary columns
    
    Returns:
        Dictionary with memory savings metrics
    """
    print("\n" + "="*60)
    print("EXERCISE 1: Memory Optimization Basics")
    print("="*60)
    
    results = {
        "initial_memory_mb": 0,
        "optimized_memory_mb": 0,
        "savings_percentage": 0,
        "optimization_steps": []
    }
    
    # Create sample data with inefficient types
    np.random.seed(42)
    n_rows = 100000
    
    data = {
        'id': np.arange(n_rows, dtype=np.int64),  # Using int64 when int32 would suffice
        'score': np.random.randn(n_rows).astype(np.float64) * 100,  # float64
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_rows),  # Strings
        'status': np.random.choice(['active', 'inactive', 'pending'], n_rows),
        'count': np.random.randint(0, 1000, n_rows, dtype=np.int64),  # int64 for small values
        'price': np.random.uniform(0, 1000, n_rows).astype(np.float64),
        'flag': np.random.choice([True, False], n_rows)  # Boolean
    }
    
    df = pd.DataFrame(data)
    initial_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
    results["initial_memory_mb"] = round(initial_memory, 2)
    results["optimization_steps"].append(f"Initial memory: {initial_memory:.2f} MB")
    
    print(f"Initial DataFrame shape: {df.shape}")
    print(f"Initial memory usage: {initial_memory:.2f} MB")
    print("\nData types before optimization:")
    print(df.dtypes)
    
    # Step 1: Downcast integer columns
    print("\n--- Step 1: Downcasting integer columns ---")
    int_cols = df.select_dtypes(include=['int64']).columns
    for col in int_cols:
        original_dtype = str(df[col].dtype)
        df[col] = pd.to_numeric(df[col], downcast='integer')
        new_dtype = str(df[col].dtype)
        if original_dtype != new_dtype:
            results["optimization_steps"].append(f"Downcasted {col}: {original_dtype} -> {new_dtype}")
    
    # Step 2: Downcast float columns
    print("\n--- Step 2: Downcasting float columns ---")
    float_cols = df.select_dtypes(include=['float64']).columns
    for col in float_cols:
        original_dtype = str(df[col].dtype)
        df[col] = pd.to_numeric(df[col], downcast='float')
        new_dtype = str(df[col].dtype)
        if original_dtype != new_dtype:
            results["optimization_steps"].append(f"Downcasted {col}: {original_dtype} -> {new_dtype}")
    
    # Step 3: Convert strings to categorical
    print("\n--- Step 3: Converting strings to categorical ---")
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        unique_count = df[col].nunique()
        total_count = len(df[col])
        if unique_count / total_count < 0.5:  # Convert if cardinality < 50%
            original_memory = df[col].memory_usage(deep=True) / 1024  # KB
            df[col] = df[col].astype('category')
            new_memory = df[col].memory_usage(deep=True) / 1024
            savings = (original_memory - new_memory) / original_memory * 100
            results["optimization_steps"].append(
                f"Categorical {col}: {unique_count} unique, saved {savings:.1f}%"
            )
    
    # Step 4: Optimize boolean columns
    print("\n--- Step 4: Optimizing boolean columns ---")
    bool_cols = df.select_dtypes(include=['bool']).columns
    for col in bool_cols:
        df[col] = df[col].astype('uint8')  # More efficient than bool for storage
        results["optimization_steps"].append(f"Optimized {col}: bool -> uint8")
    
    # Calculate final memory
    optimized_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
    results["optimized_memory_mb"] = round(optimized_memory, 2)
    savings_pct = (initial_memory - optimized_memory) / initial_memory * 100
    results["savings_percentage"] = round(savings_pct, 2)
    
    print(f"\nOptimized memory usage: {optimized_memory:.2f} MB")
    print(f"Memory savings: {savings_pct:.1f}%")
    print("\nData types after optimization:")
    print(df.dtypes)
    
    return results

def exercise_2_chunked_processing_large_files() -> Dict[str, Any]:
    """
    Exercise 2: Chunked Processing for Large Files
    
    Learn to process files larger than available RAM using:
    1. Pandas read_csv with chunksize parameter
    2. Incremental aggregation
    3. Filtering within chunks
    4. Memory monitoring during processing
    
    Returns:
        Dictionary with processing metrics and results
    """
    print("\n" + "="*60)
    print("EXERCISE 2: Chunked Processing for Large Files")
    print("="*60)
    
    results = {
        "total_rows_processed": 0,
        "peak_memory_mb": 0,
        "processing_time_seconds": 0,
        "aggregation_results": {},
        "chunk_stats": []
    }
    
    # Create a large CSV file if it doesn't exist
    csv_path = "large_sales_chunked.csv"
    if not os.path.exists(csv_path):
        print(f"Creating large CSV file: {csv_path}")
        np.random.seed(42)
        n_rows = 1000000  # 1 million rows
        
        # Generate data in chunks to avoid memory issues
        chunk_size = 100000
        chunks = []
        
        for i in range(0, n_rows, chunk_size):
            chunk_rows = min(chunk_size, n_rows - i)
            
            chunk_data = {
                'transaction_id': np.arange(i, i + chunk_rows),
                'customer_id': np.random.randint(1000, 9999, chunk_rows),
                'product_id': np.random.randint(1, 100, chunk_rows),
                'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], chunk_rows),
                'quantity': np.random.randint(1, 10, chunk_rows),
                'price': np.random.uniform(10, 1000, chunk_rows),
                'sale_date': pd.date_range('2023-01-01', periods=chunk_rows, freq='H'),
                'region': np.random.choice(['North', 'South', 'East', 'West'], chunk_rows)
            }
            
            chunk_df = pd.DataFrame(chunk_data)
            chunks.append(chunk_df)
        
        # Combine and write to CSV
        large_df = pd.concat(chunks, ignore_index=True)
        large_df.to_csv(csv_path, index=False)
        print(f"Created {csv_path} with {len(large_df):,} rows")
        del large_df, chunks
        gc.collect()
    
    # Now process the file in chunks
    print(f"\nProcessing {csv_path} in chunks...")
    start_time = time.time()
    start_memory = get_memory_usage_mb()
    
    # Initialize aggregation variables
    total_revenue = 0.0
    total_quantity = 0
    category_revenue = {}
    category_quantity = {}
    region_stats = {}
    row_count = 0
    
    chunk_size = 100000  # Process 100k rows at a time
    chunk_counter = 0
    
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        chunk_counter += 1
        chunk_rows = len(chunk)
        row_count += chunk_rows
        
        # Process chunk: Calculate revenue (quantity * price)
        chunk['revenue'] = chunk['quantity'] * chunk['price']
        
        # Update aggregations
        total_revenue += chunk['revenue'].sum()
        total_quantity += chunk['quantity'].sum()
        
        # Category-wise aggregations
        for category, group in chunk.groupby('category'):
            cat_revenue = group['revenue'].sum()
            cat_quantity = group['quantity'].sum()
            
            category_revenue[category] = category_revenue.get(category, 0) + cat_revenue
            category_quantity[category] = category_quantity.get(category, 0) + cat_quantity
        
        # Region statistics
        for region, group in chunk.groupby('region'):
            region_revenue = group['revenue'].sum()
            region_count = len(group)
            region_stats[region] = region_stats.get(region, {'revenue': 0, 'count': 0})
            region_stats[region]['revenue'] += region_revenue
            region_stats[region]['count'] += region_count
        
        # Track chunk statistics
        chunk_memory = get_memory_usage_mb()
        results["chunk_stats"].append({
            "chunk_number": chunk_counter,
            "rows_processed": chunk_rows,
            "memory_mb": round(chunk_memory, 2),
            "cumulative_rows": row_count
        })
        
        if chunk_counter % 5 == 0:
            print(f"  Processed chunk {chunk_counter}: {row_count:,} rows total")
    
    end_time = time.time()
    end_memory = get_memory_usage_mb()
    
    # Calculate processing metrics
    processing_time = end_time - start_time
    peak_memory = max([stat["memory_mb"] for stat in results["chunk_stats"]])
    
    results["total_rows_processed"] = row_count
    results["peak_memory_mb"] = peak_memory
    results["processing_time_seconds"] = round(processing_time, 2)
    
    # Store aggregation results
    results["aggregation_results"] = {
        "total_revenue": round(total_revenue, 2),
        "total_quantity": total_quantity,
        "avg_transaction_value": round(total_revenue / row_count, 2),
        "top_category_by_revenue": max(category_revenue.items(), key=lambda x: x[1])[0] if category_revenue else None,
        "top_category_by_quantity": max(category_quantity.items(), key=lambda x: x[1])[0] if category_quantity else None,
        "category_revenue": {k: round(v, 2) for k, v in category_revenue.items()},
        "region_stats": region_stats
    }
    
    print(f"\nProcessing complete!")
    print(f"Total rows processed: {row_count:,}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Total quantity: {total_quantity:,}")
    print(f"Processing time: {processing_time:.2f} seconds")
    print(f"Peak memory usage: {peak_memory:.2f} MB")
    print(f"Memory increase during processing: {end_memory - start_memory:.2f} MB")
    
    # Clean up
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Cleaned up temporary file: {csv_path}")
    
    return results

def exercise_3_selective_loading_and_filtering() -> Dict[str, Any]:
    """
    Exercise 3: Selective Loading and Early Filtering
    
    Learn techniques to minimize memory usage by:
    1. Loading only required columns
    2. Filtering during read operations
    3. Using appropriate data types from the start
    4. Leveraging query() and eval() for efficient filtering
    
    Returns:
        Dictionary with performance comparisons
    """
    print("\n" + "="*60)
    print("EXERCISE 3: Selective Loading and Early Filtering")
    print("="*60)
    
    results = {
        "naive_loading": {},
        "selective_loading": {},
        "filter_during_read": {},
        "performance_comparison": {}
    }
    
    # Create a test CSV file
    test_csv = "test_selective.csv"
    if not os.path.exists(test_csv):
        print(f"Creating test file: {test_csv}")
        np.random.seed(42)
        n_rows = 500000
        
        data = {
            'id': np.arange(n_rows),
            'name': [f'Customer_{i}' for i in range(n_rows)],
            'age': np.random.randint(18, 80, n_rows),
            'income': np.random.uniform(30000, 150000, n_rows),
            'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_rows),
            'purchase_amount': np.random.uniform(10, 1000, n_rows),
            'purchase_date': pd.date_range('2023-01-01', periods=n_rows, freq='H'),
            'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows),
            'rating': np.random.randint(1, 6, n_rows),
            'is_premium': np.random.choice([True, False], n_rows, p=[0.2, 0.8])
        }
        
        df = pd.DataFrame(data)
        df.to_csv(test_csv, index=False)
        print(f"Created {test_csv} with {n_rows:,} rows")
    
    # Method 1: Naive loading (load everything)
    print("\n--- Method 1: Naive Loading ---")
    start_time = time.time()
    start_memory = get_memory_usage_mb()
    
    df_naive = pd.read_csv(test_csv)
    naive_memory = df_naive.memory_usage(deep=True).sum() / (1024 * 1024)
    naive_rows = len(df_naive)
    
    # Filter after loading
    df_filtered = df_naive[(df_naive['age'] > 30) & (df_naive['income'] > 50000) & (df_naive['city'] == 'New York')]
    filtered_rows = len(df_filtered)
    
    end_time = time.time()
    naive_time = end_time - start_time
    
    results["naive_loading"] = {
        "load_time_seconds": round(naive_time, 3),
        "memory_mb": round(naive_memory, 2),
        "total_rows": naive_rows,
        "filtered_rows": filtered_rows,
        "filter_ratio": round(filtered_rows / naive_rows * 100, 2)
    }
    
    print(f"Load time: {naive_time:.3f} seconds")
    print(f"Memory usage: {naive_memory:.2f} MB")
    print(f"Rows loaded: {naive_rows:,}")
    print(f"Rows after filtering: {filtered_rows:,} ({filtered_rows/naive_rows*100:.1f}%)")
    
    # Clean up
    del df_naive, df_filtered
    gc.collect()
    
    # Method 2: Selective loading (only needed columns)
    print("\n--- Method 2: Selective Loading ---")
    start_time = time.time()
    start_memory = get_memory_usage_mb()
    
    # Only load columns we need for filtering and analysis
    usecols = ['id', 'age', 'income', 'city', 'purchase_amount', 'category']
    df_selective = pd.read_csv(test_csv, usecols=usecols)
    selective_memory = df_selective.memory_usage(deep=True).sum() / (1024 * 1024)
    
    # Filter
    df_filtered = df_selective[(df_selective['age'] > 30) & (df_selective['income'] > 50000) & (df_selective['city'] == 'New York')]
    filtered_rows = len(df_filtered)
    
    end_time = time.time()
    selective_time = end_time - start_time
    
    results["selective_loading"] = {
        "load_time_seconds": round(selective_time, 3),
        "memory_mb": round(selective_memory, 2),
        "columns_loaded": len(usecols),
        "filtered_rows": filtered_rows
    }
    
    print(f"Load time: {selective_time:.3f} seconds")
    print(f"Memory usage: {selective_memory:.2f} MB")
    print(f"Columns loaded: {len(usecols)} (vs 10 in naive)")
    print(f"Rows after filtering: {filtered_rows:,}")
    
    # Clean up
    del df_selective, df_filtered
    gc.collect()
    
    # Method 3: Filter during read (using chunks)
    print("\n--- Method 3: Filter During Read (Chunked) ---")
    start_time = time.time()
    start_memory = get_memory_usage_mb()
    
    filtered_chunks = []
    chunk_size = 50000
    
    for chunk in pd.read_csv(test_csv, chunksize=chunk_size):
        # Apply filter to each chunk
        chunk_filtered = chunk[(chunk['age'] > 30) & (chunk['income'] > 50000) & (chunk['city'] == 'New York')]
        if not chunk_filtered.empty:
            filtered_chunks.append(chunk_filtered)
    
    if filtered_chunks:
        df_filtered = pd.concat(filtered_chunks, ignore_index=True)
        filtered_rows = len(df_filtered)
    else:
        df_filtered = pd.DataFrame()
        filtered_rows = 0
    
    end_time = time.time()
    chunked_time = end_time - start_time
    chunked_memory = get_memory_usage_mb() - start_memory
    
    results["filter_during_read"] = {
        "load_time_seconds": round(chunked_time, 3),
        "memory_increase_mb": round(chunked_memory, 2),
        "filtered_rows": filtered_rows,
        "chunk_size": chunk_size
    }
    
    print(f"Processing time: {chunked_time:.3f} seconds")
    print(f"Memory increase: {chunked_memory:.2f} MB")
    print(f"Rows filtered: {filtered_rows:,}")
    
    # Performance comparison
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    comparison = {
        "time_savings": {
            "selective_vs_naive": round((naive_time - selective_time) / naive_time * 100, 1),
            "chunked_vs_naive": round((naive_time - chunked_time) / naive_time * 100, 1)
        },
        "memory_savings": {
            "selective_vs_naive": round((naive_memory - selective_memory) / naive_memory * 100, 1),
            "chunked_vs_naive": "N/A (streaming)"
        },
        "recommendations": [
            "Use `usecols` parameter to load only needed columns",
            "Filter during read when possible using chunked processing",
            "For very large files, consider Dask or PySpark"
        ]
    }
    
    results["performance_comparison"] = comparison
    
    print(f"\nTime savings (selective vs naive): {comparison['time_savings']['selective_vs_naive']}%")
    print(f"Time savings (chunked vs naive): {comparison['time_savings']['chunked_vs_naive']}%")
    print(f"Memory savings (selective vs naive): {comparison['memory_savings']['selective_vs_naive']}%")
    print("\nRecommendations:")
    for i, rec in enumerate(comparison['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Clean up test file
    if os.path.exists(test_csv):
        os.remove(test_csv)
        print(f"\nCleaned up test file: {test_csv}")
    
    return results

def exercise_4_advanced_optimization_techniques() -> Dict[str, Any]:
    """
    Exercise 4: Advanced Optimization Techniques
    
    Explore advanced Pandas optimization methods:
    1. Using Parquet/Feather formats for faster I/O
    2. Memory mapping with numpy arrays
    3. Sparse data structures
    4. Parallel processing with multiprocessing
    
    Returns:
        Dictionary with optimization results
    """
    print("\n" + "="*60)
    print("EXERCISE 4: Advanced Optimization Techniques")
    print("="*60)
    
    results = {
        "format_comparison": {},
        "sparse_optimization": {},
        "parallel_processing": {}
    }
    
    # Create test data
    np.random.seed(42)
    n_rows = 100000
    n_cols = 20
    
    print(f"Creating test data: {n_rows:,} rows × {n_cols} columns")
    
    # Create DataFrame with mixed data types
    data = {}
    for i in range(n_cols):
        if i < 5:
            # Integer columns
            data[f'int_{i}'] = np.random.randint(0, 1000, n_rows, dtype=np.int64)
        elif i < 10:
            # Float columns
            data[f'float_{i}'] = np.random.randn(n_rows).astype(np.float64)
        elif i < 15:
            # Categorical columns (low cardinality)
            data[f'cat_{i}'] = np.random.choice([f'Category_{j}' for j in range(10)], n_rows)
        else:
            # Sparse columns (mostly zeros)
            sparse_data = np.zeros(n_rows, dtype=np.float64)
            non_zero_indices = np.random.choice(n_rows, size=n_rows//10, replace=False)
            sparse_data[non_zero_indices] = np.random.randn(len(non_zero_indices))
            data[f'sparse_{i}'] = sparse_data
    
    df = pd.DataFrame(data)
    print(f"DataFrame created: {df.shape[0]:,} rows, {df.shape[1]} columns")
    
    # Part 1: File format comparison
    print("\n--- Part 1: File Format Comparison ---")
    
    formats = ['csv', 'parquet', 'feather']
    format_results = {}
    
    for fmt in formats:
        filename = f'test_data.{fmt}'
        
        # Write
        start_time = time.time()
        if fmt == 'csv':
            df.to_csv(filename, index=False)
        elif fmt == 'parquet':
            df.to_parquet(filename, compression='snappy')
        elif fmt == 'feather':
            df.to_feather(filename)
        write_time = time.time() - start_time
        
        # Get file size
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        
        # Read
        start_time = time.time()
        if fmt == 'csv':
            df_read = pd.read_csv(filename)
        elif fmt == 'parquet':
            df_read = pd.read_parquet(filename)
        elif fmt == 'feather':
            df_read = pd.read_feather(filename)
        read_time = time.time() - start_time
        
        format_results[fmt] = {
            "write_time_seconds": round(write_time, 3),
            "read_time_seconds": round(read_time, 3),
            "file_size_mb": round(file_size, 2),
            "memory_usage_mb": round(df_read.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        }
        
        print(f"\n{fmt.upper()}:")
        print(f"  Write time: {write_time:.3f}s")
        print(f"  Read time: {read_time:.3f}s")
        print(f"  File size: {file_size:.2f} MB")
        
        # Clean up
        os.remove(filename)
    
    results["format_comparison"] = format_results
    
    # Part 2: Sparse data optimization
    print("\n--- Part 2: Sparse Data Optimization ---")
    
    # Identify sparse columns (mostly zeros)
    sparse_threshold = 0.9  # 90% zeros
    sparse_cols = []
    
    for col in df.columns:
        if df[col].dtype in [np.float64, np.float32, np.int64, np.int32]:
            zero_count = (df[col] == 0).sum()
            zero_ratio = zero_count / len(df)
            if zero_ratio > sparse_threshold:
                sparse_cols.append((col, zero_ratio))
    
    print(f"Found {len(sparse_cols)} sparse columns (> {sparse_threshold*100:.0f}% zeros):")
    for col, ratio in sparse_cols[:5]:  # Show first 5
        print(f"  {col}: {ratio*100:.1f}% zeros")
    
    if len(sparse_cols) > 5:
        print(f"  ... and {len(sparse_cols) - 5} more")
    
    # Convert to sparse (for demonstration, we'll convert one column)
    if sparse_cols:
        sparse_col = sparse_cols[0][0]
        
        # Original memory
        original_memory = df[sparse_col].memory_usage(deep=True) / 1024  # KB
        
        # Convert to sparse (Pandas SparseDtype)
        df_sparse = df.copy()
        df_sparse[sparse_col] = df_sparse[sparse_col].astype(pd.SparseDtype("float64", 0))
        
        # Sparse memory
        sparse_memory = df_sparse[sparse_col].memory_usage(deep=True) / 1024
        
        savings = (original_memory - sparse_memory) / original_memory * 100
        
        results["sparse_optimization"] = {
            "sparse_column": sparse_col,
            "zero_percentage": round(sparse_cols[0][1] * 100, 1),
            "original_memory_kb": round(original_memory, 2),
            "sparse_memory_kb": round(sparse_memory, 2),
            "savings_percentage": round(savings, 2),
            "total_sparse_columns": len(sparse_cols)
        }
        
        print(f"\nSparse optimization for '{sparse_col}':")
        print(f"  Original memory: {original_memory:.2f} KB")
        print(f"  Sparse memory: {sparse_memory:.2f} KB")
        print(f"  Savings: {savings:.1f}%")
    
    # Part 3: Parallel processing demonstration
    print("\n--- Part 3: Parallel Processing Concepts ---")
    
    # Note: Actual multiprocessing implementation would be more complex
    # This is a conceptual demonstration
    
    parallel_concepts = {
        "techniques": [
            "Multiprocessing with pandas (using joblib or multiprocessing)",
            "Dask for out-of-core computations",
            "Modin for parallel pandas operations",
            "Swifter for applying functions in parallel"
        ],
        "use_cases": [
            "Apply complex function to DataFrame rows/columns",
            "Process multiple files simultaneously",
            "Cross-validation for machine learning",
            "Feature engineering on large datasets"
        ],
        "considerations": [
            "Overhead of process creation may outweigh benefits for small datasets",
            "Memory duplication across processes",
            "Global Interpreter Lock (GIL) limitations with threading",
            "I/O-bound vs CPU-bound operations"
        ]
    }
    
    results["parallel_processing"] = parallel_concepts
    
    print("\nParallel processing techniques:")
    for technique in parallel_concepts["techniques"]:
        print(f"  • {technique}")
    
    print("\nKey considerations:")
    for consideration in parallel_concepts["considerations"]:
        print(f"  • {consideration}")
    
    return results

def exercise_5_real_world_scenario() -> Dict[str, Any]:
    """
    Exercise 5: Real-World Memory Optimization Scenario
    
    Apply all learned techniques to optimize a realistic dataset:
    1. Analyze memory usage and identify optimization opportunities
    2. Apply appropriate optimizations
    3. Validate results and measure improvements
    4. Create production-ready optimization pipeline
    
    Returns:
        Dictionary with comprehensive optimization results
    """
    print("\n" + "="*60)
    print("EXERCISE 5: Real-World Memory Optimization Scenario")
    print("="*60)
    
    results = {
        "scenario_description": "E-commerce analytics pipeline optimization",
        "initial_state": {},
        "optimized_state": {},
        "improvements": {},
        "recommendations": []
    }
    
    # Scenario: E-commerce transaction data
    print("\nScenario: Optimizing e-commerce transaction data processing")
    print("Dataset: 200,000 transactions, 15 columns, mixed data types")
    
    # Create realistic e-commerce data
    np.random.seed(42)
    n_transactions = 200000
    
    print(f"\nGenerating {n_transactions:,} transaction records...")
    
    # Generate data with realistic distributions
    transaction_ids = np.arange(1000000, 1000000 + n_transactions)
    customer_ids = np.random.randint(1000, 50000, n_transactions)
    
    # Product categories with realistic distribution
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports', 'Beauty', 'Toys']
    category_probs = [0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10]
    product_categories = np.random.choice(categories, n_transactions, p=category_probs)
    
    # Prices with realistic distribution (some expensive, many cheap)
    prices = np.random.exponential(50, n_transactions) + 10
    prices = np.round(prices, 2)
    
    # Quantities (mostly 1, some bulk)
    quantities = np.random.choice([1, 1, 1, 2, 3, 4, 5, 10], n_transactions, p=[0.7, 0.7, 0.7, 0.1, 0.05, 0.03, 0.02, 0.01])
    
    # Dates (over 2 years)
    dates = pd.date_range('2022-01-01', '2023-12-31', periods=n_transactions)
    
    # Customer segments
    segments = ['Bronze', 'Silver', 'Gold', 'Platinum']
    segment_probs = [0.5, 0.3, 0.15, 0.05]
    customer_segments = np.random.choice(segments, n_transactions, p=segment_probs)
    
    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay']
    payment_probs = [0.4, 0.3, 0.15, 0.1, 0.05]
    payment_types = np.random.choice(payment_methods, n_transactions, p=payment_probs)
    
    # Create DataFrame
    data = {
        'transaction_id': transaction_ids.astype(np.int64),
        'customer_id': customer_ids.astype(np.int64),
        'product_category': product_categories,
        'price': prices.astype(np.float64),
        'quantity': quantities.astype(np.int64),
        'total_amount': (prices * quantities).astype(np.float64),
        'transaction_date': dates,
        'customer_segment': customer_segments,
        'payment_method': payment_types,
        'discount_applied': np.random.choice([True, False], n_transactions, p=[0.3, 0.7]),
        'returned': np.random.choice([True, False], n_transactions, p=[0.05, 0.95]),
        'review_score': np.random.randint(1, 6, n_transactions),
        'shipping_cost': np.random.uniform(0, 20, n_transactions).astype(np.float64),
        'tax_amount': np.random.uniform(0, 50, n_transactions).astype(np.float64),
        'processing_fee': np.random.uniform(0, 5, n_transactions).astype(np.float64)
    }
    
    df = pd.DataFrame(data)
    
    # Initial state analysis
    print("\n--- Initial State Analysis ---")
    initial_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
    initial_dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    results["initial_state"] = {
        "dataframe_shape": df.shape,
        "memory_mb": round(initial_memory, 2),
        "data_types": initial_dtypes,
        "column_count": len(df.columns)
    }
    
    print(f"DataFrame shape: {df.shape}")
    print(f"Initial memory: {initial_memory:.2f} MB")
    print("\nMemory by column (top 10):")
    mem_by_col = df.memory_usage(deep=True).sort_values(ascending=False) / 1024  # KB
    for col, mem in mem_by_col.head(10).items():
        print(f"  {col}: {mem:.2f} KB")
    
    # Optimization pipeline
    print("\n--- Applying Optimizations ---")
    optimizations_applied = []
    
    # 1. Downcast numeric columns
    print("\n1. Downcasting numeric columns...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        original_dtype = str(df[col].dtype