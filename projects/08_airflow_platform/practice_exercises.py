#!/usr/bin/env python3
"""
Week 8: Apache Airflow Platform - Practice Exercises
=====================================================

This file contains practice exercises for Apache Airflow workflow orchestration
with a focus on data engineering pipelines and 8GB RAM optimization.

IMPORTANT: These are practice exercises only. Solutions are deferred to focus
on educational framework completion first (interview questions and gotchas).

Learning Objectives:
1. Airflow DAG (Directed Acyclic Graph) fundamentals
2. Operators and task dependencies
3. Scheduling and cron expressions
4. XComs for task communication
5. Error handling and retries
6. Sensors for external dependencies
7. Airflow UI and monitoring
8. Resource optimization for 8GB RAM

Exercises are progressive in difficulty:
- Beginner (1-3): Basic DAGs and operators
- Intermediate (4-6): Scheduling, error handling, XComs
- Advanced (7-10): Production pipelines, monitoring, optimization
"""

import os
import sys
from datetime import datetime, timedelta

# Exercise 1: Basic DAG with PythonOperator and BashOperator
"""
Create a simple DAG that:
1. Prints "Starting pipeline" with a BashOperator
2. Executes a Python function that generates a list of 10 random numbers
3. Saves the numbers to a file using another PythonOperator
4. Prints "Pipeline completed" with a BashOperator

Requirements:
- DAG should run daily starting from 2024-01-01
- Set retries=2 with 5-minute delay
- Use catchup=False
- Implement proper task dependencies (sequential execution)
- Log appropriate messages at each step

Expected Output:
- DAG visible in Airflow UI with 4 tasks
- Tasks execute in correct order
- File created with random numbers
- Logs show execution progress
"""

# Exercise 2: Task Dependencies and Branching
"""
Create a DAG that demonstrates different dependency patterns:
1. Create three independent data extraction tasks (extract_a, extract_b, extract_c)
2. Create two processing tasks that depend on specific extracts:
   - process_ab depends on extract_a AND extract_b
   - process_c depends on extract_c
3. Create a final aggregation task that depends on BOTH process_ab AND process_c
4. Add a cleanup task that runs regardless of success/failure (trigger_rule=ALL_DONE)

Requirements:
- Use PythonOperator for all tasks
- Each extract task should simulate different data sources
- Processing tasks should combine/transform data
- Aggregation task should merge results
- Implement proper error handling in each task

Expected Output:
- DAG with parallel execution of extract tasks
- Correct dependency graph in Airflow UI
- Tasks execute according to dependencies
- Cleanup task always runs
"""

# Exercise 3: Scheduling with Cron Expressions
"""
Create three DAGs with different scheduling patterns:
1. DAG 1: Run every weekday at 9 AM (Monday-Friday)
2. DAG 2: Run on the 1st and 15th of every month at midnight
3. DAG 3: Run every 2 hours during business hours (8 AM - 6 PM) on weekdays

Requirements:
- Each DAG should have at least 2 tasks
- Implement timezone awareness (UTC)
- Add descriptions explaining the schedule
- Test schedule intervals using Airflow's next execution date
- Add SLA (Service Level Agreement) of 1 hour for each DAG

Expected Output:
- Three DAGs with correct scheduling
- Next execution dates match expected patterns
- SLA configuration visible in UI
- Timezone properly handled
"""

# Exercise 4: XComs for Task Communication
"""
Create a DAG that demonstrates XCom usage for passing data between tasks:
1. Task 1: Generate a dictionary of configuration parameters
2. Task 2: Process the configuration and add derived parameters
3. Task 3: Use the configuration to generate a data report
4. Task 4: Archive the configuration and results

Requirements:
- Use XCom to pass configuration between tasks
- Implement both push and pull operations
- Handle large data by using XCom backends (not default for large data)
- Add error handling for missing XCom values
- Log the data being passed at each step

Expected Output:
- Configuration passed successfully between tasks
- Tasks can access data from previous tasks
- Proper handling of XCom size limitations
- Logs show data flow between tasks
"""

# Exercise 5: Error Handling and Retries
"""
Create a DAG that demonstrates robust error handling:
1. Task 1: Simulate an external API call that may fail (30% failure rate)
2. Task 2: Process the API response
3. Task 3: Send notifications on success/failure

Requirements:
- Implement exponential backoff for retries (1min, 2min, 4min)
- Add retry callback to log retry attempts
- Implement on_failure_callback to send alert email (simulated)
- Use PythonOperator with custom error simulation
- Add task timeouts (5 minutes)

Expected Output:
- Tasks retry with exponential backoff on failure
- Failure notifications triggered
- Timeout handling working
- Retry logs show backoff pattern
"""

