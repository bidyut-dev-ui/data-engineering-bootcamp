# Streaming with Redpanda: Gotchas & Best Practices

## 🚨 Critical Gotchas in Streaming Pipelines

### 1. **Memory Explosion from Unbounded In-Memory Aggregation**

**WRONG:** Keeping all aggregation state in memory indefinitely
```python
# Problem: This dictionary grows without bound
volume_aggregation = {}
for message in consumer:
    symbol = message.value['symbol']
    volume_aggregation[symbol] = volume_aggregation.get(symbol, 0) + message.value['volume']
    # Dictionary grows forever as new symbols appear
```

**CORRECT:** Implement windowed aggregation with cleanup
```python
from collections import defaultdict
import time

# Time-based windowing (1-minute windows)
window_duration = 60  # seconds
window_start = time.time()
volume_aggregation = defaultdict(int)

for message in consumer:
    # Check if window expired
    current_time = time.time()
    if current_time - window_start > window_duration:
        # Process and reset window
        print(f"Window results: {dict(volume_aggregation)}")
        volume_aggregation.clear()
        window_start = current_time
    
    # Aggregate within window
    symbol = message.value['symbol']
    volume_aggregation[symbol] += message.value['volume']
```

### 2. **Consumer Lag Causing Memory Pressure**

**WRONG:** Processing messages slower than they arrive
```python
consumer = KafkaConsumer(
    'financial_ticks',
    bootstrap_servers=['localhost:19092'],
    auto_offset_reset='latest',  # Ignores backlog
    enable_auto_commit=True,
    group_id='my-group'
)

for message in consumer:
    # Heavy processing that takes 1 second per message
    time.sleep(1)  # Messages arrive every 0.1 seconds
    # Result: Consumer lag grows, memory fills with buffered messages
```

**CORRECT:** Batch processing with appropriate configuration
```python
consumer = KafkaConsumer(
    'financial_ticks',
    bootstrap_servers=['localhost:19092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Manual commit for control
    group_id='my-group',
    max_poll_records=100,  # Limit batch size
    fetch_max_bytes=1048576,  # 1MB max fetch
    max_partition_fetch_bytes=1048576
)

# Process in batches
while True:
    batch = consumer.poll(timeout_ms=1000, max_records=100)
    for tp, messages in batch.items():
        for message in messages:
            process_message(message)
        # Commit after processing batch
        consumer.commit()
```

### 3. **Producer Blocking on Full Buffer**

**WRONG:** Producer without backpressure handling
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Rapid fire without checking buffer
for i in range(1000000):
    producer.send('topic', value={'data': i})
    # Buffer fills, blocks indefinitely
```

**CORRECT:** Implement backpressure with timeouts
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    max_block_ms=5000,  # 5 second timeout
    buffer_memory=33554432,  # 32MB buffer (not default 32MB)
    batch_size=16384  # 16KB batches
)

messages_in_flight = 0
MAX_IN_FLIGHT = 1000

for i in range(1000000):
    # Check if we're overwhelming the producer
    while messages_in_flight >= MAX_IN_FLIGHT:
        producer.flush(timeout=1.0)
        messages_in_flight = producer.in_flight_request_count()
    
    future = producer.send('topic', value={'data': i})
    messages_in_flight += 1
    
    # Optional: Add callback to track completion
    def callback(metadata, exception):
        nonlocal messages_in_flight
        messages_in_flight -= 1
        if exception:
            print(f"Failed to send: {exception}")
    
    future.add_callback(callback)
```

### 4. **Missing Error Handling Causing Silent Data Loss**

**WRONG:** No error handling in consumer loop
```python
for message in consumer:
    data = message.value
    # If this fails, loop breaks and consumer stops
    result = complex_processing(data['field_that_might_not_exist'])
```

**CORRECT:** Comprehensive error handling with dead-letter queue
```python
from kafka import KafkaProducer

# Setup dead-letter producer
dlq_producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for message in consumer:
    try:
        data = message.value
        # Safe access with defaults
        symbol = data.get('symbol', 'UNKNOWN')
        volume = data.get('volume', 0)
        
        if volume <= 0:
            raise ValueError(f"Invalid volume: {volume}")
        
        # Process message
        process_tick(symbol, volume)
        
        # Commit offset only on success
        consumer.commit()
        
    except KeyError as e:
        print(f"Missing field {e} in message: {data}")
        # Send to dead-letter queue for analysis
        dlq_producer.send('dead_letter_queue', value={
            'original': data,
            'error': str(e),
            'timestamp': time.time()
        })
        # Skip this message but continue
        consumer.commit()
        
    except ValueError as e:
        print(f"Validation error: {e}")
        # Send to validation error queue
        dlq_producer.send('validation_errors', value={
            'original': data,
            'error': str(e)
        })
        consumer.commit()
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Don't commit - retry on restart
        # Or implement exponential backoff
        time.sleep(5)  # Brief pause before retry
```

