#!/bin/bash
set -e

echo "Waiting for LocalStack to be ready..."
sleep 5

echo "Creating S3 bucket: wealth-management-raw-data"
awslocal s3 mb s3://wealth-management-raw-data

echo "Creating DynamoDB table: ProcessedTransactions"
awslocal dynamodb create-table \
    --table-name ProcessedTransactions \
    --attribute-definitions \
        AttributeName=transaction_id,AttributeType=S \
        AttributeName=user_id,AttributeType=S \
    --key-schema \
        AttributeName=transaction_id,KeyType=HASH \
        AttributeName=user_id,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1

echo "AWS LocalStack Setup Complete!"
awslocal s3 ls
awslocal dynamodb list-tables
