# Pandas Basics: Gotchas & Best Practices for Data Engineering

## 🚨 Common Gotchas in Pandas

### 1. **Memory Bloat with Object dtypes**
**Problem**: Pandas defaults to `object` dtype for strings, which uses significantly more memory than categorical or string dtypes.

```python
# ❌ Bad: Default object dtype
df = pd.read_csv('large_file.csv')  # All strings become object dtype

# ✅ Good: Specify dtypes or use categorical
df = pd.read_csv('large_file.csv', dtype={'category_column': 'category'})
df['text_column'] = df['text_column'].astype('string')  # Python 3.7+
```

**Impact on 8GB RAM**: A 1GB CSV with object dtypes can consume 3-4GB in memory.

### 2. **SettingWithCopyWarning**
**Problem**: Modifying a slice of DataFrame without proper copy handling.

```python
# ❌ Bad: Causes SettingWithCopyWarning
filtered = df[df['sales'] > 1000]
filtered['discount'] = 0.1  # Warning! May not modify original df

# ✅ Good: Use .copy() or .loc[]
filtered = df[df['sales'] > 1000].copy()
filtered['discount'] = 0.1

# OR use .loc on original
df.loc[df['sales'] > 1000, 'discount'] = 0.1
```

### 3. **In-Place vs Copy Operations**
**Problem**: Some operations return copies, others modify in-place.

```python
# ❌ Confusing: Some methods return new DataFrame
df = df.dropna()  # Returns new DataFrame
df.dropna(inplace=True)  # Modifies in-place

# ✅ Consistent: Prefer method chaining with returns
df = (df
      .dropna()
      .reset_index(drop=True)
      .astype({'column': 'int32'}))
```

### 4. **NaN vs None Confusion**
**Problem**: Pandas uses `np.nan` for missing numeric values, `None` for objects, but they behave differently.

```python
# ❌ Inconsistent checking
df['column'].isnull()  # Checks both NaN and None
df['column'] == np.nan  # Always False! Use .isna()

# ✅ Consistent approach
missing = df['column'].isna()
df['column'].fillna(0, inplace=True)  # For numeric
df['column'].fillna('Unknown', inplace=True)  # For strings
```

### 5. **Date Parsing Performance**
**Problem**: Automatic date parsing is slow and memory-intensive.

```python
# ❌ Bad: Automatic parsing
df = pd.read_csv('data.csv', parse_dates=['date_column'])  # Slow for large files

# ✅ Good: Load as string, convert selectively
df = pd.read_csv('data.csv', dtype={'date_column': 'str'})
df['date_column'] = pd.to_datetime(df['date_column'], format='%Y-%m-%d', errors='coerce')
```

### 6. **GroupBy Memory Explosion**
**Problem**: GroupBy operations can create intermediate DataFrames that consume excessive memory.

```python
# ❌ Bad: Creating multiple grouped objects
grouped = df.groupby('category')
mean = grouped.mean()
sum = grouped.sum()  # Recomputes grouping

# ✅ Good: Use agg() for multiple aggregations
result = df.groupby('category').agg({
    'sales': ['mean', 'sum', 'count'],
    'profit': 'sum'
})
```

### 7. **Chained Indexing Performance**
**Problem**: Multiple bracket indexing causes repeated operations.

```python
# ❌ Bad: Chained indexing
df[df['category'] == 'A']['sales'].mean()  # Creates intermediate DataFrame

# ✅ Good: Single .loc access
df.loc[df['category'] == 'A', 'sales'].mean()
```

### 8. **Iterating Over Rows**
**Problem**: `df.iterrows()` and `df.apply()` are slow for large datasets.

```python
# ❌ Bad: Row-wise iteration
for index, row in df.iterrows():
    process(row)  # Very slow!

# ✅ Good: Vectorized operations or numpy
df['new_column'] = df['column1'] * df['column2']  # Vectorized
result = np.where(df['value'] > threshold, 'High', 'Low')  # NumPy
```

### 9. **Memory Leak with Large Operations**
**Problem**: Intermediate results aren't garbage collected.

```python
# ❌ Bad: Creating many intermediate DataFrames
df1 = df[['col1', 'col2']]
df2 = df1.dropna()
df3 = df2.groupby('col1').sum()
# All three DataFrames stay in memory

# ✅ Good: Use method chaining and del
result = (df[['col1', 'col2']]
          .dropna()
          .groupby('col1')
          .sum())
del df  # Explicitly free memory if needed
```

