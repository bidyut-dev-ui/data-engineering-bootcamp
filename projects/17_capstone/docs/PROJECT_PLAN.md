# Capstone Project: End-to-End Data Engineering & ML Platform

## Project Overview
Build a complete data platform that ingests real-time data, processes it with Airflow, stores it in a warehouse, trains ML models, and serves predictions via API.

## System Architecture

```
┌─────────────┐
│ Data Source │ (Simulated API)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Airflow   │ (Orchestration)
│   - Extract │
│   - Clean   │
│   - Load    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Postgres   │ (Data Warehouse)
│ Star Schema │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌──────────┐   ┌──────────┐
│ ML Model │   │ FastAPI  │
│ Training │   │ Analytics│
└──────────┘   └──────────┘
```

## Business Case
**Company**: E-commerce platform
**Problem**: Need to predict customer churn and provide real-time analytics
**Solution**: Automated pipeline that:
1. Ingests customer activity data daily
2. Stores in a queryable warehouse
3. Trains churn prediction model weekly
4. Serves predictions and analytics via API

## Technical Requirements

### Week 21: Planning & Architecture
- [ ] Define data schema
- [ ] Design star schema for warehouse
- [ ] Plan Airflow DAGs
- [ ] Define API endpoints
- [ ] Create project structure

### Week 22: Data Pipeline (Airflow)
- [ ] Create data generator (simulated API)
- [ ] Build extraction DAG
- [ ] Build transformation DAG
- [ ] Build loading DAG
- [ ] Add error handling and monitoring

### Week 23: ML & API
- [ ] Train churn prediction model
- [ ] Create model serving API
- [ ] Add analytics endpoints
- [ ] Integrate with warehouse

### Week 24: Integration & Polish
- [ ] Docker Compose for entire stack
- [ ] Add monitoring and logging
- [ ] Create documentation
- [ ] Performance testing

## Deliverables

1. **Working System**: All components running via `docker compose up`
2. **Documentation**: README with architecture diagrams
3. **Demo Script**: Automated demo showing end-to-end flow
4. **Presentation**: 5-minute walkthrough video (optional)

## Success Criteria
- ✅ Data flows from source → warehouse → API
- ✅ Airflow DAGs run successfully
- ✅ ML model achieves >80% accuracy
- ✅ API responds in <500ms
- ✅ System runs on 8GB RAM
- ✅ All components containerized
