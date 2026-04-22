# Advanced Pandas Interview Questions for Data Engineers

## 🧠 Memory Optimization & Performance

### 1. How would you process a 10GB CSV file on a machine with only 8GB RAM?
**Answer:** Use chunked processing with `pd.read_csv(chunksize=...)`. Process the file in manageable pieces, aggregating results incrementally. Also optimize dtypes (use `int32` instead of `int64`, `float32` instead of `float64`, `category` for low-cardinality strings), and consider using `usecols` to load only necessary columns.

**Follow-up:** What chunk size would you choose and why?
**Answer:** Start with 100,000 rows per chunk, monitor memory usage, and adjust. The goal is to keep each chunk's memory footprint well below available RAM (e.g., 500MB-1GB per chunk) to leave room for processing overhead.

### 2. What are the most effective ways to reduce Pandas DataFrame memory usage?
**Answer:**
1. **Downcast numeric columns**: Use `pd.to_numeric(..., downcast='integer'/'float')`
2. **Convert strings to categorical**: For columns with few unique values relative to row count
3. **Specify dtypes at read time**: Provide `dtype` dictionary to `read_csv`
4. **Load only needed columns**: Use `usecols` parameter
5. **Use sparse data structures**: For data with many zeros/NaNs
6. **Delete unused columns/rows**: Use `df.drop()` and `del` statement

### 3. Explain the memory difference between `int64`, `int32`, `int16`, and `int8`. When would you use each?
**Answer:**
- `int64`: 8 bytes, range ≈ -9.2e18 to 9.2e18 (default, often wasteful)
- `int32`: 4 bytes, range ≈ -2.1e9 to 2.1e9 (good for IDs, counts up to 2 billion)
- `int16`: 2 bytes, range -32,768 to 32,767 (good for ages, small counts)
- `int8`: 1 byte, range -128 to 127 (good for binary flags, small categories)

**Use case example:** For a column of ages (0-120), `int8` saves 87.5% memory vs `int64`.

### 4. What's the performance impact of using `.apply()` vs vectorized operations?
**Answer:** `.apply()` is essentially a Python-level loop and can be 50-100x slower than vectorized operations. Vectorized operations use NumPy's C‑level optimizations and SIMD instructions.

```python
# SLOW: .apply()
df['new'] = df['value'].apply(lambda x: x * 2)

# FAST: Vectorized
df['new'] = df['value'] * 2

# EVEN FASTER: NumPy directly
df['new'] = np.multiply(df['value'].values, 2)
```

### 5. How does `category` dtype reduce memory, and what are its limitations?
**Answer:** `category` dtype stores strings as integer codes with a lookup table. Memory savings are proportional to `(1 - unique_count/total_rows)`. A column with 10 unique values across 1M rows saves ~99% memory.

**Limitations:**
- Not suitable for high-cardinality columns (many unique values)
- Some operations slower (e.g., string methods need conversion)
- Cannot use all comparison operators directly
- Sorting is by category order, not lexicographic

## 🔄 Chunked Processing & Large Datasets

### 6. Write a function to compute the mean of a column in a 20GB CSV without loading it entirely.
**Answer:**
```python
def chunked_mean(filepath, column, chunk_size=100000):
    total = 0
    count = 0
    for chunk in pd.read_csv(filepath, chunksize=chunk_size, usecols=[column]):
        total += chunk[column].sum()
        count += len(chunk)
    return total / count if count > 0 else 0
```

### 7. How would you perform a groupby-aggregation on a dataset larger than RAM?
**Answer:** Use incremental aggregation with dictionaries or defaultdict:
```python
from collections import defaultdict

def chunked_groupby_sum(filepath, group_col, value_col, chunk_size=50000):
    totals = defaultdict(float)
    for chunk in pd.read_csv(filepath, chunksize=chunk_size, usecols=[group_col, value_col]):
        for group, value in zip(chunk[group_col], chunk[value_col]):
            totals[group] += value
    return dict(totals)
```

### 8. What are the trade-offs between chunked processing and using Dask/Modin?
**Answer:**
- **Chunked processing (pure Pandas)**: More control, no new dependencies, but requires manual implementation for complex operations.
- **Dask**: Automatic parallelization, familiar DataFrame API, but has overhead for small datasets and requires learning its execution model.
- **Modin**: Drop‑in replacement for Pandas, uses Ray/Dask backend, good for multi‑core, but less control over memory usage.

