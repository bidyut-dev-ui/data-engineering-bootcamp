from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import random

# Simulating an API call
def extract_weather_data(**kwargs):
    print("Extracting data...")
    # Simulate fetching data for 3 cities
    data = [
        {'city': 'London', 'temp': random.randint(5, 20), 'condition': 'Rainy'},
        {'city': 'New York', 'temp': random.randint(10, 25), 'condition': 'Sunny'},
        {'city': 'Tokyo', 'temp': random.randint(15, 30), 'condition': 'Cloudy'}
    ]
    # Push to XCom (Cross-Communication)
    kwargs['ti'].xcom_push(key='weather_data', value=data)

def transform_data(**kwargs):
    print("Transforming data...")
    # Pull from XCom
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(key='weather_data', task_ids='extract_weather')
    
    transformed_data = []
    for entry in raw_data:
        # Convert Celsius to Fahrenheit
        temp_f = (entry['temp'] * 9/5) + 32
        entry['temp_f'] = round(temp_f, 1)
        entry['processed_at'] = datetime.now().isoformat()
        transformed_data.append(entry)
        
    ti.xcom_push(key='processed_data', value=transformed_data)

def load_data(**kwargs):
    print("Loading data...")
    ti = kwargs['ti']
    data = ti.xcom_pull(key='processed_data', task_ids='transform_weather')
    
    # In a real scenario, we would insert into Postgres
    # Here we just print to logs
    for entry in data:
        print(f"INSERTING: {entry}")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    '02_weather_etl',
    default_args=default_args,
    description='Simulated Weather ETL pipeline',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id='extract_weather',
        python_callable=extract_weather_data,
    )

    transform = PythonOperator(
        task_id='transform_weather',
        python_callable=transform_data,
    )

    load = PythonOperator(
        task_id='load_weather',
        python_callable=load_data,
    )

    extract >> transform >> load
