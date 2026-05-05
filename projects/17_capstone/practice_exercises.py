#!/usr/bin/env python3
"""
Practice Exercises for 17_capstone: Customer Analytics & Churn Prediction Platform

This file contains 10 hands-on exercises covering end-to-end data platform integration,
including ETL pipeline design, Airflow orchestration, data warehousing, ML model development,
API design, and system integration.

Each exercise is designed to reinforce concepts from the capstone project and prepare
you for real-world data engineering challenges.
"""

import json
import random
import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass


@dataclass
class CustomerData:
    """Sample customer data structure for exercises"""
    customer_id: str
    signup_date: str
    last_purchase_date: str
    total_purchases: int
    total_spent: float
    avg_order_value: float
    days_since_last_purchase: int
    churn_label: bool


def exercise_1_end_to_end_architecture() -> Dict[str, Any]:
    """
    Exercise 1: End-to-End Architecture Design
    
    Design the architecture for a customer analytics platform that:
    1. Ingests raw JSON customer data
    2. Processes it through an Airflow ETL pipeline
    3. Stores processed data in a data warehouse (star schema)
    4. Trains a churn prediction model
    5. Serves predictions via a REST API
    
    Return a dictionary with your architecture components and data flow.
    """
    print("=" * 60)
    print("EXERCISE 1: End-to-End Architecture Design")
    print("=" * 60)
    
    # Your task: Design the architecture
    architecture = {
        "data_sources": [
            "Raw JSON customer data files",
            "Transactional database exports",
            "Web analytics events"
        ],
        "ingestion_layer": [
            "Scheduled batch ingestion (Airflow)",
            "Data validation checks",
            "Schema validation"
        ],
        "processing_layer": [
            "ETL pipeline (Python/Pandas)",
            "Data cleaning and transformation",
            "Feature engineering"
        ],
        "storage_layer": [
            "Data warehouse (PostgreSQL)",
            "Star schema: fact_sales, dim_customers, dim_products, dim_time",
            "Aggregated tables for analytics"
        ],
        "ml_layer": [
            "Feature store",
            "Model training pipeline",
            "Model registry and versioning"
        ],
        "serving_layer": [
            "FastAPI REST API",
            "Real-time prediction endpoints",
            "Analytics dashboard endpoints"
        ],
        "monitoring_layer": [
            "Pipeline health monitoring",
            "Data quality checks",
            "Model performance monitoring"
        ]
    }
    
    # Data flow description
    data_flow = [
        "1. Raw JSON → Data validation → Staging area",
        "2. Staging → ETL processing → Data warehouse",
        "3. Warehouse → Feature engineering → ML training",
        "4. Trained model → Model registry → API serving",
        "5. API requests → Real-time predictions → Dashboard"
    ]
    
    return {
        "architecture_components": architecture,
        "data_flow": data_flow,
        "key_decisions": [
            "Use Airflow for orchestration due to complex dependencies",
            "Implement star schema for analytical query performance",
            "Use FastAPI for low-latency prediction serving",
            "Implement feature store for consistent training/serving"
        ]
    }


