# Data Engineering & AI/ML Learning Syllabus (7 Months)

**Goal**: Transition from Ruby/JS to Data Engineering Team Lead (Service-based companies).
**Constraints**: 8GB RAM, No GPU, CPU-only, WSL2 Ubuntu.
**Focus**: Hands-on, local, runnable projects with production-grade patterns.

## Month 1: Python for Data Engineering & Data Processing
*Focus: Mastering the tools of the trade on limited hardware.*
- **Week 1**: Environment Setup (WSL2, Docker, VS Code) & Python Refresher (Types, Virtual Envs).
- **Week 1.5**: **Python Deep Dive for Pandas** (Iterators, Comprehensions, Unpacking, Context Managers, Lambdas). *Critical prerequisite!*
- **Week 2**: Data Manipulation with Pandas (Reading/Writing CSV/JSON/Parquet, Cleaning, Aggregating).
- **Week 2.5**: **Exploratory Data Analysis (EDA)** (Profiling, Visualizing Distributions, Correlation, Data Quality Checks). *Critical for understanding data.*
    - *Tools: Seaborn, Matplotlib (Boxplots, Heatmaps, Pairplots).*
- **Week 3**: Advanced Pandas & NumPy (Performance optimization for low RAM, chunking).
- **Week 3.5**: **Linux & Bash for Data Engineers** (Permissions, Process Management, SSH, Text Processing with grep/sed/awk). *Critical for Airflow/Docker debugging.*
- **Week 4**: Mini-Project 1: **"The Data Janitor"** - CLI tool to ingest raw messy logs, clean them, and save as Parquet.

## Month 2: Databases & SQL
*Focus: Storing and querying data efficiently.*
- **Week 5**: Dockerizing Postgres & SQLite. Connecting via Python (SQLAlchemy/Psycopg2).
- **Week 6**: Advanced SQL (CTEs, Window Functions, Indexing).
- **Week 7**: Data Modeling (Star/Snowflake schemas, Normalization).
- **Week 8**: Mini-Project 2: **"Warehouse Builder"** - ETL script to load CSVs into a Postgres Star Schema.
- **Week 8.5**: **Data Reliability Engineering** (ACID Transactions, Idempotency, Handling Partial Failures). *Critical for production pipelines.*

## Month 3: Orchestration & Pipelines (ETL/ELT)
*Focus: Automating workflows.*
- **Week 9**: Introduction to Apache Airflow (Core concepts: DAGs, Operators, Sensors).
- **Week 10**: Setting up Airflow locally (Docker Compose optimized for low RAM).
- **Week 11**: Building robust DAGs (Error handling, Retries, XComs).
- **Week 12**: Mini-Project 3: **"Orchestrated ETL"** - Airflow DAG to fetch weather API data, process it, and load to Postgres.
- **Week 12.5**: **Schema Evolution & Data Contracts** (Handling schema changes, JSON validation, Backward compatibility). *Critical for long-term maintenance.*

## Month 4: API Development & Model Serving
*Focus: Exposing data and logic.*
- **Week 13**: FastAPI Fundamentals (Routes, Pydantic models, Async).
- **Week 14**: Connecting FastAPI to Databases.
- **Week 15**: Dockerizing FastAPI applications.
- **Week 16**: Mini-Project 4: **"Data API Service"** - REST API to query the Data Warehouse created in Month 2.
- **Week 16.5**: **Statistics for Data Engineers** (Distributions, Outliers, Sampling Bias, Basic Stats). *Critical prerequisite for ML.*

## Month 5: Machine Learning & AI on CPU
*Focus: Practical ML without heavy compute.*
- **Week 17**: Scikit-learn Basics (Regression, Classification, Preprocessing pipelines).
- **Week 18**: Model Evaluation & Serialization (Pickle/Joblib).
- **Week 19**: Intro to LangChain (Prompt templates, Chains, Local LLMs - *carefully selected for CPU*).
- **Week 20**: Mini-Project 5: **"Predictive Service"** - Train a housing price model, serve predictions via FastAPI.

## Month 6: Capstone & Job Prep
*Focus: Putting it all together and getting hired.*
- **Week 21**: Capstone Planning & Architecture (Full pipeline design).
- **Week 22**: Implementation: Ingest & Clean (Airflow).
- **Week 23**: Implementation: Model & Serve (FastAPI + LangChain RAG for documentation query).
- **Week 24**: Final Polish, Docker Compose for everything.
- **Week 25**: Resume Building (Translating projects to bullet points).
- **Week 26**: Mock Interview Prep (Common DE questions).

## Month 7: Production Engineering & Team Leadership
*Focus: Building secure, observable, production-grade systems for team lead roles.*
- **Week 27**: Security & Authentication (JWT in FastAPI, RBAC, API keys, Secrets management).
- **Week 28**: Testing & Data Quality (Pytest, Great Expectations, Integration tests, Coverage).
- **Week 29**: Observability & Monitoring (Prometheus, Grafana, Structured logging, Alerting).
- **Week 30**: CI/CD & Deployment (GitHub Actions, Automated testing, Docker registry, Deployment automation).
