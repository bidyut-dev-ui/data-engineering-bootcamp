# Project 21.5: Incident Response & On-Call Playbooks

## Problem Statement
A Data Engineering Team Lead is the "First Responder" when a pipeline fails at 3 AM. Without a playbook, the team wastes time, makes mistakes, and violates SLAs (Service Level Agreements).

**The Goal:** Create a standardized Incident Response Playbook and understand the "Post-Mortem" process.

## 1. The Incident Response Playbook (The Solution)
Save this as a template for your team.

### Step 1: Detect & Triage
- **Alert:** PagerDuty/Slack alert for "Airflow DAG: `daily_revenue_agg` Failed".
- **Action:** Acknowledge the alert. Check if it's a "Transient" (network blip) or "Structural" (schema change) error.

### Step 2: Communicate
- **Action:** Post in the `#incidents` channel. 
- **Message:** "Investigating failure in `daily_revenue_agg`. Impact: Finance dashboards will be stale. ETA: 1 hour."

### Step 3: Mitigate
- **Action:** If it's a structural error, pause the DAG to prevent further corruption. If it's a memory issue, increase the Spark executor memory and retry.

### Step 4: Resolve
- **Action:** Fix the root cause (e.g., update the SQL query). Rerun the failed tasks. Verify data quality.

### Step 5: Post-Mortem
- **Action:** Document the incident. Why did it happen? How do we prevent it?

## 2. Example Playbook: "Upstream Schema Change"
**Problem:** The `users` API added a new field and renamed an old one, breaking your ingestion DAG.

**Solution (The Playbook):**
1.  **Immediate Fix:** Add a fallback value in your Pydantic model for the missing field.
2.  **Long-term Fix:** Implement a **Data Contract** (Task 1.4) that alerts you *before* the API change reaches production.

## 3. Post-Mortem Template
| Section | Details |
| :--- | :--- |
| **Summary** | Brief description of what happened. |
| **Impact** | Which users/systems were affected and for how long? |
| **Root Cause** | The technical reason for the failure. |
| **Resolution** | The steps taken to fix it. |
| **Action Items** | What will we change to ensure this never happens again? |

## Exercise
**Problem:** A critical data table was accidentally deleted by a Junior Engineer.

**Solution:**
1.  **Restore from Backup:** Use the Terraform-managed RDS Snapshots (Task 2.5) to restore to the last known good state.
2.  **Preventive Action:** Implement **RBAC** (Task 2.4) so Junior Engineers do not have `DROP TABLE` permissions in the `production` schema.
