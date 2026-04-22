#!/usr/bin/env python3
"""
Schema Evolution Practice Exercises

This module contains exercises for practicing schema evolution techniques,
data contract implementation, and handling breaking changes in data pipelines.
Focus on 8GB RAM optimization and production-ready implementations.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Exercise 1: Basic Schema Validation
def exercise_1_basic_schema_validation() -> Dict[str, Any]:
    """
    Implement a function that validates JSON data against a schema.
    
    Requirements:
    1. Check required fields exist
    2. Validate data types
    3. Return validation results with error messages
    4. Handle nested structures
    
    Returns:
        Dict with validation results
    """
    schema = {
        "user_id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "email": {"type": "string", "required": True, "pattern": r".+@.+\..+"},
        "age": {"type": "integer", "required": False, "min": 0, "max": 150},
        "metadata": {"type": "object", "required": False}
    }
    
    test_data = [
        {"user_id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
        {"user_id": 2, "name": "Bob", "email": "invalid-email", "age": 200},  # Invalid
        {"user_id": 3, "name": "Charlie"},  # Missing email
        {"user_id": "four", "name": "David", "email": "david@example.com"}  # Wrong type
    ]
    
    # TODO: Implement validation function
    def validate_data_against_schema(data: Dict, schema: Dict) -> Dict[str, Any]:
        """
        Validate a single data record against the schema.
        """
        errors = []
        
        # Your implementation here
        # Check required fields
        # Validate types
        # Check constraints (min/max, patterns)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "data": data
        }
    
    results = []
    for data in test_data:
        result = validate_data_against_schema(data, schema)
        results.append(result)
    
    return {
        "exercise": "Basic Schema Validation",
        "schema": schema,
        "test_data": test_data,
        "validation_results": results,
        "hint": "Consider using recursive validation for nested structures"
    }

# Exercise 2: Schema Evolution Detection
def exercise_2_schema_evolution_detection() -> Dict[str, Any]:
    """
    Detect schema changes between two datasets.
    
    Requirements:
    1. Compare schemas of old and new data
    2. Identify added, removed, and changed columns
    3. Detect type changes
    4. Calculate schema compatibility score
    
    Returns:
        Dict with schema comparison results
    """
    # Old schema (what pipeline expects)
    old_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25}
    ]
    
    # New schema (what actually arrived)
    new_data = [
        {"id": 3, "first_name": "Charlie", "last_name": "Brown", "email": "charlie@example.com", "age": 35, "department": "Engineering"},
        {"id": 4, "first_name": "Diana", "last_name": "Prince", "email": "diana@example.com", "age": 28, "department": "Sales"}
    ]
    
    # TODO: Implement schema comparison
    def compare_schemas(old_data: List[Dict], new_data: List[Dict]) -> Dict[str, Any]:
        """
        Compare schemas between old and new datasets.
        """
        # Extract schemas
        # Compare columns, types, required/optional
        # Calculate compatibility
        
        return {
            "added_columns": [],
            "removed_columns": [],
            "type_changes": [],
            "compatibility_score": 0.0,
            "breaking_changes": [],
            "non_breaking_changes": []
        }
    
    comparison = compare_schemas(old_data, new_data)
    
    return {
        "exercise": "Schema Evolution Detection",
        "old_data_sample": old_data,
        "new_data_sample": new_data,
        "schema_comparison": comparison,
        "hint": "Consider using pandas DataFrame dtypes for type detection"
    }

# Exercise 3: Backward Compatibility Adapter
def exercise_3_backward_compatibility_adapter() -> Dict[str, Any]:
    """
    Create an adapter to handle schema evolution while maintaining backward compatibility.
    
    Requirements:
    1. Transform new schema to match old schema
    2. Handle missing fields with defaults
    3. Combine split fields (e.g., first_name + last_name -> name)
    4. Log schema changes for monitoring
    
    Returns:
        Dict with transformation results
    """
    # Target schema (what downstream systems expect)
    target_schema = {
        "id": "integer",
        "full_name": "string",
        "email": "string",
        "age": "integer",
        "signup_date": "datetime"
    }
    
    # New incoming data with different schema
    incoming_data = [
        {
            "user_id": 101,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john.doe@company.com",
            "years_old": 42,
            "registration_timestamp": "2023-01-15T10:30:00Z"
        },
        {
            "user_id": 102,
            "first_name": "Jane",
            "last_name": "Smith",
            "email_address": "jane.smith@company.com",
            "years_old": 35
            # Missing registration_timestamp
        }
    ]
    
    # TODO: Implement adapter
    def adapt_to_target_schema(data: Dict, target_schema: Dict) -> Dict:
        """
        Adapt incoming data to match target schema.
        """
        adapted = {}
        
        # Your implementation here
        # Map fields: user_id -> id
        # Combine first_name + last_name -> full_name
        # Map email_address -> email
        # Map years_old -> age
        # Map registration_timestamp -> signup_date
        # Handle missing fields with defaults
        
        return adapted
    
    adapted_results = []
    for record in incoming_data:
        adapted = adapt_to_target_schema(record, target_schema)
        adapted_results.append(adapted)
    
    return {
        "exercise": "Backward Compatibility Adapter",
        "target_schema": target_schema,
        "incoming_data": incoming_data,
        "adapted_results": adapted_results,
        "hint": "Use field mapping dictionaries and default values for missing fields"
    }

# Exercise 4: Schema Versioning System
def exercise_4_schema_versioning_system() -> Dict[str, Any]:
    """
    Implement a simple schema versioning system.
    
    Requirements:
    1. Store schema versions with metadata
    2. Track evolution history
    3. Support schema migration scripts
    4. Validate data against specific schema versions
    
    Returns:
        Dict with versioning system demonstration
    """
    # TODO: Implement SchemaVersion class
    class SchemaVersion:
        def __init__(self, version: str, schema: Dict, description: str):
            self.version = version
            self.schema = schema
            self.description = description
            self.created_at = datetime.now()
        
        def validate(self, data: Dict) -> bool:
            """Validate data against this schema version."""
            # Your implementation
            return True
        
        def migrate_from(self, old_version: 'SchemaVersion', data: Dict) -> Dict:
            """Migrate data from old schema version to this one."""
            # Your implementation
            return data
    
    # Define schema versions
    v1_schema = {
        "user": {"type": "string", "required": True},
        "email": {"type": "string", "required": True}
    }
    
    v2_schema = {
        "user_id": {"type": "integer", "required": True},
        "username": {"type": "string", "required": True},
        "email": {"type": "string", "required": True},
        "created_at": {"type": "datetime", "required": False}
    }
    
    v1 = SchemaVersion("1.0", v1_schema, "Initial schema with user and email")
    v2 = SchemaVersion("2.0", v2_schema, "Added user_id, renamed user to username, added created_at")
    
    # Test migration
    v1_data = {"user": "alice123", "email": "alice@example.com"}
    
    return {
        "exercise": "Schema Versioning System",
        "schema_versions": [
            {"version": v1.version, "description": v1.description},
            {"version": v2.version, "description": v2.description}
        ],
        "migration_demo": {
            "v1_data": v1_data,
            "v2_data_after_migration": v2.migrate_from(v1, v1_data) if hasattr(v2, 'migrate_from') else "Not implemented"
        },
        "hint": "Consider using a registry pattern for schema versions"
    }

# Exercise 5: Data Contract Implementation
def exercise_5_data_contract_implementation() -> Dict[str, Any]:
    """
    Implement a data contract system with validation, alerts, and SLAs.
    
    Requirements:
    1. Define data contracts with schema, quality rules, and SLAs
    2. Validate incoming data against contracts
    3. Generate alerts for contract violations
    4. Track compliance metrics
    
    Returns:
        Dict with contract validation results
    """
    # TODO: Implement DataContract class
    class DataContract:
        def __init__(self, name: str, schema: Dict, quality_rules: List[Dict], sla_hours: int = 24):
            self.name = name
            self.schema = schema
            self.quality_rules = quality_rules
            self.sla_hours = sla_hours
            self.violations = []
        
        def validate(self, data: List[Dict]) -> Dict[str, Any]:
            """Validate data against contract."""
            results = {
                "passed": True,
                "violations": [],
                "compliance_rate": 0.0
            }
            
            # Your implementation
            # Check schema compliance
            # Check quality rules
            # Calculate compliance rate
            
            return results
        
        def generate_alert(self, violation: Dict) -> str:
            """Generate alert message for contract violation."""
            return f"ALERT: Data contract '{self.name}' violation: {violation}"
    
    # Define a contract
    user_contract = DataContract(
        name="user_data_contract",
        schema={
            "id": {"type": "integer", "required": True},
            "name": {"type": "string", "required": True, "min_length": 1},
            "email": {"type": "string", "required": True, "pattern": r".+@.+\..+"},
            "age": {"type": "integer", "required": False, "min": 0, "max": 120}
        },
        quality_rules=[
            {"field": "email", "rule": "not_null", "description": "Email must not be null"},
            {"field": "age", "rule": "range", "min": 0, "max": 120, "description": "Age must be between 0 and 120"}
        ],
        sla_hours=24
    )
    
    test_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
        {"id": 2, "name": "Bob", "email": None, "age": 150},  # Violation: null email, age out of range
        {"id": 3, "name": "", "email": "charlie@example.com"}  # Violation: empty name
    ]
    
    validation_results = user_contract.validate(test_data) if hasattr(user_contract, 'validate') else {"status": "Not implemented"}
    
    return {
        "exercise": "Data Contract Implementation",
        "contract": {
            "name": user_contract.name,
            "sla_hours": user_contract.sla_hours,
            "schema_fields": list(user_contract.schema.keys()),
            "quality_rules": user_contract.quality_rules
        },
        "test_data": test_data,
        "validation_results": validation_results,
        "hint": "Consider integrating with monitoring systems like Prometheus for metrics"
    }

# Exercise 6: Schema Evolution in Parquet Files
def exercise_6_schema_evolution_in_parquet() -> Dict[str, Any]:
    """
    Handle schema evolution when reading/writing Parquet files.
    
    Requirements:
    1. Read Parquet files with evolving schemas
    2. Merge schemas from multiple files
    3. Write Parquet with schema evolution support
    4. Handle backward/forward compatibility
    
    Returns:
        Dict with Parquet schema evolution results
    """
    import pyarrow as pa
    import pyarrow.parquet as pq
    
    # TODO: Implement schema evolution for Parquet
    def read_parquet_with_schema_evolution(file_paths: List[str]) -> pd.DataFrame:
        """
        Read multiple Parquet files with potentially different schemas.
        """
        # Your implementation
        # Read each file
        # Detect schema differences
        # Merge schemas
        # Combine data
        
        return pd.DataFrame()
    
    def write_parquet_with_schema_tracking(df: pd.DataFrame, file_path: str, schema_version: str):
        """
        Write DataFrame to Parquet with schema version tracking.
        """
        # Your implementation
        # Add schema version metadata
        # Write with proper schema evolution settings
        
        pass
    
    # Simulate schema evolution scenario
    schema_v1 = pa.schema([
        pa.field("id", pa.int64()),
        pa.field("name", pa.string()),
        pa.field("value", pa.float64())
    ])
    
    schema_v2 = pa.schema([
        pa.field("id", pa.int64()),
        pa.field("name", pa.string()),
        pa.field("value", pa.float64()),
        pa.field("category", pa.string())  # New field
    ])
    
    return {
        "exercise": "Schema Evolution in Parquet Files",
        "schema_v1": str(schema_v1),
        "schema_v2": str(schema_v2),
        "schema_differences": {
            "added_fields": ["category"],
            "removed_fields": [],
            "type_changes": []
        },
        "hint": "PyArrow's schema merging and metadata storage capabilities are useful here"
    }

# Exercise 7: Memory-Efficient Schema Validation for Large Datasets
def exercise_7_memory_efficient_schema_validation() -> Dict[str, Any]:
    """
    Implement schema validation that works within 8GB RAM constraints.
    
    Requirements:
    1. Process data in chunks to avoid memory overflow
    2. Stream validation for large files
    3. Early termination on critical errors
    4. Memory usage monitoring
    
    Returns:
        Dict with memory-efficient validation results
    """
    # Generate large dataset simulation
    def generate_large_dataset(num_records: int = 100000) -> List[Dict]:
        """Generate a large dataset for testing."""
        data = []
        for i in range(num_records):
            data.append({
                "id": i,
                "name": f"User_{i}",
                "email": f"user_{i}@example.com",
                "age": np.random.randint(18, 80),
                "score": np.random.random() * 100
            })
        return data
    
    schema = {
        "id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "email": {"type": "string", "required": True, "pattern": r".+@.+\..+"},
        "age": {"type": "integer", "required": True, "min": 0, "max": 150},
        "score": {"type": "float", "required": False, "min": 0, "max": 100}
    }
    
    # TODO: Implement chunked validation
    def validate_large_dataset_chunked(data_generator, schema: Dict, chunk_size: int = 1000) -> Dict[str, Any]:
        """
        Validate large dataset in chunks to stay within memory limits.
        """
        results = {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "errors_by_type": {},
            "memory_usage_mb": 0
        }
        
        # Your implementation
        # Process in chunks
        # Track memory usage
        # Aggregate results
        
        return results
    
    return {
        "exercise": "Memory-Efficient Schema Validation",
        "schema": schema,
        "dataset_size": "100,000 records (simulated)",
        "chunk_size_recommendation": "1000 records per chunk",
        "memory_optimization_strategies": [
            "Process data in chunks",
            "Use streaming validation",
            "Clear references between chunks",
            "Monitor memory usage with psutil"
        ],
        "hint": "Consider using generators instead of loading all data at once"
    }

# Exercise 8: Schema Registry Integration
def exercise_8_schema_registry_integration() -> Dict[str, Any]:
    """
    Simulate integration with a schema registry (like Confluent Schema Registry).
    
    Requirements:
    1. Register new schemas
    2. Check schema compatibility
    3. Retrieve schemas by version
    4. Handle schema evolution policies
    
    Returns:
        Dict with schema registry operations
    """
    # TODO: Implement simple schema registry
    class SimpleSchemaRegistry:
        def __init__(self):
            self.schemas = {}  # subject -> {version -> schema}
            self.compatibility_policy = "BACKWARD"  # BACKWARD, FORWARD, FULL, NONE
        
        def register_schema(self, subject: str, schema: Dict) -> int:
            """Register a new schema version."""
            # Your implementation
            return 1  # version
        
        def check_compatibility(self, subject: str, new_schema: Dict, version: int = -1) -> bool:
            """Check if new schema is compatible with existing."""
            # Your implementation
            return True
        
        def get_schema(self, subject: str, version: int = -1) -> Optional[Dict]:
            """Get schema by version (latest if -1)."""
            # Your implementation
            return None
    
    registry = SimpleSchemaRegistry()
    
    user_schema_v1 = {
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"},
            {"name": "email", "type": "string"}
        ]
    }
    
    user_schema_v2 = {
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "first_name", "type": "string"},  # Breaking change
            {"name": "last_name", "type": "string"},   # Breaking change
            {"name": "email", "type": "string"}
        ]
    }
    
    return {
        "exercise": "Schema Registry Integration",
        "schema_registry_operations": [
            "register_schema('users', user_schema_v1)",
            "register_schema('users', user_schema_v2)",
            "check_compatibility('users', user_schema_v2)",
            "get_schema('users', version=1)"
        ],
        "compatibility_policies": [
            "BACKWARD: New schema can read data written with old schema",
            "FORWARD: Old schema can read data written with new schema",
            "FULL: Both backward and forward compatible",
            "NONE: No compatibility checks"
        ],
        "hint": "Real schema registries use Avro, Protobuf, or JSON Schema formats"
    }

# Exercise 9: Automated Schema Migration
def exercise_9_automated_schema_migration() -> Dict[str, Any]:
    """
    Create automated schema migration scripts for production pipelines.
    
    Requirements:
    1. Generate migration scripts based on schema diff
    2. Support rollback capabilities
    3. Test migrations on sample data
    4. Generate migration documentation
    
    Returns:
        Dict with migration automation results
    """
    # Schema definitions
    old_schema = {
        "table": "users",
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "username", "type": "VARCHAR(50)", "nullable": False},
            {"name": "email", "type": "VARCHAR(100)", "nullable": False},
            {"name": "created_at", "type": "TIMESTAMP", "nullable": True}
        ]
    }
    
    new_schema = {
        "table": "users",
        "columns": [
            {"name": "id", "type": "BIGINT", "nullable": False},  # Type change
            {"name": "username", "type": "VARCHAR(100)", "nullable": False},  # Length increase
            {"name": "email", "type": "VARCHAR(255)", "nullable": False},  # Length increase
            {"name": "full_name", "type": "VARCHAR(150)", "nullable": True},  # New column
            {"name": "created_at", "type": "TIMESTAMP", "nullable": False},  # Nullable change
            {"name": "updated_at", "type": "TIMESTAMP", "nullable": True}  # New column
        ]
    }
    
    # TODO: Generate migration SQL
    def generate_migration_sql(old_schema: Dict, new_schema: Dict) -> List[str]:
        """Generate SQL migration statements."""
        statements = []
        
        # Your implementation
        # Compare schemas
        # Generate ALTER TABLE statements
        # Handle type changes, new columns, removed columns
        
        statements.append("-- Migration from v1 to v2")
        statements.append("ALTER TABLE users ALTER COLUMN id TYPE BIGINT;")
        statements.append("ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(100);")
        statements.append("ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255);")
        statements.append("ALTER TABLE users ADD COLUMN full_name VARCHAR(150);")
        statements.append("ALTER TABLE users ALTER COLUMN created_at SET NOT NULL;")
        statements.append("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP;")
        
        return statements
    
    migration_sql = generate_migration_sql(old_schema, new_schema)
    
    return {
        "exercise": "Automated Schema Migration",
        "old_schema": old_schema,
        "new_schema": new_schema,
        "migration_sql": migration_sql,
        "rollback_sql": [
            "-- Rollback from v2 to v1",
            "ALTER TABLE users ALTER COLUMN id TYPE INTEGER;",
            "ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(50);",
            "ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(100);",
            "ALTER TABLE users DROP COLUMN full_name;",
            "ALTER TABLE users ALTER COLUMN created_at DROP NOT NULL;",
            "ALTER TABLE users DROP COLUMN updated_at;"
        ],
        "hint": "Always test migrations on staging first and have rollback scripts ready"
    }

# Exercise 10: End-to-End Schema Evolution Pipeline
def exercise_10_end_to_end_schema_evolution_pipeline() -> Dict[str, Any]:
    """
    Build a complete schema evolution pipeline with monitoring and alerting.
    
    Requirements:
    1. Schema detection and validation
    2. Automatic adaptation or alerting
    3. Version tracking and migration
    4. Monitoring and metrics collection
    
    Returns:
        Dict with pipeline design and components
    """
    # Pipeline components
    pipeline_design = {
        "components": [
            {
                "name": "Schema Detector",
                "purpose": "Detect schema changes in incoming data",
                "implementation": "Statistical sampling + schema inference"
            },
            {
                "name": "Compatibility Checker",
                "purpose": "Check if new schema is compatible with existing",
                "implementation": "Schema registry + compatibility rules"
            },
            {
                "name": "Adapter Engine",
                "purpose": "Transform data to match expected schema",
                "implementation": "Rule-based transformations + ML suggestions"
            },
            {
                "name": "Alert Manager",
                "purpose": "Notify stakeholders of breaking changes",
                "implementation": "Slack/Email/PagerDuty integration"
            },
            {
                "name": "Migration Orchestrator",
                "purpose": "Coordinate schema migrations across systems",
                "implementation": "Workflow engine + version tracking"
            },
            {
                "name": "Monitoring Dashboard",
                "purpose": "Track schema evolution metrics",
                "implementation": "Grafana + Prometheus metrics"
            }
        ],
        "workflow": [
            "1. Ingest new data batch",
            "2. Detect schema (compare with expected)",
            "3. If compatible: process normally",
            "4. If incompatible but adaptable: apply transformations",
            "5. If breaking change: trigger alerts",
            "6. Update schema registry if change is accepted",
            "7. Monitor impact on downstream systems"
        ],
        "optimization_for_8gb_ram": [
            "Process data in streaming fashion",
            "Use efficient schema comparison algorithms",
            "Cache frequently used schemas",
            "Limit schema history retention",
            "Compress schema representations"
        ]
    }
    
    # TODO: Implement a simple pipeline
    class SchemaEvolutionPipeline:
        def __init__(self):
            self.schema_registry = {}
            self.alert_threshold = 0.1  # 10% schema drift
            
        def process_data(self, data: List[Dict], expected_schema_id: str) -> Dict[str, Any]:
            """Process data through the schema evolution pipeline."""
            result = {
                "status": "unknown",
                "schema_changes": [],
                "adaptations_applied": [],
                "alerts_generated": []
            }
            
            # Your implementation
            # 1. Detect schema
            # 2. Check compatibility
            # 3. Apply adaptations if needed
            # 4. Generate alerts if breaking
            
            return result
    
    pipeline = SchemaEvolutionPipeline()
    
    return {
        "exercise": "End-to-End Schema Evolution Pipeline",
        "pipeline_design": pipeline_design,
        "implementation_status": "Conceptual design provided",
        "key_considerations": [
            "Backward compatibility vs. innovation",
            "Performance impact of schema validation",
            "Monitoring and observability",
            "Team communication and coordination",
            "Testing strategy for schema changes"
        ],
        "hint": "Start with simple rule-based detection and gradually add ML-based suggestions"
    }

def main():
    """Run all exercises and print summaries."""
    exercises = [
        exercise_1_basic_schema_validation,
        exercise_2_schema_evolution_detection,
        exercise_3_backward_compatibility_adapter,
        exercise_4_schema_versioning_system,
        exercise_5_data_contract_implementation,
        exercise_6_schema_evolution_in_parquet,
        exercise_7_memory_efficient_schema_validation,
        exercise_8_schema_registry_integration,
        exercise_9_automated_schema_migration,
        exercise_10_end_to_end_schema_evolution_pipeline
    ]
    
    print("Schema Evolution Practice Exercises")
    print("=" * 50)
    
    for i, exercise_func in enumerate(exercises, 1):
        print(f"\nExercise {i}: {exercise_func.__name__.replace('exercise_', '').replace('_', ' ').title()}")
        print("-" * 50)
        
        try:
            result = exercise_func()
            print(f"✓ Exercise loaded successfully")
            print(f"  Description: {result.get('exercise', 'No description')}")
            
            if 'hint' in result:
                print(f"  Hint: {result['hint']}")
                
        except Exception as e:
            print(f"✗ Error in exercise: {e}")
    
    print("\n" + "=" * 50)
    print("All exercises loaded. Implement the TODO sections to complete each exercise.")
    print("Focus on:")
    print("1. Schema validation and evolution detection")
    print("2. Backward compatibility strategies")
    print("3. Memory-efficient processing for 8GB RAM")
    print("4. Production-ready error handling and monitoring")

if __name__ == "__main__":
    main()