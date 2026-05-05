# Streaming with Redpanda: Interview Questions

## 📋 Core Concepts

### 1. **What is event-driven architecture and how does it differ from batch processing?**

**Expected Answer:** Event-driven architecture processes data as it arrives in real-time, while batch processing handles data in scheduled intervals. Event-driven offers lower latency (milliseconds vs hours/days), continuous processing vs periodic, and is better for real-time analytics, monitoring, and alerting. Batch processing is better for large-scale historical analysis where completeness is more important than timeliness.

**Follow-up:** When would you choose event-driven over batch processing for a financial ticker system?

### 2. **Explain the role of a message broker like Redpanda/Kafka in streaming pipelines.**

**Expected Answer:** Message brokers act as a buffer between producers and consumers, providing:
- **Decoupling:** Producers and consumers don't need to know about each other
- **Durability:** Messages are persisted until consumed
- **Scalability:** Multiple consumers can read at different rates
- **Ordering:** Messages within a partition maintain order
- **Fault tolerance:** Replication ensures data isn't lost

**Follow-up:** How does Redpanda differ from Apache Kafka in terms of architecture and performance?

### 3. **Describe the key components of Redpanda/Kafka: topics, partitions, producers, and consumers.**

**Expected Answer:**
- **Topics:** Logical channels for organizing messages (e.g., `financial_ticks`)
- **Partitions:** Parallel units within topics for scalability and ordering guarantees
- **Producers:** Applications that publish messages to topics
- **Consumers:** Applications that read messages from topics
- **Consumer Groups:** Logical grouping of consumers that share partition assignment

**Follow-up:** How does partitioning affect message ordering and consumer scalability?

## 🔧 Technical Implementation

### 4. **How would you design a producer for financial tick data with 8GB RAM constraints?**

**Expected Answer:** 
1. Use efficient serialization (Protocol Buffers/Avro over JSON)
2. Implement batching with `linger_ms` and `batch_size` configuration
3. Set appropriate `buffer_memory` limits (e.g., 16MB instead of default 32MB)
4. Implement backpressure with `max_block_ms` timeout
5. Use compression (`gzip` or `snappy`) to reduce network/memory usage
6. Monitor memory with `psutil` and implement emergency cleanup procedures

**Follow-up:** What specific Python Kafka producer configurations would you use?

### 5. **Explain consumer groups and how they enable parallel processing.**

**Expected Answer:** Consumer groups allow multiple consumers to work together on the same topic. Each partition is assigned to exactly one consumer in the group, enabling:
- **Parallel processing:** Multiple consumers can process different partitions simultaneously
- **Load balancing:** Partitions are rebalanced when consumers join/leave
- **Fault tolerance:** If a consumer fails, its partitions are reassigned to others

**Follow-up:** What happens when you have more consumers than partitions in a consumer group?

### 6. **How would you implement exactly-once semantics in a streaming pipeline?**

**Expected Answer:** 
1. **Idempotent producers:** Use `enable_idempotence=True` with unique `transactional.id`
2. **Transactional writes:** Use producer transactions with `init_transactions()` and `commit_transaction()`
3. **Consumer isolation:** Set `isolation_level='read_committed'`
4. **Deduplication:** Store processed message IDs and check before processing
5. **Checkpointing:** Store offsets with processed results atomically

**Follow-up:** What are the performance trade-offs of exactly-once semantics?

### 7. **Describe different message delivery semantics (at-most-once, at-least-once, exactly-once).**

**Expected Answer:**
- **At-most-once:** Messages may be lost but never duplicated (fire-and-forget)
- **At-least-once:** Messages guaranteed to be delivered, but may be duplicated (acknowledgments)
- **Exactly-once:** Messages delivered exactly once (requires coordination and idempotency)

**Follow-up:** Which semantic would you choose for financial transactions vs. website click tracking?

## 🎯 Real-time Aggregation & Processing

### 8. **How would you implement real-time volume aggregation for stock symbols with 8GB RAM constraints?**

