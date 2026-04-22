# Data Reliability Engineering Interview Questions

This document contains interview questions covering data reliability engineering concepts, ACID transactions, idempotency, error handling, and robust pipeline design.

## 📋 **Fundamental Concepts**

### 1. **What are ACID transactions and why are they important for data reliability?**

**Answer:** ACID stands for Atomicity, Consistency, Isolation, and Durability:
- **Atomicity**: Transactions are all-or-nothing. If any part fails, the entire transaction rolls back.
- **Consistency**: Transactions move the database from one valid state to another, preserving all constraints.
- **Isolation**: Concurrent transactions don't interfere with each other.
- **Durability**: Committed transactions survive system failures.

**Example**: In a payment processing system, ACID ensures that money is either fully transferred or not at all, preventing partial transfers.

### 2. **Explain idempotency in data pipelines. Why is it critical for reliable systems?**

**Answer:** Idempotency means that applying an operation multiple times produces the same result as applying it once. In data pipelines:
- **Why critical**: Retries, restarts, and duplicate messages are inevitable. Idempotent pipelines handle them safely.
- **Implementation**: Use upsert patterns (`ON CONFLICT` in SQL), deduplication keys, or idempotent APIs.
- **Example**: An idempotent payment processor won't double-charge if the same payment request arrives twice.

### 3. **What's the difference between `TRUNCATE` and `DELETE` in SQL?**

**Answer:**
- **`DELETE`**: Row-by-row operation, can be rolled back, respects foreign keys, slower for large tables.
- **`TRUNCATE`**: DDL operation, faster (drops data pages), cannot be rolled back in some databases, resets auto-increment counters.
- **Use case**: Use `DELETE` when you need transaction safety; use `TRUNCATE` for fast cleanup of staging tables.

### 4. **What are race conditions and how do you prevent them in data pipelines?**

**Answer:** Race conditions occur when multiple processes access shared data simultaneously, leading to unpredictable results.

**Prevention strategies:**
1. **Database locks** (pessimistic locking)
2. **Optimistic concurrency control** (version numbers, timestamps)
3. **Isolation levels** (SERIALIZABLE, REPEATABLE READ)
4. **Distributed locks** (Redis, ZooKeeper) for distributed systems
5. **Idempotent operations** to make race conditions harmless

### 5. **Explain the "exactly-once" vs "at-least-once" vs "at-most-once" delivery semantics.**

**Answer:**
- **At-most-once**: Messages may be lost but never duplicated. Simple but unreliable.
- **At-least-once**: Messages are never lost but may be duplicated. Requires deduplication.
- **Exactly-once**: Messages are processed exactly once. Requires idempotency and transactional guarantees.

**Trade-offs**: Exactly-once is hardest to implement but most reliable for financial systems.

## 🔧 **Implementation & Design**

### 6. **How would you design an idempotent data ingestion pipeline?**

**Answer:**
1. **Deduplication key**: Use a unique identifier (e.g., `message_id`, `transaction_id`) for each record.
2. **Upsert pattern**: Use `INSERT ... ON CONFLICT DO UPDATE` or `MERGE` statements.
3. **Staging tables**: Load to staging first, then deduplicate before moving to final table.
4. **Checkpointing**: Track processed records to skip duplicates on restart.
5. **Idempotent APIs**: Design APIs that produce the same result regardless of how many times called.

### 7. **What strategies would you use for handling large files on 8GB RAM?**

**Answer:**
1. **Chunked processing**: Read and process files in manageable chunks.
2. **Streaming**: Use generators/iterators instead of loading entire files.
3. **Database batch operations**: Use `executemany()` with appropriate batch sizes.
4. **Disk-based processing**: Use SQLite or pandas with `chunksize` parameter.
5. **Memory monitoring**: Track memory usage and adjust batch sizes dynamically.

### 8. **How do you implement checkpoint-based recovery for long-running ETL jobs?**