**Rule of thumb:** Use chunked Pandas for simple linear workflows, Dask for complex multi‑step pipelines, Modin for interactive analysis on multi‑core machines.

### 9. How would you join a large DataFrame with a small lookup table efficiently?
**Answer:** Load the small table into memory, convert to dictionary, and use `.map()` during chunked processing:
```python
# Small lookup table
lookup = pd.read_csv('lookup.csv')
lookup_dict = lookup.set_index('key')['value'].to_dict()

# Process large file in chunks
results = []
for chunk in pd.read_csv('large.csv', chunksize=100000):
    chunk['lookup_value'] = chunk['key'].map(lookup_dict)
    results.append(chunk)
final = pd.concat(results)
```

## ⚡ Performance Tuning & Advanced Operations

### 10. What is the most efficient way to filter rows based on multiple conditions?
**Answer:** Use boolean indexing with combined conditions, avoiding chained operations:
```python
# GOOD: Single boolean expression
mask = (df['col1'] > 10) & (df['col2'] == 'value') & (df['col3'].notna())
result = df[mask]

# BAD: Chained indexing (creates intermediate copies)
result = df[df['col1'] > 10][df['col2'] == 'value'][df['col3'].notna()]
```

### 11. Explain how to use `pd.eval()` for performance gains.
**Answer:** `pd.eval()` evaluates string expressions using numexpr backend, which can be faster for complex operations on large DataFrames:
```python
# Standard way (slower for large DataFrames)
df['result'] = df['a'] * 2 + df['b'] ** 2 - df['c'] / 3

# Using pd.eval (often faster)
df['result'] = pd.eval("df['a'] * 2 + df['b'] ** 2 - df['c'] / 3")
```
**Note:** Benefits are most noticeable with large DataFrames and complex expressions.

### 12. What are the performance implications of different join types (merge vs. join vs. concat)?
**Answer:**
- `merge()`: Most flexible, SQL‑like joins, can be memory intensive if not optimized
- `join()`: Convenience method for index‑based joins, similar performance to merge
- `concat()`: For stacking DataFrames vertically/horizontally, very fast for simple concatenation

**Optimization tip:** Sort and set indexes on join keys before merging, and use `pd.merge()` with `sort=False` if order doesn't matter.

### 13. How would you handle time‑series data with irregular timestamps efficiently?
**Answer:** Use `pd.to_datetime()` with `format` parameter for faster parsing, set timestamp as index, and use `.asfreq()` or `.resample()` for regular intervals:
```python
# Efficient datetime parsing
df['timestamp'] = pd.to_datetime(df['timestamp_str'], format='%Y-%m-%d %H:%M:%S')
df.set_index('timestamp', inplace=True)

# Resample to hourly
hourly = df.resample('H').mean()
```

## 🐞 Debugging & Optimization

### 14. How do you profile memory usage of a Pandas DataFrame?
**Answer:**
```python
# Overall memory
print(df.memory_usage(deep=True).sum() / 1024**2, 'MB')

# Per column
print(df.memory_usage(deep=True))

# Detailed per column with info
for col in df.columns:
    print(f"{col}: {df[col].dtype}, {df[col].memory_usage(deep=True) / 1024**2:.2f} MB")
```

### 15. What tools would you use to identify performance bottlenecks in Pandas code?
**Answer:**
- **`%timeit` / `%%timeit`** in Jupyter for micro‑benchmarks
- **`line_profiler`** for line‑by‑line timing
- **`memory_profiler`** for memory usage tracking
- **`snakeviz`** for visualization of profiling results
- **Pandas' built‑in** `pd.options.display.precision` and `pd.show_versions()`

### 16. How would you handle a "MemoryError" in the middle of a long‑running process?
**Answer:**
1. **Immediate**: Catch the exception, save progress, and restart with smaller chunk size
2. **Diagnostic**: Use `psutil` to monitor memory usage throughout process
3. **Preventive**: Implement checkpointing – save intermediate results every N chunks
4. **Alternative**: Switch to out‑of‑core frameworks (Dask) or database solutions

## 🏗️ Architecture & Design

