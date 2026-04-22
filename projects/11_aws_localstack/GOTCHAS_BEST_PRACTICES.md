# AWS LocalStack Gotchas & Best Practices for 8GB RAM Environments

## 🚨 Critical Gotchas

### 1. **LocalStack Memory Consumption Spikes**
LocalStack runs multiple AWS services in Docker containers, each consuming memory. On 8GB RAM systems, this can quickly exhaust available memory.

```bash
# WRONG: Starting all services without memory limits
localstack start

# CORRECT: Limit services and configure memory
localstack start --services=s3,dynamodb --host=0.0.0.0
# Add to docker-compose.yml:
#   mem_limit: 2g
#   environment:
#     - DEFAULT_REGION=us-east-1
#     - LAMBDA_EXECUTOR=docker-reuse
```

### 2. **S3 Bucket Name Validation Differences**
LocalStack may have different bucket naming validation compared to real AWS.

```python
# WRONG: Assuming AWS S3 bucket naming rules apply exactly
bucket_name = "my.bucket.name"  # Dots may cause issues in LocalStack

# CORRECT: Use simpler bucket names for LocalStack
bucket_name = "my-bucket-name"  # Hyphens work consistently
# Or check LocalStack version compatibility
```

### 3. **DynamoDB Throughput Configuration**
LocalStack may not enforce the same throughput limits as AWS, leading to unrealistic expectations.

```python
# WRONG: Assuming unlimited throughput in production
table = dynamodb.create_table(
    TableName='users',
    BillingMode='PAY_PER_REQUEST'  # LocalStack may not simulate throttling
)

# CORRECT: Test with realistic limits
# 1. Set explicit provisioned throughput
# 2. Implement retry logic with exponential backoff
# 3. Monitor response times
```

### 4. **IAM Policy Simulation Gaps**
LocalStack's IAM simulation may not match AWS's exact permission evaluation logic.

```python
# WRONG: Assuming IAM policy evaluation is identical
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:*",
        "Resource": "*"
    }]
}
# LocalStack may allow this, but AWS would require more specific resources

# CORRECT: Use AWS Policy Simulator for production validation
# Keep LocalStack for basic permission testing only
```

### 5. **Data Persistence Across Restarts**
LocalStack data is ephemeral by default, disappearing on container restart.

```bash
# WRONG: Assuming data persists
docker-compose down
docker-compose up -d
# All S3 buckets and DynamoDB tables are gone!

# CORRECT: Configure persistence
# In docker-compose.yml:
#   volumes:
#     - "./localstack_data:/var/lib/localstack"
#   environment:
#     - PERSISTENCE=1
```

### 6. **Endpoint URL Configuration**
Forgetting to configure endpoint URLs leads to calls going to real AWS.

```python
# WRONG: No endpoint override
s3_client = boto3.client('s3')
# This connects to real AWS S3!

# CORRECT: Always set endpoint URL for LocalStack
import boto3
from botocore.config import Config

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)
```

### 7. **Large File Handling Limitations**
LocalStack may have different memory handling for large S3 objects.

```python
# WRONG: Uploading 1GB file directly
with open('large_file.bin', 'rb') as f:
    s3_client.upload_fileobj(f, 'my-bucket', 'large_file.bin')
# May cause memory issues in LocalStack

# CORRECT: Use multipart upload for large files
# Or chunk files for LocalStack testing
def upload_large_file_safely(file_path, bucket, key, chunk_size=10*1024*1024):
    # Implement chunked upload
    pass
```

### 8. **DynamoDB Streams and Lambda Integration**
LocalStack's event-driven architecture may have timing issues.

```python
# WRONG: Assuming immediate Lambda invocation
# DynamoDB stream → Lambda may have delays in LocalStack

# CORRECT: Add polling/retry logic in tests
import time

def wait_for_lambda_invocation(max_wait=30):
    start = time.time()
    while time.time() - start < max_wait:
        # Check if Lambda was invoked
        if lambda_was_invoked():
            return True
        time.sleep(1)
    return False
```