**Answer:**
1. **Checkpoint storage**: Use a database table or file to track progress.
2. **Atomic checkpoints**: Save checkpoints transactionally with data.
3. **Restart logic**: On restart, read last checkpoint and resume from that point.
4. **Example**: For file processing, track line numbers or file offsets.
5. **Considerations**: Ensure checkpoints are saved before marking data as processed.

### 9. **What's the difference between optimistic and pessimistic locking? When would you use each?**

**Answer:**
- **Pessimistic locking**: Assume conflicts will happen, lock resources upfront (e.g., `SELECT ... FOR UPDATE`). Use when contention is high.
- **Optimistic locking**: Assume conflicts are rare, detect them at commit time (e.g., version numbers). Use when contention is low.

**Example**: Use pessimistic locking for inventory systems where stock updates are frequent; use optimistic locking for user profile updates.

### 10. **How would you handle schema evolution in a production data pipeline?**

**Answer:**
1. **Backward compatibility**: New schemas should accept old data.
2. **Schema registry**: Central repository for schema definitions.
3. **Data versioning**: Include schema version with each record.
4. **Migration scripts**: Automated, idempotent schema migrations.
5. **A/B testing**: Deploy new schema alongside old, compare results.

## 🚨 **Error Handling & Recovery**

### 11. **What's a deadlock and how do you prevent it in database transactions?**

**Answer:** Deadlock occurs when two transactions wait for each other's locks indefinitely.

**Prevention strategies:**
1. **Lock ordering**: Always acquire locks in the same order.
2. **Timeout mechanisms**: Set transaction timeouts.
3. **Deadlock detection**: Let database detect and abort one transaction.
4. **Smaller transactions**: Reduce lock duration.
5. **Optimistic concurrency**: Avoid locks where possible.

### 12. **How do you design a retry mechanism for unreliable external APIs?**

**Answer:**
1. **Exponential backoff**: Increase wait time between retries (e.g., 1s, 2s, 4s, 8s).
2. **Jitter**: Add randomness to prevent thundering herd.
3. **Circuit breaker**: Stop retrying after repeated failures.
4. **Idempotent retries**: Ensure retries are safe.
5. **Logging**: Log retry attempts for monitoring.

### 13. **What monitoring would you implement for a production data pipeline?**

**Answer:**
1. **Success/failure rates**: Track pipeline completion status.
2. **Latency metrics**: Measure processing time per batch/record.
3. **Data quality metrics**: Record counts, null rates, value distributions.
4. **Resource usage**: CPU, memory, disk I/O.
5. **Alerting**: Set up alerts for failures, delays, or data anomalies.

### 14. **How do you ensure data consistency across distributed systems?**

**Answer:**
1. **Distributed transactions**: Use two-phase commit (2PC) or Saga pattern.
2. **Eventual consistency**: Accept temporary inconsistency with reconciliation.
3. **Idempotent operations**: Make operations safe to retry.
4. **Compensation actions**: Rollback operations that can't be undone.
5. **Consensus algorithms**: Use Paxos or Raft for strong consistency.

### 15. **What's the CAP theorem and how does it affect data reliability design?**

**Answer:** CAP theorem states you can only guarantee two of three properties:
- **Consistency**: All nodes see the same data at the same time.
- **Availability**: Every request receives a response.
- **Partition tolerance**: System continues working despite network partitions.

**Implications**: Choose based on use case:
- **CP systems** (Consistency + Partition tolerance): Financial systems, databases.
- **AP systems** (Availability + Partition tolerance): Social media, caching layers.

## 📊 **Real-World Scenarios**

### 16. **You're processing payment transactions. The pipeline crashes halfway. How do you ensure no double charges?**

**Answer:**
1. **Idempotent processing**: Use unique transaction IDs to prevent duplicates.
2. **Atomic transactions**: Process payment and record completion in same transaction.
3. **Checkpointing**: Track processed transactions to resume safely.
4. **Reconciliation**: Daily reconciliation to catch any discrepancies.
5. **Audit trail**: Log every step for forensic analysis.