def exercise_2_airflow_dag_design() -> Dict[str, Any]:
    """
    Exercise 2: Airflow DAG Design for ETL Pipeline
    
    Design an Airflow DAG that:
    1. Extracts raw customer data from JSON files
    2. Transforms data (cleaning, feature engineering)
    3. Loads data into warehouse tables
    4. Triggers model retraining when data changes
    5. Sends alerts on pipeline failures
    
    Return the DAG structure with tasks and dependencies.
    """
    print("\n" + "=" * 60)
    print("EXERCISE 2: Airflow DAG Design")
    print("=" * 60)
    
    # DAG configuration
    dag_config = {
        "dag_id": "customer_analytics_etl",
        "schedule_interval": "@daily",
        "start_date": "2024-01-01",
        "catchup": False,
        "max_active_runs": 1
    }
    
    # Task definitions
    tasks = [
        {
            "task_id": "check_new_data",
            "operator": "FileSensor",
            "description": "Check for new raw data files",
            "params": {"filepath": "/data/raw/customers/", "timeout": 3600}
        },
        {
            "task_id": "validate_schema",
            "operator": "PythonOperator",
            "description": "Validate JSON schema and data quality",
            "params": {"python_callable": "validate_customer_data"}
        },
        {
            "task_id": "extract_transform",
            "operator": "PythonOperator",
            "description": "Extract and transform raw data",
            "params": {"python_callable": "extract_transform_customers"}
        },
        {
            "task_id": "load_dim_customers",
            "operator": "PythonOperator",
            "description": "Load dimension table: customers",
            "params": {"python_callable": "load_dimension_customers"}
        },
        {
            "task_id": "load_fact_sales",
            "operator": "PythonOperator",
            "description": "Load fact table: sales",
            "params": {"python_callable": "load_fact_sales"}
        },
        {
            "task_id": "update_aggregates",
            "operator": "PythonOperator",
            "description": "Update aggregated tables for dashboards",
            "params": {"python_callable": "update_aggregated_tables"}
        },
        {
            "task_id": "trigger_model_retraining",
            "operator": "TriggerDagRunOperator",
            "description": "Trigger model retraining DAG if data changed",
            "params": {"trigger_dag_id": "model_retraining"}
        },
        {
            "task_id": "send_success_notification",
            "operator": "SlackOperator",
            "description": "Send success notification",
            "params": {"message": "ETL pipeline completed successfully"}
        }
    ]
    
    # Task dependencies (edges in DAG)
    dependencies = [
        ("check_new_data", "validate_schema"),
        ("validate_schema", "extract_transform"),
        ("extract_transform", "load_dim_customers"),
        ("extract_transform", "load_fact_sales"),
        ("load_dim_customers", "update_aggregates"),
        ("load_fact_sales", "update_aggregates"),
        ("update_aggregates", "trigger_model_retraining"),
        ("trigger_model_retraining", "send_success_notification")
    ]
    
    # Error handling tasks
    error_tasks = [
        {
            "task_id": "handle_validation_error",
            "operator": "PythonOperator",
            "description": "Handle schema validation errors",
            "trigger_rule": "all_failed"
        },
        {
            "task_id": "send_failure_notification",
            "operator": "SlackOperator",
            "description": "Send failure notification",
            "trigger_rule": "all_failed"
        }
    ]
    
    return {
        "dag_configuration": dag_config,
        "tasks": tasks,
        "dependencies": dependencies,
        "error_handling": error_tasks,
        "parallel_tasks": [
            "load_dim_customers and load_fact_sales can run in parallel",
            "update_aggregates waits for both dimension and fact loads"
        ]
    }