## ✅ Best Practices

### 1. **Memory Optimization for 8GB RAM**

```yaml
# docker-compose.yml optimization
version: '3.8'
services:
  localstack:
    image: localstack/localstack
    mem_limit: 2g  # Limit LocalStack container memory
    environment:
      - SERVICES=s3,dynamodb  # Only start needed services
      - DEBUG=0  # Disable debug mode to reduce memory
      - DATA_DIR=/tmp/localstack_data
      - LAMBDA_EXECUTOR=docker-reuse  # Reuse containers
      - DOCKER_HOST=unix:///var/run/docker.sock
    ports:
      - "4566:4566"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./localstack_data:/tmp/localstack_data"
```

### 2. **Service Isolation Strategy**

```python
# Create separate test environments
class LocalStackTestEnvironment:
    def __init__(self, services=None):
        self.services = services or ['s3', 'dynamodb']
        self.clients = {}
        
    def start(self):
        # Start only required services
        subprocess.run([
            'localstack', 'start',
            '--services', ','.join(self.services),
            '--host', '0.0.0.0'
        ])
        
    def get_client(self, service):
        if service not in self.clients:
            self.clients[service] = boto3.client(
                service,
                endpoint_url='http://localhost:4566',
                region_name='us-east-1'
            )
        return self.clients[service]
```

### 3. **Resource Cleanup Automation**

```python
import boto3
import contextlib

@contextlib.contextmanager
def temporary_s3_bucket(s3_client, bucket_name):
    """Context manager for temporary S3 bucket."""
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        yield bucket_name
    finally:
        # Clean up all objects
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                objects = [{'Key': obj['Key']} for obj in page['Contents']]
                s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': objects}
                )
        # Delete bucket
        s3_client.delete_bucket(Bucket=bucket_name)

# Usage
with temporary_s3_bucket(s3_client, 'test-bucket-123') as bucket:
    # Test code here
    s3_client.put_object(Bucket=bucket, Key='test.txt', Body=b'Hello')
```

### 4. **Realistic Data Volume Testing**

```python
def generate_test_data_with_memory_limits(num_records, max_memory_mb=500):
    """Generate test data within memory constraints."""
    record_size_bytes = 1024  # 1KB per record
    total_size_mb = (num_records * record_size_bytes) / (1024 * 1024)
    
    if total_size_mb > max_memory_mb:
        # Use generator for large datasets
        def record_generator():
            for i in range(num_records):
                yield {
                    'id': str(i),
                    'data': 'x' * (record_size_bytes - 100),
                    'timestamp': datetime.now().isoformat()
                }
        return record_generator()
    else:
        # Generate list for small datasets
        return [
            {
                'id': str(i),
                'data': 'x' * (record_size_bytes - 100),
                'timestamp': datetime.now().isoformat()
            }
            for i in range(num_records)
        ]
```

### 5. **Error Handling and Retry Logic**

```python
from botocore.exceptions import ClientError
import time

def aws_operation_with_retry(operation_func, max_retries=3, delay=1):
    """Execute AWS operation with retry logic."""
    for attempt in range(max_retries):
        try:
            return operation_func()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            # Retry on specific errors
            if error_code in ['ThrottlingException', 'RequestLimitExceeded']:
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                raise
        except ConnectionError:
            # LocalStack might be restarting
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
```

### 6. **Performance Monitoring**

```python
import psutil
import time

class ResourceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
        
    def check_memory_usage(self, warning_threshold_mb=4000):
        """Check if memory usage is approaching 8GB limit."""
        current_memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
        if current_memory_mb > warning_threshold_mb:
            print(f"⚠️  Warning: Memory usage at {current_memory_mb:.1f}MB")
            return False
        return True
    
    def log_performance(self, operation_name):
        elapsed = time.time() - self.start_time
        memory_used_mb = (psutil.Process().memory_info().rss - self.start_memory) / (1024 * 1024)
        print(f"📊 {operation_name}: {elapsed:.2f}s, {memory_used_mb:.1f}MB")

# Usage in tests
monitor = ResourceMonitor()
# Perform operations
monitor.log_performance("S3 upload batch")
```

