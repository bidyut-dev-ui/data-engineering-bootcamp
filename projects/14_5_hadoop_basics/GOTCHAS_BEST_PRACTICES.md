# Hadoop Gotchas & Best Practices for 8GB RAM

This document outlines common pitfalls, gotchas, and best practices when working with Hadoop on resource-constrained systems (8GB RAM laptops).

## 🚨 Critical Gotchas (What to Avoid)

### 1. **Memory Overcommitment**
**Gotcha**: Running Hadoop services without memory limits can crash your system.
**Solution**: Always set memory limits in `docker-compose.yml`:
```yaml
services:
  namenode:
    mem_limit: 1g
  datanode:
    mem_limit: 512m
```

### 2. **HDFS Small Files Problem**
**Gotcha**: Storing millions of small files (< 128MB) in HDFS causes NameNode memory exhaustion.
**Solution**:
- Combine small files into larger ones (use `hadoop archive`)
- Use SequenceFile or Avro containers
- Set `dfs.namenode.fs-limits.min-block-size` appropriately

### 3. **MapReduce Memory Issues**
**Gotcha**: MapReduce jobs fail with "Java heap space" errors on 8GB RAM.
**Solution**:
```bash
# Set these in mapred-site.xml
mapreduce.map.memory.mb=1024
mapreduce.reduce.memory.mb=1024
mapreduce.map.java.opts=-Xmx768m
mapreduce.reduce.java.opts=-Xmx768m
```

### 4. **Docker Port Conflicts**
**Gotcha**: Hadoop services use many ports (8088, 9870, 9864, etc.) that may conflict with other services.
**Solution**:
```bash
# Check for port conflicts before starting
netstat -tulpn | grep :8088
# Use different ports in docker-compose if needed
```

### 5. **Disk Space Exhaustion**
**Gotcha**: Hadoop writes intermediate data to disk; small `/tmp` partitions fill up quickly.
**Solution**:
```bash
# Set Hadoop temp directory to a location with more space
export HADOOP_TMP_DIR=/path/to/large/disk/tmp
# Monitor disk usage regularly
df -h /tmp
```

## ✅ Best Practices

### 1. **Resource Allocation Strategy**
For 8GB RAM systems, follow this allocation:
- **OS & Docker**: 2GB
- **Hadoop Services**: 4GB total
  - NameNode: 1GB
  - DataNode: 512MB
  - ResourceManager: 1GB
  - NodeManager: 1GB
  - HistoryServer: 512MB
- **Remaining**: 2GB for applications (Spark, Hive, etc.)

### 2. **Data Size Management**
**Rule of Thumb**: Keep individual files between 128MB and 1GB.
- **Too small** (< 128MB): Inefficient, NameNode overhead
- **Too large** (> 1GB): Memory pressure during processing

**Optimal file count**: Aim for 10-100 files per job, not thousands.

### 3. **Configuration Optimization**
```xml
<!-- core-site.xml -->
<property>
  <name>io.file.buffer.size</name>
  <value>131072</value>  <!-- 128KB buffer for better I/O -->
</property>

<!-- hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>1</value>  <!-- Single node, no replication needed -->
</property>

<!-- mapred-site.xml -->
<property>
  <name>mapreduce.task.io.sort.mb</name>
  <value>256</value>  <!-- Reduced for 8GB RAM -->
</property>
```

### 4. **Monitoring & Debugging**
**Essential monitoring commands**:
```bash
# Check Hadoop services
docker-compose ps

# Check HDFS health
hdfs dfsadmin -report

# Check YARN applications
yarn application -list

# Check disk space
hdfs dfs -df -h

# Check NameNode memory
jstat -gc $(jps | grep NameNode | awk '{print $1}') 1000
```

### 5. **Performance Tuning for 8GB RAM**
**MapReduce tuning**:
```bash
# Reduce task parallelism to avoid memory contention
mapreduce.job.maps=2
mapreduce.job.reduces=2

# Enable compression for intermediate data
mapreduce.map.output.compress=true
mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec
```