### 17. **How would you migrate a non-idempotent pipeline to be idempotent?**

**Answer:**
1. **Add deduplication keys**: Identify natural keys or add synthetic IDs.
2. **Implement upsert logic**: Replace `INSERT` with `INSERT ... ON CONFLICT`.
3. **Add idempotency tokens**: Generate and track unique IDs for each operation.
4. **Backfill strategy**: Process historical data with deduplication.
5. **Testing**: Verify idempotency by running pipeline twice with same input.

### 18. **What strategies would you use for handling late-arriving data?**

**Answer:**
1. **Watermarking**: Track maximum processed timestamp.
2. **Window-based processing**: Process data in time windows, allow late arrivals.
3. **Reconciliation jobs**: Periodic jobs to fix late data.
4. **Versioned data**: Store multiple versions of records.
5. **Alerting**: Notify when data is significantly delayed.

### 19. **How do you balance consistency vs performance in a high-throughput pipeline?**

**Answer:**
1. **Read-your-writes consistency**: Ensure users see their own writes immediately.
2. **Eventual consistency**: Accept some delay for non-critical data.
3. **Caching strategy**: Use caches with appropriate invalidation.
4. **Batching**: Group writes to reduce transaction overhead.
5. **Monitoring**: Track consistency lag and adjust as needed.

### 20. **What's the difference between logical and physical data integrity?**

**Answer:**
- **Logical integrity**: Ensures data makes sense (business rules, constraints).
- **Physical integrity**: Ensures data is stored correctly (no corruption, backups work).

**Examples**: Logical = "order total equals sum of line items"; Physical = "database file isn't corrupted".

## 🛠️ **Database-Specific Questions**

### 21. **How do PostgreSQL and SQLite handle transactions differently?**

**Answer:**
- **PostgreSQL**: Full ACID compliance, MVCC (Multi-Version Concurrency Control), supports multiple isolation levels.
- **SQLite**: ACID-compliant but simpler, file-based, supports WAL (Write-Ahead Logging).
- **Use cases**: PostgreSQL for production systems, SQLite for embedded/local development.

### 22. **What isolation levels does PostgreSQL support and when would you use each?**

**Answer:**
1. **READ UNCOMMITTED** (not actually supported, maps to READ COMMITTED)
2. **READ COMMITTED**: Default, sees only committed data.
3. **REPEATABLE READ**: Sees snapshot at transaction start.
4. **SERIALIZABLE**: Highest isolation, prevents all anomalies.

**Recommendation**: Use READ COMMITTED for most cases, SERIALIZABLE for financial transactions.

### 23. **Explain WAL (Write-Ahead Logging) and its benefits for reliability.**

**Answer:** WAL writes changes to a log before applying them to the database.

**Benefits:**
1. **Crash recovery**: Can replay log after crash.
2. **Concurrent reads/writes**: Readers don't block writers.
3. **Performance**: Sequential log writes are faster than random disk writes.
4. **Replication**: Log can be shipped to replicas.

### 24. **How do you handle database connection failures in a Python application?**

**Answer:**
1. **Retry logic**: Exponential backoff for transient failures.
2. **Connection pooling**: Reuse connections, handle pool exhaustion.
3. **Circuit breaker**: Stop trying after repeated failures.
4. **Graceful degradation**: Continue with reduced functionality.
5. **Health checks**: Monitor database availability.

### 25. **What's the difference between savepoints and nested transactions?**

**Answer:**
- **Savepoints**: Markers within a transaction that you can roll back to.
- **Nested transactions**: Not supported in most SQL databases; simulated with savepoints.

**Use case**: Use savepoints for partial rollback within complex transactions.

## 📈 **Performance & Optimization**

### 26. **How do you optimize transaction performance without sacrificing reliability?**

**Answer:**
1. **Batch operations**: Use `executemany()` instead of individual inserts.
2. **Appropriate isolation**: Use lower isolation levels when possible.
3. **Indexing**: Proper indexes reduce lock contention.
4. **Connection pooling**: Reduce connection overhead.
5. **Asynchronous processing**: Process in background where appropriate.

