from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Task functions
def task_a():
    print("Task A: Starting parallel execution")

def task_b():
    print("Task B: Running in parallel with A")

def task_c():
    print("Task C: Running in parallel with A and B")

def task_d():
    print("Task D: Waiting for A, B, and C to complete")

# Default arguments demonstrating best practices
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': False,  # Set to True in production
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
}

# DAG with daily schedule
with DAG(
    'week_10_config',
    default_args=default_args,
    description='Week 10: Configuration and Scheduling Patterns',
    schedule_interval='@daily',  # Runs once per day at midnight
    catchup=False,  # Don't run for past dates
    tags=['week10', 'tutorial'],
) as dag:

    # Bash operator for simple commands
    start = BashOperator(
        task_id='start_pipeline',
        bash_command='echo "Pipeline started at $(date)"',
    )

    # Parallel tasks
    parallel_a = PythonOperator(
        task_id='parallel_task_a',
        python_callable=task_a,
    )

    parallel_b = PythonOperator(
        task_id='parallel_task_b',
        python_callable=task_b,
    )

    parallel_c = PythonOperator(
        task_id='parallel_task_c',
        python_callable=task_c,
    )

    # Task that waits for all parallel tasks
    join = PythonOperator(
        task_id='join_results',
        python_callable=task_d,
    )

    end = BashOperator(
        task_id='end_pipeline',
        bash_command='echo "Pipeline completed successfully!"',
    )

    # Define dependencies
    # Linear: start -> parallel tasks
    start >> [parallel_a, parallel_b, parallel_c]
    
    # All parallel tasks must complete before join
    [parallel_a, parallel_b, parallel_c] >> join
    
    # Linear: join -> end
    join >> end

# Alternative scheduling examples (commented out):
# schedule_interval='@hourly'           # Every hour
# schedule_interval='@weekly'           # Every week
# schedule_interval='0 0 * * 0'         # Every Sunday at midnight (cron)
# schedule_interval='*/15 * * * *'      # Every 15 minutes
# schedule_interval=timedelta(hours=6)  # Every 6 hours
