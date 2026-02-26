import boto3
import pandas as pd
from io import BytesIO

# Configure boto3 for LocalStack
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

BUCKET_NAME = "wealth-management-raw-data"
FILE_NAME = "raw_transactions.csv"
TABLE_NAME = "ProcessedTransactions"

def process_and_load():
    try:
        print(f"Fetching {FILE_NAME} from S3...")
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        csv_content = response['Body'].read()
        
        # Process using Pandas
        df = pd.read_csv(BytesIO(csv_content))
        print(f"Loaded {len(df)} records into Pandas DataFrame.")
        print(f"Sample data:\n{df.head(2)}\n")
        
        # For this exercise, let's filter only high-value BUY transactions
        high_value = df[(df['type'] == 'BUY') & (df['amount'] * df['price'] > 5000)]
        print(f"Filtered to {len(high_value)} high-value BUY transactions.")
        
        print(f"Loading into DynamoDB table: {TABLE_NAME}...")
        table = dynamodb.Table(TABLE_NAME)
        
        # Batch write to DynamoDB
        with table.batch_writer() as batch:
            for _, row in high_value.iterrows():
                # Convert floats to strings for DynamoDB (or use Decimal)
                item = {
                    'transaction_id': str(row['transaction_id']),
                    'user_id': str(row['user_id']),
                    'timestamp': str(row['timestamp']),
                    'symbol': str(row['symbol']),
                    'total_value': str(round(row['amount'] * row['price'], 2))
                }
                batch.put_item(Item=item)
                
        print("Data loaded to DynamoDB successfully!")

    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    process_and_load()