## 🎯 Best Practices for 8GB RAM Environments

### 1. **Memory-Efficient Consumer Configuration**

```python
consumer = KafkaConsumer(
    'financial_ticks',
    bootstrap_servers=['localhost:19092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='volume-aggregator-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    
    # Memory optimization settings
    fetch_max_bytes=524288,      # 512KB per fetch (reduces buffer)
    max_partition_fetch_bytes=524288,
    max_poll_records=500,        # Process 500 messages max per poll
    fetch_max_wait_ms=500,       # Wait up to 500ms for data
    heartbeat_interval_ms=3000,  # Keep heartbeat reasonable
    session_timeout_ms=10000,
    
    # Critical for memory: don't buffer too much
    max_poll_interval_ms=300000,  # 5 minutes max between polls
)
```

### 2. **Streaming Aggregation with Periodic Flush**

```python
import sqlite3
import threading

class MemoryEfficientAggregator:
    def __init__(self, db_path='aggregation.db', flush_interval=1000):
        self.db_path = db_path
        self.flush_interval = flush_interval
        self.in_memory = defaultdict(int)
        self.count = 0
        
        # Setup SQLite for overflow
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aggregates 
            (symbol TEXT, volume INTEGER, timestamp INTEGER)
        ''')
        self.conn.commit()
        
        # Lock for thread safety
        self.lock = threading.Lock()
    
    def add(self, symbol, volume):
        with self.lock:
            self.in_memory[symbol] += volume
            self.count += 1
            
            # Flush to disk if threshold reached
            if self.count >= self.flush_interval:
                self._flush_to_disk()
    
    def _flush_to_disk(self):
        timestamp = int(time.time())
        for symbol, volume in self.in_memory.items():
            self.cursor.execute(
                'INSERT INTO aggregates VALUES (?, ?, ?)',
                (symbol, volume, timestamp)
            )
        self.conn.commit()
        self.in_memory.clear()
        self.count = 0
    
    def get_totals(self):
        # Combine in-memory and disk data
        totals = dict(self.in_memory)
        self.cursor.execute('SELECT symbol, SUM(volume) FROM aggregates GROUP BY symbol')
        for symbol, volume in self.cursor.fetchall():
            totals[symbol] = totals.get(symbol, 0) + volume
        return totals
```

### 3. **Producer Optimization for High Throughput**

```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    
    # Optimize for throughput with memory limits
    batch_size=16384,           # 16KB batches
    linger_ms=5,                # Wait up to 5ms to batch
    compression_type='gzip',    # Compress to reduce network/memory
    buffer_memory=16777216,     # 16MB buffer (half of default)
    max_request_size=1048576,   # 1MB max request size
    retries=3,                  # Retry failed sends
    retry_backoff_ms=100,       # Backoff between retries
    
    # Critical: don't block indefinitely
    max_block_ms=5000,          # 5 second timeout
    request_timeout_ms=30000,   # 30 second request timeout
)

# Efficient sending pattern
def send_efficiently(producer, topic, data):
    """Send with memory awareness"""
    try:
        # Check if buffer is getting full
        if producer._metadata.buffer_available_bytes() < 1024 * 1024:  # 1MB left
            producer.flush(timeout=1.0)
        
        future = producer.send(topic, value=data)
        
        # Non-blocking check with timeout
        try:
            future.get(timeout=2.0)
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            return False
            
    except Exception as e:
        print(f"Producer error: {e}")
        return False
```

### 4. **Monitoring Memory Usage in Streaming Apps**

