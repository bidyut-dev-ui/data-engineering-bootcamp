# AWS LocalStack Interview Questions

## 📋 Fundamentals

### 1. What is AWS LocalStack and why is it used in data engineering?
LocalStack is a fully functional local cloud stack that emulates AWS services on your local machine. It's used for:
- **Local development**: Test AWS integrations without incurring costs
- **CI/CD pipelines**: Run integration tests without connecting to real AWS
- **Offline development**: Work without internet connectivity
- **Cost savings**: Avoid AWS charges during development
- **Rapid prototyping**: Quickly test AWS service interactions

### 2. How does LocalStack differ from AWS CloudFormation Local or SAM Local?
- **LocalStack**: Emulates multiple AWS services (S3, DynamoDB, Lambda, etc.)
- **SAM Local**: Specifically for Serverless Application Model, focuses on Lambda/API Gateway
- **CloudFormation Local**: Validates CloudFormation templates locally
- **Key difference**: LocalStack provides actual service emulation, while others focus on template validation

### 3. What are the main components of LocalStack architecture?
1. **Gateway**: Single endpoint (localhost:4566) that routes requests
2. **Service emulators**: Individual components for each AWS service
3. **Persistence layer**: Optional data persistence across restarts
4. **Docker integration**: Runs services in containers
5. **Proxy layer**: Translates AWS SDK calls to local service calls

### 4. Explain the memory considerations when running LocalStack on an 8GB RAM machine.
```yaml
# Critical considerations:
1. Service Selection: Only run needed services (not all 80+)
2. Container Limits: Set mem_limit in docker-compose.yml
3. Data Volume: Limit test data size
4. Concurrent Operations: Control parallel requests
5. Cleanup: Regular resource cleanup

# Example configuration for 8GB RAM:
services:
  localstack:
    mem_limit: 2g
    environment:
      - SERVICES=s3,dynamodb  # Only essential services
      - DEBUG=0  # Disable debug to save memory
```

## 🔧 Technical Implementation

### 5. How do you configure boto3 to work with LocalStack?
```python
import boto3
from botocore.config import Config

# Correct configuration
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',  # LocalStack endpoint
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    ),
    region_name='us-east-1',
    aws_access_key_id='test',      # Dummy credentials
    aws_secret_access_key='test'   # Dummy credentials
)

# Common mistake: Forgetting endpoint_url
# This would connect to real AWS!
```

### 6. What are the limitations of LocalStack compared to real AWS?
1. **Service coverage**: Not all AWS services are fully implemented
2. **Scale limitations**: No true auto-scaling or load balancing
3. **Performance characteristics**: Different latency/throughput patterns
4. **IAM simulation**: Simplified permission model
5. **Regional differences**: Single region (us-east-1) by default
6. **Data persistence**: Ephemeral by default, requires configuration
7. **Cost simulation**: No cost tracking or billing alerts

### 7. How would you handle large file uploads to S3 in LocalStack with memory constraints?
```python
def upload_large_file_with_memory_management(file_path, bucket, key, chunk_size=10*1024*1024):
    """Upload large files with chunking for 8GB RAM environments."""
    import boto3
    from botocore.exceptions import ClientError
    
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    
    # Check file size
    file_size = os.path.getsize(file_path)
    
    if file_size > 100 * 1024 * 1024:  # 100MB threshold
        # Use multipart upload
        mpu = s3.create_multipart_upload(Bucket=bucket, Key=key)
        
        parts = []
        with open(file_path, 'rb') as f:
            part_number = 1
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Upload part
                part = s3.upload_part(
                    Bucket=bucket,
                    Key=key,
                    PartNumber=part_number,
                    UploadId=mpu['UploadId'],
                    Body=chunk
                )
                parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                part_number += 1
                
                # Clear memory
                del chunk
        
        # Complete multipart upload
        s3.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=mpu['UploadId'],
            MultipartUpload={'Parts': parts}
        )
    else:
        # Direct upload for smaller files
        with open(file_path, 'rb') as f:
            s3.upload_fileobj(f, bucket, key)
    
    return True
```

### 8. How do you implement retry logic for DynamoDB operations in LocalStack?
```python
import time
from botocore.exceptions import ClientError
from functools import wraps

def retry_on_throttling(max_retries=3, delay=1):
    """Decorator for retrying throttled DynamoDB operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    
                    # Retry on throttling errors
                    if error_code in ['ThrottlingException', 'ProvisionedThroughputExceededException']:
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
            return None
        return wrapper
    return decorator

# Usage
@retry_on_throttling(max_retries=5, delay=2)
def put_item_with_retry(table, item):
    """Put item with automatic retry on throttling."""
    response = table.put_item(Item=item)
    return response
```

