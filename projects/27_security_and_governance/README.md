# Week 27: Security, Authentication, & Governance

**Tag:** `#role-datacompany-senior`, `#skill-security`

## Overview
Data Company's Senior Data Engineer role sits at the intersection of data engineering, platform reliability, and data security. In a highly regulated environment (SOC, SEBI, ISO), securing financial data is paramount.

## Learning Objectives
- Implementing robust Authentication (JWT/API Keys) and Authorization (Role-Based Access Control)
- Secrets Management (managing credentials outside of source code)
- PII Masking & Data Scrubbing
- Encryption at Rest and in Transit (using Python `cryptography`)
- Basic Data Lineage concepts (auditing where data comes from)

## Project Instructions
You will take the FastAPI application built in previous weeks and secure it. You will implement middleware that intercepts requests to redact sensitive PII (like account numbers or balances) before logging, and store user credentials using bcrypt hashing.

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Password Hashing (Encryption at Rest)
Test out the bcrypt implementation to see how passwords should be safely processed before hitting a database:
```bash
python 02_hashing_basics.py
```

### 3. PII Masking Middleware (Encryption in Transit / Logging)
Run the secure FastAPI server:
```bash
uvicorn main:app --reload
```

In a separate terminal, try passing sensitive PII to the server:
```bash
curl -X GET "http://127.0.0.1:8000/user/lookup?ssn=123-45-6789&email=john.doe@datacompany.com"
```
Look at the logs running in your first terminal. You will see that the SSN and Email inside the URL log have been automatically masked with `***`!