### 27. **What's the N+1 query problem and how do you solve it?**

**Answer:** N+1 problem occurs when you fetch a list of items (1 query) then make additional queries for each item (N queries).

**Solutions:**
1. **Eager loading**: Use JOINs or `SELECT ... IN` to fetch all data at once.
2. **Batch loading**: Load related data in batches.
3. **Caching**: Cache frequently accessed data.
4. **Denormalization**: Store related data together.

### 28. **How do you design a pipeline that can handle 10x data volume increase?**

**Answer:**
1. **Horizontal scaling**: Add more workers/nodes.
2. **Partitioning**: Split data by key ranges or time.
3. **Stream processing**: Process data as it arrives.
4. **Database sharding**: Distribute data across multiple databases.
5. **Performance testing**: Load test with projected volumes.

### 29. **What metrics would you track to ensure pipeline reliability?**

**Answer:**
1. **Success rate**: Percentage of successful runs.
2. **Error rate**: Types and frequencies of errors.
3. **Latency**: Processing time percentiles (p50, p95, p99).
4. **Throughput**: Records/bytes processed per second.
5. **Data quality**: Validation failure rates.
6. **Resource utilization**: CPU, memory, disk I/O.

### 30. **How do you perform zero-downtime database migrations?**

**Answer:**
1. **Backward compatibility**: New code works with old schema.
2. **Feature flags**: Gradually enable new functionality.
3. **Blue-green deployment**: Switch between old and new versions.
4. **Online schema changes**: Use tools that support online DDL.
5. **Rollback plan**: Ability to quickly revert if issues arise.

## 🧪 **Testing & Validation**

### 31. **How would you test the idempotency of a data pipeline?**

**Answer:**
1. **Duplicate input test**: Run pipeline twice with same input, verify same output.
2. **Partial failure test**: Crash pipeline mid-run, restart, verify no duplicates.
3. **Concurrent execution test**: Run multiple instances simultaneously.
4. **Property-based testing**: Generate random inputs and verify idempotency property.
5. **Integration tests**: Test with real database and failure scenarios.

### 32. **What's chaos engineering and how does it relate to data reliability?**

**Answer:** Chaos engineering is intentionally injecting failures to test system resilience.

**Application to data reliability:**
1. **Network failures**: Simulate database connection drops.
2. **Process crashes**: Kill pipeline processes mid-execution.
3. **Resource exhaustion**: Simulate memory/disk full scenarios.
4. **Clock skew**: Test with incorrect timestamps.
5. **Learn and improve**: Use findings to strengthen reliability.

### 33. **How do you validate data quality in a reliable pipeline?**

**Answer:**
1. **Schema validation**: Ensure data matches expected structure.
2. **Business rule validation**: Check domain-specific constraints.
3. **Statistical validation**: Verify distributions, outliers.
4. **Referential integrity**: Check foreign key relationships.
5. **Freshness checks**: Ensure data isn't stale.

### 34. **What's the role of data contracts in reliable systems?**

**Answer:** Data contracts define the schema, semantics, and quality expectations for data.

**Benefits:**
1. **Clear expectations**: Producers and consumers agree on data format.
2. **Early detection**: Catch schema violations before production.
3. **Versioning**: Manage schema evolution systematically.
4. **Automated validation**: Enforce contracts in CI/CD pipelines.

### 35. **How do you perform disaster recovery testing for a data pipeline?**

**Answer:**
1. **Regular backups**: Test backup restoration process.
2. **Failover testing**: Switch to standby systems.
3. **Data loss simulation**: Test recovery from partial data loss.
4. **Recovery time objectives**: Measure time to restore service.
5. **Documentation**: Keep recovery procedures up to date.

## 🎯 **System Design Questions**

### 36. **Design a payment processing system that guarantees exactly-once semantics.**

