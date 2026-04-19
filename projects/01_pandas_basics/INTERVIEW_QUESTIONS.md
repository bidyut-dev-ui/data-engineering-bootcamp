# Pandas Basics: Interview Questions & Answers

## 📋 Table of Contents
1. [Fundamental Concepts](#fundamental-concepts)
2. [Data Loading & Inspection](#data-loading--inspection)
3. [Data Cleaning & Transformation](#data-cleaning--transformation)
4. [Aggregation & GroupBy](#aggregation--groupby)
5. [Memory Optimization](#memory-optimization)
6. [Performance & Efficiency](#performance--efficiency)
7. [File Formats & I/O](#file-formats--io)
8. [Real-World Scenarios](#real-world-scenarios)
9. [8GB RAM Specific Questions](#8gb-ram-specific-questions)
10. [Interview Preparation Tips](#interview-preparation-tips)

---

## 🎯 Fundamental Concepts

### 1. **What is Pandas and why is it essential for data engineering?**
**Answer**: Pandas is a Python library providing high-performance, easy-to-use data structures (DataFrame, Series) and data analysis tools. It's essential for data engineering because:
- **Data Manipulation**: Efficiently clean, transform, and reshape data
- **Integration**: Works seamlessly with SQL databases, CSV, JSON, Parquet, etc.
- **Performance**: Built on NumPy with C optimizations for speed
- **Memory Efficiency**: Offers tools for handling large datasets (chunking, dtype optimization)
- **ETL Pipelines**: Foundation for Extract, Transform, Load processes

**Example**: A data engineer uses Pandas to clean customer data before loading into a data warehouse.

### 2. **Explain the difference between Series and DataFrame**
**Answer**:
- **Series**: 1-dimensional labeled array capable of holding any data type
- **DataFrame**: 2-dimensional labeled data structure with columns of potentially different types

```python
# Series example
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# DataFrame example
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z']
})
```

**Key Difference**: Series is a single column, DataFrame is a collection of Series (multiple columns).

### 3. **What are the main data structures in Pandas and when would you use each?**
**Answer**:
1. **Series**: Single column of data with index. Use for time series, single metrics.
2. **DataFrame**: Tabular data with rows and columns. Use for most data manipulation.
3. **Panel** (deprecated): 3D data structure. Use `MultiIndex` DataFrames instead.
4. **Index**: Immutable array implementing ordered, sliceable set.

```python
# Series: Temperature readings over time
temps = pd.Series([72, 75, 68], index=pd.date_range('2024-01-01', periods=3))

# DataFrame: Sales data
sales_df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=3),
    'product': ['A', 'B', 'A'],
    'sales': [100, 150, 200]
})
```

### 4. **How does Pandas handle missing data?**
**Answer**: Pandas uses `NaN` (Not a Number) for missing numeric data and `None` for missing object data. Key methods:
- **Detection**: `isna()`, `notna()`, `isnull()`, `notnull()`
- **Handling**: `dropna()`, `fillna()`, `interpolate()`
- **Statistics**: `mean()`, `sum()` etc. skip NaN by default

```python
df = pd.DataFrame({'A': [1, 2, None], 'B': [4, None, 6]})

# Detect missing
print(df.isna())

# Fill missing with mean
df_filled = df.fillna(df.mean())

# Drop rows with any missing values
df_dropped = df.dropna()
```

### 5. **Explain the difference between `.loc[]` and `.iloc[]`**
**Answer**:
- **`.loc[]`**: Label-based indexing using row/column names
- **`.iloc[]`**: Integer position-based indexing

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['x', 'y', 'z'])

# .loc - uses labels
df.loc['x', 'A']  # Returns 1
df.loc[['x', 'y'], 'A']  # Returns rows x and y from column A

# .iloc - uses positions
df.iloc[0, 0]  # Returns 1 (first row, first column)
df.iloc[0:2, 0]  # Returns first two rows from first column
```

---

## 📊 Data Loading & Inspection

### 6. **How do you efficiently load a large CSV file with 8GB RAM constraints?**
**Answer**: Use these techniques:
1. **Specify dtypes**: Prevent Pandas from guessing types
2. **Use `usecols`**: Load only needed columns
3. **Chunk processing**: Process in batches
4. **Low memory mode**: Let Pandas handle memory

```python
# Method 1: Specify dtypes and columns
dtype_spec = {
    'id': 'int32',
    'amount': 'float32',
    'category': 'category'
}
df = pd.read_csv('large.csv', dtype=dtype_spec, usecols=['id', 'amount', 'category'])

# Method 2: Chunk processing
chunks = []
for chunk in pd.read_csv('large.csv', chunksize=10000):
    processed = clean_chunk(chunk)
    chunks.append(processed)
df = pd.concat(chunks)
```

### 7. **What methods would you use to inspect a DataFrame's structure and content?**
**Answer**:
```python
# Basic inspection
df.head()          # First 5 rows
df.tail()          # Last 5 rows
df.shape           # (rows, columns)
df.columns         # Column names
df.dtypes          # Data types per column
df.info()          # Concise summary

# Statistical inspection
df.describe()      # Summary statistics for numeric columns
df.describe(include='all')  # Includes categorical

# Memory usage
df.memory_usage(deep=True)  # Detailed memory usage

# Missing values
df.isna().sum()    # Count missing per column
df.isna().mean()   # Percentage missing
```

### 8. **How do you check for duplicate rows and handle them?**
**Answer**:
```python
# Check for duplicates
duplicates = df.duplicated()  # Boolean Series
duplicate_count = df.duplicated().sum()

# Show duplicate rows
df[df.duplicated(keep=False)]  # keep=False marks all duplicates

# Remove duplicates
df_deduped = df.drop_duplicates()

# Remove duplicates based on specific columns
df_deduped = df.drop_duplicates(subset=['email', 'date'])

# Keep first/last occurrence
df_keep_first = df.drop_duplicates(keep='first')
df_keep_last = df.drop_duplicates(keep='last')
```

### 9. **What's the difference between `df.info()` and `df.describe()`?**
**Answer**:
- **`df.info()`**: Shows DataFrame structure - dtypes, non-null counts, memory usage
- **`df.describe()`**: Shows statistical summary - count, mean, std, min, percentiles, max

```python
# info() output:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 1000 entries, 0 to 999
# Data columns (total 5 columns):
#  #   Column  Non-Null Count  Dtype  
# ---  ------  --------------  -----  
#  0   A       1000 non-null   int64  
#  1   B       950 non-null    float64
# Memory usage: 39.2 KB

# describe() output:
#               A           B
# count  1000.000000  950.000000
# mean     50.123000   25.456000
# std      15.789000    5.123000
# min      10.000000   15.000000
# 25%      40.000000   22.000000
# 50%      50.000000   25.000000
# 75%      60.000000   28.000000
# max      90.000000   35.000000
```

---

## 🧹 Data Cleaning & Transformation

### 10. **How do you handle missing values in a dataset?**
**Answer**: Choose strategy based on data and context:
1. **Remove**: `df.dropna()` - when missing data is minimal
2. **Fill with constant**: `df.fillna(value)` - for categorical data
3. **Fill with statistic**: `df.fillna(df.mean())` - for numeric data
4. **Forward/backward fill**: `df.fillna(method='ffill')` - time series
5. **Interpolation**: `df.interpolate()` - for ordered data

```python
# Different strategies
df_filled_mean = df.fillna(df.mean())  # Numeric columns
df_filled_mode = df.fillna(df.mode().iloc[0])  # Categorical
df_filled_forward = df.fillna(method='ffill')  # Time series
df_dropped = df.dropna(thresh=0.8*len(df.columns))  # Keep rows with ≥80% data
```

### 11. **How would you normalize/standardize a column?**
**Answer**: Normalization scales to [0,1], standardization scales to mean=0, std=1.

```python
# Min-Max Normalization (0 to 1)
df['normalized'] = (df['column'] - df['column'].min()) / (df['column'].max() - df['column'].min())

# Z-score Standardization (mean=0, std=1)
df['standardized'] = (df['column'] - df['column'].mean()) / df['column'].std()

# Using scikit-learn
from sklearn.preprocessing import MinMaxScaler, StandardScaler
scaler = MinMaxScaler()
df[['normalized']] = scaler.fit_transform(df[['column']])
```

### 12. **Explain how to handle categorical variables in Pandas**
**Answer**:
1. **Label Encoding**: Convert to numeric codes
2. **One-Hot Encoding**: Create binary columns
3. **Ordinal Encoding**: For ordered categories
4. **Target Encoding**: Encode by target mean

```python
# Label Encoding
df['category_code'] = df['category'].astype('category').cat.codes

# One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['category'], prefix='cat')

# Ordinal Encoding with mapping
size_map = {'S': 1, 'M': 2, 'L': 3, 'XL': 4}
df['size_code'] = df['size'].map(size_map)
```

### 13. **How do you merge/join DataFrames?**
**Answer**: Use `merge()` or `join()`:
- **`merge()`**: More flexible, SQL-like joins
- **`join()`**: Convenience method for index-based joins

```python
# Inner join (default)
result = pd.merge(df1, df2, on='key')

# Left join
result = pd.merge(df1, df2, on='key', how='left')

# Right join  
result = pd.merge(df1, df2, on='key', how='right')

# Outer join
result = pd.merge(df1, df2, on='key', how='outer')

# Join on index
result = df1.join(df2, how='inner')
```

### 14. **What's the difference between `apply()`, `map()`, and `applymap()`?**
**Answer**:
- **`apply()`**: Apply function along axis (rows or columns)
- **`map()`**: Element-wise transformation for Series
- **`applymap()`**: Element-wise transformation for DataFrame

```python
# apply() - column-wise or row-wise
df['length'] = df['text'].apply(len)  # Apply to Series
df_mean = df.apply(np.mean, axis=0)   # Apply to each column

# map() - Series only (element-wise)
df['category_code'] = df['category'].map({'A': 1, 'B': 2, 'C': 3})

# applymap() - DataFrame element-wise
df_log = df.applymap(np.log)  # Apply log to every element
```

---

## 📈 Aggregation & GroupBy

### 15. **Explain the GroupBy operation in Pandas**
**Answer**: `groupby()` splits data into groups, applies function, combines results.

```python
# Basic groupby
grouped = df.groupby('category')

# Multiple aggregations
result = df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'sum'
})

# Named aggregations (Pandas 0.25+)
result = df.groupby('category').agg(
    total_sales=('sales', 'sum'),
    avg_price=('price', 'mean'),
    count=('id', 'count')
)
```

### 16. **How do you handle multi-level indexes (MultiIndex)?**
**Answer**: MultiIndex allows hierarchical indexing.

```python
# Create MultiIndex
df = df.set_index(['year', 'month', 'day'])

# Access data
df.loc[2023]  # All 2023 data
df.loc[(2023, 12)]  # December 2023
df.loc[(2023, 12, 25)]  # Christmas 2023

# Reset index
df_reset = df.reset_index()

# Flatten column MultiIndex
df.columns = ['_'.join(col).strip() for col in df.columns.values]
```

### 17. **What are pivot tables and when would you use them?**
**Answer**: Pivot tables summarize data by grouping and aggregating.

```python
# Simple pivot table
pivot = pd.pivot_table(df, 
                       values='sales', 
                       index='region', 
                       columns='product', 
                       aggfunc='sum',
                       fill_value=0)

# Multiple aggregations
pivot = pd.pivot_table(df,
                       values=['sales', 'profit'],
                       index='region',
                       columns='month',
                       aggfunc={'sales': 'sum', 'profit': 'mean'},
                       margins=True)  # Add totals
```

### 18. **How do you calculate rolling statistics?**
**Answer**: Use `.rolling()` for moving windows.

```python
# 7-day moving average
df['7d_avg'] = df['sales'].rolling(window=7).mean()

# 30-day rolling sum with minimum 5 observations
df['30d_sum'] = df['sales'].rolling(window=30, min_periods=5).sum()

# Expanding window (cumulative)
df['cumulative'] = df['sales'].expanding().sum()

# Custom aggregation
def custom_agg(x):
    return (x.max() - x.min()) / x.mean()

df['range_mean_ratio'] = df['sales'].rolling(10).apply(custom_agg)
```

---

## 💾 Memory Optimization

### 19. **How do you reduce memory usage of a DataFrame?**
**Answer**:
1. **Downcast numeric types**: `int64` → `int32` or `int8`
2. **Use categorical for strings**: Low-cardinality columns
3. **Use `string` dtype**: Python 3.7+ for text
4. **Load only needed columns**: `usecols` parameter
5. **Process in chunks**: For very large files

```python
def optimize_memory(df):
    """Optimize DataFrame memory usage."""
    # Downcast integers
    int_cols = df.select_dtypes(include=['int']).columns
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    # Downcast floats
    float_cols = df.select_dtypes(include=['float']).columns
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    # Convert to categorical
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # < 50% unique
            df[col] = df[col].astype('category')
    
    return df
```

### 20. **What's the memory difference between `object` and `category` dtypes?**
**Answer**: 
- **`object`**: Stores Python objects (strings) with overhead for each element
- **`category`**: Stores unique values once, references them (like factor in R)

```python
import pandas as pd
import numpy as np

# Create sample data
n = 1000000
categories = ['A', 'B', 'C', 'D']
df = pd.DataFrame({
    'object_col': np.random.choice(categories, n),
    'category_col': pd.Categorical(np.random.choice(categories, n))
})

# Compare memory
print(f"Object dtype: {df['object_col'].memory_usage(deep=True) / 1024**2:.2f} MB")
print(f"Category dtype: {df['category_col'].memory_usage(deep=True) / 1024**2:.2f} MB")
# Output: Object: ~8MB, Category: ~1MB (80%+ savings)
```

### 21. **How do you process data that doesn't fit in memory?**
**Answer**: Chunk processing with Dask or manual chunking.

```python
# Manual chunking
def process_large_file(filepath, chunk_size=10000):
    results = []
    
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Process chunk
        chunk_processed = clean_data(chunk)
        
        # Aggregate or save chunk
        results.append(aggregate_chunk(chunk_processed))
        
        # Clear memory
        del chunk_processed
        
    return combine_results(results)

# Using Dask (out-of-core computation)
import dask.dataframe as dd
ddf = dd.read_csv('large.csv')
result = ddf.groupby('category').sales.mean().compute()
```

### 22. **What are the memory implications of different operations?**
**Answer**:
- **`.copy()`**: Creates full copy (2x memory)
- **`.loc[]` vs `[]`**: `.loc` is more memory efficient
- **Chained operations**: Create intermediate copies
- **`.astype()`**: Creates copy unless `inplace=True`
- **`.groupby()`**: Can create large intermediate structures

**Memory-Safe Pattern**:
```python
# ❌ Bad: Multiple intermediate copies
df1 = df[df['sales'] > 100]
df2 = df1.dropna()
df3 = df2.groupby('region').sum()

# ✅ Good: Method chaining
result = (df[df['sales'] > 100]
          .dropna()
          .groupby('region')
          .sum())
```

---

## ⚡ Performance & Efficiency

### 23. **Why is vectorization faster than iteration?**
**Answer**: Vectorization uses NumPy's C-based operations (single instruction, multiple data) vs Python's interpreted loop.

```python
import numpy as np
import pandas as pd

# ❌ Slow: Python loop
def slow_multiply(df):
    result = []
    for i in range(len(df)):
        result.append(df['A'].iloc[i] * df['B'].iloc[i])
    return result

# ✅ Fast: Vectorized
def fast_multiply(df):
    return df['A'] * df['B']

# Benchmark (10x-100x faster for vectorized)
```

### 24. **When should you use `.eval()` or `.query()`?**
**Answer**: For complex expressions on large DataFrames.

```python
# .query() for filtering
df_filtered = df.query('sales > 1000 and region == "North"')

# .eval() for complex calculations
df['result'] = df.eval('(sales - cost) / sales * 100')

# Benefits:
# 1. More readable
# 2. Can be faster for large DataFrames
# 3. Avoids intermediate variables
```

### 25. **How do you optimize Pandas for speed?**
**Answer**:
1. **Use vectorized operations**: Avoid loops
2. **Use `.loc[]`/`.iloc[]`**: Avoid chained indexing
3. **Use `.at[]`/`.iat[]`**: For scalar access
4. **Pre-allocate memory**: When building DataFrames
5. **Use NumPy for math**: `np.sqrt()` vs `df['col'] ** 0.5`

```python
# Pre-allocation for speed
n = 1000000
result = pd.DataFrame(index=range(n), columns=['A', 'B'])
result['A'] = np.random.randn(n)
result['B'] = result['A'] * 2  # Vectorized

# Use .at for single cell access
result.at[500, 'A'] = 999  # Faster than result.loc[500, 'A'] = 999
```

---

## 📁 File Formats & I/O

### 26. **Compare CSV, Parquet, and Feather formats**
**Answer**:

| Format | Pros | Cons | Best For |
|--------|------|------|----------|
| **CSV** | Human-readable, universal | No schema, slow, large files | Data exchange, small datasets |
| **Parquet** | Columnar, compressed, schema | Requires library, slower write | Analytics, large datasets |
| **Feather** | Very fast I/O, preserves dtypes | Larger files than Parquet | Intermediate storage, Python-only |

```python
# Benchmark different formats
import time

def benchmark_formats(df):
    results = {}
    
    # CSV
    start = time.time()
    df.to_csv('test.csv', index=False)
    results['csv_write'] = time.time() - start
    
    # Parquet
    start = time.time()
    df.to_parquet('test.parquet', index=False)
    results['parquet_write'] = time.time() - start
    
    # Feather
    start = time.time()
    df.to_feather('test.feather')
    results['feather_write'] = time.time() - start
    
    return results
```

### 27. **How do you handle different character encodings?**
**Answer**: Use `encoding` parameter and handle errors.

```python
# Try different encodings
encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        df = pd.read_csv('file.csv', encoding=encoding)
        print(f"Success with {encoding}")
        break
    except UnicodeDecodeError:
        continue

# Read with error handling
df = pd.read_csv('file.csv', encoding='utf-8', errors='replace')  # Replace errors
df = pd.read_csv('file.csv', encoding='utf-8', errors='ignore')   # Ignore errors
```

### 28. **What are the best practices for reading/writing large files?**
**Answer**:
1. **Specify dtypes**: Avoid type inference
2. **Use chunks**: For processing
3. **Compress**: Use gzip/snappy
4. **Parallel I/O**: Use `swifter` or `dask`
5. **Memory mapping**: For very large files

```python
# Read with compression
df = pd.read_csv('data.csv.gz', compression='gzip')

# Write with compression
df.to_parquet('data.parquet', compression='snappy')

# Parallel processing with swifter
import swifter
df['new'] = df['col'].swifter.apply(lambda x: x*2)
```

---

## 🌐 Real-World Scenarios

### 29. **How would you build an ETL pipeline with Pandas?**
**Answer**:
```python
def etl_pipeline(input_file, output_file):
    """Complete ETL pipeline with error handling."""
    
    # Extract
    try:
        df = pd.read_csv(input_file, 
                        dtype={'id': 'int32', 'amount': 'float32'},
                        parse_dates=['date'],
                        low_memory=False)
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        return
    
    # Transform
    df_clean = (df
                .dropna(subset=['critical_column'])
                .pipe(standardize_column_names)
                .pipe(handle_missing_values)
                .pipe(optimize_dtypes)
                .assign(total_sales=lambda x: x['quantity'] * x['price'])
                .query('total_sales > 0'))
    
    # Load
    df_clean.to_parquet(output_file, index=False, compression='snappy')
    
    # Logging
    print(f"Processed {len(df)} rows, saved {len(df_clean)} rows")
    print(f"Memory saved: {df.memory_usage().sum() - df_clean.memory_usage().sum()} bytes")
    
    return df_clean
```

### 30. **How do you handle time series data in Pandas?**
**Answer**:
```python
# Set datetime index
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')

# Resampling
df_daily = df.resample('D').mean()  # Daily average
df_hourly = df.resample('H').sum()  # Hourly sum

# Rolling windows
df['7d_avg'] = df['value'].rolling('7D').mean()  # 7-day rolling average

# Time-based indexing
df.loc['2024-01']  # January 2024
df.loc['2024-01-01':'2024-01-07']  # First week

# Shift for lag/lead
df['lag_1'] = df['value'].shift(1)  # Previous value
df['lead_1'] = df['value'].shift(-1)  # Next value
```

### 31. **How would you detect and handle outliers?**
**Answer**:
```python
def detect_outliers_iqr(df, column):
    """Detect outliers using IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

def handle_outliers(df, column, method='cap'):
    """Handle outliers using different methods."""
    if method == 'cap':
        # Cap at bounds
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        df[column] = df[column].clip(lower, upper)
        
    elif method == 'remove':
        # Remove outliers
        df = df[~detect_outliers_iqr(df, column).index]
        
    elif method == 'transform':
        # Log transform
        df[column] = np.log1p(df[column])
        
    return df
```

---

## 💻 8GB RAM Specific Questions

### 32. **What's your strategy for working with datasets larger than available RAM?**
**Answer**:
1. **Chunk processing**: Read/process in manageable pieces
2. **Filter early**: Remove unnecessary data ASAP
3. **Aggregate incrementally**: Maintain running totals
4. **Use disk**: Store intermediate results
5. **Consider alternatives**: Dask, Vaex, or database

```python
def process_oversized_file(filepath, output_path):
    """Process file larger than RAM."""
    # First pass: Get schema and sample
    sample = pd.read_csv(filepath, nrows=1000)
    
    # Determine dtypes from sample
    dtype_dict = {}
    for col in sample.columns:
        if sample[col].dtype == 'object':
            # Check if categorical
            if sample[col].nunique() / len(sample) < 0.5:
                dtype_dict[col] = 'category'
        elif 'int' in str(sample[col].dtype):
            dtype_dict[col] = 'int32'
        elif 'float' in str(sample[col].dtype):
            dtype_dict[col] = 'float32'
    
    # Process in chunks
    chunks = []
    for chunk in pd.read_csv(filepath, dtype=dtype_dict, chunksize=10000):
        # Process and aggregate
        aggregated = chunk.groupby('key_column').agg({'value': 'sum'})
        chunks.append(aggregated)
    
    # Combine results
    result = pd.concat(chunks).groupby(level=0).sum()
    result.to_csv(output_path)
```

### 33. **How do you monitor memory usage during Pandas operations?**
**Answer**:
```python
import psutil
import pandas as pd

def monitor_memory(operation_name):
    """Decorator to monitor memory usage."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            process = psutil.Process()
            before = process.memory_info().rss / 1024**2  # MB
            
            result = func(*args, **kwargs)
            
            after = process.memory_info().rss / 1024**2
            print(f"{operation_name}: {after - before:.2f} MB delta")
            
            return result
        return wrapper
    return decorator

@monitor_memory("Data cleaning")
def clean_data(df):
    return df.dropna().reset_index(drop=True)

# Usage
df = pd.read_csv('data.csv')
df_clean = clean_data(df)
```

### 34. **What are the signs of memory issues and how do you debug them?**
**Answer**:
**Signs**:
- Slow performance, swapping to disk
- `MemoryError` exceptions
- System becomes unresponsive
- High memory usage in task manager

**Debugging**:
```python
import pandas as pd
import sys

def debug_memory(df, label=""):
    """Debug memory usage of DataFrame."""
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"{label}: {memory_mb:.2f} MB")
    
    # Per column breakdown
    for col in df.columns:
        col_memory = df[col].memory_usage(deep=True) / 1024**2
        print(f"  {col}: {col_memory:.2f} MB ({df[col].dtype})")
    
    # Check for object dtypes (memory hogs)
    object_cols = df.select_dtypes(include=['object']).columns
    if len(object_cols) > 0:
        print(f"Warning: {len(object_cols)} object columns detected")
        for col in object_cols:
            unique_ratio = df[col].nunique() / len(df)
            print(f"  {col}: {unique_ratio:.1%} unique - consider 'category' dtype")
```

### 35. **How do you choose optimal chunk size for processing?**
**Answer**: Balance between memory usage and I/O overhead.

```python
def find_optimal_chunksize(filepath, available_mb=2000):
    """Find optimal chunk size based on available memory."""
    # Get file size
    file_size_mb = os.path.getsize(filepath) / 1024**2
    
    # Read first chunk to estimate row size
    sample = pd.read_csv(filepath, nrows=1000)
    sample_mb = sample.memory_usage(deep=True).sum() / 1024**2
    row_size_kb = (sample_mb * 1024) / 1000  # KB per row
    
    # Calculate optimal chunk size
    target_chunk_mb = available_mb * 0.5  # Use 50% of available
    optimal_rows = int((target_chunk_mb * 1024) / row_size_kb)
    
    # Round to nearest 1000
    optimal_rows = (optimal_rows // 1000) * 1000
    
    print(f"File: {file_size_mb:.1f} MB")
    print(f"Row size: {row_size_kb:.2f} KB")
    print(f"Optimal chunk: {optimal_rows:,} rows (~{optimal_rows * row_size_kb / 1024:.1f} MB)")
    
    return max(1000, min(optimal_rows, 100000))  # Between 1k and 100k
```

---

## 🎯 Interview Preparation Tips

### 36. **Common Pandas Interview Questions**
1. "How would you merge two DataFrames with different column names?"
2. "Explain the difference between `merge()` and `concat()`"
3. "How do you handle datetime operations in Pandas?"
4. "What's the most memory-efficient way to read a 10GB CSV?"
5. "How would you calculate month-over-month growth?"
6. "Explain how `groupby()` works internally"
7. "How do you handle timezone-aware datetime objects?"
8. "What's the difference between `pivot()` and `pivot_table()`?"

### 37. **Performance Optimization Questions**
1. "Why is `.iloc[]` faster than `.loc[]` for integer indexing?"
2. "When should you use `.eval()` vs regular operations?"
3. "How does Pandas handle missing values in groupby operations?"
4. "What's the memory overhead of a DataFrame index?"
5. "How do you parallelize Pandas operations?"

### 38. **Real-World Scenario Questions**
1. "You have a 20GB CSV file and 8GB RAM. How do you process it?"
2. "How would you build a data validation pipeline with Pandas?"
3. "What's your approach to handling schema evolution?"
4. "How do you ensure data quality in an ETL pipeline?"
5. "Describe how you'd monitor and alert on data pipeline issues"

### 39. **Code Review Questions**
```python
# Question: What's wrong with this code?
def process_data(df):
    result = []
    for i in range(len(df)):
        row = df.iloc[i]
        if row['sales'] > 1000:
            result.append(row['profit'] * 1.1)
        else:
            result.append(row['profit'])
    df['adjusted_profit'] = result
    return df

# Answer: Uses slow row-wise iteration. Should use vectorized operations:
def process_data_fixed(df):
    df['adjusted_profit'] = df['profit'] * np.where(df['sales'] > 1000, 1.1, 1.0)
    return df
```

### 40. **System Design Questions**
1. "Design a system to process 100GB of daily sales data with Pandas"
2. "How would you architect a data pipeline that handles schema changes?"
3. "What monitoring would you implement for a production Pandas pipeline?"
4. "How do you handle backfills or reprocessing of historical data?"

---

## 📚 Resources for Further Study

### Books
1. **"Python for Data Analysis"** by Wes McKinney (Pandas creator)
2. **"Pandas Cookbook"** by Theodore Petrou
3. **"Data Science