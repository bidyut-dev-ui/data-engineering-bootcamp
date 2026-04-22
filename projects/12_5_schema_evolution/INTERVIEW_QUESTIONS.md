# Schema Evolution & Data Contracts Interview Questions

## Overview
This document contains interview questions for schema evolution and data contracts, covering fundamental concepts, technical implementation, real-world scenarios, and best practices for handling schema changes in data pipelines.

## Core Concepts

### 1. **What is schema evolution and why is it important in data engineering?**
Schema evolution refers to the process of managing changes to data structure over time while maintaining compatibility with existing data and downstream consumers. It's critical because:
- Data sources evolve (APIs change, new features added)
- Business requirements change (new metrics, dimensions)
- Without proper schema evolution, pipelines break, causing data loss or corruption
- Enables agile development while maintaining data reliability

### 2. **Explain the difference between backward compatibility, forward compatibility, and full compatibility.**
- **Backward compatibility**: New schema can read data written with old schema (new code reads old data)
- **Forward compatibility**: Old schema can read data written with new schema (old code reads new data)
- **Full compatibility**: Both backward and forward compatibility (rare in practice)
- **Example**: Adding optional fields is backward compatible; removing required fields breaks backward compatibility

### 3. **What are data contracts and how do they differ from schema validation?**
Data contracts are formal agreements between data producers and consumers specifying:
- Schema structure (fields, types, constraints)
- Data quality expectations (completeness, accuracy, timeliness)
- Service level agreements (freshness, availability)
- Change management procedures (notification, deprecation periods)

**Difference**: Schema validation checks if data matches a schema; data contracts define the entire relationship including business rules, SLAs, and change protocols.

### 4. **Describe common schema evolution patterns and when to use each.**
1. **Schema-on-read**: Store raw data, apply schema during reading (flexible but complex queries)
2. **Schema-on-write**: Validate and enforce schema during ingestion (consistent but rigid)
3. **Schema versioning**: Store schema version with each record (explicit but requires version management)
4. **Schema registry**: Central repository for schemas with compatibility checks (enterprise-scale)
5. **Evolutionary database design**: Use database features (ALTER TABLE, migrations)

### 5. **How does Parquet handle schema evolution compared to JSON or Avro?**
- **Parquet**: Schema stored in file footer, supports adding columns (backward compatible), removing columns requires careful handling, type changes problematic
- **JSON**: Schema-less, maximum flexibility but no type safety, validation happens at application level
- **Avro**: Schema stored with data, supports rich evolution rules (default values, aliases), excellent for streaming
- **Comparison**: Avro best for evolution, Parquet for analytics, JSON for flexibility

## Technical Implementation

### 6. **How would you implement schema validation for a streaming data pipeline?**
```python
# Key components:
1. Schema registry integration (fetch latest schema)
2. Real-time validation (validate each message/record)
3. Dead-letter queue for invalid records
4. Metrics and alerts for schema violations
5. Automatic schema evolution detection
```

### 7. **Design a backward compatibility adapter for handling schema changes.**
```python
def adapt_v2_to_v1(v2_record):
    """Convert V2 schema (first_name, last_name, age) to V1 (name, email)"""
    return {
        'name': f"{v2_record.get('first_name', '')} {v2_record.get('last_name', '')}".strip(),
        'email': v2_record.get('email', 'unknown@example.com')  # Default value
    }
```
**Key considerations**: Default values, type conversions, field mappings, error handling for missing required fields.

### 8. **How would you implement a schema versioning system?**
```python
# Approach:
1. Store schema version with each record (metadata field)
2. Maintain schema registry (database or file-based)
3. Version migration scripts for each schema change
4. Compatibility checking between versions
5. Automated testing of all schema versions
```

### 9. **What strategies would you use for memory-efficient schema validation on 8GB RAM?**
```python
# Strategies:
1. Streaming validation (validate records one at a time)
2. Chunked processing (validate in manageable batches)
3. Sampling for large datasets (validate sample, extrapolate)
4. Use efficient validators (jsonschema with lazy validation)
5. Disk-based validation for extremely large datasets
```

### 10. **How would you implement automated schema migration for a production database?**
```python
# Steps:
1. Analyze current vs target schema differences
2. Generate migration plan (add/drop/rename columns, type changes)
3. Execute in stages (backup → migrate → verify → switch)
4. Maintain rollback capability
5. Monitor performance during migration
```

