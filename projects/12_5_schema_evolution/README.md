# Week 12.5: Schema Evolution & Data Contracts

**Goal**: Learn how to handle data when the structure changes (because it always does).

## Why This Matters
Upstream teams change APIs without telling you. If your pipeline expects `name` but gets `first_name`, your pipeline crashes. A robust pipeline detects this and adapts (or alerts).

## Scenario
Your pipeline consumes user data. 
- **Yesterday (V1)**: Data had `name` and `email`.
- **Today (V2)**: Data has `first_name`, `last_name`, and `age`. `email` is gone.
- **Task**: Detect the break and write an adapter to fix it.

## Concepts Covered
1. **Schema Validation**: Checking if required columns exist.
2. **Backward Compatibility**: Can the new data fit into the old table?
3. **Evolution Strategies**:
   - **Reject**: Fail the pipeline (Safe).
   - **Adapt**: Transform new schema to old (Flexible).
   - **Evolve**: Update the destination table (Complex).

## Instructions

### 1. Setup
```bash
cd projects/12_5_schema_evolution
```

### 2. Generate Data
Create V1 (Old) and V2 (New) JSON files.
```bash
python generate_data.py
```

### 3. Run Pipeline
Run the validation script. It will process V1, fail on V2, and then apply a fix.
```bash
python validate_schema.py
```

**Expected Output**:
- V1: Success.
- V2: "CRITICAL ALERT: Schema changed!"
- Fix: "Detected new schema... Adapting..." -> Success.

## Interview Questions

**Q: What is a "Data Contract"?**
A: An agreement between data producers and consumers about the schema, quality, and SLA of the data. If the producer breaks it, they are responsible.

**Q: How do you handle a "Breaking Change" in a production pipeline?**
A: 
1. **Alert**: Notify the team immediately.
2. **Pause**: Stop ingestion to prevent bad data.
3. **Backfill**: Once the parser is updated, re-process the failed data.

**Q: Parquet vs JSON for schema evolution?**
A: Parquet stores schema in the footer, making evolution tricky (need to merge schemas). JSON is schema-less, so it's flexible but dangerous (no type safety).

## Homework / Challenge
1. Use `pydantic` to define a strict schema model and validate the JSONs against it.
2. Write a script that automatically detects *new* columns and adds them to a `metadata` JSON column instead of failing.