## 🎯 Advanced Scenarios

### 9. How would you simulate a data pipeline from S3 to DynamoDB using LocalStack?
```python
def s3_to_dynamodb_pipeline(bucket_name, table_name, batch_size=100):
    """Simulate production data pipeline in LocalStack."""
    import boto3
    import json
    
    # Initialize clients
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
    table = dynamodb.Table(table_name)
    
    # List objects in S3
    objects = s3.list_objects_v2(Bucket=bucket_name)
    
    batch_items = []
    for obj in objects.get('Contents', []):
        # Get object from S3
        response = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
        data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Transform data
        transformed = transform_data_for_dynamodb(data)
        
        # Add to batch
        batch_items.append({'PutRequest': {'Item': transformed}})
        
        # Batch write when batch is full
        if len(batch_items) >= batch_size:
            table.batch_write_item(RequestItems={table_name: batch_items})
            batch_items = []
    
    # Write remaining items
    if batch_items:
        table.batch_write_item(RequestItems={table_name: batch_items})
    
    return len(objects.get('Contents', []))

def transform_data_for_dynamodb(data):
    """Transform S3 data for DynamoDB schema."""
    # Example transformation
    return {
        'id': data.get('id') or str(uuid.uuid4()),
        'timestamp': data.get('timestamp') or int(time.time()),
        'data': data.get('payload', {}),
        'metadata': {
            'source': 's3_pipeline',
            'processed_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
```

### 10. What strategies would you use to test IAM policies with LocalStack?
```python
def test_iam_policy_with_localstack(policy_document, actions, resources):
    """Test IAM policy evaluation in LocalStack."""
    import boto3
    
    # Note: LocalStack has limited IAM simulation
    # For comprehensive testing, use AWS Policy Simulator
    
    iam = boto3.client('iam', endpoint_url='http://localhost:4566')
    
    # Create test user and policy
    user_name = 'test-user-' + str(int(time.time()))
    policy_name = 'test-policy-' + str(int(time.time()))
    
    try:
        # Create user
        iam.create_user(UserName=user_name)
        
        # Create policy
        policy = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        
        # Attach policy to user
        iam.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy['Policy']['Arn']
        )
        
        # Simulate actions (LocalStack may not fully simulate)
        # In production, use AWS Policy Simulator API
        print(f"Policy created: {policy_name}")
        print("Note: LocalStack IAM simulation is limited")
        print("Use AWS Policy Simulator for accurate evaluation")
        
        return True
        
    except Exception as e:
        print(f"IAM test failed: {e}")
        return False
        
    finally:
        # Cleanup
        try:
            iam.detach_user_policy(UserName=user_name, PolicyArn=policy['Policy']['Arn'])
            iam.delete_policy(PolicyArn=policy['Policy']['Arn'])
            iam.delete_user(UserName=user_name)
        except:
            pass
```

### 11. How do you handle schema evolution in DynamoDB with LocalStack?
```python
class DynamoDBSchemaManager:
    """Manage DynamoDB schema evolution in LocalStack."""
    
    def __init__(self, table_name, endpoint_url='http://localhost:4566'):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.table_name = table_name
        self.table = None
    
    def create_table_with_schema(self, schema_version=1):
        """Create table with versioned schema."""
        schemas = {
            1: {
                'KeySchema': [
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                'AttributeDefinitions': [
                    {'AttributeName': 'id', 'AttributeType': 'S'}
                ]
            },
            2: {
                'KeySchema': [
                    {'AttributeName': 'pk', 'KeyType': 'HASH'},
                    {'AttributeName': 'sk', 'KeyType': 'RANGE'}
                ],
                'AttributeDefinitions': [
                    {'AttributeName': 'pk', 'AttributeType': 'S'},
                    {'AttributeName': 'sk', 'AttributeType': 'S'}
                ],
                'GlobalSecondaryIndexes': [
                    {
                        'IndexName': 'gsi1',
                        'KeySchema': [
                            {'AttributeName': 'sk', 'KeyType': 'HASH'},
                            {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ]
            }
        }
        
        schema = schemas.get(schema_version, schemas[1])
        
        self.table = self.dynamodb.create_table(
            TableName=f"{self.table_name}_v{schema_version}",
            **schema,
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Wait for table to be created
        self.table.wait_until_exists()
        return self.table
    
    def migrate_data(self, from_version, to_version):
        """Migrate data between schema versions."""
        old_table = self.dynamodb.Table(f"{self.table_name}_v{from_version}")
        new_table = self.dynamodb.Table(f"{self.table_name}_v{to_version}")
        
        # Scan old table
        response = old_table.scan()
        items = response.get('Items', [])
        
        # Transform and write to new table
        with new_table.batch_writer() as batch:
            for item in items:
                transformed = self.transform_item(item, from_version, to_version)
                batch.put_item(Item=transformed)
        
        return len(items)
    
    def transform_item(self, item, from_version, to_version):
        """Transform item between schema versions."""
        if from_version == 1 and to_version == 2:
            return {
                'pk': f"USER#{item['id']}",
                'sk': f"PROFILE#{item['id']}",
                'id': item['id'],
                'data': item.get('data', {}),
                'created_at': item.get('created_at', int(time.time()))
            }
        return item
```