**Expected Answer:**
1. Use windowed aggregation (time-based or count-based) to limit memory
2. Implement periodic flushing to disk (SQLite/Redis) for overflow
3. Use efficient data structures (`defaultdict(int)` for counters)
4. Consider approximate algorithms (HyperLogLog for cardinality) if exact counts aren't critical
5. Implement memory monitoring with emergency cleanup triggers

**Code Example:**
```python
from collections import defaultdict
import time
import sqlite3

class WindowedAggregator:
    def __init__(self, window_seconds=60):
        self.window_seconds = window_seconds
        self.window_start = time.time()
        self.aggregation = defaultdict(int)
        self.overflow_db = sqlite3.connect(':memory:')
    
    def add(self, symbol, volume):
        # Check if window expired
        if time.time() - self.window_start > self.window_seconds:
            self._flush_window()
        
        self.aggregation[symbol] += volume
    
    def _flush_window(self):
        # Store current window to disk, reset memory
        timestamp = int(time.time())
        for symbol, volume in self.aggregation.items():
            # Store in SQLite
            pass
        self.aggregation.clear()
        self.window_start = time.time()
```

**Follow-up:** How would you handle late-arriving data in your windowed aggregation?

### 9. **What are the challenges of maintaining state in streaming applications, and how do you address them?**

**Expected Answer:**
**Challenges:**
- Memory growth with unbounded state
- State recovery after failures
- Consistency across distributed consumers
- Handling out-of-order events

**Solutions:**
1. **Windowed state:** Use time or count-based windows
2. **External state stores:** Redis, RocksDB, or database for large state
3. **Checkpointing:** Regular state persistence with Kafka Streams/Spark Streaming
4. **Idempotent operations:** Design processing to be repeatable
5. **Watermarks:** Handle late data in event-time processing

**Follow-up:** How would you implement fault-tolerant state management for a trading volume dashboard?

## ⚡ Performance & Optimization

### 10. **How would you optimize a streaming pipeline for high throughput on limited RAM?**

**Expected Answer:**
1. **Producer side:**
   - Enable compression (`gzip`, `snappy`, `lz4`)
   - Use appropriate `batch_size` (16-64KB)
   - Set `linger_ms` for batching efficiency
   - Limit `buffer_memory` based on available RAM

2. **Consumer side:**
   - Adjust `fetch_max_bytes` and `max_poll_records`
   - Use efficient deserialization
   - Process in batches, not message-by-message
   - Implement backpressure with pause/resume

3. **System level:**
   - Tune Redpanda memory limits in docker-compose
   - Use appropriate partition count (3-10 for 8GB RAM)
   - Set reasonable retention policies (time and size based)

**Follow-up:** What metrics would you monitor to identify bottlenecks?

### 11. **Explain consumer lag and how to monitor/address it.**

**Expected Answer:** Consumer lag is the difference between the latest message in a partition and the last message processed by a consumer. High lag indicates the consumer can't keep up.

**Monitoring:**
- Use `rpk group describe` or Kafka Admin API
- Monitor `records-lag` and `records-lag-max` metrics
- Set up alerts for lag thresholds

**Addressing:**
1. **Increase parallelism:** Add more consumers/partitions
2. **Optimize processing:** Profile and optimize consumer code
3. **Increase resources:** More CPU/RAM for consumer
4. **Batch processing:** Process messages in batches
5. **Scale horizontally:** Deploy more consumer instances

**Follow-up:** What would you do if one partition has significantly higher lag than others?

### 12. **Compare different compression algorithms (gzip, snappy, lz4) for streaming data.**

**Expected Answer:**
- **gzip:** Highest compression ratio, but CPU intensive (good for bandwidth-limited networks)
- **snappy:** Fast compression/decompression, moderate ratio (good for CPU-bound systems)
- **lz4:** Extremely fast, lower compression ratio (best for low-latency requirements)
- **zstd:** Good balance of speed and ratio (modern alternative)

**For 8GB RAM systems:** Use `snappy` or `lz4` to reduce CPU overhead while still saving memory/bandwidth.

