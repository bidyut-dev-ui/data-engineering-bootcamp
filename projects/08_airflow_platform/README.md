# Month 3: Orchestration with Apache Airflow (Weeks 9-12)

**Goal**: Master workflow orchestration by building, scheduling, and monitoring data pipelines with Apache Airflow on limited hardware.

## Scenario
You are a Data Engineer responsible for automating daily ETL jobs. Manual execution is error-prone and doesn't scale. Your task is to learn Airflow to orchestrate these workflows, handle failures gracefully, and provide visibility to stakeholders.

## Concepts Covered
1. **DAGs (Directed Acyclic Graphs)**: Defining workflows as code
2. **Operators**: PythonOperator, BashOperator, and task dependencies
3. **Scheduling**: Cron expressions and `schedule_interval`
4. **XComs**: Passing data between tasks
5. **Error Handling**: Retries, retry delays, and failure callbacks
6. **Sensors**: Waiting for external conditions
7. **Airflow UI**: Monitoring, logs, and manual triggers
8. **Resource Optimization**: Running Airflow on 8GB RAM

## Structure
- `docker-compose.yml`: Lightweight Airflow setup (Webserver + Scheduler + Postgres)
- `dags/`: Contains progressive DAGs for each week
    - `week_09_hello_world.py`: **Week 9** - Introduction to DAGs and Operators
    - `week_10_config.py`: **Week 10** - Configuration and scheduling patterns
    - `week_11_robust_dag.py`: **Week 11** - Error handling, retries, and XComs
    - `week_12_weather_etl.py`: **Week 12** - Mini-Project 3: Complete ETL pipeline

## Instructions

### Week 9: Introduction to Airflow

#### 1. Setup
Navigate to the folder:
```bash
cd projects/08_airflow_platform
```

#### 2. Start Airflow
Launch the Airflow platform:
```bash
docker compose up -d
```
**Note**: First startup takes 1-2 minutes. Airflow needs to initialize the metadata database.

Check if containers are running:
```bash
docker compose ps
```

#### 3. Access the UI
Open your browser to `http://localhost:8080`
- **Username**: `airflow`
- **Password**: `airflow`

**What You'll See**: The Airflow dashboard showing all available DAGs.

#### 4. Run Week 9 DAG
1. Find `week_09_hello_world` in the DAG list
2. Toggle the switch on the left to **enable** it
3. Click the **Play** button (▶) on the right to trigger manually
4. Click on the DAG name to see the Graph view
5. Click on a task → **Logs** to see output

**Expected Output**: 
- `print_date` task shows current timestamp
- `hello_python` task prints "Hello from Python!"

### Week 10: Configuration & Scheduling

#### 5. Run Week 10 DAG
The `week_10_config.py` DAG demonstrates:
- Different schedule intervals (`@daily`, `@hourly`, cron expressions)
- Default arguments (owner, retries, email alerts)
- Task dependencies (linear vs parallel)

Enable and trigger `week_10_config` in the UI.

**Expected Output**: Multiple tasks running in parallel, demonstrating dependency management.

### Week 11: Robust Pipelines

#### 6. Run Week 11 DAG
The `week_11_robust_dag.py` demonstrates:
- **Retries**: A task that fails 50% of the time
- **XComs**: Passing data between tasks

Enable and trigger `week_11_robust_dag`.

**Expected Output**: 
- `risky_task` may fail and retry (check logs)
- `consume_data` successfully receives data from `process_data`

### Week 12: Mini-Project 3 - Weather ETL

#### 7. Run the Weather ETL
The `week_12_weather_etl.py` is a complete ETL pipeline:
1. **Extract**: Simulates fetching weather data from an API
2. **Transform**: Converts Celsius to Fahrenheit, adds timestamps
3. **Load**: Inserts into a database (simulated via logs)

Enable and trigger `week_12_weather_etl`.

**Expected Output**: Check logs for each task to see the data flowing through the pipeline.

### 8. Cleanup
Airflow consumes significant resources. Stop when not in use:
```bash
docker compose down
```

To completely remove volumes (fresh start):
```bash
docker compose down -v
```

## Homework / Challenge

### Challenge 1: Custom DAG
Create `week_13_challenge.py`:
1. Build a DAG that runs every 6 hours
2. Task 1: Generate 10 random numbers and push to XCom
3. Task 2: Pull the numbers and calculate the average
4. Task 3: Print "High" if average > 5, else "Low"

### Challenge 2: Error Handling
Modify `week_11_robust_dag.py`:
1. Add an `on_failure_callback` that prints "Task Failed!"
2. Set `retries=5` and observe the behavior
3. Add a `BashOperator` that sends an email (simulated with `echo`)

### Challenge 3: Real Data
Modify `week_12_weather_etl.py`:
1. Use the `requests` library to fetch real weather data from `https://wttr.in/London?format=j1`
2. Parse the JSON response
3. Store the temperature in a local SQLite database

## Troubleshooting

**Issue**: Airflow UI not loading
- **Solution**: Wait 2-3 minutes for initialization. Check logs: `docker compose logs webserver`

**Issue**: Out of memory
- **Solution**: This setup is optimized for 8GB RAM. Close other applications. If needed, reduce worker parallelism in `docker-compose.yml`.

**Issue**: DAG not appearing
- **Solution**: Check for Python syntax errors: `docker compose exec webserver airflow dags list`
