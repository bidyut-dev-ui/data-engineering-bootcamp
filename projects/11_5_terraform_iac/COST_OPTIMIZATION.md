# Cost Optimization for Data Engineers (Team Lead Guide)

## 1. Storage Tiers
**Strategy:** Move old data to cheaper storage.
- **AWS S3 Standard:** For active data.
- **S3 Intelligent-Tiering:** Automatically moves data based on access.
- **S3 Glacier Deep Archive:** For audit logs/backups that are rarely accessed ($0.00099 per GB).

## 2. Compute Scaling (Spark/Airflow)
**Strategy:** Only pay for what you use.
- **Spot Instances:** Use EC2 Spot for Spark clusters. Save up to 90% vs on-demand.
- **Auto-scaling:** Configure Airflow Celery workers to scale down to zero at night if no DAGs are running.

## 3. Data Transfer Costs
**Strategy:** Keep data in the same region.
- Avoid transferring large datasets between AWS regions or out of the cloud to your local machine unnecessarily.
- Use **VPC Endpoints** for S3 to avoid NAT Gateway charges.

## 4. Resource Tagging
**Strategy:** Visibility is the first step to optimization.
- Enforce a tagging policy via Terraform: `Project`, `Owner`, `Environment`, `CostCenter`.
- Use AWS Cost Explorer to find which specific team's pipeline is the most expensive.

## 5. Query Optimization
**Strategy:** Process less data.
- **Partitioning:** Ensure Athena/Redshift Spectrum queries only read relevant partitions.
- **Columnar Formats:** Use Parquet/ORC to reduce data scanned (and thus cost).