## 🚀 Performance & Optimization

### 12. How would you optimize a LocalStack setup for CI/CD pipelines?
```yaml
# docker-compose.ci.yml
version: '3.8'
services:
  localstack:
    image: localstack/localstack:latest
    container_name: localstack-ci
    mem_limit: 1g  # Strict memory limit for CI
    environment:
      - SERVICES=s3,dynamodb,lambda  # Only needed services
      - DEBUG=0
      - DATA_DIR=/tmp/localstack_data
      - LAMBDA_EXECUTOR=docker-reuse
      - DOCKER_HOST=unix:///var/run/docker.sock
      - HOSTNAME_EXTERNAL=localstack
    ports:
      - "4566:4566"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./ci-data:/tmp/localstack_data"
    networks:
      - test-network

# CI/CD pipeline script
#!/bin/bash
# Start LocalStack
docker-compose -f docker-compose.ci.yml up -d

# Wait for health check
echo "Waiting for LocalStack to be ready..."
timeout 60 bash -c 'until curl -s http://localhost:4566/health | grep -q "running"; do sleep 2; done'

# Run tests
pytest tests/ --cov=app --cov-report=xml

# Stop LocalStack
docker-compose -f docker-compose.ci.yml down -v
```

### 13. What monitoring would you implement for LocalStack in production-like testing?
```python
class LocalStackMonitor:
    """Monitor LocalStack performance and health."""
    
    def __init__(self, endpoint_url='http://localhost:4566'):
        self.endpoint_url = endpoint_url
        self.metrics = {
            'start_time': time.time(),
            'requests': 0,
            'errors': 0,
            'latency': []
        }
    
    def check_health(self):
        """Check LocalStack health endpoint."""
        try:
            response = requests.get(f"{self.endpoint_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'healthy': True,
                    'services': data.get('services', {}),
                    'timestamp': time.time()
                }
            return {'healthy': False, 'error': f"Status {response.status_code}"}
        except Exception as e:
            return {'healthy': False, 'error': str(e)}
    
    def monitor_operation(self, operation_func, *args, **kwargs):
        """Monitor an AWS operation."""
        start_time = time.time()
        self.metrics['requests'] += 1
        
        try:
            result = operation_func(*args, **kwargs)
            latency = time.time() - start_time
            self.metrics['latency'].append(latency)
            return result
        except Exception as e:
            self.metrics['errors'] += 1
            raise
    
    def get_performance_report(self):
        """Generate performance report."""
        if not self.metrics['latency']:
            avg_latency = 0
        else:
            avg_latency = sum(self.metrics['latency']) / len(self.metrics['latency'])
        
        return {
            'uptime_seconds': time.time() - self.metrics['start_time'],
            'total_requests': self.metrics['requests'],
            'error_rate': self.metrics['errors'] / max(self.metrics['requests'], 1),
            'average_latency': avg_latency,
            'p95_latency': sorted(self.metrics['latency'])[int(len(self.metrics['latency']) * 0.95)] if self.metrics['latency'] else 0
        }
```

