# Data Janitor: Gotchas & Best Practices

This guide covers common pitfalls and best practices for building data cleaning CLI tools, processing JSONL logs, and working with Parquet files in memory-constrained environments (8GB RAM).

## 🚨 Critical Gotchas

### 1. **Memory Explosion with JSONL Parsing**
```python
# WRONG: Loading entire file into memory
with open('logs.jsonl') as f:
    data = [json.loads(line) for line in f]  # Can crash with large files!

# CORRECT: Process line by line
def process_jsonl_stream(file_path):
    with open(file_path) as f:
        for line in f:
            yield json.loads(line)  # One object at a time
```

### 2. **Schema Inference Issues**
```python
# WRONG: Letting pandas infer dtypes
df = pd.read_json('logs.jsonl', lines=True)  # May use object dtype for everything

# CORRECT: Specify dtypes upfront
dtype_spec = {
    'timestamp': 'datetime64[ns]',
    'action': 'category',
    'ip': 'string',
    'user_agent': 'string'
}
df = pd.read_json('logs.jsonl', lines=True, dtype=dtype_spec)
```

### 3. **Nested JSON Flattening Pitfalls**
```python
# WRONG: Assuming consistent nesting
for entry in data:
    ip = entry['metadata']['ip']  # KeyError if metadata missing!

# CORRECT: Safe access with .get()
ip = entry.get('metadata', {}).get('ip', '0.0.0.0')
```

### 4. **Parquet Writing Without Schema**
```python
# WRONG: Writing without schema optimization
df.to_parquet('output.parquet')  # May use inefficient defaults

# CORRECT: Optimize before writing
df['action'] = df['action'].astype('category')  # Reduce cardinality
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.to_parquet('output.parquet', compression='snappy', index=False)
```

### 5. **CLI Argument Validation Failures**
```python
# WRONG: No validation
parser.add_argument('--input-dir', type=str)

# CORRECT: Validate existence
def dir_path(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Directory doesn't exist: {path}")
    return path

parser.add_argument('--input-dir', type=dir_path, required=True)
```

## 🏆 Best Practices

### 1. **Memory-Efficient Processing for 8GB RAM**

#### Chunked Processing
```python
def process_large_jsonl(file_path, chunk_size=10000):
    """Process JSONL in chunks to stay under memory limits."""
    chunks = []
    current_chunk = []
    
    with open(file_path) as f:
        for i, line in enumerate(f):
            current_chunk.append(json.loads(line))
            
            if len(current_chunk) >= chunk_size:
                # Process and clear chunk
                df_chunk = pd.DataFrame(current_chunk)
                process_chunk(df_chunk)
                current_chunk = []
                
                # Monitor memory
                if get_memory_usage_mb() > 6000:  # Leave 2GB buffer
                    chunk_size = max(1000, chunk_size // 2)
    
    # Process remaining
    if current_chunk:
        df_chunk = pd.DataFrame(current_chunk)
        process_chunk(df_chunk)
```

#### Selective Column Loading
```python
# Only load needed columns
columns_needed = ['timestamp', 'action', 'metadata.ip', 'metadata.user_agent']
df = pd.read_json('logs.jsonl', lines=True, dtype={
    'timestamp': 'datetime64[ns]',
    'action': 'category'
})
```

### 2. **Robust Error Handling**

#### Graceful Failure Recovery
```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def process_file_safely(file_path, output_dir):
    """Process file with comprehensive error handling."""
    try:
        # Check file exists and is readable
        if not Path(file_path).is_file():
            logger.error(f"File not found: {file_path}")
            return False
            
        # Process with timeout
        result = process_with_timeout(file_path, timeout=300)
        
        # Validate output
        if not validate_output(result):
            logger.warning(f"Output validation failed for {file_path}")
            # Move to quarantine for manual inspection
            quarantine_file(file_path)
            return False
            
        return True
        
    except json.JSONDecodeError as e:
        logger.error(f"Malformed JSON in {file_path}: {e}")
        quarantine_file(file_path)
        return False
        
    except MemoryError:
        logger.critical(f"Memory limit exceeded processing {file_path}")
        # Try with smaller chunk size
        return process_with_smaller_chunks(file_path)
        
    except Exception as e:
        logger.exception(f"Unexpected error processing {file_path}")
        return False
```

### 3. **Performance Optimization**

#### Use Efficient Data Structures
```python
from collections import defaultdict
import numpy as np

# WRONG: List of dicts for aggregation
results = []
for entry in data:
    results.append({'action': entry['action'], 'count': 1})

# CORRECT: Use defaultdict for counting
action_counts = defaultdict(int)
for entry in data:
    action_counts[entry['action']] += 1
```

#### Vectorized Operations
```python
# WRONG: Looping through DataFrame
for idx, row in df.iterrows():
    df.loc[idx, 'action_lower'] = row['action'].lower()

# CORRECT: Vectorized operation
df['action'] = df['action'].str.lower()
```

### 4. **Production-Ready CLI Design**

#### Comprehensive Logging
```python
import logging
import sys

def setup_logging(verbose=False):
    """Configure logging for CLI tool."""
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('janitor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Quiet noisy libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)
```