**Follow-up:** When would you enable compression at the producer vs. topic level?

## 🐛 Fault Tolerance & Recovery

### 13. **How would you handle consumer failures and ensure no data loss?**

**Expected Answer:**
1. **Enable auto-commit with careful configuration:**
   ```python
   enable_auto_commit=True,
   auto_commit_interval_ms=5000,
   ```
2. **Implement manual offset management** for critical applications
3. **Use consumer groups** for automatic rebalancing
4. **Implement dead-letter queues** for poison pills
5. **Add retry logic with exponential backoff**
6. **Monitor consumer health** with heartbeats and session timeouts

**Follow-up:** What's the trade-off between `auto_offset_reset='earliest'` and `'latest'`?

### 14. **Describe strategies for handling schema evolution in streaming data.**

**Expected Answer:**
1. **Schema registry:** Use Confluent Schema Registry or Redpanda's built-in schema registry
2. **Backward/forward compatibility:** Design schemas with default values and optional fields
3. **Versioned topics:** `financial_ticks_v1`, `financial_ticks_v2`
4. **Content-based routing:** Route messages to different processors based on schema version
5. **Schema-on-read:** Store raw bytes and apply schema at consumption time

**Example with Avro:**
```python
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext

# Register and use schemas with compatibility checks
```

**Follow-up:** How would you migrate consumers from v1 to v2 schema without downtime?

### 15. **How would you implement a dead-letter queue (DLQ) pattern for failed messages?**

**Expected Answer:**
1. **Create DLQ topic:** `financial_ticks_dlq`
2. **Catch exceptions** in consumer processing
3. **Publish failed messages** to DLQ with error metadata
4. **Implement DLQ consumer** for analysis/reprocessing
5. **Add retry logic** with exponential backoff before DLQ

**Code Example:**
```python
dlq_producer = KafkaProducer(...)

try:
    process_message(message)
    consumer.commit()
except Exception as e:
    # Send to DLQ with error context
    dlq_producer.send('financial_ticks_dlq', value={
        'original_message': message.value,
        'error': str(e),
        'timestamp': time.time(),
        'partition': message.partition,
        'offset': message.offset
    })
    # Commit to skip this message
    consumer.commit()
```

**Follow-up:** What metadata would you include in DLQ messages for debugging?

## 📊 Monitoring & Observability

### 16. **What metrics would you monitor for a production streaming pipeline?**

**Expected Answer:**
1. **Throughput:** Messages per second in/out
2. **Latency:** End-to-end processing time (publish to consume)
3. **Consumer lag:** Per-partition lag in messages/time
4. **Error rates:** Failed messages, DLQ size
5. **Resource usage:** CPU, memory, disk I/O
6. **Redpanda metrics:** Under-replicated partitions, leader elections
7. **Business metrics:** Processing completeness, data quality

**Tools:** Prometheus/Grafana for metrics, ELK stack for logs, custom dashboards for business metrics.

**Follow-up:** How would you set up alerts for critical issues?

### 17. **How would you debug a streaming pipeline where consumers are falling behind?**

**Expected Answer:**
1. **Check consumer lag:** `rpk group describe` or Kafka tools
2. **Monitor consumer metrics:** Poll rate, fetch size, processing time
3. **Profile consumer code:** Identify slow operations (I/O, network calls)
4. **Check partition distribution:** Ensure even load across consumers
5. **Review configuration:** `fetch.max.bytes`, `max.poll.records`, `max.partition.fetch.bytes`
6. **Check network:** Latency between consumer and brokers
7. **Monitor system resources:** CPU, memory, garbage collection

**Debugging steps:**
```bash
# Check consumer groups
rpk group describe my-consumer-group

# Check topic details
rpk topic describe financial_ticks

# Monitor consumer metrics
kafka-consumer-groups.sh --bootstrap-server localhost:19092 --describe --group my-group
```

**Follow-up:** What would you do if one consumer is much slower than others in the same group?

## 🎯 Scenario-Based Questions