## Real-World Scenarios

### 11. **You discover a breaking schema change in production. The pipeline has been failing for 2 hours. What's your response plan?**
1. **Immediate**: Pause ingestion to prevent data loss
2. **Diagnosis**: Identify the change and affected systems
3. **Fix**: Implement adapter or update pipeline
4. **Recovery**: Reprocess failed data from checkpoint
5. **Prevention**: Add schema validation and alerts
6. **Post-mortem**: Document root cause and improve processes

### 12. **A new field appears in your data source unexpectedly. How do you handle it?**
**Options**:
- **Reject**: Fail pipeline (safe but disruptive)
- **Ignore**: Drop unexpected fields (lose data)
- **Store**: Add to metadata/extra columns (flexible but messy)
- **Adapt**: Map to existing schema if possible
- **Evolve**: Update schema to include new field

**Decision factors**: Data criticality, frequency of changes, downstream dependencies, business requirements.

### 13. **How would you design a schema registry for a microservices architecture?**
```python
# Architecture:
1. Central schema repository (Git, database, dedicated service)
2. Versioning with semantic versioning (major.minor.patch)
3. Compatibility checking (automated CI/CD)
4. Client libraries for schema validation
5. Change notification system (webhooks, events)
6. Access control and audit logging
```

### 14. **You need to merge data from multiple sources with different schemas. What's your approach?**
1. **Schema analysis**: Identify common fields and differences
2. **Canonical model**: Define target schema representing business entities
3. **Transformers**: Create source-specific adapters to canonical model
4. **Data quality**: Handle missing fields, type mismatches, value mappings
5. **Unified storage**: Store in flexible format (JSONB, variant) or normalized tables

### 15. **How do you handle schema evolution in a data warehouse with historical reporting requirements?**
**Challenges**: Historical queries must work across schema versions, performance impact of joins on evolved schemas.

**Solutions**:
- **Slowly changing dimensions**: Type 2 SCD for tracking changes
- **Versioned tables**: Separate table per schema version
- **Unified view**: View that handles schema differences
- **Data vault modeling**: Hub-satellite-link architecture for flexibility
- **Time travel**: Use database features (Snowflake, BigQuery)

## Performance & Optimization

### 16. **What are the performance implications of different schema evolution strategies?**
- **Schema-on-read**: Higher query latency, flexible storage
- **Schema-on-write**: Faster queries, ingestion bottleneck
- **Schema versioning**: Storage overhead, query complexity
- **Evolutionary databases**: Migration downtime, index rebuilding

### 17. **How would you benchmark schema evolution performance?**
```python
# Metrics to track:
1. Ingestion throughput with/without validation
2. Query performance across schema versions
3. Storage efficiency (compression, encoding)
4. Memory usage during validation
5. Recovery time from schema changes
```

### 18. **What optimization techniques would you use for schema evolution on 8GB RAM?**
```python
# Techniques:
1. Lazy validation (validate only when needed)
2. Columnar validation (validate column by column)
3. Sampling-based validation for large datasets
4. Disk-spill for large validation sets
5. Parallel validation across chunks
```

## Advanced Topics

### 19. **Explain how to implement schema evolution in a distributed data processing system (Spark, Flink).**
```python
# Spark example:
1. Use schema inference with sampling
2. Define schema evolution policy (mergeSchema=True)
3. Handle type conflicts with custom resolvers
4. Use Delta Lake or Iceberg for ACID transactions
5. Implement checkpointing for recovery
```

### 20. **How would you implement data quality checks as part of schema validation?**
```python
# Beyond schema:
1. Value range validation (min/max, allowed values)
2. Pattern matching (regex for emails, phones)
3. Referential integrity (foreign key checks)
4. Business rule validation (derived fields, calculations)
5. Statistical validation (distribution checks, outliers)
```

### 21. **Describe how to use machine learning for schema evolution prediction.**
```python
# ML approach:
1. Historical schema change analysis
2. Feature engineering (change frequency, impact)
3. Prediction model (will schema change soon?)
4. Recommendation system (suggest evolution strategy)
5. Anomaly detection (unexpected schema changes)
```

## Practical Exercises

