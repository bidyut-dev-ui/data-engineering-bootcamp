# Schema Evolution: Gotchas & Best Practices

This guide covers common pitfalls and best practices for handling schema evolution, data contracts, and breaking changes in data pipelines with 8GB RAM constraints.

## 🚨 Critical Gotchas

### 1. **Silent Schema Drift**
```python
# WRONG: Assuming schema never changes
df = pd.read_json('data.json')
processed = df[['id', 'name', 'email']]  # May fail if columns missing

# CORRECT: Validate schema before processing
def validate_schema(df, expected_columns):
    missing = set(expected_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return True
```

### 2. **Breaking Changes in Production**
```python
# WRONG: Hard-coded field mappings
def process_user(user):
    name = user['name']  # KeyError if field renamed to 'full_name'
    email = user['email']  # KeyError if field removed

# CORRECT: Safe field access with defaults
def process_user_safely(user):
    name = user.get('name') or user.get('full_name') or 'Unknown'
    email = user.get('email') or user.get('email_address') or None
```

### 3. **Schema Inference Memory Explosion**
```python
# WRONG: Loading entire dataset for schema inference
df = pd.read_json('10gb_file.json')  # Crashes on 8GB RAM
schema = df.dtypes

# CORRECT: Sample-based schema inference
def infer_schema_safely(file_path, sample_size=1000):
    with open(file_path) as f:
        sample = [json.loads(next(f)) for _ in range(sample_size)]
    df_sample = pd.DataFrame(sample)
    return df_sample.dtypes
```

### 4. **Parquet Schema Evolution Pitfalls**
```python
# WRONG: Writing Parquet without schema tracking
df.to_parquet('data.parquet')  # Loses schema version info

# CORRECT: Store schema metadata
import pyarrow as pa

table = pa.Table.from_pandas(df)
schema_metadata = {
    'schema_version': '1.2.0',
    'created_at': datetime.now().isoformat(),
    'fields': str(table.schema)
}
table = table.replace_schema_metadata(schema_metadata)
pq.write_table(table, 'data.parquet')
```

### 5. **Backward Compatibility Assumptions**
```python
# WRONG: Assuming all changes are backward compatible
def migrate_v1_to_v2(data):
    # Adds new field 'category'
    data['category'] = 'default'  # Breaks if v1 code reads v2 data
    
# CORRECT: Test backward compatibility
def is_backward_compatible(old_schema, new_schema):
    # All fields in old schema must exist in new schema with same type
    for field in old_schema.fields:
        if field.name not in new_schema.names:
            return False
        if old_schema.field(field.name).type != new_schema.field(field.name).type:
            return False
    return True
```

## 🏆 Best Practices

### 1. **Schema Validation Strategy**

#### Early Validation
```python
def validate_incoming_data(data, schema_registry):
    """Validate data as early as possible in the pipeline."""
    schema = schema_registry.get_latest_schema('users')
    
    errors = []
    for record in data:
        # Check required fields
        for field in schema.required_fields:
            if field not in record:
                errors.append(f"Missing required field: {field}")
        
        # Check data types
        for field, expected_type in schema.field_types.items():
            if field in record:
                actual_type = type(record[field]).__name__
                if actual_type != expected_type:
                    errors.append(f"Type mismatch for {field}: {actual_type} != {expected_type}")
    
    if errors:
        raise ValidationError(f"Schema validation failed: {errors}")
```

#### Schema Sampling for Large Datasets
```python
def validate_large_dataset(file_path, schema, sample_rate=0.01):
    """Validate large datasets using statistical sampling."""
    import random
    
    with open(file_path) as f:
        total_lines = sum(1 for _ in f)
    
    sample_size = max(100, int(total_lines * sample_rate))
    sample_indices = random.sample(range(total_lines), sample_size)
    
    with open(file_path) as f:
        for i, line in enumerate(f):
            if i in sample_indices:
                record = json.loads(line)
                validate_record(record, schema)
    
    logger.info(f"Validated {sample_size} samples from {total_lines} records")
```

### 2. **Schema Evolution Patterns**

#### Additive Changes (Safe)
```python
# Adding optional fields is backward compatible
new_schema = {
    **old_schema,
    'new_field': {'type': 'string', 'required': False, 'default': None}
}
```

#### Field Renaming (Requires Adapter)
```python
def create_field_mapping_adapter(old_to_new_mapping):
    """Create adapter for field renames."""
    def adapter(record):
        adapted = {}
        for old_field, new_field in old_to_new_mapping.items():
            if old_field in record:
                adapted[new_field] = record[old_field]
            elif new_field in record:
                adapted[new_field] = record[new_field]
        return adapted
    return adapter
```