### 18. **You're building a real-time fraud detection system. How would you design the streaming architecture?**

**Expected Answer:**
1. **Multiple topics:** `transactions`, `alerts`, `fraud_rules`
2. **Kafka Streams/KSQL** for pattern matching
3. **Stateful processing** for user behavior baselines
4. **Machine learning integration** for anomaly detection
5. **Low-latency requirements** with exactly-once semantics
6. **Alerting pipeline** to `alerts` topic for immediate action
7. **Batch layer** for model retraining with historical data

**Architecture:**
```
Transactions → Kafka → [Real-time ML Model] → [Rule Engine] → Alerts
                    ↘ [Feature Store] ↗           ↘ [DLQ for review] ↗
```

**Follow-up:** How would you handle model updates without stopping the stream?

### 19. **Your streaming pipeline needs to join real-time data with historical reference data. What approaches would you consider?**

**Expected Answer:**
1. **Kafka Streams KTable:** Load reference data into in-memory table
2. **External lookup service:** Redis/DB query per message (higher latency)
3. **Broadcast joins:** Replicate reference data to all partitions
4. **Co-partitioning:** Ensure related data goes to same partition
5. **Dual-write pattern:** Write to both stream and DB, read from DB

**Considerations for 8GB RAM:**
- Use Redis with LRU eviction for reference data
- Implement caching with TTL
- Consider probabilistic data structures (Bloom filters) for existence checks
- Partition reference data to fit in memory

**Follow-up:** How would you handle updates to reference data?

### 20. **How would you design a streaming pipeline that needs to reprocess historical data?**

**Expected Answer:**
1. **Replay capability:** Store raw data in long-term storage (S3, HDFS)
2. **Offset management:** Ability to reset consumer offsets
3. **Dual-write:** Write to both Kafka and data lake
4. **Batch re-processing layer:** Use Spark/Flink for historical runs
5. **Schema evolution handling:** Versioned topics or schema registry

**Implementation:**
- Use **Kafka Connect** to sink to data lake
- Implement **consumer reset tool** for replay
- Design **idempotent processors** for safe reprocessing
- Maintain **watermarks** to track processed vs. reprocessed data

**Follow-up:** How would you ensure reprocessing doesn't affect real-time processing?

## 💻 Coding Exercises

### 21. **Write a memory-efficient Kafka consumer that processes messages in batches.**

```python
from kafka import KafkaConsumer
import json
from typing import List, Callable

class BatchConsumer:
    def __init__(self, topic: str, bootstrap_servers: List[str], 
                 batch_size: int = 100, max_wait_ms: int = 1000):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='batch-consumer',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            max_poll_records=batch_size,
            fetch_max_wait_ms=max_wait_ms
        )
        self.batch_size = batch_size
        
    def process_batches(self, processor: Callable[[List[dict]], None]):
        """Process messages in batches for memory efficiency"""
        while True:
            batch = self.consumer.poll(timeout_ms=1000, max_records=self.batch_size)
            
            if not batch:
                continue
                
            all_messages = []
            for tp, messages in batch.items():
                for message in messages:
                    all_messages.append(message.value)
            
            # Process batch
            processor(all_messages)
            
            # Commit offsets for the entire batch
            self.consumer.commit()
```

**Follow-up:** How would you modify this to handle partial batch failures?

### 22. **Implement a windowed aggregator that flushes to disk when memory threshold is reached.**

