# Quick Reference Guide

## Project Structure
```
AI-ML/
├── Prompt.md                    # Context reset prompt
├── Syllabus.md                  # 6-month roadmap
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── projects/
    ├── 00_setup_and_refresher/  # Week 1
    ├── 01_pandas_basics/        # Week 2
    ├── 02_advanced_pandas/      # Week 3
    ├── 03_data_janitor/         # Week 4
    ├── 04_databases_docker/     # Week 5
    ├── 05_advanced_sql/         # Week 6
    ├── 06_data_modeling/        # Week 7
    ├── 07_warehouse_builder/    # Week 8
    ├── 08_airflow_platform/     # Weeks 9-12
    ├── 09_fastapi_basics/       # Week 13
    ├── 10_fastapi_db/           # Week 14
    ├── 12_data_api_service/     # Weeks 15-16
    ├── 13_sklearn_basics/       # Week 17
    ├── 14_model_evaluation/     # Week 18
    ├── 15_langchain_basics/     # Week 19
    ├── 16_predictive_service/   # Week 20
    ├── 17_capstone/             # Weeks 21-24
    └── 18_job_prep/             # Weeks 25-26
```

## Common Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Docker
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f [service_name]

# Check running containers
docker compose ps
```

### Airflow
```bash
# Access UI
http://localhost:8080
# User: airflow, Password: airflow

# Check DAGs
docker compose exec airflow-webserver airflow dags list
```

### FastAPI
```bash
# Run locally
uvicorn app.main:app --reload

# Access docs
http://localhost:8000/docs
```

## File Sizes to Expect

Generated data files (ignored by git):
- `housing_data.csv`: ~35 KB
- `large_sales.csv`: ~247 MB
- `sales_data.csv`: ~35 KB
- Model files (`.joblib`): ~1-5 MB
- Database files (`.db`): ~10-100 MB

## Git Workflow

### Initial Setup
```bash
cd /home/bidyut/MyWorkspace/AI-ML
git init
git add .
git commit -m "Initial commit: Complete 6-month Data Engineering curriculum"
```

### What Gets Committed
✅ All Python source files (`.py`)
✅ All documentation (`.md`)
✅ Configuration files (`requirements.txt`, `docker-compose.yml`)
✅ Dockerfiles
✅ Project structure

### What Gets Ignored
❌ Virtual environments (`venv/`)
❌ Generated data files (`.csv`, `.json`, `.parquet`)
❌ Model files (`.joblib`, `.pkl`)
❌ Database files (`.db`, `.sqlite`)
❌ Logs and temporary files
❌ Python cache (`__pycache__/`)

## Troubleshooting

### Docker Issues
```bash
# Clean up everything
docker system prune -a --volumes

# Restart Docker Desktop (Windows)
# Or restart Docker daemon (Linux)
```

### Port Conflicts
- Airflow: 8080
- FastAPI: 8000
- Postgres (Warehouse): 5434
- Postgres (Airflow): 5432

If port is in use:
```bash
# Find process using port
lsof -i :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# Kill process or change port in docker-compose.yml
```

### Memory Issues
If Docker runs out of memory:
1. Close other applications
2. Increase Docker memory limit (Docker Desktop settings)
3. Run one project at a time
4. Use `docker compose down` when done

## Learning Tips

1. **Follow the order**: Start with Week 1, progress sequentially
2. **Read before running**: Review README.md in each project first
3. **Run the code**: Don't just read, execute and observe
4. **Do the homework**: Challenges reinforce learning
5. **Take notes**: Document what you learn
6. **Build on previous weeks**: Each project uses skills from earlier weeks

## Resume & Interview Prep

### Key Projects to Highlight
1. **Capstone** (Week 21-24): Full end-to-end platform
2. **Warehouse Builder** (Week 8): ETL and data modeling
3. **Predictive Service** (Week 20): ML deployment

### Interview Focus Areas
- SQL queries (practice on paper)
- ETL concepts (explain your pipelines)
- System design (draw diagrams)
- Behavioral (use STAR method)

## Resources

### Documentation
- `projects/18_job_prep/RESUME_GUIDE.md`
- `projects/18_job_prep/INTERVIEW_QUESTIONS.md`
- Each project's `README.md`

### External Learning
- PostgreSQL docs: https://www.postgresql.org/docs/
- Airflow docs: https://airflow.apache.org/docs/
- FastAPI docs: https://fastapi.tiangolo.com/
- Scikit-learn docs: https://scikit-learn.org/

## Next Steps

1. ✅ Curriculum complete
2. ⏭️ Start learning: `cd projects/00_setup_and_refresher`
3. ⏭️ Commit to git
4. ⏭️ Begin Week 1

Good luck on your Data Engineering journey! 🚀
