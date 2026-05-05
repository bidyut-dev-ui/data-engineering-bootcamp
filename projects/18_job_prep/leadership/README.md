# Phase 3: Leadership Job Prep & Soft Skills

## Overview
A Data Engineering Team Lead is not just a senior developer. You are expected to design systems, mentor others, and manage stakeholders.

## 1. Data Architecture Strategy (The Solution)
**Problem:** A stakeholder asks you: "Should we build our new data lake using Snowflake, Databricks, or a custom S3 + Athena setup?"

**Solution (The Leadership Response):**
Don't just pick a tool. Explain the **Trade-offs**:
- **Snowflake:** Great for SQL-heavy teams, zero management, but can be expensive and has proprietary storage.
- **Databricks:** Best for Spark/ML heavy workloads and Lakehouse architecture, but requires more engineering effort to manage clusters.
- **S3 + Athena:** Most cost-effective and flexible, but requires manual partitioning, schema management, and is slower for complex joins.

**Recommendation:** "Since our team is 80% SQL analysts, I recommend **Snowflake** to reduce our 'Time to Insight', even if the storage costs are slightly higher."

## 2. Agile & Project Management
**Problem:** You have 3 critical tasks but only enough capacity for 1.
1.  Fixing a bug in a production dashboard.
2.  Building a new feature for the CEO.
3.  Migrating an old database to save $5,000/month.

**Solution (The Prioritization):**
1.  **Production Bug:** Priority 1. Protects the current business value.
2.  **CEO Feature:** Priority 2. Stakeholder management and future value.
3.  **Cost Migration:** Priority 3. Financial optimization, but can wait a week.

## 3. Mentorship & Team Growth
**Problem:** A Junior Engineer keeps making the same mistake in their Airflow DAGs.

**Solution:**
1.  **Don't just fix it for them.**
2.  **Code Review:** Leave a comment explaining *why* the approach is wrong (e.g., "This creates a bottleneck because...").
3.  **1-on-1:** Set up a 15-minute call to walk through the logic.
4.  **Documentation:** Ask the Junior to update the team's "Best Practices" wiki to reinforce their learning.

## Exercise: The Stakeholder Conflict
**Problem:** The Marketing Lead wants data refreshed every 1 minute. The Finance Lead says every 24 hours is enough. Your infra can only handle 15 minutes without cost spikes.

**Solution:**
- **Facilitate:** Bring both leads into a meeting.
- **Explain Costs:** Show that 1-minute refreshes will triple the cloud bill.
- **Negotiate:** Ask Marketing: "What decision do you make every minute that can't wait 15 minutes?"
- **Compromise:** Settle on **15-minute refreshes for Marketing** and **24-hour snapshots for Finance**.
