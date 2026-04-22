#!/usr/bin/env python3
"""
AWS LocalStack Practice Exercises

This module contains 10 practice exercises covering AWS cloud-native concepts
using LocalStack for local development. Exercises focus on S3, DynamoDB, IAM,
and cloud data engineering patterns.

Memory Considerations:
- All exercises are designed to work within 8GB RAM constraints
- Use LocalStack to avoid actual AWS costs
- Implement proper resource cleanup to prevent memory leaks
- Monitor Docker container resource usage
"""

import boto3
import pandas as pd
import numpy as np
import json
import time
import os
import io
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# LocalStack configuration
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"


def get_localstack_client(service_name: str):
    """Create boto3 client configured for LocalStack."""
    return boto3.client(
        service_name=service_name,
        endpoint_url=LOCALSTACK_ENDPOINT,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def exercise_1_localstack_setup_and_verification() -> Dict[str, Any]:
    """
    Exercise 1: LocalStack Setup and Verification
    
    Implement LocalStack setup and verification:
    1. Check if LocalStack Docker container is running
    2. Verify S3 service is available
    3. Verify DynamoDB service is available
    4. Create test resources to confirm functionality
    5. Return service status and connection details
    
    Returns:
        Dictionary with service status, connection details, and verification results
    """
    pass


def exercise_2_s3_bucket_operations() -> Dict[str, Any]:
    """
    Exercise 2: S3 Bucket Operations
    
    Implement comprehensive S3 operations:
    1. Create S3 bucket with proper configuration
    2. Upload files with different storage classes
    3. Implement multipart upload for large files
    4. Set bucket policies and CORS configuration
    5. Implement versioning and lifecycle policies
    6. Perform bucket listing and object metadata retrieval
    
    Returns:
        Dictionary with bucket operations results, performance metrics, and configuration
    """
    pass


def exercise_3_dynamodb_table_operations() -> Dict[str, Any]:
    """
    Exercise 3: DynamoDB Table Operations
    
    Implement DynamoDB operations:
    1. Create table with proper key schema (partition and sort keys)
    2. Configure provisioned throughput and auto-scaling
    3. Implement CRUD operations (PutItem, GetItem, UpdateItem, DeleteItem)
    4. Use batch operations for efficiency
    5. Implement conditional writes and transactions
    6. Create secondary indexes (GSI, LSI)
    
    Returns:
        Dictionary with table configuration, operation results, and performance metrics
    """
    pass


def exercise_4_data_ingestion_pipeline() -> Dict[str, Any]:
    """
    Exercise 4: Data Ingestion Pipeline
    
    Implement a complete data ingestion pipeline:
    1. Generate synthetic financial transaction data
    2. Upload raw data to S3 in partitioned structure (date/hour)
    3. Implement S3 event notification simulation
    4. Process data from S3 using boto3 and pandas
    5. Transform and validate data
    6. Load processed data to DynamoDB
    
    Returns:
        Dictionary with pipeline metrics, data quality checks, and performance stats
    """
    pass


def exercise_5_iam_policies_and_security() -> Dict[str, Any]:
    """
    Exercise 5: IAM Policies and Security
    
    Implement IAM security best practices:
    1. Create IAM roles and policies for least privilege access
    2. Implement bucket policies for S3 access control
    3. Create DynamoDB fine-grained access control
    4. Implement encryption at rest and in transit
    5. Set up logging and monitoring (CloudTrail simulation)
    6. Implement cross-account access patterns
    
    Returns:
        Dictionary with IAM configurations, security policies, and access control results
    """
    pass


def exercise_6_query_patterns_and_optimization() -> Dict[str, Any]:
    """
    Exercise 6: Query Patterns and Optimization
    
    Implement efficient query patterns:
    1. Design DynamoDB table for specific access patterns
    2. Implement query operations with filter expressions
    3. Use scan operations efficiently with pagination
    4. Implement global and local secondary index queries
    5. Optimize for read/write capacity
    6. Implement caching strategies
    
    Returns:
        Dictionary with query patterns, performance benchmarks, and optimization results
    """
    pass


def exercise_7_error_handling_and_resilience() -> Dict[str, Any]:
    """
    Exercise 7: Error Handling and Resilience
    
    Implement robust error handling:
    1. Handle S3 upload/download failures with retry logic
    2. Implement DynamoDB conditional check failures
    3. Handle throttling and rate limiting
    4. Implement circuit breaker pattern for service failures
    5. Create idempotent operations
    6. Implement dead letter queues for failed processing
    
    Returns:
        Dictionary with error handling implementations, resilience patterns, and failure scenarios
    """
    pass


def exercise_8_monitoring_and_observability() -> Dict[str, Any]:
    """
    Exercise 8: Monitoring and Observability
    
    Implement monitoring solutions:
    1. Create custom metrics for S3 operations
    2. Implement DynamoDB table metrics collection
    3. Set up logging for all operations
    4. Create dashboards for system health
    5. Implement alerting for abnormal patterns
    6. Perform cost estimation and optimization
    
    Returns:
        Dictionary with monitoring configurations, metrics collection, and observability patterns
    """
    pass


def exercise_9_multi_service_integration() -> Dict[str, Any]:
    """
    Exercise 9: Multi-Service Integration
    
    Implement integration between multiple AWS services:
    1. Create S3 trigger for Lambda function (simulated)
    2. Implement SQS queue for message processing
    3. Use SNS for notifications
    4. Implement Step Functions workflow (simulated)
    5. Create API Gateway endpoints (simulated)
    6. Implement event-driven architecture patterns
    
    Returns:
        Dictionary with service integrations, workflow patterns, and event-driven architectures
    """
    pass


def exercise_10_production_readiness_and_cost_optimization() -> Dict[str, Any]:
    """
    Exercise 10: Production Readiness and Cost Optimization
    
    Implement production-ready patterns:
    1. Implement infrastructure as code (CloudFormation/Terraform simulation)
    2. Set up CI/CD pipeline for deployment
    3. Implement blue-green deployment strategies
    4. Optimize for cost (storage classes, provisioned capacity)
    5. Implement disaster recovery and backup strategies
    6. Create runbooks and operational procedures
    
    Returns:
        Dictionary with production patterns, cost optimization results, and operational procedures
    """
    pass


def main():
    """Run all AWS LocalStack practice exercises in sequence."""
    exercises = [
        ("LocalStack Setup and Verification", exercise_1_localstack_setup_and_verification),
        ("S3 Bucket Operations", exercise_2_s3_bucket_operations),
        ("DynamoDB Table Operations", exercise_3_dynamodb_table_operations),
        ("Data Ingestion Pipeline", exercise_4_data_ingestion_pipeline),
        ("IAM Policies and Security", exercise_5_iam_policies_and_security),
        ("Query Patterns and Optimization", exercise_6_query_patterns_and_optimization),
        ("Error Handling and Resilience", exercise_7_error_handling_and_resilience),
        ("Monitoring and Observability", exercise_8_monitoring_and_observability),
        ("Multi-Service Integration", exercise_9_multi_service_integration),
        ("Production Readiness and Cost Optimization", exercise_10_production_readiness_and_cost_optimization),
    ]
    
    results = {}
    
    print("=" * 80)
    print("AWS LocalStack Practice Exercises")
    print("=" * 80)
    print(f"Running {len(exercises)} exercises...\n")
    
    # Check if LocalStack is running
    try:
        s3_client = get_localstack_client('s3')
        s3_client.list_buckets()
        print("✓ LocalStack connection successful")
    except Exception as e:
        print(f"✗ LocalStack connection failed: {e}")
        print("Please ensure LocalStack Docker container is running:")
        print("  docker compose up -d")
        return {"error": "LocalStack not available", "details": str(e)}
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * len(name))
        
        try:
            # Execute the exercise function
            result = func()
            results[name] = result
            
            # Print summary if available
            if isinstance(result, dict):
                if 'success' in result:
                    print(f"  Status: {'✓ Success' if result['success'] else '✗ Failed'}")
                if 'metrics' in result:
                    print(f"  Metrics: {result['metrics']}")
                if 'message' in result:
                    print(f"  Message: {result['message']}")
            else:
                print(f"  Result: {type(result).__name__}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
            results[name] = {"error": str(e)}
    
    print("\n" + "=" * 80)
    print("Exercise Summary:")
    print("=" * 80)
    
    successful = sum(1 for r in results.values() if isinstance(r, dict) and r.get('success', False))
    print(f"\nCompleted: {successful}/{len(exercises)} exercises")
    
    # Cleanup resources
    print("\nCleaning up resources...")
    try:
        s3_client = get_localstack_client('s3')
        dynamodb_client = get_localstack_client('dynamodb')
        
        # List and delete buckets created during exercises
        buckets = s3_client.list_buckets()
        for bucket in buckets.get('Buckets', []):
            bucket_name = bucket['Name']
            if bucket_name.startswith('exercise-') or bucket_name.startswith('test-'):
                try:
                    # Delete all objects first
                    objects = s3_client.list_objects_v2(Bucket=bucket_name)
                    if 'Contents' in objects:
                        for obj in objects['Contents']:
                            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    # Delete bucket
                    s3_client.delete_bucket(Bucket=bucket_name)
                    print(f"  Deleted bucket: {bucket_name}")
                except Exception as e:
                    print(f"  Failed to delete bucket {bucket_name}: {e}")
        
        # List and delete tables
        tables = dynamodb_client.list_tables()
        for table_name in tables.get('TableNames', []):
            if table_name.startswith('exercise-') or table_name.startswith('test-'):
                try:
                    dynamodb_client.delete_table(TableName=table_name)
                    print(f"  Deleted table: {table_name}")
                except Exception as e:
                    print(f"  Failed to delete table {table_name}: {e}")
                    
    except Exception as e:
        print(f"  Cleanup error: {e}")
    
    # Return comprehensive results
    return {
        "total_exercises": len(exercises),
        "completed": successful,
        "results": results,
        "timestamp": datetime.now().isoformat(),
        "localstack_endpoint": LOCALSTACK_ENDPOINT
    }


if __name__ == "__main__":
    # Check if LocalStack is running
    print("Checking LocalStack availability...")
    
    try:
        import docker
        client = docker.from_env()
        containers = client.containers.list()
        localstack_running = any('localstack' in container.name for container in containers)
        
        if not localstack_running:
            print("LocalStack container not found. Starting with docker-compose...")
            import subprocess
            try:
                subprocess.run(["docker", "compose", "up", "-d"], check=True)
                print("LocalStack started. Waiting for services to be ready...")
                time.sleep(10)
            except Exception as e:
                print(f"Failed to start LocalStack: {e}")
                print("Please start LocalStack manually:")
                print("  cd data-engineering-bootcamp/projects/11_aws_localstack")
                print("  docker compose up -d")
    except ImportError:
        print("Docker Python SDK not available. Assuming LocalStack is running...")
    
    # Run all exercises
    main()