```python
import psutil
import resource
import threading

class MemoryMonitor:
    def __init__(self, warning_mb=6000, critical_mb=7000):
        self.warning_mb = warning_mb
        self.critical_mb = critical_mb
        self.process = psutil.Process()
        self.running = True
        
    def start_monitoring(self, interval=10):
        """Start background memory monitoring"""
        def monitor():
            while self.running:
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                
                if memory_mb > self.critical_mb:
                    print(f"🚨 CRITICAL: Memory at {memory_mb:.1f}MB")
                    # Trigger emergency actions
                    self._emergency_cleanup()
                    
                elif memory_mb > self.warning_mb:
                    print(f"⚠️ WARNING: Memory at {memory_mb:.1f}MB")
                    # Trigger gentle cleanup
                    self._gentle_cleanup()
                
                time.sleep(interval)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        return thread
    
    def _emergency_cleanup(self):
        """Emergency actions when memory is critical"""
        # 1. Force garbage collection
        import gc
        gc.collect()
        
        # 2. Reduce Kafka buffer sizes if possible
        # 3. Log state and prepare for graceful degradation
        print("Emergency cleanup triggered")
        
    def _gentle_cleanup(self):
        """Preventative cleanup when memory is high"""
        # Clear caches, flush buffers, etc.
        print("Gentle cleanup triggered")

# Usage in streaming app
monitor = MemoryMonitor(warning_mb=6000, critical_mb=7000)
monitor.start_monitoring()
```

## 🔧 Configuration Recommendations for 8GB RAM

### Redpanda/Docker Compose Configuration:
```yaml
# docker-compose.yml
version: '3.7'
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v23.2.11
    command:
      - redpanda
      - start
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082
      - --rpc-addr 0.0.0.0:33145
      - --memory=2G  # Limit Redpanda memory usage
      - --smp=1      # Single CPU core
      - --overprovisioned
    ports:
      - "18082:18082"
      - "19092:19092"
      - "8080:8080"  # Redpanda Console
```

### Topic Configuration for Memory Efficiency:
```bash
# Create topics with appropriate retention
rpk topic create financial_ticks \
  --partitions 3 \
  --replicas 1 \
  --retention-time 1h \        # Keep data for 1 hour only
  --segment-bytes 100000000 \  # 100MB segments
  --retention-bytes 1000000000 # 1GB total retention
```

## 📊 Performance Expectations on 8GB RAM

| Scenario | Expected Throughput | Memory Usage | Recommendations |
|----------|-------------------|--------------|-----------------|
| **Low volume** (100 msg/sec) | < 1% CPU | ~200MB | Single consumer, no batching needed |
| **Medium volume** (1,000 msg/sec) | 5-10% CPU | ~500MB | Enable batching, consider compression |
| **High volume** (10,000 msg/sec) | 20-30% CPU | 1-2GB | Multiple partitions, optimized serialization |
| **Very high volume** (100,000 msg/sec) | 50%+ CPU | 3-4GB | Multiple consumers, disk spillover |

## 🛠️ Debugging Common Issues

### 1. **Consumer Not Receiving Messages**
```python
# Check consumer assignment
print(consumer.assignment())  # Should show partitions
print(consumer.beginning_offsets(consumer.assignment()))  # Check offsets

# Check if group is balanced
print(consumer.poll(timeout_ms=1000))  # Should return messages
```

### 2. **High Memory Usage**
```bash
# Monitor Redpanda memory
docker stats redpanda

# Check Python process memory
ps aux | grep python | grep -v grep

# Check Kafka buffer memory
print(producer.config['buffer_memory'])
print(producer._metadata.buffer_available_bytes())
```

### 3. **Slow Processing Causing Lag**
```python
# Monitor consumer lag
from kafka import KafkaAdminClient
from kafka.admin import ConsumerGroupDescription

admin = KafkaAdminClient(bootstrap_servers='localhost:19092')
group_desc = admin.describe_consumer_groups(['volume-aggregator-group'])
print(group_desc)

# Or use rpk CLI
# rpk group describe volume-aggregator-group
```

## 🎯 Key Takeaways

1. **Always implement windowing** for aggregations to prevent unbounded memory growth
2. **Configure appropriate batch sizes** and buffer limits based on your RAM
3. **Monitor memory continuously** and have emergency cleanup procedures
4. **Use dead-letter queues** for error handling instead of stopping the pipeline
5. **Test with production-like data volumes** before deployment
6. **Plan for scale** with multiple partitions and consumer groups
7. **Implement backpressure** to prevent overwhelming producers/consumers
8. **Regularly commit offsets** to minimize reprocessing on restart

## 🔗 Related Resources

- [Redpanda Documentation](https://docs.redpanda.com/)
- [Kafka-Python Best Practices](https://kafka-python.readthedocs.io/en/master/usage.html)
- [Streaming Architecture Patterns](https://www.confluent.io/patterns/)
- [Memory Management in Python](https://realpython.com/python-memory-management/)