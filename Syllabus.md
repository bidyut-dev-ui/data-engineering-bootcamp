# Data Engineering Leadership Syllabus (7 Months)

**Goal**: Transition from Ruby/JS to Data Engineering Team Lead (Service-based companies).
**Constraints**: 8GB RAM, No GPU, CPU-only, WSL2 Ubuntu.
**Focus**: Hands-on, local, runnable projects with production-grade patterns.

---

## Month 1: Python for Data Engineering & Data Processing
*Focus: Transitioning your Ruby skills to Python's data ecosystem on limited hardware.*
- **Week 0.5**: Python Fundamentals for Complete Beginners.
- **Week 1**: Environment Setup (WSL2, Docker) & Python Refresher.
- **Week 1.5**: Python Deep Dive (Iterators, Generators, Decorators).
- **Week 1.75**: **[Team Lead]** Python OOP & ABCs (`projects/01_5_python_oop`). *Mapping Ruby mixins to Python inheritance.*
- **Week 2**: Data Manipulation with Pandas (Reading Parquet/JSON, Cleaning).
- **Week 2.5**: Exploratory Data Analysis (EDA) & Data Profiling.
- **Week 2.75**: PySpark Basics for 8GB RAM (Memory optimization).
- **Week 3**: Advanced Pandas (Chunking large files out-of-core).
- **Week 3.5**: Linux & Bash for Data Engineers (grep, awk).
- **Week 4**: Mini-Project 1: **"The Data Janitor"** - CLI tool to ingest raw logs and save as Parquet.

## Month 2: Databases, Modeling & SQL
*Focus: Storing and querying data efficiently beyond basic CRUD.*
- **Week 5**: Dockerizing Postgres. Connecting via Python (SQLAlchemy).
- **Week 6**: Advanced SQL (CTEs, Window Functions, LAG/LEAD).
- **Week 7**: Data Modeling (Star/Snowflake schemas, Normalization vs Denormalization).
- **Week 8**: Mini-Project 2: **"Warehouse Builder"** - ETL script to load CSVs into Postgres.
- **Week 8.5**: **[Team Lead]** Data Reliability (ACID, Idempotency, Handling Partial Failures).

## Month 3: Orchestration, Infrastructure, & Streaming
*Focus: Automating workflows and treating infrastructure as code.*
- **Week 9**: Introduction to Apache Airflow (DAGs, Operators, Sensors).
- **Week 10**: Setting up Airflow locally (Docker Compose optimized for low RAM).
- **Week 11**: Building robust DAGs (XComs, Branching, Error handling).
- **Week 11.5**: **[Team Lead]** Infrastructure as Code via Terraform (`projects/11_5_terraform_iac`).
- **Week 12**: Mini-Project 3: **"Orchestrated ETL"** - Airflow pipeline to fetch API data.
- **Week 12.5**: **[Team Lead]** Schema Evolution & Data Contracts (`projects/12_5_schema_evolution`).
- **Week 12.75**: **[Team Lead]** Streaming with Redpanda/Kafka (`projects/15_5_streaming_redpanda`).

## Month 4: The Modern Data Stack & APIs
*Focus: Data Build Tool (dbt) and exposing data via REST APIs.*
- **Week 13**: Advanced PySpark (Catalyst Optimizer, Shuffle Partitions).
- **Week 14**: **[Team Lead]** dbt (data build tool) Fundamentals (`projects/14_5_dbt_modeling`).
- **Week 15**: FastAPI Fundamentals (Routes, Async logic).
- **Week 15.5**: **[Team Lead]** Pydantic V2 Mastery (`projects/09_5_pydantic_v2`).
- **Week 16**: Connecting FastAPI to the Data Warehouse.
- **Week 17**: Mini-Project 4: **"Data API Service"** - REST API querying the Warehouse.

## Month 5: Advanced Data Platform & AI Architecture
*Focus: Preparing for modern AI-driven data systems.*
- **Week 18**: Statistics for Data Engineers (Distributions, Outliers).
- **Week 19**: **[Team Lead]** Vector Databases & Similarity Search (`projects/16_5_vector_databases`).
- **Week 19.5**: Intro to LangChain (Prompt templates, RAG architecture).
- **Week 20**: Mini-Project 5: **"Predictive Service"** - Serving data for a mock ML model.

## Month 6: Capstone & Production Engineering
*Focus: Ensuring pipelines don't break in production (The "Lead" mindset).*
- **Week 21**: Capstone Planning & Architecture.
- **Week 22**: **[Team Lead]** Tested Pipelines (Pytest & Great Expectations).
- **Week 23**: **[Team Lead]** Monitored Platforms (Prometheus & Grafana).
- **Week 24**: **[Team Lead]** CI/CD Pipelines (GitHub Actions).
- **Week 25**: **[Team Lead]** Security & Governance (PII Masking, RBAC).
- **Week 26**: **[Team Lead]** Data Lineage & Profiling (`projects/21_6_data_lineage`, `projects/21_7_profiling`).

## Month 7: Team Leadership & Job Preparation
*Focus: Mentorship, architecture trade-offs, and interview mastery.*
- **Week 27**: **[Team Lead]** Incident Response Playbooks (`projects/21_5_incident_response`).
- **Week 28**: Architecture Trade-offs & Mentorship (`projects/18_job_prep/leadership/`).
- **Week 29**: Code Review Exercises (`projects/18_job_prep/code_reviews/`).
- **Week 30**: Live Coding Prep (FastAPI, Django ORM, Algorithms) (`projects/18_job_prep/LIVE_CODING_PRACTICE.md`).
- **Week 31**: Resume Polish & Final Mock Interviews.
