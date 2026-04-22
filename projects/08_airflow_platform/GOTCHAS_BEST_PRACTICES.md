# Apache Airflow Platform: Gotchas & Best Practices

## Overview
This document covers common pitfalls, optimization techniques, and best practices for Apache Airflow workflow orchestration, with special focus on 8GB RAM constraints and production data pipelines.

## 🚨 Critical Gotchas

### 1. **DAG Definition and Scheduling**
**Gotcha**: DAGs are parsed continuously by the scheduler, causing high CPU usage with complex DAGs.
**Solution**:
- Keep DAG files lightweight - move heavy logic to operators
- Use `.airflowignore` to exclude test/dev DAGs from parsing
- Implement top-level code guards to prevent execution during parsing
- Use `default_args` for common parameters

```python
# BAD: Heavy computation in DAG file
def complex_computation():
    # This runs every time scheduler parses the DAG
    return heavy_processing()

with DAG(...) as dag:
    task = PythonOperator(
        task_id='task1',
        python_callable=complex_computation  # Called during parsing!
    )

# GOOD: Move heavy logic to operator or separate module
def task_function(**context):
    # Only runs when task executes
    return heavy_processing()

with DAG(...) as dag:
    task = PythonOperator(
        task_id='task1',
        python_callable=task_function
    )
```

### 2. **XCom Size Limitations**
**Gotcha**: XCom has default size limits (48KB for metadata database) causing serialization errors.
**Solution**:
- Use XCom only for small metadata (task IDs, status, counts)
- For large data, use external storage (S3, GCS, database)
- Implement custom XCom backend for larger payloads
- Use Airflow 2.0+ with XCom backend support

```python
# BAD: Storing large DataFrame in XCom
def process_data(**context):
    df = pd.read_csv('large_file.csv')  # 100MB file
    context['task_instance'].xcom_push(key='large_data', value=df)  # Will fail!

# GOOD: Store reference in XCom, data externally
def process_data(**context):
    df = pd.read_csv('large_file.csv')
    # Save to external storage
    output_path = f's3://bucket/data/{context["ds"]}_processed.parquet'
    df.to_parquet(output_path)
    # Store only reference in XCom
    context['task_instance'].xcom_push(key='output_path', value=output_path)
```

### 3. **Dynamic DAG Generation**
**Gotcha**: Dynamically generating DAGs in loops can cause memory leaks and performance issues.
**Solution**:
- Generate DAGs at module level, not in functions
- Use `globals()` carefully
- Implement DAG factory pattern
- Test DAG generation in isolation

```python
# BAD: Generating DAGs in function called repeatedly
def create_dag(dag_id):
    with DAG(dag_id, ...) as dag:
        # ... tasks
    return dag

for i in range(100):
    dag = create_dag(f'dynamic_dag_{i}')
    globals()[dag.dag_id] = dag  # Memory leak risk

# GOOD: DAG factory at module level
def create_dag_factory(dag_id, schedule):
    """Factory function that returns a DAG"""
    with DAG(dag_id=dag_id, schedule_interval=schedule, ...) as dag:
        # ... tasks
    return dag

# Create DAGs once at module level
for i, config in enumerate(DAG_CONFIGS):
    dag_id = f'dynamic_dag_{i}'
    dag = create_dag_factory(dag_id, config['schedule'])
    globals()[dag_id] = dag
```

### 4. **Database Connection Pooling**
**Gotcha**: Airflow creates many database connections, exhausting pool on 8GB RAM.
**Solution**:
- Configure `sql_alchemy_pool_size` and `sql_alchemy_max_overflow`
- Use `executor = LocalExecutor` for single machine (not Celery)
- Monitor connection count with `SELECT count(*) FROM pg_stat_activity`
- Set `parallelism` and `dag_concurrency` appropriately

```python
# airflow.cfg optimization for 8GB RAM
[core]
executor = LocalExecutor
parallelism = 8  # Reduced from default 32
dag_concurrency = 6  # Reduced from default 16
max_active_runs_per_dag = 3

[scheduler]
max_threads = 2  # Reduced from default 2 * cpu cores

[webserver]
workers = 2  # Reduced from default 4
worker_timeout = 120

[database]
sql_alchemy_pool_size = 5  # Reduced from default 5
sql_alchemy_max_overflow = 10  # Reduced from default 10
```

### 5. **Task Instance Cleanup**
**Gotcha**: Task instances accumulate, filling database and slowing scheduler.
**Solution**:
- Configure `max_active_runs_per_dag`
- Implement DAG catchup=False for backfills
- Use `airflow db clean` to purge old data
- Set up automated cleanup with retention policies