```python
import sqlite3
import threading
from collections import defaultdict
from datetime import datetime, timedelta
import psutil

class DiskSpillingAggregator:
    def __init__(self, db_path: str, memory_limit_mb: int = 100):
        self.in_memory = defaultdict(int)
        self.memory_limit = memory_limit_mb * 1024 * 1024
        self.lock = threading.Lock()
        
        # Setup SQLite for disk spillover
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aggregates 
            (symbol TEXT, volume INTEGER, window_start INTEGER, 
             window_end INTEGER, processed INTEGER DEFAULT 0)
        ''')
        self.conn.commit()
        
    def add(self, symbol: str, volume: int):
        with self.lock:
            self.in_memory[symbol] += volume
            
            # Check memory usage
            process = psutil.Process()
            if process.memory_info().rss > self.memory_limit:
                self._spill_to_disk()
    
    def _spill_to_disk(self):
        """Move in-memory aggregates to disk"""
        window_end = int(datetime.now().timestamp())
        window_start = window_end - 60  # 1-minute window
        
        for symbol, volume in self.in_memory.items():
            self.cursor.execute(
                'INSERT INTO aggregates VALUES (?, ?, ?, ?, 0)',
                (symbol, volume, window_start, window_end)
            )
        
        self.conn.commit()
        self.in_memory.clear()
        print(f"Spilled {len(self.in_memory)} symbols to disk")
    
    def get_totals(self, window_minutes: int = 5) -> dict:
        """Get totals for last N minutes from memory and disk"""
        cutoff = int((datetime.now() - timedelta(minutes=window_minutes)).timestamp())
        
        totals = defaultdict(int)
        
        # Add in-memory
        for symbol, volume in self.in_memory.items():
            totals[symbol] += volume
        
        # Add from disk
        self.cursor.execute(
            'SELECT symbol, SUM(volume) FROM aggregates '
            'WHERE window_end > ? GROUP BY symbol',
            (cutoff,)
        )
        
        for symbol, volume in self.cursor.fetchall():
            totals[symbol] += volume
        
        return dict(totals)
```

**Follow-up:** How would you make this thread-safe for multiple producers?

## 📚 Advanced Topics

### 23. **Explain the trade-offs between different stream processing frameworks (Kafka Streams vs. Spark Streaming vs. Flink).**

**Expected Answer:**
- **Kafka Streams:** Lightweight, embedded, exactly-once, but JVM-only
- **Spark Streaming:** Micro-batch processing, rich ecosystem, but higher latency
- **Flink:** True streaming, low latency, stateful processing, but complex deployment
- **ksqlDB:** SQL interface, good for simple transformations, limited for complex logic

**For 8GB RAM:** Kafka Streams or lightweight custom consumers are preferable over Spark/Flink which have higher overhead.

**Follow-up:** When would you choose a heavyweight framework like Flink over Kafka Streams?

### 24. **How would you implement exactly-once processing across multiple Kafka topics?**

**Expected Answer:**
1. **Transactional producers:** Use `transactional.id` and producer transactions
2. **Consume-transform-produce pattern:** Read from input topic, process, write to output topic atomically
3. **Store offsets with output:** Write offsets to output topic or external store
4. **Idempotent operations:** Ensure processing can be safely retried
5. **Two-phase commit:** For multiple output systems

**Code pattern:**
```python
producer = KafkaProducer(
    transactional_id='my-transactional-producer',
    enable_idempotence=True
)

producer.init_transactions()

consumer = KafkaConsumer(
    isolation_level='read_committed'
)

producer.begin_transaction()
try:
    for message in consumer:
        result = process(message)
        producer.send('output-topic', value=result)
    
    # Send offsets to transaction
    producer.send_offsets_to_transaction(
        consumer.position(consumer.assignment()),
        consumer.consumer_group_metadata()
    )
    
    producer.commit_transaction()
except Exception:
    producer.abort_transaction()
```

**Follow-up:** What are the performance implications of transactional producers?

### 25. **Describe how you would handle backpressure in a streaming pipeline.**

**Expected Answer:**
1. **Producer backpressure:** Monitor buffer memory, implement blocking with timeouts
2. **Consumer backpressure:** Pause/resume partitions based on processing capacity
3. **Rate limiting:** Use token bucket or leaky bucket algorithms
4. **Dynamic scaling:** Scale consumers based on lag metrics
5. **Load shedding:** Drop low-priority messages during overload

