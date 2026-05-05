# Project 11.5: Infrastructure as Code (IaC) & Cost Optimization

## Overview
As a Data Engineering Team Lead, you don't just write code; you provision the infrastructure it runs on. **Terraform** is the industry standard for managing cloud resources (S3, RDS, EC2, Lambda) in a repeatable, version-controlled way.

This module also covers **Cost Optimization**, ensuring your pipelines don't waste the company's money.

## Learning Objectives
- Master **Terraform Basics**: Providers, Resources, Variables, and State.
- Understand **Modules**: Creating reusable infrastructure components.
- Learn **Cost Optimization Strategies**: Spot instances, storage tiers, and compute scaling.
- Practice **LocalStack Integration**: Test your Terraform locally without an AWS bill.

## Files
- `terraform/main.tf`: Core infrastructure definition.
- `terraform/variables.tf`: Configuration variables.
- `terraform/outputs.tf`: Exported values (e.g., DB endpoint).
- `COST_OPTIMIZATION.md`: Best practices for reducing cloud DE costs.
- `GOTCHAS_BEST_PRACTICES.md`: Terraform pitfalls (State locks, manual changes).

## Exercise
1. Define an S3 bucket for data lake storage.
2. Define a Postgres RDS instance for a data warehouse.
3. Add tags to all resources for cost tracking.
