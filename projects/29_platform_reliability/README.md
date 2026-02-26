# Week 29: Platform Reliability & Incident Response

**Tag:** `#role-datacompany-senior`, `#skill-reliability`

## Overview
"Bias toward reliability over cleverness." This module shifts the focus from building data pipelines to operating them in a production environment where trust is foundational. If data breaks, trust breaks.

## Learning Objectives
- Understanding SLAs, SLOs, and Error Budgets
- Implementing Data Freshness and Data Quality checks (Great Expectations)
- Configuring Airflow to send Slack/Email alerts on task failures
- Writing effective Incident Runbooks
- End-to-end debugging of production failures

## Project Instructions
In this module, you will intentionally introduce a silent failure into your Wealth Management Data Platform pipeline (e.g., a schema change that drops records without crashing). You will then build the monitoring and alerting necessary to detect this failure and write a runbook detailing how a team should respond to it.

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Run the Data Quality Checks
We utilize the `Great Expectations` library to programmatically define SLOs (Service Level Objectives) for our data ingestion. Run the script to see what happens when "good" versus "incident" data flows through the system.
```bash
python 01_data_quality_checks.py
```

### 3. Study the Incident Runbook
Open `02_incident_runbook.md`. As a Senior Data Engineer, half your job is writing code; the other half is owning that code when it breaks in production. Read through this runbook to understand how enterprise teams triage and recover from data incidents under pressure.
