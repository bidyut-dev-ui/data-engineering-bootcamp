# Data Engineering Bootcamp: Zero to Production in 7 Months

> A complete, hands-on curriculum for transitioning from software development to Data Engineering. Built for **8GB RAM, CPU-only** environments. No cloud costs, no GPU required.

[![Status](https://img.shields.io/badge/Status-Complete-success)]()
[![Projects](https://img.shields.io/badge/Projects-30+-blue)]()
[![Duration](https://img.shields.io/badge/Duration-7%20Months-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![PySpark](https://img.shields.io/badge/PySpark-8GB%20RAM%20Optimized-yellow)]()

## 🎯 What You'll Build

By the end of this bootcamp, you'll have:
- ✅ **5 Production-Ready Projects** deployable via Docker
- ✅ **ETL Pipelines** orchestrated with Apache Airflow
- ✅ **Data Warehouse** with optimized star schema
- ✅ **ML Model Serving** via FastAPI
- ✅ **End-to-End Platform** integrating all components
- ✅ **Portfolio** ready for Data Engineer interviews
- ✅ **Production Engineering Skills** for team lead roles

## 🚀 Roles & Skills You Will Master
This bootcamp is strictly mapped to demanding, real-world tech stacks. Rather than just learning the syntax of Python, you will build systems that prepare you for:

### **1. Enterprise Data Engineering & ETL**
- **Core Skills:** Designing fault-tolerant ETL/ELT pipelines, Data Modeling, and Star Schemas.
- **The Tech Stack:** **Apache Airflow** for DAG orchestration, and **PostgreSQL** Data Warehouses (teaching the core analytical concepts you will need for cloud engines like **Snowflake**, **Databricks**, or **AWS Redshift**).

### **2. Generative AI & ML Engineering**
- **Core Skills:** Retrieval-Augmented Generation (RAG), Mathematical Embeddings, and Similarity Search.
- **The Tech Stack:** **LangChain**, Local CPU Models, **FastAPI** model serving, and **Vector Databases** (mastering the math behind Vector Search locally via **pgvector** before you pay for cloud equivalents like **Pinecone** or **Weaviate**).

### **3. Streaming & Cloud-Native Platforms**
- **Core Skills:** Real-time event ingestion, NoSQL modeling, and Cloud Architectures.
- **The Tech Stack:** **Kafka** (running the low-RAM C++ alternative **Redpanda**), and **AWS Services** (mocking **S3**, **DynamoDB**, and **IAM** entirely locally via **LocalStack**).

## 📚 Curriculum Overview

### **Month 1: Python & Data Processing**
Master the fundamentals of data manipulation and cleaning.
- Week 0.5: **Python Fundamentals** (Variables, Data Types, Control Flow, Functions, Data Structures) *For complete beginners*
- Week 1: Environment Setup (WSL2, Docker, Python)
- Week 1.5: **Python Deep Dive** (Iterators, Generators, Context Managers)
- Week 2: Pandas Basics (CSV/JSON/Parquet, cleaning, aggregation)
- Week 2.5: **Exploratory Data Analysis** (Profiling, Visualization with Seaborn/Matplotlib, Data Quality)
- Week 2.75: **PySpark Basics for 8GB RAM** (Distributed processing on limited hardware)
- Week 3: Advanced Pandas (memory optimization, chunking for large files)
- Week 3.5: **Linux & Bash** (Permissions, SSH, Text Processing)
- Week 4: **Project 1** - CLI Data Cleaning Tool

### **Month 2: Databases & SQL**
Learn to design and query data warehouses.
- Week 5: Postgres & SQLite with Docker
- Week 6: Advanced SQL (CTEs, Window Functions, Indexing)
- Week 7: Data Modeling (Star Schema, Normalization)
- Week 8: **Project 2** - ETL to Data Warehouse
- Week 8.5: **Data Reliability** (ACID, Idempotency, Transactions)

### **Month 3: Orchestration with Airflow**
Automate and monitor data pipelines.
- Week 9-10: Airflow Setup & Configuration
- Week 11: Robust DAGs (Error handling, Retries, XComs)
- Week 12: **Project 3** - Weather ETL Pipeline
- Week 12.5: **Schema Evolution** (Handling changes, JSON validation)

### **Month 4: API Development & Advanced PySpark**
Expose data and models via REST APIs while mastering distributed processing.
- Week 13: **Advanced PySpark Part 1** (Catalyst Optimizer, Memory Management)
- Week 14: **Advanced PySpark Part 2** (Join Strategies, MLlib, Streaming)
- Week 14.5: **Hadoop Fundamentals** (HDFS, MapReduce, YARN on 8GB RAM)
- Week 15: FastAPI Fundamentals
- Week 16: Database Integration with FastAPI
- Week 16.5: **Event-Driven & Streaming Pipelines** (Redpanda, real-time ingestion)
- Week 17: **Project 4** - Data Warehouse API with PySpark Integration
- Week 17.5: **Statistics Fundamentals** (Distributions, Outliers, Bias)

### **Month 5: Machine Learning & AI**
Train and deploy ML models on CPU with PySpark integration.
- Week 18: Scikit-learn (Regression, Classification)
- Week 19: Model Evaluation & Serialization
- Week 19.5: **Django for Data Applications** (Web framework for data dashboards)
- Week 19.75: **Vector Databases & RAG** (Similarity Search, pgvector)
- Week 20: LangChain Basics (Prompt Engineering, RAG)
- Week 21: **Project 5** - ML Prediction Service with PySpark MLlib

### **Month 6: Capstone & Job Prep**
Integrate everything and prepare for interviews.
- Week 22: Capstone Planning & Architecture
- Week 23: Implementation: Ingest & Clean (Airflow)
- Week 24: Implementation: Model & Serve (FastAPI + LangChain RAG)
- Week 25: Final Polish, Docker Compose for everything
- Week 26: Resume Building & Portfolio
- Week 27: Interview Preparation (PySpark & Data Engineering questions)

### **Month 7: Production Engineering & Team Leadership**
Build secure, observable, production-grade systems.
- Week 28: Security & Authentication (JWT, RBAC, PII masking)
- Week 29: Testing & Data Quality (Pytest, Great Expectations)
- Week 30: Observability & Monitoring (Prometheus, Grafana, Alerting)
- Week 31: CI/CD & Deployment (GitHub Actions, Docker registry)

📖 **[View Full Syllabus](Syllabus.md)**

## 🚀 Quick Start

### Prerequisites
- **OS**: WSL2 Ubuntu 22 (or native Linux)
- **RAM**: 8GB minimum
- **Storage**: 10GB free space
- **Software**: Python 3.10+, Docker, Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd data-engineering-bootcamp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
cd projects/00_setup_and_refresher
python check_env.py
```

### Your First Project

```bash
cd projects/01_pandas_basics
python generate_data.py
python 01_basics_tutorial.py
```

## 📁 Repository Structure

```
data-engineering-bootcamp/
├── README.md                    # You are here
├── Syllabus.md                  # Detailed 7-month roadmap
├── QUICK_REFERENCE.md           # Commands & troubleshooting
├── requirements.txt             # Python dependencies
└── projects/
    ├── 00_setup_and_refresher/  # Week 1
    ├── 01_pandas_basics/        # Week 2
    ├── 02_advanced_pandas/      # Week 3
    ├── 02_5_pyspark_basics/     # Week 2.75 - PySpark Basics for 8GB RAM
    ├── 03_data_janitor/         # Week 4 - Project 1
    ├── 04_databases_docker/     # Week 5
    ├── 05_advanced_sql/         # Week 6
    ├── 06_data_modeling/        # Week 7
    ├── 07_warehouse_builder/    # Week 8 - Project 2
    ├── 08_airflow_platform/     # Weeks 9-12 - Project 3
    ├── 11_aws_localstack/       # Week 11.5 - AWS Mocking
    ├── 03_pyspark_advanced/     # Weeks 13-14 - Advanced PySpark
    ├── 09_fastapi_basics/       # Week 15
    ├── 10_fastapi_db/           # Week 16
    ├── 15_5_streaming_redpanda/ # Week 16.5 - Real-time Streaming
    ├── 12_data_api_service/     # Weeks 17-18 - Project 4
    ├── 13_sklearn_basics/       # Week 19
    ├── 14_model_evaluation/     # Week 20
    ├── 15_langchain_basics/     # Week 21
    ├── 19_5_vector_databases/   # Week 21.5 - RAG
    ├── 16_predictive_service/   # Week 22 - Project 5
    ├── 17_capstone/             # Weeks 23-26 - Capstone
    ├── 18_job_prep/             # Weeks 27-28
    ├── 27_security_and_governance/ # Week 29 - IAM & PII Masking
    └── 29_platform_reliability/ # Week 30 - Incident Runbooks
```

Each project contains:
- `README.md` - Instructions and learning objectives
- Source code with detailed comments
- Sample data generators
- Homework challenges

## 🎓 Learning Approach

### **Hands-On First**
Every concept is taught through executable code. No theory-only lessons.

### **Progressive Complexity**
Each week builds on previous skills. By Week 31, you're integrating 7 months of learning.

### **Production Patterns**
Learn industry best practices: Docker, error handling, logging, testing.

### **Resource Constrained**
All projects run on 8GB RAM. Learn to optimize for real-world constraints.

## 🛠️ Technologies Covered

**Languages**: Python, SQL, Bash
**Data Processing**: Pandas, NumPy, PySpark, Hadoop
**Databases**: PostgreSQL, SQLite
**Orchestration**: Apache Airflow
**APIs**: FastAPI, REST, Django
**ML/AI**: Scikit-learn, LangChain, PySpark MLlib
**DevOps**: Docker, Docker Compose, GitHub Actions
**Tools**: Git, Linux, VS Code
**Monitoring**: Prometheus, Grafana
**Security**: JWT, RBAC, PII masking

## 📊 Project Highlights

### **Capstone: Wealth Management Data Platform**
A complete end-to-end system featuring:
- Daily ETL pipeline (Airflow)
- Star schema data warehouse (Postgres)
- Transaction anomaly detection model (RandomForest)
- REST API for secure data access (FastAPI)
- Full stack orchestration (Docker Compose)

**Skills Demonstrated**: System design, ETL, ML deployment, API development

### **Trade Data Warehouse Builder**
Production-ready ETL pipeline:
- Ingests trade CSV files from multiple sources
- Transforms and validates financial data
- Loads into optimized star schema
- Handles errors and retries

**Skills Demonstrated**: Data modeling, SQL optimization, pipeline design

### **ML Prediction Service**
Containerized ML service:
- Trains housing price prediction model
- Serves predictions via FastAPI
- Includes batch processing
- Production-ready with Docker

**Skills Demonstrated**: ML deployment, API design, containerization

### **Production Monitoring Platform**
Enterprise-grade observability:
- Prometheus metrics collection
- Grafana dashboards
- Structured logging
- Alerting and incident response

**Skills Demonstrated**: Monitoring, observability, production engineering

## 💼 Career Preparation

### **Resume Building**
- Translate projects into professional bullet points
- Quantify achievements (e.g., "Processed 1M+ records daily")
- ATS-friendly formatting
- [Resume Guide](projects/18_job_prep/RESUME_GUIDE.md)

### **Interview Prep & Job Mapping**
- 26 common Data Engineer questions with answers
- **Searchable Job Targeting**: We store specific target roles in `projects/18_job_prep/job_descriptions/`. Search the repo for tags like `#role-datacompany-senior` or `#role-genai-engineer` to highlight exactly which weeks you must complete to pass that specific interview.
- Behavioral questions (STAR method)
- [Interview Questions](projects/18_job_prep/INTERVIEW_QUESTIONS.md)

### **Portfolio Showcase**
Frame your projects for recruiters:
- "Built automated Airflow pipeline reducing data processing time by 80%"
- "Designed star schema warehouse supporting 50+ analytical queries"
- "Deployed ML model serving 10K+ predictions daily via FastAPI"
- "Implemented RAG pipeline searching 1M+ vectors locally via pgvector"
- "Built real-time transaction ingestion pipeline handling 5K msgs/sec with Redpanda"
- "Implemented production monitoring with Prometheus/Grafana reducing MTTR by 60%"

## 🎯 Target Audience

### **Perfect For:**
- ✅ Software developers transitioning to Data Engineering
- ✅ Self-learners who prefer hands-on projects
- ✅ Budget-conscious learners (no cloud costs)
- ✅ Those with limited hardware (8GB RAM)
- ✅ Job seekers targeting service-based companies (TCS, Accenture, etc.)
- ✅ Aspiring team leads needing production engineering skills

### **Not Ideal For:**
- ❌ Complete programming beginners (assumes Python/coding basics)
- ❌ Those seeking cloud-specific certifications (AWS/Azure/GCP)
- ❌ Big data specialists (focuses on fundamentals, not Spark/Hadoop)

## 📖 Documentation

- **[Syllabus.md](Syllabus.md)** - Week-by-week breakdown
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands, troubleshooting, Git workflow
- **Project READMEs** - Detailed instructions for each week

## 🤝 Contributing

This is a personal learning repository, but feedback is welcome:
- Found a bug? Open an issue
- Have a suggestion? Submit a pull request
- Want to share your progress? Tag me!

## 📝 License

MIT License - Feel free to use this curriculum for your own learning journey.

## 🙏 Acknowledgments

Built with guidance from:
- Real-world Data Engineering practices
- Industry-standard tools and patterns
- Feedback from service-based company interviews

---

**Ready to start?** Head to [`projects/00_setup_and_refresher`](projects/00_setup_and_refresher) and begin your journey! 🚀

**Questions?** Check [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for common commands and troubleshooting.