#### Configuration Management
```python
import yaml
from dataclasses import dataclass

@dataclass
class JanitorConfig:
    input_dir: str
    output_dir: str
    filter_bots: bool = True
    compression: str = 'snappy'
    chunk_size: int = 10000
    
    @classmethod
    def from_yaml(cls, config_path):
        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)
```

### 5. **Data Quality Assurance**

#### Automated Validation
```python
def validate_log_data(df):
    """Comprehensive data validation."""
    checks = {
        'timestamp_not_null': df['timestamp'].notna().all(),
        'timestamp_range': df['timestamp'].between('2023-01-01', '2024-12-31').all(),
        'action_values': set(df['action'].unique()).issubset({'login', 'logout', 'view', 'purchase'}),
        'ip_format': df['ip'].str.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$').all(),
    }
    
    return {
        'passed': all(checks.values()),
        'details': checks,
        'failed_checks': [k for k, v in checks.items() if not v]
    }
```

#### Schema Evolution Handling
```python
def handle_schema_changes(current_df, expected_schema):
    """Handle schema changes in incoming data."""
    missing_cols = set(expected_schema) - set(current_df.columns)
    extra_cols = set(current_df.columns) - set(expected_schema)
    
    # Add missing columns with defaults
    for col in missing_cols:
        current_df[col] = expected_schema[col].get('default', None)
    
    # Warn about extra columns
    if extra_cols:
        logging.warning(f"Unexpected columns: {extra_cols}")
        # Optionally drop or keep with prefix
        current_df = current_df.drop(columns=list(extra_cols))
    
    return current_df
```

## 🔧 Optimization Techniques for 8GB RAM

### 1. **Memory Monitoring**
```python
import psutil
import os

def get_memory_usage_mb():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def check_memory_limit(soft_limit_mb=6000):
    """Check if approaching memory limit."""
    usage = get_memory_usage_mb()
    if usage > soft_limit_mb:
        logging.warning(f"Memory usage high: {usage:.1f}MB")
        return True
    return False
```

### 2. **Disk Spillover Strategy**
```python
import tempfile
import pickle

def process_with_disk_spill(data_iterator, process_func):
    """Process data with disk spillover when memory is full."""
    temp_files = []
    
    try:
        batch = []
        for item in data_iterator:
            batch.append(item)
            
            if len(batch) >= 1000 or check_memory_limit():
                # Process batch
                result = process_func(batch)
                
                # Spill to disk if needed
                if check_memory_limit():
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
                    pickle.dump(result, temp_file)
                    temp_files.append(temp_file.name)
                    temp_file.close()
                
                batch = []
        
        # Process final batch
        if batch:
            process_func(batch)
            
    finally:
        # Cleanup temp files
        for temp_file in temp_files:
            os.unlink(temp_file)
```

### 3. **Incremental Processing**
```python
def incremental_parquet_writer(output_path):
    """Write to Parquet incrementally to avoid memory buildup."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    
    writer = None
    
    def write_chunk(chunk_df):
        nonlocal writer
        
        table = pa.Table.from_pandas(chunk_df)
        
        if writer is None:
            # First chunk: create writer with schema
            writer = pq.ParquetWriter(output_path, table.schema, compression='snappy')
        
        writer.write_table(table)
    
    def close_writer():
        if writer:
            writer.close()
    
    return write_chunk, close_writer
```

## 📊 Performance Benchmarks

### Expected Performance on 8GB RAM:
- **1GB JSONL file**: ~30-60 seconds with chunked processing
- **Memory usage**: Should stay under 6GB peak
- **Parquet compression**: 70-80% size reduction with snappy
- **Processing rate**: 10,000-50,000 rows/second depending on complexity

### Optimization Impact:
| Technique | Memory Reduction | Speed Improvement |
|-----------|------------------|-------------------|
| Chunked processing | 80% | -20% |
| Column pruning | 60% | +30% |
| Categorical dtype | 40% | +15% |
| Vectorized ops | 0% | +200% |

## 🚀 Deployment Checklist

### Before Production:
- [ ] Set up comprehensive logging
- [ ] Implement retry logic for transient failures
- [ ] Add monitoring (memory, CPU, disk)
- [ ] Create configuration file support
- [ ] Write unit tests for critical functions
- [ ] Document all command-line options
- [ ] Set up CI/CD pipeline
- [ ] Create Docker container
- [ ] Performance test with production-sized data

### Monitoring Metrics to Track:
- Processing time per file
- Memory usage peaks
- Error rates by type
- Output file sizes
- Schema change frequency
- Bot detection effectiveness

## 🎯 Key Takeaways

1. **Always process large files in chunks** - Never load everything into memory
2. **Validate early and often** - Catch data quality issues before processing
3. **Use appropriate dtypes** - Categorical for low-cardinality, datetime for timestamps
4. **Implement comprehensive error handling** - Tools should never crash silently
5. **Monitor memory usage** - Critical for 8GB RAM environments
6. **Optimize for your specific workload** - Test different chunk sizes and compression
7. **Design for schema evolution** - Data formats will change over time
8. **Make it observable** - Logging and metrics are essential for production

By following these best practices, you'll build a robust, memory-efficient data janitor tool that can handle real-world log processing tasks within 8GB RAM constraints.