```bash
# Cleanup command examples
# Keep last 7 days, remove older
airflow db clean --clean-before-timestamp "2024-01-01" \
  --verbose \
  --yes

# Cleanup configuration in airflow.cfg
[core]
# Keep task instances for 30 days
dagbag_import_timeout = 30
dag_file_processor_timeout = 50

[scheduler]
# Cleanup old task instances
min_file_process_interval = 30
dag_dir_list_interval = 300
```

## 🏆 Best Practices

### 1. **DAG Structure and Organization**
```python
"""
Best practice DAG structure:
1. Import statements at top
2. Default arguments
3. DAG definition
4. Task definitions
5. Task dependencies
6. Optional: Helper functions in separate module
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments reused across DAGs
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
    'catchup': False,  # Critical for production
    'max_active_runs': 1,  # Prevent overlapping runs
}

# DAG definition
with DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for customer data',
    schedule_interval='0 2 * * *',  # 2 AM daily
    tags=['etl', 'production', 'daily'],
    concurrency=2,
) as dag:
    
    # Task definitions
    extract = BashOperator(
        task_id='extract_data',
        bash_command='python /scripts/extract.py {{ ds }}',
        retries=2,
    )
    
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_function,
        op_kwargs={'date': '{{ ds }}'},
    )
    
    load = PythonOperator(
        task_id='load_data',
        python_callable=load_function,
        provide_context=True,
    )
    
    # Task dependencies
    extract >> transform >> load
```

### 2. **Error Handling and Retry Strategy**
```python
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class RobustPythonOperator(BaseOperator):
    """Custom operator with enhanced error handling"""
    
    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.retry_exceptions = kwargs.pop('retry_exceptions', [])
        self.max_retry_delay = kwargs.pop('max_retry_delay', timedelta(hours=1))
        super().__init__(*args, **kwargs)
    
    def execute(self, context):
        try:
            return self.python_callable(**context)
        except tuple(self.retry_exceptions) as e:
            self.log.warning(f"Retryable error: {e}")
            raise
        except Exception as e:
            self.log.error(f"Non-retryable error: {e}")
            # Send alert
            self.send_alert(context, e)
            raise AirflowException(f"Task failed: {e}")
    
    def send_alert(self, context, error):
        """Send alert on critical failure"""
        # Implement alerting logic
        pass

# Usage in DAG
transform = RobustPythonOperator(
    task_id='transform_with_retry',
    python_callable=transform_function,
    retry_exceptions=[ConnectionError, TimeoutError],
    retries=5,
    retry_delay=timedelta(minutes=1),
    max_retry_delay=timedelta(minutes=30),
    email_on_retry=True,
    email_on_failure=True,
)
```

### 3. **Resource Management for 8GB RAM**
```python
# airflow.cfg optimizations for limited resources
[core]
# Reduce parallelism to match available RAM
parallelism = 8  # Default: 32
dag_concurrency = 6  # Default: 16
max_active_runs_per_dag = 2  # Default: 16

# Optimize scheduler
[scheduler]
max_threads = 2  # Default: 2 * cpu cores
scheduler_heartbeat_sec = 10  # Default: 5
processor_poll_interval = 10  # Default: 1

# Optimize executor
[celery]  # If using Celery
worker_concurrency = 2  # Default: 16
worker_autoscale = 2,4  # Default: 16,12

# Database optimization
[database]
sql_alchemy_pool_size = 5  # Default: 5
sql_alchemy_max_overflow = 10  # Default: 10
sql_alchemy_pool_recycle = 1800  # Recycle connections every 30min
```

### 4. **Monitoring and Alerting**
```python
from airflow.models import DagRun, TaskInstance
from airflow.utils.state import State
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def monitor_dag_health(**context):
    """Monitor DAG health and send alerts"""
    dag_id = context['dag'].dag_id
    dag_run = context['dag_run']
    
    # Check for long-running tasks
    long_running_tasks = []
    for ti in dag_run.get_task_instances():
        if ti.state == State.RUNNING:
            duration = datetime.utcnow() - ti.start_date
            if duration > timedelta(hours=1):
                long_running_tasks.append(ti.task_id)
    
    # Check for failed tasks
    failed_tasks = [ti.task_id for ti in dag_run.get_task_instances() 
                   if ti.state == State.FAILED]
    
    # Send alerts if needed
    if long_running_tasks or failed_tasks:
        send_slack_alert({
            'dag_id': dag_id,
            'run_id': dag_run.run_id,
            'long_running': long_running_tasks,
            'failed': failed_tasks,
            'execution_date': context['execution_date']
        })
    
    return {
        'long_running_tasks': long_running_tasks,
        'failed_tasks': failed_tasks,
        'total_tasks': len(dag_run.get_task_instances())
    }

# Add monitoring task to DAG
monitor = PythonOperator(
    task_id='monitor_dag_health',
    python_callable=monitor_dag_health,
    provide_context=True,
    dag=dag,
)
```