**Implementation:**
```python
class BackpressureConsumer:
    def __init__(self, max_queue_size=1000):
        self.processing_queue = []
        self.max_queue_size = max_queue_size
        self.consumer = KafkaConsumer(...)
    
    def process_with_backpressure(self):
        for message in self.consumer:
            # Check queue size
            if len(self.processing_queue) >= self.max_queue_size:
                # Pause consumption
                self.consumer.pause(*self.consumer.assignment())
                # Process backlog
                self._process_backlog()
                # Resume consumption
                self.consumer.resume(*self.consumer.assignment())
            
            self.processing_queue.append(message)
```

**Follow-up:** How would you implement backpressure in a multi-stage pipeline?

## 🔍 Practical Implementation Questions

### 26. **How would you test a streaming pipeline?**

**Expected Answer:**
1. **Unit tests:** Mock Kafka with `kafka-python` test utilities
2. **Integration tests:** Test container with Redpanda
3. **End-to-end tests:** Complete pipeline with synthetic data
4. **Load tests:** Generate high volume to test under pressure
5. **Fault injection:** Network partitions, broker failures
6. **Data validation:** Schema compliance, data quality checks

**Testing tools:** `testcontainers`, `pytest`, `faker` for data generation, custom mock consumers/producers.

**Follow-up:** How would you simulate network partitions in tests?

### 27. **What security considerations are important for streaming pipelines?**

**Expected Answer:**
1. **Authentication:** SASL/SCRAM, SSL certificates
2. **Authorization:** ACLs for topics/producer/consumer
3. **Encryption:** TLS for data in transit
4. **Data masking:** PII redaction in streams
5. **Audit logging:** Who produced/consumed what data
6. **Network security:** VPC, firewall rules, private endpoints

**Redpanda security:**
```yaml
# In redpanda config
sasl:
  enabled: true
  mechanism: SCRAM-SHA-256
tls:
  enabled: true
  require_client_auth: true
```

**Follow-up:** How would you implement field-level encryption for sensitive data in Kafka messages?

### 28. **How would you deploy and monitor a streaming pipeline in production?**

**Expected Answer:**
**Deployment:**
1. **Containerization:** Docker with health checks
2. **Orchestration:** Kubernetes with HPA based on consumer lag
3. **Configuration management:** Environment variables/secrets
4. **Blue-green deployment:** Zero-downtime updates
5. **Rollback strategy:** Quick revert on issues

**Monitoring:**
1. **Infrastructure:** CPU, memory, disk, network
2. **Kafka metrics:** Lag, throughput, error rates
3. **Business metrics:** Processing latency, data quality
4. **Alerting:** PagerDuty/Slack alerts for critical issues
5. **Logging:** Structured logs with correlation IDs

**Follow-up:** What would your CI/CD pipeline look like for streaming applications?

## 🎯 Final Recommendations

### Study Resources:
- **Redpanda Documentation:** https://docs.redpanda.com/
- **Kafka: The Definitive Guide** by Neha Narkhede et al.
- **Confluent Blog:** Real-world streaming patterns
- **Kafka Summit Talks:** Advanced streaming use cases

### Practice Projects:
1. Build a real-time dashboard for streaming metrics
2. Implement exactly-once processing with transactions
3. Create a schema evolution strategy for a changing data model
4. Design a multi-datacenter replication setup
5. Build a streaming ETL pipeline with joins and aggregations

### Interview Preparation:
1. **Understand trade-offs** between different streaming approaches
2. **Practice explaining** complex concepts simply
3. **Be ready for coding exercises** with memory constraints
4. **Prepare examples** from your experience with streaming
5. **Ask insightful questions** about the company's streaming needs

## 🔗 Related Resources in This Repository

- [`practice_exercises.py`](practice_exercises.py): Hands-on exercises for streaming concepts
- [`GOTCHAS_BEST_PRACTICES.md`](GOTCHAS_BEST_PRACTICES.md): Common pitfalls and solutions
- [`02_producer.py`](02_producer.py): Example producer implementation
- [`03_consumer_aggregator.py`](03_consumer_aggregator.py): Example consumer with aggregation
- [`README.md`](README.md): Project overview and setup instructions