### 17. Design a system to process daily 50GB CSV files on a 16GB RAM machine.
**Answer:**
- **Ingestion**: Use chunked reading with optimized dtypes
- **Processing**: Implement incremental aggregation; avoid materializing full dataset
- **Storage**: Write results to Parquet (columnar, compressed) or a database
- **Monitoring**: Track memory usage, chunk times, and disk I/O
- **Fallback**: Have a mechanism to resume from last checkpoint if job fails

### 18. When would you choose Parquet over CSV for large datasets?
**Answer:** Choose Parquet when:
- Data is read multiple times (columnar storage = faster queries)
- Schema evolution is needed (Parquet supports it)
- Compression is important (Parquet compresses better)
- You need to query subsets of columns efficiently

Choose CSV when:
- Data is produced/consumed by simple tools (text editors, shell)
- Interoperability with non‑data‑engineering systems is required
- Data is written once and read linearly

### 19. How would you implement a rolling window operation on a dataset that doesn't fit in memory?
**Answer:** For time‑series data, process in chronological chunks with overlap equal to window size:
```python
window_size = 30
chunk_size = 100000
overlap = window_size

previous_tail = None
for chunk in pd.read_csv('data.csv', chunksize=chunk_size):
    if previous_tail is not None:
        chunk = pd.concat([previous_tail, chunk])
    
    # Perform rolling operation
    chunk['rolling_mean'] = chunk['value'].rolling(window_size).mean()
    
    # Save results except the overlapping part
    save_results(chunk.iloc[:-overlap] if len(chunk) > overlap else chunk)
    
    # Keep tail for next chunk
    previous_tail = chunk.iloc[-overlap:].copy()
```

### 20. What are the advantages of using `pandas.DataFrame` vs `numpy.ndarray` for numerical data?
**Answer:**
- **DataFrame advantages**: Column names, mixed types, missing value handling, time‑series support, SQL‑like operations, easy I/O
- **NumPy advantages**: Faster pure numerical operations, less memory overhead, better integration with scientific libraries, GPU support via CuPy

**Use DataFrame when** you need heterogeneous data, labeled axes, or database‑like operations. **Use NumPy when** you need maximum performance on homogeneous numerical arrays.

## 🎯 Behavioral & Scenario‑Based Questions

### 21. Describe a time you optimized a slow Pandas pipeline. What was your approach?
**Sample answer:** "I once reduced a 2‑hour ETL job to 15 minutes. I started by profiling with `line_profiler` and `memory_profiler`, discovering that `.apply()` and repeated `.merge()` calls were bottlenecks. I replaced `.apply()` with vectorized operations, pre‑filtered columns with `usecols`, and used `.map()` instead of merge for lookups. I also implemented chunked processing for the largest dataset and switched output format from CSV to Parquet."

### 22. How would you explain memory optimization techniques to a non‑technical stakeholder?
**Answer:** "Think of data like water in pipes. Default settings use big pipes (large memory) even for small amounts of water (data). We're replacing those big pipes with smaller, right‑sized pipes (optimized data types) and adding valves to control flow (chunking). This lets us process more data with the same infrastructure, reducing costs and improving speed."

### 23. What would you do if your optimized code is still too slow for production requirements?
**Answer:**
1. **Re‑evaluate algorithm**: Is there a more efficient algorithm or data structure?
2. **Parallelize**: Use multiprocessing, Dask, or Modin
3. **Scale hardware**: Consider more RAM, faster SSD, or more CPU cores
4. **Alternative tools**: Evaluate Polars, Vaex, or DuckDB
5. **Database solution**: Load data into SQLite/PostgreSQL and query there
6. **Approximation**: If exact results aren't needed, consider sampling or probabilistic data structures

### 24. How do you stay updated with Pandas performance best practices?
**Answer:** Follow Pandas release notes, participate in Stack Overflow Pandas tag, read blogs from core contributors, experiment with new features in side projects, and benchmark different approaches for common operations.

## 📊 Real‑World Problem Solving