#### Type Widening (Usually Safe)
```python
# int32 -> int64: Safe (widening)
# string -> int: Breaking (requires transformation)
# int -> string: Breaking (requires transformation)

def handle_type_widening(record, field, old_type, new_type):
    """Handle type widening conversions."""
    type_widening_rules = {
        ('int32', 'int64'): lambda x: int(x),
        ('float32', 'float64'): lambda x: float(x),
        ('string', 'text'): lambda x: str(x)
    }
    
    key = (old_type, new_type)
    if key in type_widening_rules:
        record[field] = type_widening_rules[key](record[field])
    else:
        raise TypeError(f"Cannot convert {old_type} to {new_type}")
```

### 3. **Data Contract Implementation**

#### Contract Definition
```python
@dataclass
class DataContract:
    name: str
    schema: Dict
    quality_rules: List[QualityRule]
    sla_hours: int
    alert_channels: List[str]
    
    def validate(self, data: pd.DataFrame) -> ValidationResult:
        """Validate data against contract."""
        result = ValidationResult()
        
        # Schema validation
        result.schema_violations = self._validate_schema(data)
        
        # Quality validation
        result.quality_violations = self._validate_quality(data)
        
        # SLA check
        result.sla_met = len(result.violations) == 0
        
        return result
    
    def generate_alert(self, violation: Violation):
        """Generate alert for contract violation."""
        message = f"""
        🚨 DATA CONTRACT VIOLATION 🚨
        Contract: {self.name}
        Violation: {violation.type}
        Field: {violation.field}
        Value: {violation.value}
        Timestamp: {datetime.now()}
        """
        
        for channel in self.alert_channels:
            self._send_alert(channel, message)
```

#### Contract Testing
```python
def test_data_contract():
    """Test data contract with various scenarios."""
    contract = DataContract(
        name="user_data",
        schema=USER_SCHEMA,
        quality_rules=[NOT_NULL_RULE, EMAIL_FORMAT_RULE],
        sla_hours=24
    )
    
    # Test valid data
    valid_data = pd.DataFrame([...])
    result = contract.validate(valid_data)
    assert result.sla_met == True
    
    # Test invalid data
    invalid_data = pd.DataFrame([...])
    result = contract.validate(invalid_data)
    assert result.sla_met == False
    assert len(result.violations) > 0
```

### 4. **Memory-Efficient Schema Processing (8GB RAM)**

#### Chunked Schema Validation
```python
def validate_large_file_chunked(file_path, schema, chunk_size=10000):
    """Validate large files in chunks to stay within memory limits."""
    import pandas as pd
    
    chunk_iterator = pd.read_json(file_path, lines=True, chunksize=chunk_size)
    
    results = []
    for i, chunk in enumerate(chunk_iterator):
        logger.info(f"Processing chunk {i} ({len(chunk)} records)")
        
        # Validate chunk
        chunk_result = validate_chunk(chunk, schema)
        results.append(chunk_result)
        
        # Check memory usage
        if get_memory_usage_mb() > 6000:  # 6GB threshold
            logger.warning("Memory usage high, reducing chunk size")
            chunk_size = max(1000, chunk_size // 2)
    
    return aggregate_results(results)
```

#### Streaming Schema Detection
```python
def detect_schema_streaming(file_path, max_samples=1000):
    """Detect schema from streaming data without loading everything."""
    schema_candidates = []
    
    with open(file_path) as f:
        for i, line in enumerate(f):
            if i >= max_samples:
                break
                
            record = json.loads(line)
            schema_candidates.append(infer_record_schema(record))
    
    # Merge schemas
    merged_schema = merge_schemas(schema_candidates)
    return merged_schema
```

### 5. **Schema Registry Best Practices**

#### Schema Versioning
```python
class SchemaVersion:
    def __init__(self, version: str, schema: Dict, compatibility: str):
        self.version = version
        self.schema = schema
        self.compatibility = compatibility  # BACKWARD, FORWARD, FULL, NONE
        self.created_at = datetime.now()
        self.deprecated = False
    
    def is_compatible_with(self, other: 'SchemaVersion') -> bool:
        """Check compatibility between schema versions."""
        if self.compatibility == 'NONE' or other.compatibility == 'NONE':
            return False
        
        # Implement compatibility checking logic
        return check_schema_compatibility(self.schema, other.schema)
```

#### Schema Migration Coordination
```python
def coordinate_schema_migration(
    old_schema: SchemaVersion,
    new_schema: SchemaVersion,
    data_paths: List[str]
) -> MigrationPlan:
    """Coordinate schema migration across multiple data sources."""
    
    plan = MigrationPlan(
        old_version=old_schema.version,
        new_version=new_schema.version,
        steps=[]
    )
    
    # 1. Validate compatibility
    if not new_schema.is_compatible_with(old_schema):
        plan.steps.append("⚠️ Breaking change detected - requires downtime")
    
    # 2. Create migration scripts
    plan.steps.extend(generate_migration_scripts(old_schema, new_schema))
    
    # 3. Schedule migration
    plan.steps.append("Schedule migration during maintenance window")
    
    # 4. Test migration
    plan.steps.append("Test migration on sample data")
    
    # 5. Execute migration
    plan.steps.append("Execute migration with rollback plan")
    
    return plan
```