### 14. How do you handle data persistence across LocalStack restarts in testing?
```python
def configure_localstack_persistence():
    """Configure LocalStack for data persistence."""
    
    # docker-compose.yml configuration
    docker_compose_config = """
version: '3.8'
services:
  localstack:
    image: localstack/localstack
    environment:
      - SERVICES=s3,dynamodb
      - PERSISTENCE=1
      - DATA_DIR=/tmp/localstack_data
    ports:
      - "4566:4566"
    volumes:
      - "./localstack_data:/tmp/localstack_data"
"""
    
    # Write configuration
    with open('docker-compose.persistent.yml', 'w') as f:
        f.write(docker_compose_config)
    
    # Test persistence
    import subprocess
    
    # Start with persistence
    subprocess.run(['docker-compose', '-f', 'docker-compose.persistent.yml', 'up', '-d'])
    time.sleep(10)
    
    # Create test resource
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
    s3.create_bucket(Bucket='test-persistence')
    s3.put_object(Bucket='test-persistence', Key='test.txt', Body=b'Hello World')
    
    # Restart LocalStack
    subprocess.run(['docker-compose', '-f', 'docker-compose.persistent.yml', 'restart', 'localstack'])
    time.sleep(10)
    
    # Check if resource still exists
    try:
        response = s3.get_object(Bucket='test-persistence', Key='test.txt')
        data = response['Body'].read()
        return data == b'Hello World'
    except:
        return False
```

## 🧪 Testing Strategies

### 15. How would you write integration tests for AWS services using LocalStack?
```python
import pytest
import boto3
import tempfile
import os

@pytest.fixture(scope="session")
def localstack_session():
    """Session fixture for LocalStack."""
    # Start LocalStack (simplified - in reality use docker-compose)
    yield {
        'endpoint_url': 'http://localhost:4566',
        'region': 'us-east-1'
    }
    # Cleanup would happen here

@pytest.fixture
def s3_client(localstack_session):
    """S3 client fixture."""
    return boto3.client(
        's3',
        endpoint_url=localstack_session['endpoint_url'],
        region_name=localstack_session['region']
    )

@pytest.fixture
def s3_bucket(s3_client):
    """Create temporary S3 bucket for tests."""
    bucket_name = 'test-bucket-' + str(int(time.time()))
    s3_client.create_bucket(Bucket=bucket_name)
    yield bucket_name
    # Cleanup
    try:
        # Delete all objects
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
    except:
        pass

def test_s3_upload_download(s3_client, s3_bucket):
    """Test S3 upload and download functionality."""
    test_data = b"Hello, LocalStack!"
    
    # Upload
    s3_client.put_object(
        Bucket=s3_bucket,
        Key='test.txt',
        Body=test_data
    )
    
    # Download
    response = s3_client.get_object(Bucket=s3_bucket, Key='test.txt')
    downloaded_data = response['Body'].read()
    
    assert downloaded_data == test_data

def test_s3_list_objects(s3_client, s3_bucket):
    """Test S3 list objects functionality."""
    # Upload multiple files
    for i in range(5):
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=f'file_{i}.txt',
            Body=f'Content {i}'.encode()
        )
    
    # List objects
    response = s3_client.list_objects_v2(Bucket=s3_bucket)
    keys = [obj['Key'] for obj in response.get('Contents', [])]
    
    assert len(keys) == 5
    assert all(f'file_{i}.txt' in keys for i in range(5))

class TestDynamoDBIntegration:
    """DynamoDB integration tests."""
    
    @pytest.fixture
    def dynamodb_table(self, localstack_session):
        """Create temporary DynamoDB table."""
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=localstack_session['endpoint_url'],
            region_name=localstack_session['region']
        )
        
        table_name = 'test-table-' + str(int(time.time()))
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Wait for table to be active
        table.wait_until_exists()
        
        yield table
        
        # Cleanup
        table.delete()
    
    def test_dynamodb_put_get(self, dynamodb_table):
        """Test DynamoDB put and get operations."""
        # Put item
        dynamodb_table.put_item(Item={
            'id': 'test-1',
            'name': 'Test Item',
            'value': 42
        })
        
        # Get item
        response = dynamodb_table.get_item(Key={'id': 'test-1'})
        item = response.get('Item', {})
        
        assert item['id'] == 'test-1'
        assert item['name'] == 'Test Item'
        assert item['value'] == 42
    
    def test_dynamodb_query(self, dynamodb_table):
        """Test DynamoDB query operations."""
        # Put multiple items
        for i in range(10):
            dynamodb_table.put_item(Item={
                'id': f'item-{i}',
                'category': 'test',
                'value': i * 10
            })
        
        # Query items (note: need GSI for query on non-key attributes)
        # This is a simplified example
        response = dynamodb_table.scan()
        items = response.get('Items', [])
        
        assert len(items) == 10
```

