from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import random

def risky_task():
    """A task that fails 50% of the time to demonstrate retries."""
    if random.random() < 0.5:
        raise ValueError("Simulated Failure!")
    print("Task succeeded!")

def process_data(**kwargs):
    """Demonstrate XCom push/pull."""
    ti = kwargs['ti']
    ti.xcom_push(key='my_key', value='Important Data')

def consume_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(key='my_key', task_ids='process_data')
    print(f"Received data: {data}")

default_args = {
    'owner': 'airflow',
    'retries': 3, # Retry up to 3 times
    'retry_delay': timedelta(seconds=30), # Wait 30s between retries
}

with DAG(
    'week_11_robust_dag',
    default_args=default_args,
    description='Demonstrating Retries and XComs',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    t1_risky = PythonOperator(
        task_id='risky_task',
        python_callable=risky_task,
    )

    t2_process = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )

    t3_consume = PythonOperator(
        task_id='consume_data',
        python_callable=consume_data,
    )

    # t1 must succeed before t2 starts
    t1_risky >> t2_process >> t3_consume