# Exercise 6: Sensors and External Dependencies
"""
Create a DAG that uses sensors to wait for external conditions:
1. FileSensor: Wait for a file to appear in /tmp/data/input/
2. HttpSensor: Wait for an API endpoint to return 200 status
3. TimeDeltaSensor: Wait for 30 seconds (simulating external process)
4. CustomSensor: Create a sensor that checks database table for new records

Requirements:
- Implement proper timeout and poke_interval for sensors
- Add mode='reschedule' to free up worker slots
- Handle sensor failures gracefully
- Continue pipeline only when all sensors are satisfied
- Log sensor status changes

Expected Output:
- DAG waits for all conditions before proceeding
- Sensors properly reschedule to free resources
- Timeout handling for sensors that never succeed
- Logs show sensor polling activity
"""

# Exercise 7: ETL Pipeline with Data Quality Checks
"""
Create a production-ready ETL pipeline DAG:
1. Extract: Read data from CSV file
2. Transform: Clean, validate, and transform data
3. Load: Insert data into PostgreSQL database
4. Data Quality: Run data quality checks (row count, null values, constraints)
5. Notification: Send summary report

Requirements:
- Use DockerOperator to run extraction in isolated container
- Implement data validation with pandas
- Add data quality checks with custom operators
- Handle incremental loads (only new/updated data)
- Implement idempotency (rerunning doesn't create duplicates)
- Add monitoring metrics (execution time, row counts)

Expected Output:
- Complete ETL pipeline with data quality gates
- Idempotent operations
- Incremental loading working
- Quality check failures stop pipeline
- Metrics logged for monitoring
"""

# Exercise 8: Dynamic DAG Generation
"""
Create a system that generates DAGs dynamically based on configuration:
1. Read YAML configuration file defining multiple data sources
2. For each data source, generate a DAG with standard ETL pattern
3. All DAGs should share common utilities and error handling
4. Add global monitoring DAG that tracks all generated DAGs

Requirements:
- Use Airflow's DagBag and context managers
- Implement template DAG class
- Handle configuration changes without restarting Airflow
- Add DAG-level metrics and alerts
- Test with at least 3 different data source configurations

Expected Output:
- Multiple DAGs generated from single codebase
- Configuration-driven pipeline generation
- Shared utilities across DAGs
- Monitoring DAG showing status of all generated DAGs
"""

# Exercise 9: Resource Optimization for 8GB RAM
"""
Optimize Airflow deployment for 8GB RAM constraints:
1. Configure Airflow components (webserver, scheduler, worker) with memory limits
2. Implement DAG optimization techniques:
   - Use sensors with mode='reschedule'
   - Implement task pooling for resource-intensive tasks
   - Add task concurrency limits
   - Use lightweight operators where possible
3. Monitor and tune database connections
4. Implement DAG file parsing optimization

Requirements:
- Create docker-compose.yml with resource limits
- Configure Airflow executor (LocalExecutor vs CeleryExecutor)
- Implement task pools for limiting concurrent heavy tasks
- Add memory profiling for DAG execution
- Optimize PostgreSQL configuration for limited memory

Expected Output:
- Airflow deployment running within 8GB RAM
- Resource limits in docker-compose
- Optimized DAG execution
- Monitoring showing memory usage
- Task pools limiting concurrent resource usage
"""

# Exercise 10: Production Monitoring and Alerting
"""
Implement comprehensive monitoring for Airflow in production:
1. Create metrics collection for:
   - DAG execution times and success rates
   - Task duration percentiles
   - Queue wait times
   - Resource usage (CPU, memory)
2. Implement alerting for:
   - DAG failures
   - SLA misses
   - High resource usage
   - Long-running tasks
3. Create dashboard DAG that generates daily reports

Requirements:
- Use Airflow's statsd integration
- Implement custom metrics collection
- Create alert operators (email, Slack, PagerDuty simulation)
- Build monitoring DAG that runs hourly
- Add automated remediation for common issues

Expected Output:
- Comprehensive monitoring system
- Alerts triggered on defined conditions
- Daily monitoring reports
- Metrics available for visualization
- Automated remediation for simple issues
"""

# Main function to run exercises (placeholder - solutions deferred)
def main():
    """Main function to demonstrate exercise structure."""
    print("Apache Airflow Platform - Practice Exercises")
    print("=" * 60)
    print("This file contains 10 practice exercises for mastering Airflow")
    print("for data engineering workflow orchestration with 8GB RAM optimization.")
    print("\nExercises cover:")
    print("1. Basic DAGs with PythonOperator and BashOperator")
    print("2. Task dependencies and branching logic")
    print("3. Scheduling with cron expressions")
    print("4. XComs for task communication")
    print("5. Error handling and retries")
    print("6. Sensors and external dependencies")
    print("7. ETL pipeline with data quality checks")
    print("8. Dynamic DAG generation")
    print("9. Resource optimization for 8GB RAM")
    print("10. Production monitoring and alerting")
    print("\nNote: Solutions are deferred to focus on educational framework completion.")
    print("Complete these exercises to practice your Airflow skills for production data pipelines.")

if __name__ == "__main__":
    main()