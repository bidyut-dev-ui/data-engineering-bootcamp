# Hadoop Interview Questions & Answers

This document contains common Hadoop interview questions categorized by difficulty level. Each question includes a detailed answer and practical examples relevant to 8GB RAM constraints.

## 📊 Difficulty Levels
- **Beginner**: Basic concepts, terminology, setup
- **Intermediate**: Architecture, configuration, optimization
- **Advanced**: Troubleshooting, performance tuning, integration

---

## 🟢 Beginner Questions

### 1. **What is Hadoop and what problems does it solve?**
**Answer**: Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of computers. It solves:
- **Storage**: HDFS (Hadoop Distributed File System) stores petabytes of data across multiple machines
- **Processing**: MapReduce processes data in parallel across the cluster
- **Fault tolerance**: Data is replicated across nodes; if one fails, data is still available
- **Scalability**: Add more nodes to handle more data

**Example for 8GB RAM**: Even on a single machine, Hadoop's architecture teaches distributed systems concepts. Docker containers simulate multiple nodes.

### 2. **Explain HDFS architecture components**
**Answer**: HDFS has two main components:
- **NameNode**: Master server that manages file system metadata (file names, locations, permissions). Stores this in memory (critical for 8GB RAM optimization).
- **DataNode**: Slave servers that store actual data blocks. Multiple DataNodes provide redundancy.

**Additional components**:
- **Secondary NameNode**: Checkpoints NameNode metadata (not a backup!)
- **JournalNode**: For High Availability (HA) setups

### 3. **What is MapReduce? Explain Map and Reduce phases**
**Answer**: MapReduce is a programming model for processing large datasets in parallel.
- **Map phase**: Processes input data and produces intermediate key-value pairs
  ```python
  # Example: WordCount mapper
  def mapper(line):
      for word in line.split():
          yield (word, 1)
  ```
- **Shuffle phase**: Groups intermediate values by key
- **Reduce phase**: Aggregates values for each key
  ```python
  # Example: WordCount reducer
  def reducer(word, counts):
      yield (word, sum(counts))
  ```

### 4. **What is YARN?**
**Answer**: YARN (Yet Another Resource Negotiator) is Hadoop's resource management layer. It separates resource management from data processing.
- **ResourceManager**: Global resource scheduler
- **NodeManager**: Per-node agent managing containers
- **ApplicationMaster**: Per-application manager requesting resources

### 5. **How do you check HDFS health?**
**Answer**: Use these commands:
```bash
# Check if NameNode is running
hdfs dfsadmin -report

# Check disk space
hdfs dfs -df -h

# Check DataNode status
hdfs dfsadmin -printTopology

# For 8GB RAM: Also monitor memory usage
docker stats hadoop-namenode
```

---

## 🟡 Intermediate Questions

### 6. **Explain the small files problem in HDFS**
**Answer**: Storing many small files (< 128MB) causes:
- **NameNode memory exhaustion**: Each file consumes ~150 bytes of memory
- **Inefficient storage**: Blocks are 128MB minimum; small files waste space
- **Processing overhead**: More mappers needed, increasing overhead

**Solutions for 8GB RAM**:
1. Combine files using `hadoop archive`
2. Use SequenceFile format
3. Implement a compaction job
4. Set `dfs.namenode.fs-limits.min-block-size` appropriately

### 7. **How does Hadoop ensure fault tolerance?**
**Answer**: Multiple mechanisms:
- **Data replication**: Default 3 copies across different nodes
- **Heartbeats**: DataNodes send periodic heartbeats to NameNode
- **Block reporting**: DataNodes report block locations
- **Checkpointing**: Secondary NameNode creates fsimage checkpoints
- **Safe mode**: NameNode starts in safe mode until sufficient DataNodes report

**For single-node (8GB RAM)**: Replication factor should be 1 to save memory/disk.

### 8. **What is speculative execution in MapReduce?**
**Answer**: When a task runs slower than expected, YARN launches a duplicate task on another node. The first to finish wins, the other is killed.

**Pros**: Mitigates slow nodes (stragglers)
**Cons**: Wastes resources (not ideal for 8GB RAM)

**Configuration**:
```xml
<property>
  <name>mapreduce.map.speculative</name>
  <value>false</value>  <!-- Disable for resource-constrained systems -->
</property>
```

### 9. **Compare Hadoop MapReduce vs Apache Spark**
**Answer**:

| Aspect | MapReduce | Spark |
|--------|-----------|-------|
| **Processing** | Batch-only | Batch + Streaming + ML |
| **Speed** | Disk-based (slower) | Memory-based (faster) |
| **Memory** | Spills to disk | Requires more RAM |
| **API** | Lower-level (Java) | Higher-level (Scala/Python/Java/R) |
| **Ease of use** | More complex | Simpler, richer API |
| **8GB RAM suitability** | Better (spills to disk) | Requires careful tuning |

**Recommendation**: Use MapReduce for very large datasets that don't fit in memory; use Spark for iterative algorithms and interactive queries.

### 10. **How do you optimize MapReduce for 8GB RAM?**
**Answer**: Key optimizations:
1. **Reduce memory per task**:
   ```xml
   mapreduce.map.memory.mb=1024
   mapreduce.reduce.memory.mb=1024
   ```
2. **Enable compression**:
   ```xml
   mapreduce.map.output.compress=true
   mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec
   ```
3. **Adjust JVM heap**:
   ```xml
   mapreduce.map.java.opts=-Xmx768m
   mapreduce.reduce.java.opts=-Xmx768m
   ```
4. **Reduce task count**:
   ```bash
   # Fewer mappers/reducers
   -D mapreduce.job.maps=2
   -D mapreduce.job.reduces=2
   ```

### 11. **Explain Hive architecture and components**
**Answer**: Hive provides SQL-like interface (HiveQL) to Hadoop data.
- **Metastore**: Stores schema information (RDBMS like MySQL/PostgreSQL)
- **Driver**: Compiles HiveQL to MapReduce/Tez/Spark jobs
- **Execution Engine**: Executes the compiled jobs
- **HiveServer2**: Thrift server for client connections

**For 8GB RAM**: Use embedded Derby metastore to save memory.

### 12. **What is data locality in Hadoop?**
**Answer**: Processing data on the node where it's stored to minimize network transfer.
- **Node-local**: Data on same node (best)
- **Rack-local**: Data in same rack (good)
- **Off-rack**: Data in different rack (worst)

**YARN considers** data locality when scheduling tasks. On 8GB RAM single node, all data is node-local.

---

## 🔴 Advanced Questions

### 13. **How would you troubleshoot a slow MapReduce job?**
**Answer**: Systematic approach:
1. **Check resource utilization**:
   ```bash
   # Monitor during job execution
   top -p $(jps | grep NodeManager | awk '{print $1}')
   ```
2. **Review counters**:
   ```bash
   yarn logs -applicationId <app_id> | grep COUNTER
   ```
3. **Identify skew**:
   - Check if reducers have uneven loads
   - Use `-D mapreduce.job.reduces=1` to debug
4. **Check for spills**:
   - Disk I/O indicates memory pressure
   - Adjust `mapreduce.task.io.sort.mb`
5. **Review logs**:
   ```bash
   yarn logs -applicationId <app_id> > job.log
   grep -i "error\|exception\|slow\|timeout" job.log
   ```

### 14. **Explain Hadoop security mechanisms**
**Answer**: 
1. **Authentication**: Kerberos (enterprise) or simple (development)
2. **Authorization**: 
   - HDFS: POSIX permissions (user/group/other)
   - YARN: ACLs for queue access
3. **Encryption**: 
   - Data at rest: HDFS transparent encryption
   - Data in transit: SSL/TLS
4. **Auditing**: Logs all access attempts

**For 8GB RAM development**: Use simple authentication, focus on learning concepts.

### 15. **How does Hadoop handle data skew in joins?**
**Answer**: Data skew occurs when one key has many more values than others.
**Solutions**:
1. **Salting**: Add random prefix to keys to distribute load
   ```python
   # Before: (user_id, data)
   # After: (user_id_salt, data) where salt = random(1,10)
   ```
2. **Skew join**: Handle large keys separately
3. **Map-side join**: For small tables, broadcast to all mappers
4. **Bucketing**: Pre-partition data into buckets

### 16. **Compare HDFS, HBase, and Hive storage**
**Answer**:

| Storage | Use Case | Access Pattern | 8GB RAM Suitability |
|---------|----------|----------------|---------------------|
| **HDFS** | Large files, batch processing | Sequential scans | Good (with small datasets) |
| **HBase** | Random read/write, real-time | Random access | Poor (requires more RAM) |
| **Hive** | SQL queries, analytics | Declarative queries | Good (with ORC format) |

**Recommendation**: Use HDFS for raw storage, Hive for analytics on 8GB RAM.

