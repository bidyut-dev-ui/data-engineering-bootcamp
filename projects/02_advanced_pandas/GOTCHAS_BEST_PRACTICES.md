# Advanced Pandas Gotchas & Best Practices for Memory-Constrained Environments

## 🚨 Critical Gotchas (Common Mistakes)

### 1. **Memory Bloat from Default Data Types**
**Problem**: Pandas defaults to `int64` and `float64` even for small numbers, wasting memory.
```python
# WRONG: Letting pandas infer data types
df = pd.read_csv('large_data.csv')  # All integers become int64 (8 bytes each)

# CORRECT: Specify optimal dtypes upfront
dtype_spec = {
    'customer_id': 'int32',      # 4 bytes instead of 8
    'age': 'int8',               # 1 byte (range 0-255)
    'price': 'float32',          # 4 bytes instead of 8
    'category': 'category'       # Categorical for low-cardinality strings
}
df = pd.read_csv('large_data.csv', dtype=dtype_spec)
```

### 2. **Loading Entire Dataset for Simple Aggregations**
**Problem**: Loading multi-GB file just to compute a sum or count.
```python
# WRONG: Loading everything
df = pd.read_csv('10gb_file.csv')  # MemoryError on 8GB RAM!
total = df['sales'].sum()

# CORRECT: Use chunking
total = 0
for chunk in pd.read_csv('10gb_file.csv', chunksize=100000):
    total += chunk['sales'].sum()
```

### 3. **Forgetting to Release Memory with Garbage Collection**
**Problem**: Large intermediate DataFrames not being garbage collected.
```python
# WRONG: Keeping unnecessary references
large_df = pd.read_csv('data.csv')
processed = large_df[large_df['value'] > 100]  # Keeps reference to large_df
# large_df still in memory!

# CORRECT: Delete references and force GC
large_df = pd.read_csv('data.csv')
processed = large_df[large_df['value'] > 100].copy()
del large_df  # Explicit deletion
import gc
gc.collect()  # Force garbage collection
```

### 4. **Inefficient String Storage**
**Problem**: Storing repetitive strings as object dtype (huge memory overhead).
```python
# WRONG: Strings as objects
df['category'] = df['category'].astype('object')  # Each string stored separately

# CORRECT: Convert to categorical for low-cardinality columns
unique_categories = df['category'].nunique()
if unique_categories < len(df) * 0.5:  # Less than 50% unique
    df['category'] = df['category'].astype('category')  # 5-10x memory reduction
```

### 5. **Chunking Without Proper State Management**
**Problem**: Accumulating results incorrectly across chunks.
```python
# WRONG: Recreating accumulator each iteration
results = []
for chunk in pd.read_csv('data.csv', chunksize=10000):
    results.append(chunk.groupby('category').sum())  # Memory grows!

# CORRECT: Use incremental aggregation
from collections import defaultdict
totals = defaultdict(float)
counts = defaultdict(int)

for chunk in pd.read_csv('data.csv', chunksize=10000):
    for category, value in zip(chunk['category'], chunk['sales']):
        totals[category] += value
        counts[category] += 1
```

## ✅ Best Practices for 8GB RAM Environments

### 1. **Profile Before Optimizing**
```python
def profile_dataframe(df):
    """Comprehensive memory profiling"""
    print(f"Shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Per-column analysis
    for col in df.columns:
        dtype = df[col].dtype
        memory_mb = df[col].memory_usage(deep=True) / 1024**2
        unique = df[col].nunique() if dtype == 'object' else None
        print(f"  {col}: {dtype}, {memory_mb:.2f} MB, unique={unique}")
```

### 2. **Systematic Downcasting Strategy**
```python
def optimize_dtypes(df):
    """Downcast numeric columns to smallest possible dtype"""
    optimized = df.copy()
    
    # Integer columns
    int_cols = optimized.select_dtypes(include=['int64', 'int32']).columns
    for col in int_cols:
        optimized[col] = pd.to_numeric(optimized[col], downcast='integer')
    
    # Float columns  
    float_cols = optimized.select_dtypes(include=['float64', 'float32']).columns
    for col in float_cols:
        optimized[col] = pd.to_numeric(optimized[col], downcast='float')
    
    # Object to categorical conversion
    obj_cols = optimized.select_dtypes(include=['object']).columns
    for col in obj_cols:
        if optimized[col].nunique() / len(optimized) < 0.5:  # < 50% unique
            optimized[col] = optimized[col].astype('category')
    
    return optimized
```

### 3. **Chunked Processing Patterns**
```python
def chunked_aggregation(file_path, chunk_size=100000):
    """Process large files without loading into memory"""
    # Pattern 1: Simple aggregation
    total = 0
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        total += chunk['value'].sum()
    
    # Pattern 2: Grouped aggregation
    from collections import defaultdict
    grouped_totals = defaultdict(float)
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        for group in chunk.groupby('category'):
            grouped_totals[group[0]] += group[1]['sales'].sum()
    
    # Pattern 3: Filter and save subset
    filtered_chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        filtered = chunk[chunk['value'] > threshold]
        filtered_chunks.append(filtered)
    
    result = pd.concat(filtered_chunks, ignore_index=True)
    return result
```

