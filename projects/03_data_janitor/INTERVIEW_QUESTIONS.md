# Data Janitor Interview Questions

Comprehensive interview questions covering data cleaning, CLI tools, JSONL processing, Parquet optimization, and memory-constrained environments (8GB RAM).

## 📊 Core Concepts

### 1. **What is a "data janitor" tool and why is it important in data engineering?**
- **Expected Answer**: A data janitor tool automates the cleaning, transformation, and standardization of raw, messy data into analysis-ready formats. It's critical because data engineers spend 60-80% of their time on data cleaning, and automated tools ensure consistency, reproducibility, and efficiency.
- **Follow-up**: How would you design a data janitor tool for server logs?

### 2. **Explain the difference between structured, semi-structured, and unstructured data with examples relevant to log processing.**
- **Expected Answer**: 
  - Structured: Database tables with fixed schema (e.g., CSV, Parquet)
  - Semi-structured: JSON, XML, YAML - has structure but flexible schema
  - Unstructured: Raw text, images, audio
  - Server logs are typically semi-structured JSONL
- **Follow-up**: How does this affect your processing approach?

### 3. **Describe the JSONL (JSON Lines) format and its advantages over regular JSON for log data.**
- **Expected Answer**: JSONL stores one JSON object per line, allowing:
  - Stream processing (read line by line)
  - Parallel processing
  - Easy appending
  - Error recovery (bad lines can be skipped)
- **Follow-up**: How would you handle malformed lines in a JSONL file?

## 🔧 Technical Implementation

### 4. **How would you process a 10GB JSONL file on a machine with only 8GB RAM?**
- **Expected Answer**:
  1. Use chunked reading (pandas `chunksize` or line-by-line)
  2. Process each chunk independently
  3. Write intermediate results to disk
  4. Use efficient dtypes (categorical, datetime)
  5. Monitor memory usage and adjust chunk size dynamically
- **Follow-up**: What chunk size would you start with and why?

### 5. **Explain how to flatten nested JSON structures efficiently.**
- **Expected Answer**:
  - Use `pandas.json_normalize()` for simple cases
  - For complex nesting, use recursion or iterative flattening
  - Handle missing keys gracefully with `.get()`
  - Consider schema evolution (new nested fields)
- **Follow-up**: Write Python code to flatten `{"metadata": {"ip": "1.2.3.4", "user": {"id": 123}}}`

### 6. **What are the key data quality checks you would implement for server logs?**
- **Expected Answer**:
  1. Timestamp validation (format, range, monotonicity)
  2. Required field presence
  3. Value domain validation (e.g., action ∈ {login, logout, view})
  4. IP address format validation
  5. Bot detection (user agent patterns)
  6. Duplicate detection
- **Follow-up**: How would you handle logs with missing timestamps?

### 7. **Compare different approaches for reading JSONL files in Python.**
- **Expected Answer**:
  - `pandas.read_json(lines=True)`: Easy but memory-intensive
  - `ijson`: Stream parsing, low memory but slower
  - Line-by-line with `json.loads()`: Balanced, flexible
  - `polars.scan_ndjson()`: Lazy evaluation, efficient
- **Follow-up**: When would you choose each approach?

## 🚀 CLI & Production Readiness

### 8. **Design a command-line interface for a data janitor tool. What arguments would you include?**
- **Expected Answer**:
  - Required: `--input-dir`, `--output-dir`
  - Optional: `--filter-bots`, `--compression`, `--chunk-size`
  - Flags: `--verbose`, `--dry-run`, `--help`
  - Configuration: `--config-file`
- **Follow-up**: How would you validate and document these arguments?

### 9. **What error handling strategies are essential for a production data cleaning tool?**
- **Expected Answer**:
  1. Comprehensive logging (different levels)
  2. Graceful degradation (skip bad records, continue)
  3. Retry logic for transient failures
  4. Alerting for critical errors
  5. State persistence (resume from failure)
  6. Input validation before processing
- **Follow-up**: How would you handle a corrupt JSONL file?

### 10. **How would you make your data janitor tool observable in production?**
- **Expected Answer**:
  - Log key metrics (processing time, record counts, error rates)
  - Export metrics to monitoring system (Prometheus, CloudWatch)
  - Health check endpoints
  - Performance dashboards
  - Alert rules for anomalies
- **Follow-up**: What metrics would be most important to track?

## 💾 Storage & Optimization

### 11. **Why choose Parquet over CSV for storing cleaned log data?**
- **Expected Answer**:
  - Columnar storage (faster queries on specific columns)
  - Built-in compression (70-90% size reduction)
  - Schema evolution support
  - Predicate pushdown (filter during read)
  - Splittable for parallel processing
- **Follow-up**: What compression algorithm would you use and why?

### 12. **How would you optimize Parquet file size and read performance?**
- **Expected Answer**:
  1. Choose appropriate compression (snappy for speed, gzip for size)
  2. Set optimal row group size (128MB-1GB)
  3. Use efficient dtypes (categorical for strings, proper numeric types)
  4. Partition by date/other dimensions
  5. Add column statistics for filtering