def exercise_3_star_schema_design() -> Dict[str, Any]:
    """
    Exercise 3: Data Warehouse Star Schema Design
    
    Design a star schema for customer analytics with:
    1. Fact table: customer transactions/sales
    2. Dimension tables: customers, products, time, location
    3. Appropriate surrogate keys and foreign key relationships
    4. Slowly changing dimensions (Type 2) for customer attributes
    
    Return the schema design with table definitions.
    """
    print("\n" + "=" * 60)
    print("EXERCISE 3: Star Schema Design")
    print("=" * 60)
    
    # Fact table design
    fact_sales = {
        "table_name": "fact_sales",
        "description": "Transactional sales data",
        "granularity": "One row per transaction",
        "columns": [
            {"name": "sale_id", "type": "BIGINT", "constraint": "PRIMARY KEY"},
            {"name": "customer_key", "type": "INT", "constraint": "FOREIGN KEY REFERENCES dim_customers(customer_key)"},
            {"name": "product_key", "type": "INT", "constraint": "FOREIGN KEY REFERENCES dim_products(product_key)"},
            {"name": "time_key", "type": "INT", "constraint": "FOREIGN KEY REFERENCES dim_time(time_key)"},
            {"name": "location_key", "type": "INT", "constraint": "FOREIGN KEY REFERENCES dim_location(location_key)"},
            {"name": "quantity", "type": "INT", "description": "Number of units purchased"},
            {"name": "unit_price", "type": "DECIMAL(10,2)", "description": "Price per unit"},
            {"name": "total_amount", "type": "DECIMAL(10,2)", "description": "quantity * unit_price"},
            {"name": "discount_amount", "type": "DECIMAL(10,2)", "description": "Discount applied"},
            {"name": "net_amount", "type": "DECIMAL(10,2)", "description": "total_amount - discount_amount"},
            {"name": "payment_method", "type": "VARCHAR(50)", "description": "Credit card, PayPal, etc."},
            {"name": "transaction_timestamp", "type": "TIMESTAMP", "description": "Exact time of transaction"}
        ],
        "indexes": [
            "CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key)",
            "CREATE INDEX idx_fact_sales_time ON fact_sales(time_key)",
            "CREATE INDEX idx_fact_sales_product ON fact_sales(product_key)"
        ]
    }
    
    # Dimension table: Customers (Type 2 SCD)
    dim_customers = {
        "table_name": "dim_customers",
        "description": "Customer dimension with Type 2 slowly changing dimensions",
        "columns": [
            {"name": "customer_key", "type": "INT", "constraint": "PRIMARY KEY"},
            {"name": "customer_id", "type": "VARCHAR(50)", "description": "Business/natural key"},
            {"name": "customer_name", "type": "VARCHAR(100)", "description": "Full name"},
            {"name": "email", "type": "VARCHAR(100)", "description": "Email address"},
            {"name": "signup_date", "type": "DATE", "description": "Date customer signed up"},
            {"name": "customer_tier", "type": "VARCHAR(20)", "description": "Basic, Premium, Enterprise"},
            {"name": "region", "type": "VARCHAR(50)", "description": "Geographic region"},
            {"name": "lifetime_value", "type": "DECIMAL(12,2)", "description": "Total lifetime spend"},
            {"name": "current_status", "type": "VARCHAR(20)", "description": "Active, Inactive, Churned"},
            # SCD Type 2 columns
            {"name": "row_start_date", "type": "DATE", "description": "When this version became active"},
            {"name": "row_end_date", "type": "DATE", "description": "When this version expired (NULL for current)"},
            {"name": "is_current", "type": "BOOLEAN", "description": "TRUE for current version"}
        ],
        "scd_type": 2,
        "business_key": "customer_id"
    }
    
    # Dimension table: Time
    dim_time = {
        "table_name": "dim_time",
        "description": "Time dimension with various granularities",
        "columns": [
            {"name": "time_key", "type": "INT", "constraint": "PRIMARY KEY"},
            {"name": "date", "type": "DATE", "description": "Calendar date"},
            {"name": "day_of_week", "type": "INT", "description": "1=Sunday, 7=Saturday"},
            {"name": "day_name", "type": "VARCHAR(10)", "description": "Monday, Tuesday, etc."},
            {"name": "month", "type": "INT", "description": "1-12"},
            {"name": "month_name", "type": "VARCHAR(10)", "description": "January, February, etc."},
            {"name": "quarter", "type": "INT", "description": "1-4"},
            {"name": "year", "type": "INT", "description": "e.g., 2024"},
            {"name": "is_weekend", "type": "BOOLEAN", "description": "TRUE for Saturday/Sunday"},
            {"name": "is_holiday", "type": "BOOLEAN", "description": "TRUE for holidays"}
        ]
    }
    
    # Dimension table: Products
    dim_products = {
        "table_name": "dim_products",
        "description": "Product catalog dimension",
        "columns": [
            {"name": "product_key", "type": "INT", "constraint": "PRIMARY KEY"},
            {"name": "product_id", "type": "VARCHAR(50)", "description": "Business/natural key"},
            {"name": "product_name", "type": "VARCHAR(100)", "description": "Product name"},
            {"name": "category", "type": "VARCHAR(50)", "description": "Product category"},
            {"name": "subcategory", "type": "VARCHAR(50)", "description": "Product subcategory"},
            {"name": "unit_cost", "type": "DECIMAL(10,2)", "description": "Cost to produce"},
            {"name": "retail_price", "type": "DECIMAL(10,2)", "description": "Selling price"},
            {"name": "supplier", "type": "VARCHAR(100)", "description": "Supplier name"},
            {"name": "is_active", "type": "BOOLEAN", "description": "TRUE if product is currently sold"}
        ]
    }
    
    # Sample queries that would benefit from star schema
    sample_queries = [
        "SELECT c.customer_tier, t.month_name, SUM(f.net_amount) as total_sales",
        "FROM fact_sales f",
        "JOIN dim_customers c ON f.customer_key = c.customer_key",
        "JOIN dim_time t ON f.time_key = t.time_key",
        "WHERE t.year = 2024 AND c.current_status = 'Active'",
        "GROUP BY c.customer_tier, t.month_name",
        "ORDER BY total_sales DESC"
    ]
    
    return {
        "fact_tables": [fact_sales],
        "dimension_tables": [dim_customers, dim_time, dim_products],
        "relationships": [
            "fact_sales.customer_key → dim_customers.customer_key",
            "fact_sales.product_key → dim_products.product_key",
            "fact_sales.time_key → dim_time.time_key"
        ],
        "sample_query": "\n".join(sample_queries),
        "benefits": [
            "Simplified queries for business users",
            "Improved query performance with star joins",
            "Consistent reporting across organization",
            "Easy to add new dimensions"
        ]
    }


