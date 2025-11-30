# Data Engineering Bootcamp: Zero to Production in 6 Months

> A complete, hands-on curriculum for transitioning from software development to Data Engineering. Built for **8GB RAM, CPU-only** environments. No cloud costs, no GPU required.

[![Status](https://img.shields.io/badge/Status-Complete-success)]()
[![Projects](https://img.shields.io/badge/Projects-18-blue)]()
[![Duration](https://img.shields.io/badge/Duration-6%20Months-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

## 🎯 What You'll Build

By the end of this bootcamp, you'll have:
- ✅ **5 Production-Ready Projects** deployable via Docker
- ✅ **ETL Pipelines** orchestrated with Apache Airflow
- ✅ **Data Warehouse** with optimized star schema
- ✅ **ML Model Serving** via FastAPI
- ✅ **End-to-End Platform** integrating all components
- ✅ **Portfolio** ready for Data Engineer interviews

## 📚 Curriculum Overview

### **Month 1: Python & Data Processing**
Master the fundamentals of data manipulation and cleaning.
- Week 1: Environment Setup (WSL2, Docker, Python)
- Week 1.5: **Python Deep Dive** (Iterators, Generators, Context Managers)
- Week 2: Pandas Basics (CSV/JSON/Parquet, cleaning, aggregation)
- Week 2.5: **Exploratory Data Analysis** (Profiling, Visualization with Seaborn/Matplotlib, Data Quality)
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

### **Month 4: API Development**
Expose data and models via REST APIs.
- Week 13: FastAPI Fundamentals
- Week 14: Database Integration
- Week 15-16: **Project 4** - Data Warehouse API
- Week 16.5: **Statistics Fundamentals** (Distributions, Outliers, Bias)

### **Month 5: Machine Learning**
Train and deploy ML models on CPU.
- Week 17: Scikit-learn (Regression, Classification)
- Week 18: Model Evaluation & Serialization
- Week 19: LangChain Basics (Prompt Engineering, RAG)
- Week 20: **Project 5** - ML Prediction Service

### **Month 6: Capstone & Job Prep**
Integrate everything and prepare for interviews.
- Week 21-24: **Capstone** - Customer Analytics Platform
- Week 25: Resume Building & Portfolio
- Week 26: Interview Preparation (26 common questions)

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
├── Syllabus.md                  # Detailed 6-month roadmap
├── QUICK_REFERENCE.md           # Commands & troubleshooting
├── requirements.txt             # Python dependencies
└── projects/
    ├── 00_setup_and_refresher/  # Week 1
    ├── 01_pandas_basics/        # Week 2
    ├── 02_advanced_pandas/      # Week 3
    ├── 03_data_janitor/         # Week 4 - Project 1
    ├── 04_databases_docker/     # Week 5
    ├── 05_advanced_sql/         # Week 6
    ├── 06_data_modeling/        # Week 7
    ├── 07_warehouse_builder/    # Week 8 - Project 2
    ├── 08_airflow_platform/     # Weeks 9-12 - Project 3
    ├── 09_fastapi_basics/       # Week 13
    ├── 10_fastapi_db/           # Week 14
    ├── 12_data_api_service/     # Weeks 15-16 - Project 4
    ├── 13_sklearn_basics/       # Week 17
    ├── 14_model_evaluation/     # Week 18
    ├── 15_langchain_basics/     # Week 19
    ├── 16_predictive_service/   # Week 20 - Project 5
    ├── 17_capstone/             # Weeks 21-24 - Capstone
    └── 18_job_prep/             # Weeks 25-26
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
Each week builds on previous skills. By Week 26, you're integrating 6 months of learning.

### **Production Patterns**
Learn industry best practices: Docker, error handling, logging, testing.

### **Resource Constrained**
All projects run on 8GB RAM. Learn to optimize for real-world constraints.

## 🛠️ Technologies Covered

**Languages**: Python, SQL, Bash  
**Data Processing**: Pandas, NumPy  
**Databases**: PostgreSQL, SQLite  
**Orchestration**: Apache Airflow  
**APIs**: FastAPI, REST  
**ML/AI**: Scikit-learn, LangChain  
**DevOps**: Docker, Docker Compose  
**Tools**: Git, Linux, VS Code  

## 📊 Project Highlights

### **Capstone: Customer Analytics Platform**
A complete end-to-end system featuring:
- Daily ETL pipeline (Airflow)
- Star schema data warehouse (Postgres)
- Churn prediction model (RandomForest)
- REST API for predictions (FastAPI)
- Full stack orchestration (Docker Compose)

**Skills Demonstrated**: System design, ETL, ML deployment, API development

### **Data Warehouse Builder**
Production-ready ETL pipeline:
- Ingests CSV files from multiple sources
- Transforms and validates data
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

## 💼 Career Preparation

### **Resume Building**
- Translate projects into professional bullet points
- Quantify achievements (e.g., "Processed 1M+ records daily")
- ATS-friendly formatting
- [Resume Guide](projects/18_job_prep/RESUME_GUIDE.md)

### **Interview Prep**
- 26 common Data Engineer questions with answers
- SQL query practice
- System design patterns
- Behavioral questions (STAR method)
- [Interview Questions](projects/18_job_prep/INTERVIEW_QUESTIONS.md)

### **Portfolio Showcase**
Frame your projects for recruiters:
- "Built automated ETL pipeline reducing processing time by 80%"
- "Designed star schema warehouse supporting 50+ analytical queries"
- "Deployed ML model serving 10K+ predictions daily"

## 🎯 Target Audience

### **Perfect For:**
- ✅ Software developers transitioning to Data Engineering
- ✅ Self-learners who prefer hands-on projects
- ✅ Budget-conscious learners (no cloud costs)
- ✅ Those with limited hardware (8GB RAM)
- ✅ Job seekers targeting service-based companies (TCS, Accenture, etc.)

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
