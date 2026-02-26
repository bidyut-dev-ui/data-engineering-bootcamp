# Week 11.5: Cloud-Native & NoSQL Analytics (AWS Mocking)

**Tag:** `#role-datacompany-senior`, `#skill-aws`

## Overview
This module introduces core cloud-native concepts using **LocalStack**, which provides a fully functional local AWS cloud stack. This allows us to practice enterprise Cloud Engineering without exceeding our 8GB RAM local constraints or incurring cloud costs.

## Learning Objectives
- Understanding Object Storage (AWS S3) vs Block Storage
- Implementing IAM Policies for secure access
- Integrating NoSQL databases (Amazon DynamoDB)
- Mocking cloud infrastructure with LocalStack

## System Requirements
- LocalStack Docker container (`localstack/localstack`)
- `awscli-local` (awslocal wrapper)

## Project Instructions
We will be ingesting raw financial transaction feeds into our mocked S3 bucket, performing lightweight transformations via a Python worker, and inserting the finalized records into DynamoDB for low-latency querying.

### 1. Start LocalStack
First, ensure Docker is running, then spin up the LocalStack container:
```bash
docker compose up -d
```

### 2. Setup Dependencies & AWS Resources
Install the required python packages and run the setup script to create your S3 bucket and DynamoDB table.
```bash
pip install -r requirements.txt
chmod +x 01_setup_aws.sh
./01_setup_aws.sh
```

### 3. Generate and Ingest Data
Generate the sample financial transaction dataset, then push it to your local S3 bucket.
```bash
python 02_generate_data.py
python 03_ingest_s3.py
```

### 4. Process to DynamoDB
Read the CSV directly from S3 into a Pandas DataFrame, filter for high-value BUY transactions, and write them to DynamoDB.
```bash
python 04_process_dynamodb.py
```

### 5. Verify the Results
You can query your local DynamoDB directly from the terminal to ensure the data was processed:
```bash
awslocal dynamodb scan --table-name ProcessedTransactions
```

### 6. Teardown
```bash
docker compose down
```