def exercise_4_ml_feature_engineering() -> Dict[str, Any]:
    """
    Exercise 4: Feature Engineering for Churn Prediction
    
    Create feature engineering logic for churn prediction:
    1. Recency, Frequency, Monetary (RFM) features
    2. Behavioral features (purchase patterns, engagement metrics)
    3. Temporal features (seasonality, trends)
    4. Derived features (ratios, percentages, rates)
    
    Return the feature definitions and calculation logic.
    """
    print("\n" + "=" * 60)
    print("EXERCISE 4: Feature Engineering for Churn Prediction")
    print("=" * 60)
    
    # RFM Features
    rfm_features = {
        "recency": {
            "description": "Days since last purchase",
            "calculation": "CURRENT_DATE - MAX(purchase_date)",
            "importance": "High - customers who haven't purchased recently are more likely to churn",
            "buckets": ["0-30 days", "31-90 days", "91-180 days", "181+ days"]
        },
        "frequency": {
            "description": "Number of purchases in last 90 days",
            "calculation": "COUNT(purchases) WHERE purchase_date >= CURRENT_DATE - 90",
            "importance": "High - frequent purchasers are less likely to churn",
            "normalization": "Divide by customer tenure in days"
        },
        "monetary": {
            "description": "Total spend in last 90 days",
            "calculation": "SUM(total_amount) WHERE purchase_date >= CURRENT_DATE - 90",
            "importance": "Medium - high spenders may be at risk if they stop",
            "derived": "Average order value = monetary / frequency"
        }
    }
    
    # Behavioral Features
    behavioral_features = {
        "purchase_consistency": {
            "description": "Standard deviation of days between purchases",
            "calculation": "STDDEV(days_between_purchases)",
            "interpretation": "Lower values indicate regular purchasing habits"
        },
        "category_preference": {
            "description": "Percentage of purchases in top category",
            "calculation": "MAX(category_count) / SUM(category_count)",
            "interpretation": "Higher values indicate strong category preference"
        },
        "price_sensitivity": {
            "description": "Average discount percentage used",
            "calculation": "AVG(discount_amount / total_amount)",
            "interpretation": "Higher values indicate price-sensitive customers"
        },
        "engagement_score": {
            "description": "Composite score of website visits, email opens, app usage",
            "calculation": "0.4 * website_visits + 0.3 * email_opens + 0.3 * app_sessions",
            "normalization": "Scale to 0-100 range"
        }
    }
    
    # Temporal Features
    temporal_features = {
        "tenure_days": {
            "description": "Days since customer signup",
            "calculation": "CURRENT_DATE - signup_date",
            "buckets": ["New (<30 days)", "Established (30-365 days)", "Long-term (>365 days)"]
        },
        "seasonal_purchase_ratio": {
            "description": "Ratio of holiday season purchases to regular",
            "calculation": "holiday_purchases / non_holiday_purchases",
            "interpretation": "Higher values indicate seasonal shoppers"
        },
        "purchase_day_of_week": {
            "description": "Most common day of week for purchases",
            "calculation": "MODE(DAYOFWEEK(purchase_date))",
            "encoding": "One-hot encoding for each day"
        },
        "recent_trend": {
            "description": "Slope of purchase frequency over last 90 days",
            "calculation": "Linear regression slope of purchase_count by week",
            "interpretation": "Negative slope indicates decreasing engagement"
        }
    }
    
    # Derived Features
    derived_features = {
        "rfm_score": {
            "description": "Composite RFM score (0-100)",
            "calculation": "0.4 * recency_score + 0.35 * frequency_score + 0.25 * monetary_score",
            "weights": "Recency most important for churn prediction"
        },
        "churn_risk_index": {
            "description": "Weighted combination of risk factors",
            "calculation": """
                (recency_weight * recency_score) +
                (engagement_weight * (1 - engagement_normalized)) +
                (complaint_weight * complaint_count) +
                (support_weight * support_tickets)
            """,
            "normalization": "Scale to 0-1 probability"
        },
        "customer_lifetime_value": {
            "description": "Predicted future value of customer",
            "calculation": "AVG(monthly_spend) * predicted_months_remaining",
            "prediction": "Use survival analysis for months_remaining"
        }
    }
    
    # Feature engineering pipeline steps
    pipeline_steps = [
        "1. Raw data extraction from data warehouse",
        "2. Calculate basic RFM metrics",
        "3. Compute behavioral patterns (rolling windows)",
        "4. Encode categorical variables (one-hot, target encoding)",
        "5. Create interaction features (e.g., tenure * frequency)",
        "6. Normalize/scale numerical features",
        "7. Handle missing values (imputation)",
        "8. Feature selection (correlation analysis, feature importance)"
    ]
    
    return {
        "rfm_features": rfm_features,
        "behavioral_features": behavioral_features,
        "temporal_features": temporal_features,
        "derived_features": derived_features,
        "feature_engineering_pipeline": pipeline_steps,
        "total_features_count": 25,
        "feature_selection_criteria": [
            "Remove features with >90% missing values",
            "Remove constant or quasi-constant features",
            "Remove highly correlated features (correlation > 0.95)",
            "Use feature importance from tree-based models"
        ]
    }