## 🔍 Troubleshooting

### 16. What are common issues when using LocalStack and how do you resolve them?

**Issue 1: Connection refused on port 4566**
```bash
# Check if LocalStack is running
docker ps | grep localstack

# If not running, start it
docker-compose up -d

# Check logs for errors
docker-compose logs localstack

# Verify port is available
netstat -tuln | grep 4566
```

**Issue 2: S3 bucket operations failing**
```python
# Common causes and solutions:
# 1. Bucket naming: Use lowercase, no dots
# 2. Region mismatch: Always use us-east-1 with LocalStack
# 3. Endpoint URL: Must be http://localhost:4566
# 4. Credentials: Use dummy credentials (test/test)

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)
```

**Issue 3: DynamoDB table not found**
```python
# Ensure table is created before use
table = dynamodb.create_table(...)
table.wait_until_exists()  # Wait for table to be active

# Check table status
print(table.table_status)  # Should be 'ACTIVE'
```

**Issue 4: Memory exhaustion on 8GB RAM**
```yaml
# In docker-compose.yml:
localstack:
  mem_limit: 2g
  environment:
    - SERVICES=s3,dynamodb  # Only needed services
    - DEBUG=0  # Disable debug logging
```

### 17. How do you debug Lambda functions running in LocalStack?
```python
def debug_lambda_in_localstack(function_name, payload):
    """Debug Lambda function execution in LocalStack."""
    
    lambda_client = boto3.client(
        'lambda',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1'
    )
    
    # Invoke Lambda
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    # Parse response
    result = json.loads(response['Payload'].read().decode('utf-8'))
    
    # Check for errors
    if 'FunctionError' in response:
        print(f"Lambda error: {result}")
        
        # Check LocalStack logs
        import subprocess
        logs = subprocess.run(
            ['docker', 'logs', 'localstack_main', '--tail', '100'],
            capture_output=True,
            text=True
        )
        print("LocalStack logs:", logs.stdout)
    
    return result
```

## 📈 Real-World Scenarios