### 10. **File Format Misunderstandings**
**Problem**: Different file formats have different memory characteristics.

```python
# CSV: Easy but slow, no schema preservation
# Parquet: Columnar, compressed, preserves dtypes (best for analytics)
# Feather: Fast I/O, preserves dtypes (best for intermediate storage)
# Pickle: Python-specific, fast but not portable

# ✅ Choose based on use case:
# - ETL pipeline: Parquet for storage, Feather for intermediate
# - Data sharing: CSV for compatibility
# - Python-only: Pickle for speed
```

## ✅ Best Practices for 8GB RAM Systems

### 1. **Memory Optimization Techniques**

#### Downcast Numeric Columns
```python
def optimize_numeric_dtypes(df):
    """Downcast numeric columns to smallest possible dtype."""
    for col in df.select_dtypes(include=['int', 'float']).columns:
        col_type = df[col].dtype
        
        if col_type == 'int64':
            # Downcast to smallest int
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif col_type == 'float64':
            # Downcast to float32
            df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df
```

#### Convert to Categorical
```python
def optimize_categorical(df, threshold=0.5):
    """Convert low-cardinality object columns to categorical."""
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < threshold:
            df[col] = df[col].astype('category')
    
    return df
```

#### Monitor Memory Usage
```python
def get_memory_usage(df):
    """Get detailed memory usage of DataFrame."""
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"DataFrame memory usage: {memory_mb:.2f} MB")
    
    # Per column breakdown
    for col in df.columns:
        col_memory = df[col].memory_usage(deep=True) / 1024**2
        dtype = df[col].dtype
        print(f"  {col}: {col_memory:.2f} MB ({dtype})")
    
    return memory_mb
```

### 2. **Efficient Data Loading**

#### Read Only Needed Columns
```python
# Read specific columns to save memory
columns_needed = ['id', 'date', 'sales', 'region']
df = pd.read_csv('large_file.csv', usecols=columns_needed)

# Specify dtypes upfront
dtype_spec = {
    'id': 'int32',
    'sales': 'float32',
    'region': 'category'
}
df = pd.read_csv('large_file.csv', dtype=dtype_spec, usecols=columns_needed)
```

#### Chunk Processing for Very Large Files
```python
def process_large_file(filepath, chunksize=10000):
    """Process CSV in chunks to avoid memory overflow."""
    results = []
    
    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        # Process each chunk
        chunk_processed = clean_chunk(chunk)
        results.append(chunk_processed)
    
    # Combine results
    return pd.concat(results, ignore_index=True)
```

### 3. **Cleaning Pipeline Optimization**

#### Batch Cleaning Operations
```python
def efficient_cleaning_pipeline(df):
    """Apply cleaning operations in optimal order."""
    # 1. Remove unnecessary columns first
    df = df[['essential_col1', 'essential_col2', 'essential_col3']]
    
    # 2. Filter rows early (reduces data volume)
    df = df[df['quality_score'] > 0.7]
    
    # 3. Handle missing values
    df = df.dropna(subset=['critical_column'])
    df = df.fillna({'optional_column': 'default'})
    
    # 4. Type conversions with optimization
    df = optimize_numeric_dtypes(df)
    df = optimize_categorical(df)
    
    # 5. Final transformations
    df['calculated'] = df['col1'] * df['col2']  # Vectorized
    
    return df
```

### 4. **Aggregation Strategies**

#### Use Efficient Aggregation Methods
```python
# ❌ Inefficient: Multiple groupby calls
sales_by_region = df.groupby('region')['sales'].sum()
count_by_region = df.groupby('region')['sales'].count()

# ✅ Efficient: Single agg call
summary = df.groupby('region').agg({
    'sales': ['sum', 'count', 'mean'],
    'profit': 'sum'
}).round(2)

# Flatten multi-index columns
summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
```

#### Window Functions vs GroupBy
```python
# For rolling calculations, use window functions
df['rolling_avg'] = df.groupby('category')['sales'].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)
```

### 5. **File I/O Optimization**

#### Choose Optimal File Format
```python
import time

def benchmark_formats(df):
    """Benchmark different file formats."""
    formats = {
        'csv': lambda: df.to_csv('test.csv', index=False),
        'parquet': lambda: df.to_parquet('test.parquet', index=False),
        'feather': lambda: df.to_feather('test.feather')
    }
    
    results = {}
    for name, save_func in formats.items():
        start = time.time()
        save_func()
        write_time = time.time() - start
        
        # Get file size
        size_mb = os.path.getsize(f'test.{name}') / 1024**2
        
        results[name] = {
            'write_time': write_time,
            'size_mb': size_mb
        }
    
    return results
```