- **Follow-up**: How does partitioning affect query performance?

### 13. **Explain schema evolution in Parquet and how to handle it.**
- **Expected Answer**:
  - Parquet supports adding columns (backward compatible)
  - Removing/renaming columns requires careful migration
  - Use schema merging or explicit schema during read
  - Version your schemas and document changes
- **Follow-up**: How would you handle a new field appearing in logs?

## 🧠 Memory & Performance

### 14. **What techniques would you use to monitor and control memory usage in Python?**
- **Expected Answer**:
  - Use `psutil` to track process memory
  - Implement memory limits with `resource.setrlimit()`
  - Use generators instead of lists
  - Clear references with `del` and `gc.collect()`
  - Profile with `memory_profiler`
- **Follow-up**: How would you detect memory leaks?

### 15. **Compare pandas, polars, and dask for large-scale data processing on 8GB RAM.**
- **Expected Answer**:
  - **pandas**: In-memory, intuitive, but limited by RAM
  - **polars**: Rust-based, faster, better memory management
  - **dask**: Parallel, out-of-core, scales beyond RAM but more complex
  - Choice depends on data size and processing pattern
- **Follow-up**: When would you switch from pandas to polars/dask?

### 16. **Describe vectorized operations and why they're important for performance.**
- **Expected Answer**:
  - Operations applied to entire arrays at once (NumPy/pandas)
  - Avoid Python loops, use C/Fortran backend
  - 10-100x faster than iterative approaches
  - Examples: `.str.lower()`, `.astype()`, arithmetic operations
- **Follow-up**: When can't you use vectorized operations?

## 🔍 Advanced Topics

### 17. **How would you implement incremental processing for continuously arriving logs?**
- **Expected Answer**:
  1. Watch directory for new files (watchdog, inotify)
  2. Maintain state of processed files (SQLite, Redis)
  3. Handle partial files (size-based or marker-based)
  4. Implement idempotency (skip already processed)
  5. Support backfilling historical data
- **Follow-up**: How would you handle logs that arrive out of order?

### 18. **What strategies would you use for deduplicating log entries?**
- **Expected Answer**:
  - Exact duplicate detection (hash entire record)
  - Business key deduplication (timestamp + ip + action)
  - Window-based deduplication (within time window)
  - Probabilistic (Bloom filters for large datasets)
- **Follow-up**: How would you handle near-duplicates (slightly different timestamps)?

### 19. **Explain how to detect and handle schema drift in incoming data.**
- **Expected Answer**:
  1. Regularly sample incoming data
  2. Compare against expected schema
  3. Alert on new/removed/changed fields
  4. Version schemas and support multiple versions
  5. Document schema evolution decisions
- **Follow-up**: What would you do if a required field disappears?

### 20. **How would you benchmark and profile your data janitor tool?**
- **Expected Answer**:
  1. Use `timeit` for microbenchmarks
  2. Use `cProfile` for function-level profiling
  3. Use `memory_profiler` for memory usage
  4. Test with production-sized data
  5. Measure end-to-end throughput
- **Follow-up**: What metrics would indicate a performance bottleneck?

## 🐳 Deployment & Operations

### 21. **How would you containerize the data janitor tool using Docker?**
- **Expected Answer**:
  1. Use multi-stage builds for small images
  2. Copy only necessary files
  3. Set non-root user for security
  4. Configure entrypoint and command
  5. Add health checks
  6. Use .dockerignore to exclude development files
- **Follow-up**: How would you handle configuration in Docker?

### 22. **What CI/CD pipeline would you set up for this tool?**
- **Expected Answer**:
  1. Linting and formatting checks
  2. Unit and integration tests
  3. Performance regression tests
  4. Container building and scanning
  5. Deployment to test/production
- **Follow-up**: How would you test with large datasets in CI?

### 23. **How would you monitor the tool in production?**
- **Expected Answer**:
  1. Log aggregation (ELK, CloudWatch Logs)
  2. Metrics collection (Prometheus, Datadog)
  3. Alerting (PagerDuty, OpsGenie)
  4. Distributed tracing (Jaeger, X-Ray)
  5. Business metrics (records processed, success rate)
- **Follow-up**: What would trigger a PagerDuty alert?

### 24. **Describe a rollback strategy if a new version causes issues.**
- **Expected Answer**:
  1. Versioned deployments (canary, blue-green)
  2. Quick rollback to previous version
  3. Data compatibility checks
  4. Feature flags for risky changes
  5. Comprehensive testing before deployment
- **Follow-up**: How would you ensure data consistency during rollback?

## 📈 Scenario-Based Questions

### 25. **You're processing logs and notice memory usage spikes to 7.5GB on an 8GB machine. How would you diagnose and fix this?**
- **Expected Answer**:
  1. Profile memory usage by function
  2. Check for large intermediate objects
  3. Reduce chunk size
  4. Use more memory-efficient dtypes
  5. Implement disk spilling for intermediate results
  6. Consider streaming processing instead of batch