def exercise_5_api_design_for_analytics() -> Dict[str, Any]:
    """
    Exercise 5: API Design for Analytics and Predictions
    
    Design a FastAPI service that provides:
    1. Real-time churn predictions
    2. Customer analytics endpoints
    3. Batch prediction capabilities
    4. Model information and versioning
    5. Health checks and monitoring
    
    Return the API specification with endpoints and request/response models.
    """
    print("\n" + "=" * 60)
    print("EXERCISE 5: API Design for Analytics and Predictions")
    print("=" * 60)
    
    # API Overview
    api_overview = {
        "service_name": "Customer Analytics & Churn Prediction API",
        "framework": "FastAPI",
        "authentication": "JWT tokens with role-based access",
        "rate_limiting": "100 requests/minute per API key",
        "documentation": "Auto-generated OpenAPI/Swagger UI",
        "versioning": "URL path versioning (/v1/, /v2/)"
    }
    
    # Endpoint Definitions
    endpoints = [
        {
            "path": "/health",
            "method": "GET",
            "description": "Service health check",
            "response": {
                "status": "healthy/degraded/unhealthy",
                "timestamp": "ISO 8601 timestamp",
                "version": "API version",
                "dependencies": {
                    "database": "connected",
                    "model_server": "ready",
                    "cache": "available"
                }
            }
        },
        {
            "path": "/predict/churn",
            "method": "POST",
            "description": "Real-time churn prediction for a single customer",
            "request_body": {
                "customer_id": "string",
                "features": {
                    "recency_days": 45,
                    "purchase_frequency_90d": 3,
                    "total_spend_90d": 450.50,
                    "avg_order_value": 150.17,
                    "days_since_last_login": 7,
                    "support_tickets_30d": 2,
                    "email_engagement_score": 0.75
                },
                "model_version": "optional, defaults to latest"
            },
            "response": {
                "customer_id": "string",
                "churn_probability": 0.67,
                "prediction": "churn/no_churn",
                "confidence": 0.89,
                "top_factors": [
                    {"feature": "recency_days", "importance": 0.35},
                    {"feature": "days_since_last_login", "importance": 0.28}
                ],
                "model_version": "v1.2.0",
                "inference_time_ms": 12.5
            }
        },
        {
            "path": "/predict/churn/batch",
            "method": "POST",
            "description": "Batch churn prediction for multiple customers",
            "request_body": {
                "customers": [
                    {"customer_id": "cust_001", "features": {...}},
                    {"customer_id": "cust_002", "features": {...}}
                ],
                "async": "boolean, process asynchronously"
            },
            "response": {
                "job_id": "uuid for async processing",
                "status": "processing/complete/failed",
                "results": [
                    {"customer_id": "cust_001", "churn_probability": 0.67},
                    {"customer_id": "cust_002", "churn_probability": 0.23}
                ],
                "summary": {
                    "total_customers": 100,
                    "high_risk_count": 15,
                    "avg_churn_probability": 0.42
                }
            }
        },
        {
            "path": "/analytics/summary",
            "method": "GET",
            "description": "High-level customer analytics summary",
            "query_params": {
                "time_period": "last_7_days/last_30_days/last_90_days",
                "segment": "all/premium/enterprise"
            },
            "response": {
                "time_period": "last_30_days",
                "total_customers": 12500,
                "active_customers": 9800,
                "churned_customers": 350,
                "churn_rate": 0.028,
                "avg_customer_lifetime_value": 1250.50,
                "top_risk_segments": [
                    {"segment": "premium_90d_inactive", "risk_score": 0.78},
                    {"segment": "high_value_low_engagement", "risk_score": 0.65}
                ],
                "revenue_at_risk": 437500.00
            }
        },
        {
            "path": "/customers/{customer_id}/analytics",
            "method": "GET",
            "description": "Detailed analytics for a specific customer",
            "response": {
                "customer_id": "string",
                "demographics": {...},
                "purchase_history": {...},
                "engagement_metrics": {...},
                "churn_risk_timeline": [
                    {"date": "2024-01-01", "risk_score": 0.25},
                    {"date": "2024-02-01", "risk_score": 0.42}
                ],
                "recommendations": [
                    "Send re-engagement email",
                    "Offer loyalty discount",
                    "Schedule check-in call"
                ]
            }
        },
        {
            "path": "/model/info",
            "method": "GET",
            "description": "Information about deployed ML models",
            "response": {
                "active_model": {
                    "version": "v1.2.0",
                    "algorithm": "XGBoost",
                    "training_date": "2024-03-15",
                    "performance": {
                        "accuracy": 0.89,
                        "precision": 0.85,
                        "recall": 0.82,
                        "auc": 0.91
                    },
                    "feature_count": 25
                },
                "available_models": [
                    {"version": "v1.1.0", "status": "archived"},
                    {"version": "v1.2.0", "status": "active"},
                    {"version": "v1.3.0-rc1", "status": "testing"}
                ]
            }
        }
    ]
    
    # Error Responses
    error_responses = {
        "400": "Bad Request - Invalid input parameters",
        "401": "Unauthorized - Missing or invalid authentication",
        "403": "Forbidden - Insufficient permissions",
        "404": "Not Found - Resource not found",
        "429": "Too Many Requests - Rate limit exceeded",
        "500": "Internal Server Error - Unexpected error",
        "503": "Service Unavailable - Dependency failure"
    }
    
    # Performance Requirements
    performance = {
        "p95_latency": {
            "/predict/churn": "50ms",
            "/predict/churn/batch": "500ms per 100 customers",
            "/analytics/summary": "100ms",
            "/customers/{id}/analytics": "200ms"
        },
        "throughput": "1000 requests/second",
        "availability": "99.9% uptime",
        "concurrent_users": "1000"
    }
    
    return {
        "api_overview": api_overview,
        "endpoints": endpoints,
        "error_responses": error_responses,
        "performance_requirements": performance,
        "authentication_flow": [
            "1. Client obtains JWT token from auth service",
            "2. Token included in Authorization header",
            "3. API validates token and extracts user roles",
            "4. Role-based access control applied",
            "5. Audit logging of all requests"
        ]
    }


