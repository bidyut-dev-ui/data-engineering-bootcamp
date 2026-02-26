# INCIDENT RUNBOOK: Daily ETL Wealth Management Pipeline Failure

## 1. Description
This runbook covers the scenario where the daily Airflow batch ETL pipeline (which ingests trading data into the Data Warehouse) fails.
**Severity**: High (Tier 1) - If data is not fresh by 8:00 AM EST, trading models will make decisions on stale data.

## 2. Alerts & Symptoms
- **Slack Alert**: `#alerts-data-eng` receives: `[CRITICAL] DAG wealth_management_daily failed at Task: data_quality_check`
- **PagerDuty**: On-call engineer paged.
- **Dashboards**: Grafana "Data Freshness" pane turns red.

## 3. Immediate Actions (Triaging)
1. **Acknowledge the page** in PagerDuty to let the team know you are investigating.
2. **Post in Slack**: In the `#incidents-data` channel, post: `@here Investigating pipeline failure. Current status: Triage.`
3. **Check Airflow Logs**:
   - Navigate to the Airflow UI -> `wealth_management_daily` -> Failed Task -> Logs.
   - Look for specific Great Expectations errors (e.g., "Expectation failed: amount must be > 0").

## 4. Root Cause Verification
- **Was it bad source data?** 
  - If the source vendor sent corrupted CSVs, escalate to the Provider Engineering team. 
  - *Action*: Quarantine the bad file (move to `s3://quarantine-bucket/`) and attempt to re-run with yesterday's data if a fallback is permitted.
- **Was it an infrastructure failure?**
  - Did the database run out of memory (OOM)? Did Redpanda/LocalStack crash?
  - *Action*: Check Docker/Kubernetes stats. Restart the pod if it's a transient failure.

## 5. Remediation & Recovery
1. **Fix the data/code issue**.
2. **Clear the failed Airflow task**. This triggers a retry (idempotent design means it's safe to re-run).
3. **Verify Data Correctness**. Query the target Postgres table to ensure no duplicate records were inserted during the partial failure.
```sql
SELECT transaction_id, COUNT(*) FROM transactions GROUP BY transaction_id HAVING COUNT(*) > 1;
```

## 6. Post-Incident Review (PIR)
Once the pipeline is green and data is serving to stakeholders:
1. Document the root cause in the JIRA incident ticket.
2. Determine what went wrong and how to automate a fix so this specific failure never pages an engineer again. (Bias toward reliability over cleverness).
