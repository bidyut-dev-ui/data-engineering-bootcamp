import boto3
import os

# Configure boto3 to use our LocalStack endpoint instead of real AWS
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

BUCKET_NAME = "wealth-management-raw-data"
FILE_NAME = "raw_transactions.csv"

def upload_to_s3():
    if not os.path.exists(FILE_NAME):
        print(f"Error: {FILE_NAME} not found. Run 02_generate_data.py first.")
        return

    print(f"Uploading {FILE_NAME} to S3 bucket '{BUCKET_NAME}'...")
    
    try:
        s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print("Upload successful!")
        
        # Verify
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        print("\nObjects in Bucket:")
        for obj in response.get('Contents', []):
            print(f" - {obj['Key']} ({obj['Size']} bytes)")

    except Exception as e:
        print(f"Failed to upload: {e}")

if __name__ == "__main__":
    upload_to_s3()