def exercise_6_docker_containerization() -> Dict[str, Any]:
    """
    Exercise 6: Docker Containerization of Full Stack
    
    Design Docker containers for the complete platform:
    1. Multi-container Docker Compose setup
    2. Service definitions for each component
    3. Networking and volume configuration
    4. Environment variables and secrets management
    5. Health checks and dependency ordering
    
    Return the Docker Compose configuration.
    """
    print("\n" + "=" * 60)
    print("EXERCISE 6: Docker Containerization")
    print("=" * 60)
    
    # Docker Compose version and services
    docker_compose = {
        "version": "3.8",
        "services": {
            "postgres": {
                "image": "postgres:15-alpine",
                "container_name": "customer_warehouse",
                "environment": [
                    "POSTGRES_DB=customer_analytics",
                    "POSTGRES_USER=admin",
                    "POSTGRES_PASSWORD_FILE=/run/secrets/db_password"
                ],
                "secrets": ["db_password"],
                "volumes": [
                    "postgres_data:/var/lib/postgresql/data",
                    "./init.sql:/docker-entrypoint-initdb.d/init.sql"
                ],
                "ports": ["5432:5432"],
                "healthcheck": {
                    "test": ["CMD-SHELL", "pg_isready -U admin"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 5
                },
                "restart": "unless-stopped"
            },
            "airflow": {
                "image": "apache/airflow:2.7.3",
                "container_name": "airflow_scheduler",
                "depends_on": {
                    "postgres": {"condition": "service_healthy"}
                },
                "environment": [
                    "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
                    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://admin:${DB_PASSWORD}@postgres/customer_analytics",
                    "AIRFLOW__CORE__LOAD_EXAMPLES=False"
                ],
                "secrets": ["db_password"],
                "volumes": [
                    "airflow_dags:/opt/airflow/dags",
                    "airflow_logs:/opt/airflow/logs",
                    "./dags:/opt/airflow/dags/custom",
                    "./plugins:/opt/airflow/plugins"
                ],
                "ports": ["8080:8080"],
                "command": "standalone",
                "healthcheck": {
                    "test": ["CMD", "curl", "-f", "http://localhost:8080/health"],
                    "interval": "30s",
                    "timeout": "10s",
                    "retries": 3
                }
            },
            "ml_api": {
                "build": {
                    "context": "./api",
                    "dockerfile": "Dockerfile.ml_api"
                },
                "container_name": "ml_prediction_api",
                "depends_on": {
                    "postgres": {"condition": "service_healthy"},
                    "redis": {"condition": "service_started"}
                },
                "environment": [
                    "DATABASE_URL=postgresql://admin:${DB_PASSWORD}@postgres/customer_analytics",
                    "REDIS_URL=redis://redis:6379/0",
                    "MODEL_PATH=/models/churn_model_v1.pkl",
                    "LOG_LEVEL=INFO"
                ],
                "secrets": ["db_password", "api_secret_key"],
                "volumes": [
                    "model_volume:/models",
                    "./api/logs:/app/logs"
                ],
                "ports": ["8000:8000"],
                "healthcheck": {
                    "test": ["CMD", "curl", "-f", "http://localhost:8000/health"],
                    "interval": "30s",
                    "timeout": "5s",
                    "retries": 3
                },
                "deploy": {
                    "resources": {
                        "limits": {
                            "cpus": "2.0",
                            "memory": "4G"
                        },
                        "reservations": {
                            "cpus": "1.0",
                            "memory": "2G"
                        }
                    }
                }
            },
            "redis": {
                "image": "redis:7-alpine",
                "container_name": "cache_redis",
                "command": "redis-server --appendonly yes",
                "volumes": ["redis_data:/data"],
                "ports": ["6379:6379"],
                "healthcheck": {
                    "test": ["CMD", "redis-cli", "ping"],
                    "interval": "10s",
                    "timeout": "5s",
                    "retries": 3
                }
            },
            "grafana": {
                "image": "grafana/grafana:10.2.0",
                "container_name": "monitoring_grafana",
                "environment": [
                    "GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}"
                ],
                "secrets": ["grafana_password"],
                "volumes": [
                    "grafana_data:/var/lib/grafana",
                    "./grafana/dashboards:/etc/grafana/provisioning/dashboards"
                ],
                "ports": ["3000:3000"],
                "depends_on": ["postgres", "ml_api"]
            }
        },
        "volumes": {
            "postgres_data": {},
            "airflow_dags": {},
            "airflow_logs": {},
            "model_volume": {},
            "redis_data": {},
            "grafana_data": {}
        },
        "secrets": {
            "db_password": {
                "file": "./secrets/db_password.txt"
            },
            "api_secret_key": {
                "file": "./secrets/api_key.txt"
            },
            "grafana_password": {
                "file": "./secrets/grafana