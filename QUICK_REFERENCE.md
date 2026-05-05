# Quick Reference Guide

## 🚀 How to Start (Day 1 for a Ruby on Rails Dev)

Since you are transitioning from Ruby on Rails, your primary focus should be adapting your object-oriented mindset to Python and distributed data systems. 

**Your First 3 Steps:**
1. **`00_setup_and_refresher/`**: Ensure WSL2 and Docker are running. 
2. **`01_5_python_oop/`**: (CRITICAL) Python classes and decorators behave differently than Ruby modules and mixins. Start here to map your Ruby knowledge to Python.
3. **`03_5_linux_bash/`**: You likely know this, but skim it to ensure your WSL2 environment is solid.

---

## 📁 Project Structure (The "Team Lead" Edition)

The repository is organized progressively. Start from 00 and work your way up.

### Core Python & Data Wrangling (Months 1-2)
*Transitioning your Ruby skills to Python Data handling.*
- `00_setup_and_refresher/`  - WSL2, Docker, Python Envs
- `00_5_python_fundamentals/` - Basic Syntax
- `01_python_deep_dive/`      - Iterators, Generators
- `01_5_python_oop/`          - **[Team Lead]** Python OOP & ABCs
- `01_pandas_basics/`         - Tabular data manipulation
- `02_advanced_pandas/`       - Memory-efficient chunking
- `02_5_eda/`                 - Exploratory Data Analysis
- `03_data_janitor/`          - Mini-Project: Data Cleaning
- `03_5_linux_bash/`          - CLI tools (grep, awk)

### Distributed Data & Databases (Months 2-3)
*Handling data too big for Ruby's ActiveRecord.*
- `02_5_pyspark_basics/`      - Intro to Spark
- `03_pyspark_advanced/`      - Spark optimization for 8GB RAM
- `04_databases_docker/`      - Postgres via Docker
- `05_advanced_sql/`          - CTEs, Window Functions
- `06_data_modeling/`         - Star Schema vs Snowflake
- `07_warehouse_builder/`     - Mini-Project: ETL to Postgres
- `08_5_data_reliability/`    - ACID, Idempotency

### Orchestration & Modern Data Stack (Months 3-4)
*Replacing cron jobs with directed acyclic graphs.*
- `08_airflow_platform/`      - Apache Airflow basics
- `11_aws_localstack/`        - S3/IAM locally
- `11_5_terraform_iac/`       - **[Team Lead]** Infrastructure as Code
- `12_5_schema_evolution/`    - Handling upstream API changes
- `14_5_dbt_modeling/`        - **[Team Lead]** Data Build Tool (dbt)
- `15_5_streaming_redpanda/`  - Kafka/Redpanda streaming

### APIs, Architecture, & AI (Months 5-6)
*Building Data-as-a-Service and RAG.*
- `09_fastapi_basics/`        - Python's high-speed API framework
- `09_5_pydantic_v2/`         - **[Team Lead]** Advanced Data Validation
- `10_fastapi_db/`            - Connecting APIs to Warehouses
- `12_data_api_service/`      - Mini-Project: Data API
- `16_5_vector_databases/`    - **[Team Lead]** Embeddings & Similarity Search

### Production Engineering & Team Leadership (Month 7)
*Skills required to pass Senior/Lead interviews.*
- `18_job_prep/`              - Interview Qs, Live Coding, System Design
- `20_tested_pipeline/`       - **[Team Lead]** Pytest & Great Expectations
- `21_monitored_platform/`    - **[Team Lead]** Prometheus & Grafana
- `21_5_incident_response/`   - **[Team Lead]** On-Call Playbooks
- `21_6_data_lineage/`        - **[Team Lead]** OpenLineage & Metadata
- `21_7_profiling/`           - **[Team Lead]** Query & Code Profiling
- `22_cicd_pipeline/`         - **[Team Lead]** GitHub Actions
- `27_security_and_governance/`- **[Team Lead]** PII Masking & RBAC

---

## 💻 Common Commands

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker
```bash
docker compose up -d           # Start services
docker compose logs -f airflow # View logs
docker system prune -a         # Clean up if you hit 8GB RAM limits
```

### Testing (Pytest)
```bash
pytest projects/20_tested_pipeline/tests/ -v
```

---

## 🧠 Translation Guide: Ruby to Python Data Engineering
- **ActiveRecord** -> **SQLAlchemy** (for OLTP apps) or **dbt** (for analytical SQL).
- **RSpec** -> **Pytest**.
- **Sidekiq/Resque** -> **Apache Airflow** (Airflow is for massive data workflows, not just background jobs).
- **Gemfile** -> **requirements.txt** or **pyproject.toml**.
- **Hashes** -> **Dictionaries** (but for large data, you use Pandas DataFrames).