### 7. **Configuration Management**

```python
import os
from enum import Enum

class Environment(Enum):
    LOCALSTACK = "localstack"
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"

def get_aws_config(env=Environment.LOCALSTACK):
    """Get AWS configuration based on environment."""
    configs = {
        Environment.LOCALSTACK: {
            'endpoint_url': 'http://localhost:4566',
            'region_name': 'us-east-1',
            'use_ssl': False,
            'verify': False
        },
        Environment.DEVELOPMENT: {
            'endpoint_url': None,  # Use default
            'region_name': os.getenv('AWS_REGION', 'us-east-1'),
            'use_ssl': True,
            'verify': True
        },
        Environment.PRODUCTION: {
            'endpoint_url': None,
            'region_name': os.getenv('AWS_REGION', 'us-east-1'),
            'use_ssl': True,
            'verify': True
        }
    }
    
    return configs[env]

# Usage
config = get_aws_config(Environment.LOCALSTACK)
s3_client = boto3.client('s3', **config)
```

### 8. **Test Data Generation Optimization**

```python
import json
import gzip
from io import BytesIO

def generate_compressed_test_data(num_records, compression=True):
    """Generate test data with optional compression for memory efficiency."""
    data = [
        {
            'id': i,
            'value': f"test_value_{i}",
            'metadata': {'index': i, 'timestamp': time.time()}
        }
        for i in range(num_records)
    ]
    
    if compression:
        # Compress to reduce memory footprint
        json_str = json.dumps(data)
        buffer = BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='w') as f:
            f.write(json_str.encode())
        buffer.seek(0)
        return buffer
    else:
        return data
```

## 🎯 Production Readiness Checklist

### Before Deployment:
- [ ] Test with realistic data volumes (not just toy examples)
- [ ] Verify error handling works with real AWS error codes
- [ ] Test IAM policies with AWS Policy Simulator
- [ ] Validate S3 bucket naming conventions
- [ ] Test DynamoDB throughput with expected production loads
- [ ] Verify multipart upload for large files
- [ ] Test cross-region replication scenarios (if applicable)

### Memory Management:
- [ ] Set memory limits in docker-compose.yml
- [ ] Monitor memory usage during test execution
- [ ] Implement chunking for large operations
- [ ] Clean up temporary resources
- [ ] Use generators instead of lists for large datasets

### Performance:
- [ ] Benchmark operations with 8GB RAM constraints
- [ ] Implement retry logic with exponential backoff
- [ ] Cache frequently accessed metadata
- [ ] Use connection pooling for DynamoDB
- [ ] Implement pagination for large result sets

## 🔧 Debugging Tips

1. **Check LocalStack Logs:**
   ```bash
   docker logs localstack_main  # Main container
   docker-compose logs -f       # All services
   ```

2. **Verify Service Health:**
   ```bash
   curl http://localhost:4566/health
   # Should return {"services": {"s3": "running", "dynamodb": "running"}}
   ```

3. **Reset LocalStack State:**
   ```bash
   docker-compose down -v  # Remove volumes
   docker-compose up -d
   ```

4. **Monitor Resource Usage:**
   ```bash
   docker stats  # Container resource usage
   top           # System resource usage
   ```

## 📚 Integration with Curriculum

This module connects to:
- **Week 4 (Databases & Docker)**: Containerization concepts
- **Week 9 (FastAPI)**: Building APIs that interact with AWS services
- **Week 12 (Data API Service)**: Production API patterns
- **Week 20 (Tested Pipeline)**: Testing AWS integrations

By mastering these gotchas and best practices, you'll be prepared to work with AWS services in both local development and production environments while respecting 8GB RAM constraints.