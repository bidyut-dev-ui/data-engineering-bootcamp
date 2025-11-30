# Week 29: Observability & Monitoring

**Goal**: Learn to monitor production systems with Prometheus and Grafana, implement structured logging, and set up alerting.

## Scenario
Your data platform is in production. You need visibility into system health, performance metrics, and the ability to detect and respond to issues before users are impacted.

## Concepts Covered
1. **Prometheus**: Metrics collection and storage
2. **Grafana**: Visualization and dashboards
3. **Metrics Types**: Counter, Gauge, Histogram, Summary
4. **Structured Logging**: JSON logs for easy parsing
5. **Alerting**: Proactive issue detection
6. **SLIs/SLOs**: Service Level Indicators/Objectives
7. **Observability**: Metrics, Logs, Traces (the three pillars)

## Structure
- `api/main.py`: FastAPI with Prometheus metrics
- `prometheus/prometheus.yml`: Prometheus configuration
- `grafana/dashboards/`: Grafana dashboard JSON
- `docker-compose.yml`: Full monitoring stack
- `load_test.sh`: Generate traffic for testing

## Instructions

### 1. Start the Monitoring Stack
```bash
cd projects/21_monitored_platform
docker compose up -d
```

**Services**:
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

### 2. Access Prometheus
Visit `http://localhost:9090`

**Try these queries**:
```promql
# Request rate (requests per second)
rate(api_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))

# Active requests
api_active_requests

# Error rate
rate(pipeline_errors_total[5m])
```

### 3. Access Grafana
Visit `http://localhost:3000`
- **Username**: `admin`
- **Password**: `admin`

**Setup**:
1. Add Prometheus data source:
   - URL: `http://prometheus:9090`
   - Click "Save & Test"

2. Import dashboard:
   - Go to Dashboards → Import
   - Upload `grafana/dashboards/api-dashboard.json`

**What You'll See**:
- Request rate over time
- 95th percentile latency gauge
- Error rates
- Active requests

### 4. Generate Traffic
```bash
# Install hey (HTTP load generator)
# Ubuntu/WSL:
sudo apt-get install hey

# Or use curl in a loop:
for i in {1..100}; do
  curl http://localhost:8000/data/process?records=50
  sleep 0.1
done
```

Watch the metrics update in real-time!

### 5. Test Error Tracking
```bash
# Generate some errors
for i in {1..10}; do
  curl http://localhost:8000/data/error
done
```

Check Prometheus: `pipeline_errors_total`

## Metrics Explained

### **Counter**: Always increases
```python
request_count = Counter('api_requests_total', 'Total requests')
request_count.inc()  # Increment by 1
```

**Use for**: Total requests, errors, processed records

### **Gauge**: Can go up or down
```python
active_requests = Gauge('api_active_requests', 'Active requests')
active_requests.inc()  # +1
active_requests.dec()  # -1
active_requests.set(5)  # Set to 5
```

**Use for**: Current connections, queue size, memory usage

### **Histogram**: Distribution of values
```python
request_duration = Histogram('api_request_duration_seconds', 'Request duration')
request_duration.observe(0.25)  # Record 0.25 seconds
```

**Use for**: Latency, request size, processing time

**Queries**:
```promql
# Average
rate(api_request_duration_seconds_sum[5m]) / rate(api_request_duration_seconds_count[5m])

# 95th percentile
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))
```

## Structured Logging

### **JSON Logs** (Easy to Parse)
```python
import json
import logging

logger = logging.getLogger(__name__)

# Configure JSON formatter
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# Log with context
logger.info("Request processed", extra={
    "user_id": 123,
    "endpoint": "/data/process",
    "duration_ms": 250,
    "status": "success"
})
```

**Output**:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "user_id": 123,
  "endpoint": "/data/process",
  "duration_ms": 250,
  "status": "success"
}
```

**Benefits**:
- Easy to search (grep, jq)
- Can be ingested by log aggregators (ELK, Splunk)
- Structured queries

## Homework / Challenge

### Challenge 1: Add Custom Metrics
Add these metrics to `api/main.py`:
```python
# Database query duration
db_query_duration = Histogram('db_query_duration_seconds', 'DB query duration')

# Cache hit rate
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')
```

### Challenge 2: Create Alerting Rules
Create `prometheus/alerts.yml`:
```yaml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(pipeline_errors_total[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "95th percentile latency > 1s"
```

### Challenge 3: Add Structured Logging
Create `api/logging_config.py`:
```python
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName
        }
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        return json.dumps(log_data)
```

### Challenge 4: SLO Dashboard
Define Service Level Objectives:
- **Availability**: 99.9% uptime
- **Latency**: 95% of requests < 500ms
- **Error Rate**: < 1% of requests fail

Create Grafana dashboard showing:
- Current SLO compliance
- Error budget remaining
- Trend over time

## Production Best Practices

### **1. The Four Golden Signals**
Monitor these for every service:
1. **Latency**: How long requests take
2. **Traffic**: How many requests
3. **Errors**: Rate of failed requests
4. **Saturation**: How "full" the service is (CPU, memory, connections)

### **2. Metric Naming Convention**
```
<namespace>_<subsystem>_<name>_<unit>

Examples:
api_http_requests_total
api_http_request_duration_seconds
db_query_errors_total
cache_hit_ratio
```

### **3. Label Cardinality**
```python
# Good: Low cardinality
request_count.labels(method="GET", endpoint="/users", status="200")

# Bad: High cardinality (unique user IDs)
request_count.labels(user_id="12345")  # Don't do this!
```

### **4. Retention**
- **Prometheus**: 15 days (default)
- **Long-term**: Use Thanos or Cortex
- **Logs**: 30-90 days

## Expected Learning Outcomes
- ✅ Set up Prometheus and Grafana
- ✅ Instrument code with metrics
- ✅ Create meaningful dashboards
- ✅ Understand the four golden signals
- ✅ Implement structured logging
- ✅ Set up basic alerting

## Interview Questions

**Q: What are the three pillars of observability?**
A: Metrics (what's happening), Logs (detailed events), Traces (request flow through system).

**Q: What's the difference between monitoring and observability?**
A: Monitoring tells you WHEN something is wrong. Observability helps you understand WHY.

**Q: What metrics would you track for a data pipeline?**
A: Records processed, processing duration, error rate, data quality issues, pipeline lag.

**Q: How do you prevent alert fatigue?**
A: Set meaningful thresholds, use SLOs, group related alerts, implement escalation policies.

## Cleanup
```bash
docker compose down -v
```