### 5. **Data Pipeline Best Practices**
```python
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable

class IdempotentETLOperator(BaseOperator):
    """Operator for idempotent ETL operations"""
    
    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.source_system = kwargs.pop('source_system')
        self.target_table = kwargs.pop('target_table')
        super().__init__(*args, **kwargs)
    
    def execute(self, context):
        execution_date = context['execution_date']
        
        # Check if already processed
        if self.already_processed(execution_date):
            self.log.info(f"Data for {execution_date} already processed. Skipping.")
            return
        
        # Extract with watermark
        watermark = self.get_last_processed_date()
        data = self.extract_data(watermark, execution_date)
        
        # Transform
        transformed = self.transform_data(data)
        
        # Load with transaction
        self.load_data(transformed, execution_date)
        
        # Update watermark
        self.update_watermark(execution_date)
        
        # Log metrics
        self.log_metrics(len(data))
    
    def already_processed(self, execution_date):
        """Check if this date was already processed"""
        # Implement idempotency check
        pass
    
    def get_last_processed_date(self):
        """Get watermark for incremental load"""
        # Implement watermark logic
        pass
```

### 6. **Testing and Development**
```python
# test_dag_integrity.py
import pytest
from airflow.models import DagBag

def test_dag_integrity():
    """Test that all DAGs can be loaded without errors"""
    dag_bag = DagBag(include_examples=False)
    
    assert len(dag_bag.import_errors) == 0, \
        f"DAG import errors: {dag_bag.import_errors}"
    
    assert len(dag_bag.dags) > 0, "No DAGs found"
    
    for dag_id, dag in dag_bag.dags.items():
        # Test each DAG has at least one task
        assert len(dag.tasks) > 0, f"DAG {dag_id} has no tasks"
        
        # Test DAG has valid schedule
        assert dag.schedule_interval is not None, \
            f"DAG {dag_id} has no schedule_interval"
        
        # Test no cyclic dependencies
        dag.test_cycle()

def test_task_dependencies():
    """Test task dependencies are properly set"""
    dag_bag = DagBag()
    
    for dag_id, dag in dag_bag.dags.items():
        for task in dag.tasks:
            # Test each task has downstream tasks or is an end task
            if not task.downstream_list:
                # End task should have no downstream
                pass
            else:
                # Verify downstream tasks exist
                for downstream in task.downstream_list:
                    assert downstream in dag.task_dict, \
                        f"Downstream task {downstream} not found in DAG {dag_id}"
```

### 7. **Production Deployment Checklist**
- [ ] **DAG Testing**: All DAGs pass `python -m pytest tests/`
- [ ] **Resource Limits**: Memory/CPU limits set in docker-compose/k8s
- [ ] **Database**: PostgreSQL configured with proper connection pooling
- [ ] **Monitoring**: Metrics collection (Prometheus/Grafana) configured
- [ ] **Alerting**: Email/Slack alerts for failures and SLA misses
- [ ] **Backups**: Regular database backups with retention policy
- [ ] **Security**: RBAC configured, secrets in environment variables
- [ ] **Logging**: Centralized logging (ELK stack or similar)
- [ ] **CI/CD**: DAG deployment pipeline with testing
- [ ] **Documentation**: DAG documentation and runbooks

### 8. **Performance Optimization Checklist**
- [ ] **DAG Parsing**: Minimal imports in DAG files
- [ ] **XCom Usage**: Only small metadata, not large data
- [ ] **Database**: Indexes on `dag_run`, `task_instance` tables
- [ ] **Scheduler**: Appropriate `min_file_process_interval`
- [ ] **Executor**: Proper concurrency settings for hardware
- [ ] **Networking**: Fast connection between workers and database
- [ ] **Storage**: Fast disk for `AIRFLOW_HOME` and logs
- [ ] **Memory**: Monitor and limit per-task memory usage

