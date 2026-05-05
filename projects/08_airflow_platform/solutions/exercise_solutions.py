#!/usr/bin/env python3
"""
Solutions for Apache Airflow Practice Exercises
"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.http import HttpSensor
from datetime import datetime, timedelta
import random
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# --- Exercise 1: Basic DAG ---
with DAG(
    'exercise_1_basic_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag1:

    start = BashOperator(
        task_id='print_start',
        bash_command='echo "Starting pipeline"',
    )

    def generate_numbers(**kwargs):
        nums = [random.randint(1, 100) for _ in range(10)]
        kwargs['ti'].xcom_push(key='random_numbers', value=nums)
        return nums

    def save_to_file(**kwargs):
        ti = kwargs['ti']
        nums = ti.xcom_pull(key='random_numbers', task_ids='generate_numbers')
        path = '/tmp/random_numbers.txt'
        with open(path, 'w') as f:
            f.write(','.join(map(str, nums)))
        print(f"Saved to {path}")

    generate = PythonOperator(
        task_id='generate_numbers',
        python_callable=generate_numbers,
    )

    save = PythonOperator(
        task_id='save_to_file',
        python_callable=save_to_file,
    )

    end = BashOperator(
        task_id='print_end',
        bash_command='echo "Pipeline completed"',
    )

    start >> generate >> save >> end

# --- Exercise 2: Dependencies and Branching ---
with DAG(
    'exercise_2_dependencies',
    default_args=default_args,
    schedule_interval='@once',
) as dag2:

    def extract(source):
        print(f"Extracting data from {source}")
        return f"data_{source}"

    extract_a = PythonOperator(task_id='extract_a', python_callable=extract, op_args=['A'])
    extract_b = PythonOperator(task_id='extract_b', python_callable=extract, op_args=['B'])
    extract_c = PythonOperator(task_id='extract_c', python_callable=extract, op_args=['C'])

    def process_ab(**kwargs):
        ti = kwargs['ti']
        a = ti.xcom_pull(task_ids='extract_a')
        b = ti.xcom_pull(task_ids='extract_b')
        print(f"Processing {a} and {b}")

    def process_c(**kwargs):
        c = kwargs['ti'].xcom_pull(task_ids='extract_c')
        print(f"Processing {c}")

    proc_ab = PythonOperator(task_id='process_ab', python_callable=process_ab)
    proc_c = PythonOperator(task_id='process_c', python_callable=process_c)

    def aggregate():
        print("Aggregating results...")

    agg = PythonOperator(task_id='aggregate', python_callable=aggregate)

    cleanup = BashOperator(
        task_id='cleanup',
        bash_command='echo "Cleaning up..."',
        trigger_rule='all_done'
    )

    [extract_a, extract_b] >> proc_ab
    extract_c >> proc_c
    [proc_ab, proc_c] >> agg >> cleanup