**Spark tuning** (when integrated):
```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

## 🔧 Troubleshooting Common Issues

### Issue: "Container killed due to memory exhaustion"
**Symptoms**: YARN containers fail with exit code 137.
**Fix**:
1. Reduce container memory:
   ```bash
   export YARN_MIN_ALLOC_MB=512
   export YARN_MAX_ALLOC_MB=1024
   ```
2. Increase virtual memory ratio:
   ```bash
   export YARN_VMEM_RATIO=2.1
   ```

### Issue: "NameNode in Safe Mode"
**Symptoms**: Cannot write to HDFS, operations fail.
**Fix**:
```bash
# Leave safe mode
hdfs dfsadmin -safemode leave

# Or wait for thresholds
hdfs dfsadmin -safemode wait
```

### Issue: "Disk space low on DataNode"
**Symptoms**: DataNode stops, warnings in logs.
**Fix**:
1. Clean up temporary files:
   ```bash
   hdfs dfs -expunge
   ```
2. Increase reserved space:
   ```xml
   <property>
     <name>dfs.datanode.du.reserved</name>
     <value>1073741824</value>  <!-- 1GB reserved -->
   </property>
   ```

### Issue: "Slow MapReduce performance"
**Symptoms**: Jobs take much longer than expected.
**Debug steps**:
1. Check if data is local (data locality):
   ```bash
   yarn node -list
   ```
2. Monitor CPU and memory during job execution
3. Check for data skew (uneven distribution)

## 🎯 Optimization Checklist

Before running production jobs:

- [ ] **Memory limits** set in docker-compose.yml
- [ ] **HDFS replication factor** set to 1 (single node)
- [ ] **MapReduce memory** configured for 8GB constraints
- [ ] **Temporary directory** has sufficient space (> 5GB free)
- [ ] **Firewall/ports** are open for Hadoop services
- [ ] **Swap space** is enabled (2-4GB recommended)
- [ ] **Docker resources** are not shared with other heavy containers
- [ ] **Log rotation** is configured to prevent disk filling

## 📊 Performance Benchmarks (8GB RAM Expectations)

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| HDFS write (1GB) | 30-60 seconds | Depends on disk speed |
| MapReduce WordCount (1GB text) | 2-5 minutes | With 2 mappers, 2 reducers |
| Hive query (simple aggregation) | 10-30 seconds | On 1M row table |
| Spark DataFrame operation | 5-15 seconds | With 2 executors |
| Cluster startup | 60-90 seconds | All services healthy |

## 🔄 Maintenance Routine

**Daily checks**:
```bash
# 1. Check service health
docker-compose ps

# 2. Check HDFS health
hdfs dfsadmin -report | grep "Live datanodes"

# 3. Check disk space
df -h /tmp

# 4. Check logs for errors
docker-compose logs --tail=20 namenode
```

**Weekly tasks**:
1. Clean up old YARN application logs
2. Compact HDFS if many small files
3. Update Docker images (security patches)
4. Backup important HDFS data

## 🚀 Scaling Tips (When You Need More)

If you hit 8GB RAM limits:

1. **Vertical scaling options**:
   - Upgrade to 16GB RAM (optimal for development)
   - Add SSD for better I/O performance

2. **Horizontal scaling options**:
   - Add more Docker containers as pseudo-nodes
   - Use Docker Swarm or Kubernetes for multi-node

3. **Cloud alternatives**:
   - AWS EMR (pay-per-use)
   - Databricks Community Edition (free tier)
   - Google Dataproc (free credits available)

## 📚 Further Reading

1. [Hadoop Performance Tuning Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html)
2. [Docker Resource Constraints](https://docs.docker.com/config/containers/resource_constraints/)
3. [YARN Capacity Scheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)
4. [HDFS Architecture Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)

---

**Remember**: Hadoop was designed for clusters with hundreds of GBs of RAM. Running on 8GB requires careful tuning, but it's excellent for learning and development. Always monitor resource usage and adjust configurations accordingly.