### 4. **Memory-Efficient Joins**
```python
# WRONG: Joining large DataFrames directly
large_df = pd.read_csv('large.csv')  # 5GB
lookup_df = pd.read_csv('lookup.csv')  # 2GB
result = large_df.merge(lookup_df, on='id')  # 7GB+ intermediate!

# CORRECT: Use chunked joins or broadcast smaller DataFrame
# Option 1: Chunked join
lookup_dict = pd.read_csv('lookup.csv').set_index('id')['value'].to_dict()
results = []
for chunk in pd.read_csv('large.csv', chunksize=100000):
    chunk['lookup_value'] = chunk['id'].map(lookup_dict)
    results.append(chunk)
result = pd.concat(results)

# Option 2: Use Dask or Modin for out-of-core processing
```

### 5. **Monitoring Memory During Execution**
```python
import psutil
import os

def monitor_memory(threshold_mb=6000):
    """Alert when approaching memory limit"""
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / (1024 * 1024)
    
    if memory_mb > threshold_mb:
        print(f"⚠️  Warning: Memory usage {memory_mb:.0f}MB > {threshold_mb}MB")
        # Trigger cleanup actions
        import gc
        gc.collect()
    
    return memory_mb

# Use in loops
for i, chunk in enumerate(pd.read_csv('huge.csv', chunksize=50000)):
    if i % 10 == 0:
        memory = monitor_memory()
        print(f"Processed {i*50000} rows, memory: {memory:.0f}MB")
```

## 🎯 Performance Optimization Checklist

### Before Loading Data:
- [ ] Estimate file size and memory requirements
- [ ] Define optimal `dtype` dictionary
- [ ] Consider using `usecols` to load only needed columns
- [ ] Set `low_memory=False` for consistent dtype inference

### During Processing:
- [ ] Use `df.info(memory_usage='deep')` to monitor memory
- [ ] Delete intermediate variables with `del` statement
- [ ] Force garbage collection with `gc.collect()` after large operations
- [ ] Use `.copy()` when creating derived DataFrames to avoid chain references

### For Large Files:
- [ ] Always test with `nrows` parameter first
- [ ] Implement chunked processing for files > 1GB
- [ ] Consider alternative formats: Parquet (columnar) or Feather (fast I/O)
- [ ] Use `pd.read_csv(..., iterator=True)` for manual chunk control

### Advanced Techniques:
- [ ] Use `np.where()` instead of `.apply()` for vectorized operations
- [ ] Prefer `.loc[]` and `.iloc[]` over chained indexing
- [ ] Use `pd.eval()` for complex expressions on large DataFrames
- [ ] Consider `modin.pandas` or `dask.dataframe` for out-of-core processing

## 📊 Real-World Example: Processing 10GB CSV on 8GB RAM

```python
def process_10gb_csv(input_path, output_path):
    """Process 10GB CSV on 8GB RAM machine"""
    # Step 1: Analyze with sample
    sample = pd.read_csv(input_path, nrows=100000)
    print(f"Sample shape: {sample.shape}")
    print(f"Columns: {sample.columns.tolist()}")
    
    # Step 2: Define optimal dtypes based on sample
    dtypes = {}
    for col in sample.columns:
        if sample[col].dtype == 'int64':
            dtypes[col] = 'int32'
        elif sample[col].dtype == 'float64':
            dtypes[col] = 'float32'
        elif sample[col].dtype == 'object':
            if sample[col].nunique() < 1000:
                dtypes[col] = 'category'
    
    # Step 3: Process in chunks
    chunk_size = 50000
    first_chunk = True
    
    for chunk in pd.read_csv(input_path, chunksize=chunk_size, dtype=dtypes):
        # Perform transformations
        chunk['processed'] = chunk['value'] * 2
        
        # Write to output (append mode)
        if first_chunk:
            chunk.to_csv(output_path, index=False)
            first_chunk = False
        else:
            chunk.to_csv(output_path, mode='a', header=False, index=False)
        
        # Monitor memory
        memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
        if memory_mb > 6000:
            print(f"High memory: {memory_mb:.0f}MB, forcing GC")
            import gc
            gc.collect()
    
    print("Processing complete!")
```

## 🚀 Key Takeaways

1. **Memory is your most constrained resource** - treat it like gold
2. **Profile before optimizing** - know where memory is being used
3. **Chunking is your best friend** for files larger than RAM
4. **Dtype optimization** can reduce memory by 50-90%
5. **Clean up as you go** - delete intermediates and force GC
6. **Consider alternative libraries** (Dask, Modin) when Pandas hits limits
7. **Test with samples** before processing full datasets
8. **Monitor continuously** to avoid out-of-memory crashes