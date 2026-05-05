# Project 21.6: Data Lineage & Metadata Management

## Problem Statement
In a complex data platform, a single column change can break 10 different dashboards. A Team Lead needs to know: "If I change `user_id` to `customer_id`, what will break?"

**The Goal:** Understand **Data Lineage** (the map of data flow) and tools like **OpenLineage**.

## 1. Data Lineage Concepts (The Solution)
Lineage is the metadata that tracks where data comes from and where it goes.

### Types of Lineage:
1.  **Table-level:** "Table A feeds Table B".
2.  **Column-level:** "The `revenue` column in Table B is calculated from `amount * rate` in Table A".

## 2. Implementing Lineage with OpenLineage
OpenLineage is an open standard for metadata collection. Airflow has built-in support for it.

### Example: Airflow Lineage Configuration
```python
# In your airflow.cfg or environment
AIRFLOW__LINEAGE__BACKEND = "openlineage.lineage_backend.OpenLineageBackend"
OPENLINEAGE_URL = "http://marquez:5000" # Marquez is a popular lineage server
```

### Manual Lineage (Code Level)
If you aren't using a tool, you should document your lineage in your dbt models or code.
```sql
-- dbt model: marts/fct_revenue.sql
-- Lineage: 
-- Source: raw.sales
-- Source: staging.exchange_rates
SELECT 
    s.id,
    s.amount * e.rate as revenue
FROM {{ ref('stg_sales') }} s
JOIN {{ ref('stg_exchange_rates') }} e ON s.currency = e.currency
```

## 3. Metadata Management
**Problem:** Business users don't know what `usr_cat_id_01` means.

**Solution:** Use a Data Catalog (DataHub, Amundsen) to map technical names to business definitions.
- **Technical Name:** `usr_cat_id_01`
- **Business Name:** `Primary Customer Category`
- **Owner:** `Growth Team`

## Exercise
**Problem:** You are asked to delete a "deprecated" table. How do you ensure it's safe?

**Solution:**
1.  Check the **Downstream Lineage**. 
2.  If any active DAGs or BI Dashboards (Tableau, Looker) depend on it, you must migrate them first.
3.  Use "Delete with Confidence" - Rename the table to `deprecated_table_name` for 7 days. If no one screams, delete it.