## 🔧 Optimization Techniques for 8GB RAM

### 1. **Schema Compression**
```python
def compress_schema(schema: Dict) -> bytes:
    """Compress schema representation for storage."""
    import pickle
    import zlib
    
    # Convert to efficient representation
    simplified = {
        'fields': list(schema.keys()),
        'types': [str(type) for type in schema.values()],
        'required': [field for field, spec in schema.items() if spec.get('required', False)]
    }
    
    # Compress
    pickled = pickle.dumps(simplified)
    compressed = zlib.compress(pickled)
    
    return compressed

def decompress_schema(compressed: bytes) -> Dict:
    """Decompress schema representation."""
    import pickle
    import zlib
    
    decompressed = zlib.decompress(compressed)
    simplified = pickle.loads(decompressed)
    
    # Reconstruct full schema
    schema = {}
    for field, type_str in zip(simplified['fields'], simplified['types']):
        schema[field] = {
            'type': type_str,
            'required': field in simplified['required']
        }
    
    return schema
```

### 2. **Incremental Schema Updates**
```python
def update_schema_incrementally(
    current_schema: Dict,
    new_samples: List[Dict],
    confidence_threshold: float = 0.95
) -> Dict:
    """Update schema incrementally based on new samples."""
    updated_schema = current_schema.copy()
    
    for sample in new_samples:
        for field, value in sample.items():
            if field not in updated_schema:
                # New field detected
                field_type = infer_type(value)
                updated_schema[field] = {
                    'type': field_type,
                    'required': False,  # New fields start as optional
                    'confidence': 0.5   # Low initial confidence
                }
            else:
                # Update field statistics
                current_type = updated_schema[field]['type']
                sample_type = infer_type(value)
                
                if current_type == sample_type:
                    # Increase confidence
                    updated_schema[field]['confidence'] = min(
                        1.0, updated_schema[field].get('confidence', 0.5) + 0.1
                    )
                else:
                    # Type conflict - decrease confidence
                    updated_schema[field]['confidence'] = max(
                        0.0, updated_schema[field].get('confidence', 0.5) - 0.2
                    )
    
    # Promote fields to required if confidence high
    for field, spec in updated_schema.items():
        if spec.get('confidence', 0) > confidence_threshold:
            spec['required'] = True
    
    return updated_schema
```

### 3. **Memory Monitoring During Schema Operations**
```python
def monitor_schema_operation_memory(operation_func, *args, **kwargs):
    """Monitor memory usage during schema operations."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    try:
        result = operation_func(*args, **kwargs)
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        
        logger.info(f"Operation used {memory_used:.1f}MB memory")
        
        if memory_used > 4000:  # 4GB threshold
            logger.warning(f"High memory usage: {memory_used:.1f}MB")
            # Suggest optimizations
            suggest_memory_optimizations(operation_func.__name__, memory_used)
        
        return result
        
    except MemoryError:
        logger.error("Memory limit exceeded during schema operation")
        # Implement fallback strategy
        return fallback_schema_operation(*args, **kwargs)
```

## 📊 Performance Benchmarks

### Expected Performance on 8GB RAM:
- **Schema validation**: 10,000-50,000 records/second with chunked processing
- **Schema detection**: 1,000-5,000 samples/second
- **Schema migration**: 1,000-10,000 records/second depending on complexity
- **Memory usage**: Should stay under 6GB peak for large datasets

### Optimization Impact:
| Technique | Memory Reduction | Speed Improvement |
|-----------|------------------|-------------------|
| Chunked validation | 80% | -20% |
| Schema sampling | 90% | +50% |
| Streaming detection | 95% | +100% |
| Schema compression | 60% | -10% |

## 🚀 Deployment Checklist

### Before Production:
- [ ] Implement comprehensive schema validation
- [ ] Set up schema registry with versioning
- [ ] Define data contracts for critical datasets
- [ ] Implement schema evolution detection and alerting
- [ ] Create migration scripts for common schema changes
- [ ] Test backward/forward compatibility
- [ ] Set up monitoring for schema drift
- [ ] Document schema evolution policies
- [ ] Train team on schema management procedures

### Monitoring Metrics to Track:
- Schema validation success/failure rates
- Schema drift detection frequency
- Migration execution times
- Memory usage during schema operations
- Alert volume by schema change type
- Data contract compliance rates

## 🎯 Key Takeaways

1. **Always validate schemas early** - Catch issues before they propagate
2. **Design for evolution** - Assume schemas will change and plan accordingly
3. **Use schema registries** - Centralize schema management and versioning
4. **Implement data contracts** - Formalize agreements between data producers and consumers
5. **Monitor schema drift** - Detect changes before they break pipelines
6. **Test compatibility** - Always test backward and forward compatibility
7. **Document everything** - Schema changes should be well-documented
8. **Have rollback plans** - Always be prepared to revert schema changes

By following these best practices, you'll build robust data pipelines that can handle schema evolution gracefully while staying within 8GB RAM constraints.