### 18. Describe how you would use LocalStack to test a production data pipeline.
```python
class ProductionPipelineTester:
    """Test production data pipeline using LocalStack."""
    
    def __init__(self):
        self.s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
        self.sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
    
    def test_full_pipeline(self):
        """Test complete data pipeline."""
        
        # 1. Setup test resources
        bucket = self.create_test_bucket()
        table = self.create_test_table()
        queue = self.create_test_queue()
        
        # 2. Generate test data
        test_data = self.generate_production_like_data(1000)
        
        # 3. Upload to S3 (simulate data ingestion)
        self.upload_to_s3(bucket, test_data)
        
        # 4. Trigger processing (simulate Lambda trigger)
        self.trigger_processing(bucket, queue)
        
        # 5. Process messages (simulate worker)
        processed_count = self.process_queue_messages(queue, table)
        
        # 6. Verify results
        success = self.verify_results(table, len(test_data))
        
        # 7. Cleanup
        self.cleanup_resources(bucket, table, queue)
        
        return {
            'success': success,
            'processed': processed_count,
            'verified': len(test_data)
        }
    
    def create_test_bucket(self):
        """Create test S3 bucket."""
        bucket_name = f"test-pipeline-{int(time.time())}"
        self.s3.create_bucket(Bucket=bucket_name)
        return bucket_name
    
    def create_test_table(self):
        """Create test DynamoDB table."""
        table_name = f"test-results-{int(time.time())}"
        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        return table
    
    def create_test_queue(self):
        """Create test SQS queue."""
        queue_name = f"test-queue-{int(time.time())}"
        response = self.sqs.create_queue(QueueName=queue_name)
        return response['QueueUrl']
    
    def generate_production_like_data(self, count):
        """Generate data resembling production patterns."""
        import uuid
        import random
        
        data = []
        for i in range(count):
            data.append({
                'id': str(uuid.uuid4()),
                'timestamp': int(time.time()) - random.randint(0, 86400),
                'value': random.random() * 100,
                'category': random.choice(['A', 'B', 'C', 'D']),
                'metadata': {
                    'source': 'test',
                    'batch': f"batch-{i//100}",
                    'priority': random.choice(['high', 'medium', 'low'])
                }
            })
        return data
    
    def upload_to_s3(self, bucket, data, chunk_size=100):
        """Upload data to S3 in chunks."""
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            key = f"data/chunk_{i//chunk_size}.json"
            self.s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(chunk).encode()
            )
    
    def trigger_processing(self, bucket, queue_url):
        """Simulate S3 event triggering processing."""
        # In real scenario, S3 event would trigger Lambda
        # Here we manually send message to queue
        self.sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'bucket': bucket,
                'event': 'ObjectCreated:Put',
                'time': int(time.time())
            })
        )
    
    def process_queue_messages(self, queue_url, table, max_messages=10):
        """Process messages from queue."""
        processed = 0
        
        while True:
            # Receive messages
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=5
            )
            
            messages = response.get('Messages', [])
            if not messages:
                break
            
            # Process each message
            for message in messages:
                # Simulate processing
                with table.batch_writer() as batch:
                    batch.put_item(Item={
                        'id': str(uuid.uuid4()),
                        'message_id': message['MessageId'],
                        'processed_at': int(time.time()),
                        'status': 'success'
                    })
                
                # Delete message from queue
                self.sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                
                processed += 1
        
        return processed
    
    def verify_results(self, table, expected_count):
        """Verify processing results."""
        response = table.scan()
        actual_count = len(response.get('Items', []))
        
        # Check counts match
        if actual_count != expected_count:
            print(f"Count mismatch: expected {expected_count}, got {actual_count}")
            return False
        
        # Check data quality
        for item in response.get('Items', []):
            if 'status' not in item or item['status'] != 'success':
                print(f"Invalid item: {item}")
                return False
        
        return True
    
    def cleanup_resources(self, bucket, table, queue_url):
        """Clean up test resources."""
        # Delete S3 bucket contents and bucket
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket):
                if 'Contents' in page:
                    objects = [{'Key': obj['Key']} for obj in page['Contents']]
                    self.s3.delete_objects(
                        Bucket=bucket,
                        Delete={'Objects': objects}
                    )
            self.s3.delete_bucket(Bucket=bucket)
        except:
            pass
        
        # Delete DynamoDB table
        try:
            table.delete()
        except:
            pass
        
        # Delete SQS queue
        try:
            self.sqs.delete_queue(QueueUrl=queue_url)
        except:
            pass
```

### 19. How would you simulate AWS service failures using LocalStack?
```python
def simulate_aws_failures():
    """Simulate various AWS service failures for resilience testing."""
    
    failure_scenarios = [
        {
            'name': 'S3 Service Unavailable',
            'simulate': lambda: stop_localstack_service('s3'),
            'recover': lambda: start_localstack_service('s3')
        },
        {
            'name': 'DynamoDB Throttling',
            'simulate': lambda: configure_dynamodb_throttling(),
            'recover': lambda: reset_dynamodb_throttling()
        },
        {
            'name': 'Network Latency',
            'simulate': lambda: add_network_latency(1000),  # 1 second
            'recover': lambda: remove_network_latency()
        }
    ]
    
    for scenario in failure_scenarios:
        print(f"\nTesting: {scenario['name']}")
        
        # Simulate failure
        scenario['simulate']()
        
        # Run test operations
        success = run_resilience_tests()
        
        # Recover
        scenario['recover']()
        
        print(f"Result: {'PASS' if success else 'FAIL'}")

def stop_localstack_service(service):
    """Stop a specific LocalStack service."""
    import docker
    client = docker.from_env()
    
    # Find LocalStack container
    containers = client.containers.list(filters={'name': 'localstack'})
    if containers:
        # Execute command inside container to stop service
        container = containers[0]
        container.exec_run(f"supervisorctl stop {service}")

def configure_dynamodb_throttling():
    """Configure DynamoDB to simulate throttling."""
    # LocalStack may not support this directly
    # Alternative: Use mocking in tests
    print("Simulating DynamoDB throttling...")
    
    # Mock boto3 client to throw throttling exceptions
    import unittest.mock as mock
    
    original_client = boto3.client
    def throttling_client(*args, **kwargs):
        client = original_client(*args, **kwargs)
        
        # Patch specific methods to throw throttling errors
        original_put_item = client.put_item
        def throttling_put_item(**kwargs):
            from botocore.exceptions import ClientError
            from unittest.mock import Mock
            
            # Randomly throttle (30% chance)
            import random
            if