### 9. **Common Anti-Patterns to Avoid**
```python
# ANTI-PATTERN 1: Dynamic task generation in loops (causes DAG parsing slowness)
with DAG(...) as dag:
    for i in range(100):
        PythonOperator(task_id=f'task_{i}', ...)  # Creates 100 tasks at parse time

# ANTI-PATTERN 2: Large data in XCom
xcom_push('large_data', huge_dataframe)  # Will fail or slow database

# ANTI-PATTERN 3: No idempotency
def process_data(date):
    # Processes data without checking if already done
    # Will reprocess on retry causing duplicates

# ANTI-PATTERN 4: Tight coupling between tasks
def task1(**context):
    data = complex_processing()
    context['task_instance'].xcom_push(key='data', value=data)

def task2(**context):
    data = context['task_instance'].xcom_pull(task_ids='task1', key='data')
    # Task2 depends on Task1's internal implementation
```

### 10. **Troubleshooting Guide**

#### Issue: Scheduler High CPU Usage
**Symptoms**: Scheduler process using >80% CPU continuously
**Diagnosis**:
```bash
# Check scheduler logs
tail -f airflow-scheduler.err

# Check DAG parsing time
airflow dags list --verbose | grep "file size\|parsing time"

# Count DAG files
find $AIRFLOW_HOME/dags -name "*.py" | wc -l
```

**Solutions**:
- Reduce DAG file complexity
- Increase `min_file_process_interval`
- Use `.airflowignore` to exclude files
- Move heavy imports out of DAG files

#### Issue: Database Connection Exhaustion
**Symptoms**: "sorry, too many clients already" errors
**Diagnosis**:
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'airflow';

-- Check connection sources
SELECT client_addr, count(*) 
FROM pg_stat_activity 
WHERE datname = 'airflow'
GROUP BY client_addr;
```

**Solutions**:
- Reduce `parallelism` and `dag_concurrency`
- Configure `sql_alchemy_pool_size` appropriately
- Use `LocalExecutor` instead of `CeleryExecutor` for small setups
- Implement connection pooling at application level

#### Issue: DAG Not Triggering
**Symptoms**: DAG shows in UI but doesn't run on schedule
**Diagnosis**:
```bash
# Check scheduler health
airflow scheduler --diagnose

# Check DAG next execution
airflow dags next-execution <dag_id>

# Check scheduler logs for errors
grep -i "error\|exception" airflow-scheduler.log
```

**Solutions**:
- Verify `start_date` is in past
- Check `schedule_interval` syntax
- Ensure scheduler is running (`airflow scheduler`)
- Check for import errors in DAG

## 📈 Performance Benchmarks (8GB RAM)

| Component | Recommended Setting | Rationale |
|-----------|-------------------|-----------|
| **Parallelism** | 8-12 | Matches CPU cores, prevents memory exhaustion |
| **DAG Concurrency** | 6-8 | Limits concurrent task executions |
| **Worker Concurrency** | 2-4 (Celery) | Prevents memory overload per worker |
| **Pool Size** | 3-5 | Matches database connection limits |
| **Scheduler Interval** | 10-30 seconds | Balances responsiveness and CPU usage |
| **XCom Size Limit** | 1MB | Prevents database bloat |
| **Task Timeout** | 30-60 minutes | Prevents zombie tasks |

## 🔧 Quick Reference Commands

```bash
# Development
airflow db init                    # Initialize database
airflow webserver --port 8080      # Start webserver
airflow scheduler                   # Start scheduler
airflow tasks test <dag> <task> <date>  # Test single task

# Administration
airflow dags list                  # List all DAGs
airflow dags pause <dag>           # Pause DAG
airflow dags unpause <dag>         # Unpause DAG
airflow dags trigger <dag>         # Trigger DAG run
airflow dags backfill <dag>        # Backfill DAG

# Monitoring
airflow dags report                # DAG status report
airflow tasks list <dag>           # List tasks in DAG
airflow tasks states <dag> <run_id> # Task states for run

# Database
airflow db reset                   # Reset database (CAUTION!)
airflow db upgrade                 # Upgrade database schema
airflow db cleanup                 # Clean old records

# Testing
pytest tests/ -v                  # Run tests
airflow dags test <dag> <date>    # Test DAG execution
```

## 🚀 Production Readiness Checklist

### Before Deployment
- [ ] All DAGs pass `airflow dags test`
- [ ] Database backups configured
- [ ] Monitoring and alerting set up
- [ ] Resource limits configured (memory, CPU)
- [ ] Security review completed (RBAC, secrets)
- [ ] Disaster recovery plan documented
- [ ] Runbook for common issues created

### After Deployment
- [ ] Scheduler stable (CPU < 50%, memory stable)
- [ ] DAGs triggering on schedule
- [ ] Task success rate > 99%
- [ ] Alerting working (test failure scenario)
- [ ] Database performance acceptable
- [ ] Log aggregation working

---

*Last Updated: 2026-04-22*  
*For issues or suggestions, refer to the project README or create an issue in the repository.*