### 17. **What are Hadoop counters and how are they useful?**
**Answer**: Counters track job statistics across the cluster.
**Types**:
- **Built-in**: File system, MapReduce, Shuffle counters
- **User-defined**: Custom counters in mapper/reducer

**Example use**:
```java
context.getCounter("MyGroup", "BadRecords").increment(1);
```

**For debugging**: Monitor `MAP_INPUT_RECORDS`, `REDUCE_OUTPUT_RECORDS`, `SPILLED_RECORDS`.

### 18. **Explain Hadoop 2.x vs 3.x differences**
**Answer**: Key differences:
- **YARN improvements**: Better scheduling, Docker container support
- **HDFS erasure coding**: Reduces storage overhead from 200% to 50%
- **Multiple NameNodes**: Better scalability
- **GPU scheduling**: For ML workloads
- **Java 8+ requirement**

**For 8GB RAM**: Hadoop 3.x with erasure coding can save disk space.

### 19. **How would you migrate from Hadoop to cloud (AWS EMR)?**
**Answer**: Migration strategy:
1. **Assessment**: Inventory jobs, data sizes, dependencies
2. **Data migration**: Use `DistCp` (Distributed Copy) or S3 connectors
3. **Job migration**: Test on EMR with same configurations
4. **Optimization**: Leverage cloud features (spot instances, auto-scaling)
5. **Validation**: Compare results, performance, costs

**Consideration for 8GB RAM users**: Cloud allows scaling beyond local constraints.

### 20. **Design a Hadoop pipeline for log analysis**
**Answer**: Architecture for processing 1TB of daily logs:
1. **Ingestion**: Flume/Kafka to HDFS
2. **Storage**: HDFS with daily partitions (`/logs/YYYY/MM/DD`)
3. **Processing**: 
   - MapReduce for aggregation (count errors by hour)
   - Hive for ad-hoc queries
   - Spark Streaming for real-time alerts
4. **Output**: Results to HBase (dashboard) and HDFS (reports)
5. **Optimization for 8GB RAM**:
   - Process hourly instead of daily
   - Use compression (Snappy)
   - Limit concurrent jobs

---

## 💼 Scenario-Based Questions

### Scenario 1: "Your MapReduce job fails with 'Java heap space' error"
**Diagnosis steps**:
1. Check `mapreduce.map.java.opts` and `mapreduce.reduce.java.opts`
2. Monitor memory during execution with `jstat`
3. Check for data skew causing one reducer to get all data
4. Review `mapreduce.task.io.sort.mb` setting

**Solution**: Reduce memory settings, enable compression, add more reducers.

### Scenario 2: "HDFS becomes read-only (safe mode)"
**Causes**:
1. Disk space below threshold
2. Not enough DataNodes reporting
3. Manual safe mode entry

**Solution**:
```bash
# Check safe mode status
hdfs dfsadmin -safemode get

# Leave safe mode (if appropriate)
hdfs dfsadmin -safemode leave

# Or wait for automatic exit
hdfs dfsadmin -safemode wait
```

### Scenario 3: "YARN containers killed due to memory"
**Debugging**:
1. Check `yarn.nodemanager.resource.memory-mb` setting
2. Verify `yarn.scheduler.maximum-allocation-mb`
3. Check for memory leaks in user code
4. Monitor with `yarn top`

**Fix**: Adjust memory settings, reduce container size, fix memory leaks.

---

## 🎯 Interview Preparation Tips

1. **Hands-on practice**: Run all tutorials in this project
2. **Understand trade-offs**: Know when to use Hadoop vs alternatives
3. **Resource awareness**: Always consider 8GB RAM constraints in answers
4. **Real-world examples**: Relate concepts to actual use cases
5. **Troubleshooting mindset**: Show systematic debugging approach

## 📚 Recommended Study Path

1. **Week 1**: Complete all 5 Hadoop tutorials in this project
2. **Week 2**: Practice interview questions (this document)
3. **Week 3**: Build a mini-project (log analysis, ETL pipeline)
4. **Week 4**: Review advanced concepts and cloud integration

## 🔗 Additional Resources

1. [Hadoop: The Definitive Guide](https://www.oreilly.com/library/view/hadoop-the-definitive/9781491901687/)
2. [Hadoop Official Documentation](https://hadoop.apache.org/docs/current/)
3. [Cloudera Hadoop Tutorials](https://www.cloudera.com/tutorials.html)
4. [AWS EMR Documentation](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)

---

**Remember**: Interviewers value practical experience over theoretical knowledge. Complete the hands-on tutorials in this project to build confidence and demonstrate real skills.