#### Compression for Storage
```python
# Parquet with compression
df.to_parquet('data.parquet', compression='snappy')  # Fast compression
df.to_parquet('data.parquet', compression='gzip')    # Better compression, slower

# CSV with compression
df.to_csv('data.csv.gz', compression='gzip', index=False)
```

### 6. **Debugging and Monitoring**

#### Memory Profiling
```python
import psutil
import pandas as pd

def monitor_memory(operation_name):
    """Decorator to monitor memory usage of operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            process = psutil.Process()
            before = process.memory_info().rss / 1024**2
            
            result = func(*args, **kwargs)
            
            after = process.memory_info().rss / 1024**2
            print(f"{operation_name}: Memory Δ = {after - before:.2f} MB")
            
            return result
        return wrapper
    return decorator

@monitor_memory("Data cleaning")
def clean_data(df):
    return df.dropna().reset_index(drop=True)
```

#### Progress Tracking for Large Operations
```python
from tqdm import tqdm

def process_chunks_with_progress(filepath, chunksize=10000):
    """Process with progress bar."""
    chunks = []
    total_rows = sum(1 for _ in open(filepath)) - 1  # Count rows in file
    
    with tqdm(total=total_rows, desc="Processing") as pbar:
        for chunk in pd.read_csv(filepath, chunksize=chunksize):
            processed = clean_chunk(chunk)
            chunks.append(processed)
            pbar.update(len(chunk))
    
    return pd.concat(chunks, ignore_index=True)
```

## 🎯 Performance Comparison Table

| Operation | Naive Approach | Optimized Approach | Memory Savings |
|-----------|----------------|-------------------|----------------|
| Loading 1GB CSV | `pd.read_csv()` | Specify dtypes + usecols | 60-70% |
| String operations | `.apply(str.upper)` | `.str.upper()` vectorized | 80% faster |
| GroupBy aggregations | Multiple `.groupby()` calls | Single `.agg()` call | 50% memory |
| Missing value handling | Row-wise iteration | `.fillna()` vectorized | 90% faster |
| File export | CSV default | Parquet with snappy | 75% smaller |

## 📊 Memory Usage Guidelines for 8GB RAM

1. **Working Set Limit**: Keep active DataFrames under 2GB total
2. **Chunk Size**: Use 10,000-50,000 rows per chunk for processing
3. **Monitor**: Use `df.memory_usage(deep=True)` regularly
4. **Cleanup**: Explicit `del` and `gc.collect()` between major operations
5. **Swap Prevention**: Process in chunks to avoid swapping to disk

## 🔧 Troubleshooting Common Issues

### "MemoryError" during read_csv
```python
# Solution: Use chunks or optimize dtypes
df = pd.read_csv('large.csv', dtype={'col1': 'int32'}, usecols=['col1', 'col2'])

# OR
chunks = []
for chunk in pd.read_csv('large.csv', chunksize=50000):
    chunks.append(process(chunk))
df = pd.concat(chunks)
```

### Slow GroupBy Operations
```python
# Solution: Sort data first or use different algorithm
df = df.sort_values('group_column')
result = df.groupby('group_column', sort=False).sum()  # sort=False can help
```

### SettingWithCopyWarning
```python
# Solution: Always use .copy() or .loc
df_filtered = df[df['value'] > 0].copy()
df_filtered['new_col'] = 1  # No warning
```

## 🚀 Quick Reference Cheat Sheet

```python
# Memory optimization
df = pd.read_csv(file, dtype=spec, usecols=cols)
df = optimize_numeric_dtypes(df)
df = optimize_categorical(df)

# Efficient operations
df['new'] = df['a'] + df['b']  # Vectorized
result = df.groupby('key').agg({'val': ['sum', 'mean']})
df = df.loc[condition]  # Single .loc access

# File I/O
df.to_parquet('data.parquet', compression='snappy')  # Best for storage
df.to_feather('data.feather')  # Best for intermediate
```

## 📚 Further Reading

1. **Pandas Documentation**: Performance tuning section
2. **"Python for Data Analysis"**: Wes McKinney (Pandas creator)
3. **Real Python**: Pandas performance tutorials
4. **Towards Data Science**: Memory optimization articles

Remember: The key to working with 8GB RAM is **proactive memory management**. Always think about memory footprint before writing code, and regularly profile your operations to identify bottlenecks.