- **Follow-up**: What tools would you use for diagnosis?

### 26. **The logs suddenly include a new nested field that breaks your flattening logic. How would you handle this?**
- **Expected Answer**:
  1. Make flattening logic more robust (handle missing keys)
  2. Log schema changes for investigation
  3. Support schema evolution (add new columns)
  4. Version your processing logic
  5. Implement schema validation step
- **Follow-up**: How would you communicate this change to downstream users?

### 27. **You need to process logs from multiple regions with different timezones. How would you handle timestamp standardization?**
- **Expected Answer**:
  1. Parse timestamps with timezone information
  2. Convert to UTC for consistency
  3. Store original timezone as metadata
  4. Handle ambiguous times (daylight savings)
  5. Validate timezone consistency per source
- **Follow-up**: How would you detect incorrect timezone data?

### 28. **The tool is taking too long to process daily logs. How would you optimize it?**
- **Expected Answer**:
  1. Profile to find bottlenecks
  2. Parallelize independent operations
  3. Use more efficient libraries (polars instead of pandas)
  4. Optimize I/O (batch reads/writes)
  5. Consider incremental processing
  6. Scale horizontally (multiple workers)
- **Follow-up**: What would be your first optimization attempt?

## 💡 Behavioral & Design Questions

### 29. **How would you design this tool to be used by both data engineers and data analysts?**
- **Expected Answer**:
  1. Simple CLI for analysts (defaults, good error messages)
  2. Advanced options for engineers (tuning, monitoring)
  3. Comprehensive documentation
  4. Example configurations
  5. Integration with common workflows (Jupyter, Airflow)
- **Follow-up**: What trade-offs would you make?

### 30. **Describe how you would prioritize features for the data janitor tool.**
- **Expected Answer**:
  1. Core functionality first (cleaning, flattening, Parquet output)
  2. Then robustness (error handling, logging)
  3. Then performance (memory optimization, speed)
  4. Then advanced features (incremental processing, schema evolution)
  5. Based on user feedback and business impact
- **Follow-up**: How would you gather requirements?

## 🧪 Practical Coding Exercises

### 31. **Write a function to parse JSONL files line by line with error handling.**
```python
def parse_jsonl_safely(file_path):
    # TODO: Implement
    pass
```

### 32. **Create a function to flatten nested JSON dictionaries.**
```python
def flatten_dict(nested_dict, parent_key='', sep='_'):
    # TODO: Implement
    pass
```

### 33. **Implement memory-efficient chunked processing of large JSONL files.**
```python
def process_jsonl_in_chunks(file_path, process_func, chunk_size=10000):
    # TODO: Implement
    pass
```

### 34. **Write a CLI argument parser for the data janitor tool.**
```python
def create_parser():
    # TODO: Implement
    pass
```

### 35. **Create a function to validate log data quality.**
```python
def validate_logs(df):
    # TODO: Implement
    pass
```

## 📚 Study Resources

### Recommended Reading:
1. **Python Data Science Handbook** - Jake VanderPlas (NumPy/pandas optimization)
2. **Designing Data-Intensive Applications** - Martin Kleppmann (storage systems)
3. **The Pragmatic Programmer** - Andy Hunt & Dave Thomas (CLI design)
4. **Python Cookbook** - David Beazley & Brian K. Jones (advanced Python)

### Online Resources:
- pandas documentation (performance optimization section)
- Apache Parquet documentation (format specification)
- Real Python articles on CLI tools with argparse
- Towards Data Science articles on memory-efficient processing

### Practice Platforms:
- LeetCode (string processing, optimization problems)
- HackerRank (Python, data structures)
- Advent of Code (algorithmic thinking)

## 🎯 Interview Preparation Tips

### 1. **Understand the fundamentals**:
   - JSON/JSONL parsing
   - pandas operations (vectorization, dtype optimization)
   - Memory management in Python
   - CLI design patterns

### 2. **Practice explaining trade-offs**:
   - Memory vs. speed
   - Simplicity vs. robustness
   - Batch vs. streaming processing

### 3. **Be ready for coding exercises**:
   - Write clean, commented code
   - Include error handling
   - Consider edge cases
   - Optimize for readability first, then performance

### 4. **Prepare questions for the interviewer**:
   - What's the typical data volume?
   - What are the performance requirements?
   - How is the tool currently used?
   - What are the biggest pain points?

### 5. **Showcase your experience**:
   - Mention similar projects you've worked on
   - Discuss challenges you've overcome
   - Explain your design decisions

## 🔗 Related Resources in This Repository

- `practice_exercises.py` - Hands-on exercises for implementing the data janitor tool
- `GOTCHAS_BEST_PRACTICES.md` - Common pitfalls and optimization techniques
- `janitor.py` - Reference implementation (when completed)
- `generate_logs.py` - Tool to generate sample log data for testing

Remember: The goal is not just to answer questions correctly, but to demonstrate your problem-solving process, consideration of trade-offs, and understanding of production requirements.