### 25. You have a 100GB CSV of sensor data. How would you find the 10 sensors with the highest average reading?
**Answer:**
```python
from collections import defaultdict

def top_sensors(filepath, chunk_size=50000):
    sums = defaultdict(float)
    counts = defaultdict(int)
    
    for chunk in pd.read_csv(filepath, chunksize=chunk_size, 
                             usecols=['sensor_id', 'reading']):
        for sensor, reading in zip(chunk['sensor_id'], chunk['reading']):
            sums[sensor] += reading
            counts[sensor] += 1
    
    # Compute averages
    averages = {sensor: sums[sensor]/counts[sensor] for sensor in sums}
    
    # Return top 10
    return sorted(averages.items(), key=lambda x: x[1], reverse=True)[:10]
```

### 26. Design a data quality check pipeline for terabyte‑scale datasets using Pandas.
**Answer:**
- **Sampling**: Run full checks on representative samples (1‑5%)
- **Chunked validation**: Process in chunks, aggregating metrics (null counts, value ranges, uniqueness)
- **Statistical checks**: Use approximate algorithms (HyperLogLog for distinct counts)
- **Parallelization**: Use Dask to distribute checks across cores/workers
- **Checkpointing**: Save validation results periodically to avoid re‑computation
- **Alerting**: Flag anomalies based on historical thresholds

### 27. How would you handle schema evolution in a long‑running ETL pipeline?
**Answer:**
- **Versioned schemas**: Store JSON schema with each dataset version
- **Flexible reading**: Use `pd.read_csv(..., dtype=some_dict)` with fallback to object dtype
- **Schema validation**: Use `pandera` or `great_expectations` for runtime checks
- **Migration scripts**: Automatically transform old schemas to new ones
- **Backward compatibility**: Maintain ability to read last N schema versions

## 🔧 Technical Deep Dive

### 28. Explain how Pandas uses NumPy arrays internally and the performance implications.
**Answer:** Pandas DataFrames are collections of NumPy arrays (one per column). This allows vectorized operations but also means:
- Homogeneous data per column (all values same type)
- Copy‑on‑write semantics can cause unexpected memory usage
- Operations that break alignment (like `.append`) may trigger full copies
- Understanding NumPy's memory layout can help optimize Pandas operations

### 29. What is copy‑on‑write in Pandas and how does it affect performance?
**Answer:** Copy‑on‑write means that when you slice a DataFrame, Pandas may return a view (not a copy) initially, but if you modify the slice, a copy is made. This can cause performance surprises:
- **Benefit**: Slicing is O(1) memory
- **Drawback**: Modification after slicing triggers O(n) copy
- **Best practice**: Use `.copy()` explicitly when you need a true independent copy

### 30. How does the GIL affect Pandas performance and what are the workarounds?
**Answer:** The Global Interpreter Lock (GIL) prevents true parallel execution of Python threads. For Pandas:
- **CPU‑bound operations** are limited to single core (except for some NumPy operations that release GIL)
- **I/O‑bound operations** (reading from disk/network) can benefit from threading
- **Workarounds**: Use multiprocessing (separate processes), Dask (distributed), or Modin (Ray backend) for parallel execution

---

## 📝 Quick Reference Cheat Sheet

### Memory Optimization Checklist
- [ ] Use `dtype` parameter in `read_csv`
- [ ] Downcast numerics with `pd.to_numeric(..., downcast=...)`
- [ ] Convert low‑cardinality strings to `category`
- [ ] Delete unused columns with `df.drop(columns=...)`
- [ ] Use `chunksize` for files > 1GB
- [ ] Force garbage collection with `gc.collect()`

### Performance Anti‑Patterns to Avoid
- ❌ Using `.apply()` for simple transformations
- ❌ Chained indexing (`df[a][b]`)
- ❌ Loading entire file for simple aggregates
- ❌ Merging unsorted DataFrames
- ❌ Not specifying `dtype` when reading large files

### Essential Tools
- `df.memory_usage(deep=True)` – Memory analysis
- `%timeit` / `%%timeit` – Quick benchmarking
- `pd.show_versions()` – Environment info
- `psutil` – System‑level monitoring
- `pandarallel` / `swifter` – Easy parallelization

### When to Consider Alternatives
- **Dask**: Dataset > 10x RAM, complex multi‑step pipeline
- **Polars**: Need maximum speed on large aggregations
- **DuckDB**: SQL‑based interactive analysis
- **Vaex**: Visualization of huge datasets
- **Databases (SQL)**: Persistent storage with concurrent access