### 22. **Write a function to detect schema drift between two datasets.**
```python
def detect_schema_drift(schema1, schema2):
    """Detect differences between two schemas"""
    added = set(schema2) - set(schema1)
    removed = set(schema1) - set(schema2)
    type_changes = {}
    
    for field in set(schema1) & set(schema2):
        if schema1[field] != schema2[field]:
            type_changes[field] = (schema1[field], schema2[field])
    
    return {
        'added_fields': list(added),
        'removed_fields': list(removed),
        'type_changes': type_changes,
        'is_breaking': bool(removed) or any(
            # Type changes that break compatibility
            not is_compatible_type_change(old, new)
            for old, new in type_changes.values()
        )
    }
```

### 23. **Create a schema evolution policy document for your team.**
```markdown
# Schema Evolution Policy

## 1. Change Classification
- **Minor**: Adding optional fields, documentation changes
- **Major**: Removing fields, changing required fields
- **Breaking**: Changing field types, removing required fields

## 2. Change Process
1. Proposal (RFC document)
2. Review (team + stakeholders)
3. Implementation (with backward compatibility)
4. Testing (all existing pipelines)
5. Deployment (gradual rollout)
6. Monitoring (metrics, alerts)

## 3. Compatibility Rules
- Backward compatibility required for 90 days
- Deprecation period: 30 days notice
- Versioning: Semantic versioning (major.minor.patch)
```

### 24. **Design an alert system for schema changes.**
```python
# Components:
1. Schema change detection (comparison with baseline)
2. Severity classification (breaking vs non-breaking)
3. Notification channels (email, Slack, PagerDuty)
4. Dashboard for schema health
5. Automated runbooks for common issues
```

## Behavioral & Design Questions

### 25. **How would you convince engineering teams to adopt data contracts?**
**Approach**:
1. **Pain points**: Show current issues (broken pipelines, data quality problems)
2. **Benefits**: Reduced incidents, faster development, better collaboration
3. **Ease of adoption**: Provide tools, templates, support
4. **Success stories**: Case studies from other teams/companies
5. **Metrics**: Track improvements (incident reduction, development velocity)

### 26. **Describe how you would prioritize schema evolution work.**
**Prioritization framework**:
1. **Impact**: Number of affected pipelines/users
2. **Urgency**: Is pipeline currently broken?
3. **Complexity**: Effort required for implementation
4. **Strategic alignment**: Supports key business initiatives
5. **Risk**: Potential for data loss or corruption

### 27. **How would you design a schema evolution training program for data engineers?**
**Curriculum**:
1. **Fundamentals**: Schema concepts, compatibility types
2. **Tools**: Schema registries, validation libraries
3. **Patterns**: Common evolution strategies
4. **Case studies**: Real-world examples
5. **Hands-on**: Implement schema evolution for sample pipeline
6. **Best practices**: Documentation, testing, monitoring

## Evaluation Rubric

### Technical Knowledge (40%)
- Understanding of schema evolution concepts
- Knowledge of tools and technologies
- Ability to design solutions for real problems

### Problem Solving (30%)
- Logical approach to schema challenges
- Consideration of trade-offs and constraints
- Creative solutions for complex scenarios

### Communication (20%)
- Clear explanation of concepts
- Ability to document and present solutions
- Collaboration with stakeholders

### Practical Experience (10%)
- Hands-on experience with schema evolution
- Understanding of production considerations
- Best practices and lessons learned

## Recommended Resources

### Books & Articles
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "The Data Warehouse Toolkit" by Ralph Kimball
- "Building Evolutionary Architectures" by Neal Ford et al.
- Confluent Schema Registry documentation
- Apache Avro documentation

### Tools & Technologies
- **Schema Registries**: Confluent Schema Registry, AWS Glue Schema Registry
- **Validation**: JSON Schema, Pydantic, Great Expectations
- **Formats**: Avro, Parquet, Protocol Buffers
- **Databases**: PostgreSQL (JSONB), Snowflake (Variant), BigQuery

### Practice Platforms
- LeetCode (database problems)
- HackerRank (SQL challenges)
- Real-world projects with schema evolution requirements

## Preparation Tips

1. **Understand the fundamentals**: Schema evolution patterns, compatibility types
2. **Practice with tools**: Implement schema validation and evolution
3. **Study real cases**: How companies handle schema changes
4. **Prepare examples**: From your experience with schema challenges
5. **Think about trade-offs**: Flexibility vs consistency, performance vs safety

---

*This document provides comprehensive interview questions for schema evolution and data contracts. Use it to prepare for interviews or to evaluate candidates' understanding of these critical data engineering concepts.*