**Answer:**
1. **Idempotent API**: Accept payment with unique transaction ID.
2. **Deduplication**: Check transaction ID before processing.
3. **Atomic operations**: Record payment and mark as processed in same transaction.
4. **Compensation**: If payment fails, reverse any partial changes.
5. **Audit trail**: Log every step for reconciliation.

### 37. **How would you design a data pipeline that processes millions of events per day with 99.99% reliability?**

**Answer:**
1. **Architecture**: Use streaming (Kafka, Kinesis) with micro-batching.
2. **Idempotent processing**: Deduplicate by event ID.
3. **Checkpointing**: Track processed offsets.
4. **Monitoring**: Real-time metrics and alerting.
5. **Redundancy**: Multiple consumers, automatic failover.

### 38. **Design a system for handling GDPR "right to be forgotten" requests in a data warehouse.**

**Answer:**
1. **Data lineage**: Track where personal data flows.
2. **Soft deletion**: Mark records as deleted rather than physical delete.
3. **Propagation**: Cascade deletions to derived datasets.
4. **Audit trail**: Log all deletion requests and actions.
5. **Verification**: Confirm deletion across all systems.

### 39. **How would you implement data versioning for regulatory compliance?**

**Answer:**
1. **Slowly Changing Dimensions Type 4**: Add version columns to tables.
2. **Time travel**: Use database features (e.g., PostgreSQL temporal tables).
3. **Immutable storage**: Append-only data stores.
4. **Snapshotting**: Regular snapshots of entire dataset.
5. **Audit tables**: Track all changes with timestamps and users.

### 40. **Design a multi-region data pipeline with strong consistency requirements.**

**Answer:**
1. **Synchronous replication**: Use database clustering with synchronous replication.
2. **Distributed transactions**: Use 2PC or consensus algorithms.
3. **Conflict resolution**: Define rules for resolving conflicting writes.
4. **Latency optimization**: Route reads to nearest region.
5. **Disaster recovery**: Automatic failover between regions.

## 📚 **Resources & Best Practices**

### Recommended Books:
- **"Designing Data-Intensive Applications"** by Martin Kleppmann
- **"Database Internals"** by Alex Petrov
- **"The Data Warehouse Toolkit"** by Ralph Kimball
- **"Building Evolutionary Architectures"** by Neal Ford

### Online Resources:
- **AWS Well-Architected Framework** (Reliability Pillar)
- **Google's Site Reliability Engineering** (SRE) books
- **PostgreSQL Documentation** (Transaction Management)
- **Apache Kafka Documentation** (Exactly-once semantics)

### Practice Platforms:
- **LeetCode Database Problems**
- **HackerRank SQL Challenges**
- **System Design Interview practice**
- **Kaggle Data Engineering competitions**

## 🎯 **Interview Preparation Tips**

### 1. **Understand the fundamentals**:
- Master ACID properties and their trade-offs
- Know isolation levels and their implications
- Understand idempotency patterns

### 2. **Practice with real scenarios**:
- Design systems for specific reliability requirements
- Walk through failure scenarios and recovery strategies
- Explain trade-offs between consistency models

### 3. **Be ready for coding questions**:
- Write idempotent database operations
- Implement retry logic with exponential backoff
- Design checkpoint-based recovery systems

### 4. **Prepare real-world examples**:
- Describe a time you improved pipeline reliability
- Explain how you handled a production data incident
- Share metrics you used to measure reliability

### 5. **Ask insightful questions**:
- "What are the most common failure modes in your data pipelines?"
- "How do you balance consistency vs latency in your system?"
- "What reliability SLAs do you maintain for different data products?"

## 🔗 **Related Resources in This Repository**

- [GOTCHAS_BEST_PRACTICES.md](./GOTCHAS_BEST_PRACTICES.md) - Common pitfalls and solutions
- [README.md](./README.md) - Project overview and instructions
- [01_unreliable_ingest.py](./01_unreliable_ingest.py) - Example of unreliable ingestion
- [02_robust_ingest.py](./02_robust_ingest.py) - Robust implementation with transactions and idempotency