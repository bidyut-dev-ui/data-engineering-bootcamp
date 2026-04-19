# Data Engineering & AI/ML Learning Syllabus (7 Months)

**Goal**: Transition from Ruby/JS to Data Engineering Team Lead (Service-based companies).
**Constraints**: 8GB RAM, No GPU, CPU-only, WSL2 Ubuntu.
**Focus**: Hands-on, local, runnable projects with production-grade patterns.

## Month 1: Python for Data Engineering & Data Processing
*Focus: Mastering the tools of the trade on limited hardware.*
- **Week 0.5**: **Python Fundamentals for Complete Beginners** (Variables, Data Types, Control Flow, Functions, Data Structures, File I/O, Error Handling). *For those with no Python experience.* `#role-genai-engineer` `#skill-python`
- **Week 1**: Environment Setup (WSL2, Docker, VS Code) & Python Refresher (Types, Virtual Envs).
- **Week 1.5**: **Python Deep Dive for Pandas** (Iterators, Comprehensions, Unpacking, Context Managers, Lambdas). *Critical prerequisite!* `#role-genai-engineer` `#skill-python`
- **Week 2**: Data Manipulation with Pandas (Reading/Writing CSV/JSON/Parquet, Cleaning, Aggregating).
- **Week 2.5**: **Exploratory Data Analysis (EDA)** (Profiling, Visualizing Distributions, Correlation, Data Quality Checks). *Critical for understanding data.*
    - *Tools: Seaborn, Matplotlib (Boxplots, Heatmaps, Pairplots).*
- **Week 2.75**: **PySpark Basics for 8GB RAM** (SparkSession configuration, DataFrame operations, memory optimization for constrained hardware). `#role-datacompany-senior` `#skill-pyspark`
- **Week 3**: Advanced Pandas & NumPy (Performance optimization for low RAM, chunking).
- **Week 3.5**: **Linux & Bash for Data Engineers** (Permissions, Process Management, SSH, Text Processing with grep/sed/awk). *Critical for Airflow/Docker debugging.*
- **Week 4**: Mini-Project 1: **"The Data Janitor"** - CLI tool to ingest raw messy logs, clean them, and save as Parquet.

## Month 2: Databases & SQL
*Focus: Storing and querying data efficiently.*
- **Week 5**: Dockerizing Postgres & SQLite. Connecting via Python (SQLAlchemy/Psycopg2). `#role-genai-engineer` `#skill-database`
- **Week 6**: Advanced SQL (CTEs, Window Functions, Indexing).
- **Week 7**: Data Modeling (Star/Snowflake schemas, Normalization).
- **Week 8**: Mini-Project 2: **"Warehouse Builder"** - ETL script to load CSVs into a Postgres Star Schema. `#role-datacompany-senior`
- **Week 8.5**: **Data Reliability Engineering** (ACID Transactions, Idempotency, Handling Partial Failures). *Critical for production pipelines.* `#role-datacompany-senior` `#skill-reliability`

## Month 3: Orchestration & Pipelines (ETL/ELT)
*Focus: Automating workflows.*
- **Week 9**: Introduction to Apache Airflow (Core concepts: DAGs, Operators, Sensors).
- **Week 10**: Setting up Airflow locally (Docker Compose optimized for low RAM). `#role-genai-engineer` `#skill-devops`
- **Week 11**: Building robust DAGs (Error handling, Retries, XComs). `#role-datacompany-senior` `#skill-reliability`
- **Week 11.5**: **Cloud-Native & NoSQL Analytics** (AWS S3, DynamoDB, IAM via LocalStack). `#role-datacompany-senior` `#skill-aws`
- **Week 12**: Mini-Project 3: **"Orchestrated ETL"** - Airflow DAG to fetch weather API data, process it, and load to Postgres. `#role-datacompany-senior`
- **Week 12.5**: **Schema Evolution & Data Contracts** (Handling schema changes, JSON validation, Backward compatibility). *Critical for long-term maintenance.*

## Month 4: API Development & Advanced PySpark
*Focus: Exposing data and logic while mastering distributed processing.*
- **Week 13**: **Advanced PySpark - Catalyst Optimizer & Memory Management** (Query optimization, memory tuning, join strategies). `#role-datacompany-senior` `#skill-pyspark`
- **Week 14**: **Advanced PySpark - MLlib & Streaming** (Distributed ML pipelines, Structured Streaming, FastAPI integration). `#role-datacompany-senior` `#skill-pyspark`
- **Week 14.5**: **Hadoop Fundamentals for 8GB RAM** (HDFS basics, MapReduce with Python, YARN resource management on constrained hardware). `#role-datacompany-senior` `#skill-hadoop`
- **Week 15**: FastAPI Fundamentals (Routes, Pydantic models, Async). `#role-genai-engineer` `#skill-fastapi`
- **Week 16**: Connecting FastAPI to Databases.
- **Week 16.5**: **Event-Driven & Streaming Pipelines** (Redpanda, real-time ingestion, aggregations). `#role-datacompany-senior` `#skill-streaming`
- **Week 17**: Mini-Project 4: **"Data API Service"** - REST API to query the Data Warehouse created in Month 2.
- **Week 17.5**: **Statistics for Data Engineers** (Distributions, Outliers, Sampling Bias, Basic Stats). *Critical prerequisite for ML.*

## Month 5: Machine Learning & AI on CPU
*Focus: Practical ML without heavy compute.*
- **Week 18**: Scikit-learn Basics (Regression, Classification, Preprocessing pipelines).
- **Week 19**: Model Evaluation & Serialization (Pickle/Joblib).
- **Week 19.5**: **Django for Data Applications** (Models, Views, Templates, Django REST Framework, building data dashboards). `#role-genai-engineer` `#skill-django`
- **Week 19.75**: **Vector Databases & RAG** (Pinecone concepts via pgvector locally, Similarity Search). `#role-genai-engineer` `#skill-ai-rag`
- **Week 20**: Intro to LangChain (Prompt templates, Chains, Local LLMs - *carefully selected for CPU*). `#role-genai-engineer` `#skill-ai-rag`
- **Week 21**: Mini-Project 5: **"Predictive Service"** - Train a housing price model, serve predictions via FastAPI.

## Month 6: Capstone & Job Prep
*Focus: Putting it all together and getting hired.*
- **Week 22**: Capstone Planning & Architecture (Full pipeline design).
- **Week 23**: Implementation: Ingest & Clean (Airflow).
- **Week 24**: Implementation: Model & Serve (FastAPI + LangChain RAG for documentation query).
- **Week 25**: Final Polish, Docker Compose for everything.
- **Week 26**: Resume Building (Translating projects to bullet points).
- **Week 27**: Mock Interview Prep (Common DE questions).

## Month 7: Production Engineering & Team Leadership
*Focus: Building secure, observable, production-grade systems for team lead roles.*
- **Week 28**: Security & Authentication (JWT in FastAPI, RBAC, API keys, Secrets management, PII masking, Encryption). `#role-datacompany-senior` `#skill-security`
- **Week 29**: Testing & Data Quality (Pytest, Great Expectations, Integration tests, Coverage). `#role-genai-engineer` `#skill-devops`
- **Week 30**: Observability & Monitoring (Prometheus, Grafana, Structured logging, Alerting, Incident Runbooks). `#role-datacompany-senior` `#skill-reliability`
- **Week 31**: CI/CD & Deployment (GitHub Actions, Automated testing, Docker registry, Deployment automation). `#role-genai-engineer` `#skill-devops`
