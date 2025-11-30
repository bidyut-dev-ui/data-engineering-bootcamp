from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd
import json
import glob

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def extract_data(**context):
    """Extract data from simulated API"""
    execution_date = context['ds']  # YYYY-MM-DD
    
    # Read data file for this date
    file_pattern = f'/opt/airflow/data/raw/activity_{execution_date}.json'
    files = glob.glob(file_pattern)
    
    if not files:
        print(f"No data found for {execution_date}")
        return None
    
    with open(files[0], 'r') as f:
        data = json.load(f)
    
    print(f"Extracted {len(data)} records for {execution_date}")
    
    # Push to XCom
    context['ti'].xcom_push(key='raw_data', value=data)
    return len(data)

def transform_data(**context):
    """Transform and clean data"""
    ti = context['ti']
    raw_data = ti.xcom_pull(key='raw_data', task_ids='extract')
    
    if not raw_data:
        print("No data to transform")
        return None
    
    df = pd.DataFrame(raw_data)
    
    # Data quality checks
    df = df.dropna()
    df = df[df['page_views'] > 0]
    
    # Feature engineering
    df['engagement_score'] = (
        df['page_views'] * 0.3 +
        df['items_viewed'] * 0.4 +
        df['items_added_to_cart'] * 0.3
    )
    
    # Convert to dict for XCom
    transformed_data = df.to_dict('records')
    ti.xcom_push(key='transformed_data', value=transformed_data)
    
    print(f"Transformed {len(transformed_data)} records")
    return len(transformed_data)

def load_data(**context):
    """Load data to warehouse"""
    ti = context['ti']
    data = ti.xcom_pull(key='transformed_data', task_ids='transform')
    
    if not data:
        print("No data to load")
        return
    
    # In production, this would use PostgresHook
    # For now, we'll save to a staging file
    df = pd.DataFrame(data)
    output_file = f'/opt/airflow/data/processed/activity_{context["ds"]}.parquet'
    df.to_parquet(output_file)
    
    print(f"Loaded {len(data)} records to {output_file}")

with DAG(
    'capstone_etl',
    default_args=default_args,
    description='Daily ETL for customer activity',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['capstone', 'production'],
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    extract >> transform >> load
