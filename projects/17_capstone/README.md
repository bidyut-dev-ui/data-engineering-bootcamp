# Weeks 21-24: Capstone Project

**Goal**: Build a complete end-to-end data platform integrating all skills learned: ETL, warehousing, ML, and API development.

## Project: Customer Analytics & Churn Prediction Platform

### Business Context
An e-commerce company needs to:
1. Track customer activity in real-time
2. Store data for analytics
3. Predict which customers are likely to churn
4. Provide insights via API for dashboards

### System Components
1. **Data Generator**: Simulates customer activity API
2. **Airflow**: Orchestrates daily ETL pipeline
3. **Warehouse**: Postgres with star schema
4. **ML Model**: Churn prediction (RandomForest)
5. **API**: FastAPI serving predictions and analytics

## Structure
```
17_capstone/
├── dags/                   # Airflow DAGs
│   └── etl_pipeline.py
├── api/                    # FastAPI application
│   ├── main.py
│   └── Dockerfile
├── data/                   # Data storage
│   ├── raw/               # Simulated API responses
│   └── processed/         # Cleaned data
├── docs/                   # Documentation
│   └── PROJECT_PLAN.md
├── docker-compose.yml      # Full stack
└── generate_data.py        # Data generator
```

## Instructions

### Week 21: Setup & Planning

#### 1. Review Architecture
Read `docs/PROJECT_PLAN.md` to understand the system design.

#### 2. Generate Sample Data
```bash
cd projects/17_capstone
source ../00_setup_and_refresher/venv/bin/activate
pip install pandas pyarrow
python generate_data.py
```

This creates 30 days of customer activity data.

### Week 22: Build ETL Pipeline

#### 3. Start Airflow
```bash
docker compose up -d airflow-webserver airflow-scheduler postgres
```

Wait 2 minutes, then visit `http://localhost:8080`

#### 4. Run ETL DAG
1. Enable `capstone_etl` DAG
2. Trigger manually
3. Check logs to verify data flow

### Week 23: ML & API

#### 5. Train Model
```bash
# Create training script
python train_churn_model.py
```

#### 6. Start API
```bash
docker compose up -d api warehouse
```

Visit `http://localhost:8000/docs`

### Week 24: Integration & Testing

#### 7. Full Stack Test
```bash
# Start everything
docker compose up -d

# Verify all services
docker compose ps

# Test end-to-end flow
./test_pipeline.sh
```

## Expected Outputs

### Data Flow
1. Raw JSON files → `data/raw/`
2. Airflow processes → `data/processed/`
3. Warehouse tables populated
4. ML model trained
5. API serves predictions

### API Endpoints
- `GET /health` - System health
- `GET /analytics/summary` - Daily metrics
- `POST /predict/churn` - Churn prediction
- `GET /customers/at-risk` - High-risk customers

## Homework / Extensions

### Extension 1: Real-Time Processing
Replace daily batch with streaming:
1. Use Apache Kafka for real-time ingestion
2. Update Airflow to process micro-batches
3. Add real-time dashboard

### Extension 2: Advanced ML
Improve the model:
1. Add feature engineering (RFM analysis)
2. Try XGBoost or LightGBM
3. Implement A/B testing for models

### Extension 3: Monitoring
Add observability:
1. Prometheus metrics
2. Grafana dashboards
3. Alert on pipeline failures

## Deliverables Checklist
- [ ] All services start with `docker compose up`
- [ ] ETL DAG runs successfully
- [ ] Warehouse contains data
- [ ] ML model achieves >75% accuracy
- [ ] API returns predictions
- [ ] Documentation complete
- [ ] Demo video recorded (optional)

## Presentation Tips
When showcasing this project:
1. **Start with the problem**: "Customers churning costs $X"
2. **Show the architecture**: Diagram on whiteboard
3. **Demo the flow**: Live or recorded
4. **Highlight decisions**: "I chose X because Y"
5. **Discuss trade-offs**: "In production, I would..."

## Expected Learning Outcomes
- ✅ Integrate multiple technologies
- ✅ Design end-to-end systems
- ✅ Make architectural decisions
- ✅ Handle real-world complexity
- ✅ Present technical work effectively
