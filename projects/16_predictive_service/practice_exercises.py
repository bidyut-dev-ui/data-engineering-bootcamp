#!/usr/bin/env python3
"""
Practice Exercises for Week 20: Predictive Service

This file contains exercises to reinforce concepts from the predictive service project:
- ML model training and serialization
- FastAPI endpoint development for model serving
- Input validation with Pydantic
- Batch prediction implementation
- Model versioning strategies
- Docker containerization for ML services
- API design patterns for ML services

Each exercise includes:
1. Problem statement
2. Expected output format
3. Hints for implementation
4. Solution skeleton
"""

import sys
import json
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
from datetime import datetime
from pydantic import BaseModel, Field, validator


def exercise_1_model_training_pipeline() -> Dict[str, Any]:
    """
    Exercise 1: Model Training Pipeline
    
    Create a function that:
    1. Generates synthetic housing data
    2. Trains a RandomForestRegressor with a preprocessing pipeline
    3. Evaluates the model using R² score
    4. Saves the model with version metadata
    
    Expected Output:
    {
        "train_r2": float,
        "test_r2": float,
        "model_path": str,
        "model_version": str,
        "feature_importance": Dict[str, float]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 1: Model Training Pipeline")
    print("="*60)
    
    # TODO: Implement this function
    # 1. Generate synthetic data (1000 samples, 5 features)
    # 2. Split into train/test (80/20)
    # 3. Create pipeline with StandardScaler and RandomForestRegressor
    # 4. Train and evaluate
    # 5. Save model with joblib
    # 6. Extract feature importance
    
    return {
        "train_r2": 0.0,  # Replace with actual value
        "test_r2": 0.0,   # Replace with actual value
        "model_path": "housing_model_v1.joblib",
        "model_version": "v1.0.0",
        "feature_importance": {"square_feet": 0.0, "bedrooms": 0.0}
    }


def exercise_2_pydantic_validation() -> Dict[str, Any]:
    """
    Exercise 2: Pydantic Validation for ML Inputs
    
    Create Pydantic models for:
    1. Single prediction request with validation constraints
    2. Batch prediction request
    3. Prediction response with confidence intervals
    
    Expected Output:
    {
        "single_model_fields": List[str],
        "batch_model_fields": List[str],
        "validation_test_passed": bool,
        "error_messages": List[str]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 2: Pydantic Validation for ML Inputs")
    print("="*60)
    
    # TODO: Define Pydantic models here
    # 1. HouseFeatures: square_feet (gt=0), bedrooms (ge=1, le=10), etc.
    # 2. BatchPredictionRequest: List[HouseFeatures]
    # 3. PredictionResponse: predicted_price, confidence_interval, model_version, predicted_at
    
    # Test validation
    test_data = {
        "square_feet": 2000,
        "bedrooms": 3,
        "bathrooms": 2,
        "age_years": 10,
        "distance_to_city": 5.0
    }
    
    return {
        "single_model_fields": ["square_feet", "bedrooms", "bathrooms", "age_years", "distance_to_city"],
        "batch_model_fields": ["houses"],
        "validation_test_passed": False,  # Replace with actual test
        "error_messages": ["Test not implemented"]
    }


def exercise_3_fastapi_endpoint_design() -> Dict[str, Any]:
    """
    Exercise 3: FastAPI Endpoint Design
    
    Design API endpoints for an ML service:
    1. Health check endpoint
    2. Single prediction endpoint
    3. Batch prediction endpoint
    4. Model information endpoint
    
    Expected Output:
    {
        "endpoints": List[Dict[str, str]],
        "request_methods": Dict[str, str],
        "response_codes": Dict[str, List[int]]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 3: FastAPI Endpoint Design")
    print("="*60)
    
    # Design the API structure
    endpoints = [
        {
            "path": "/health",
            "description": "Check if model is loaded and service is healthy",
            "method": "GET"
        },
        {
            "path": "/predict",
            "description": "Get prediction for a single house",
            "method": "POST"
        },
        {
            "path": "/predict/batch",
            "description": "Get predictions for multiple houses",
            "method": "POST"
        },
        {
            "path": "/model/info",
            "description": "Get model metadata and performance metrics",
            "method": "GET"
        }
    ]
    
    return {
        "endpoints": endpoints,
        "request_methods": {ep["path"]: ep["method"] for ep in endpoints},
        "response_codes": {
            "/health": [200, 503],
            "/predict": [200, 422, 500],
            "/predict/batch": [200, 422, 500],
            "/model/info": [200, 404]
        }
    }


def exercise_4_batch_prediction_optimization() -> Dict[str, Any]:
    """
    Exercise 4: Batch Prediction Optimization
    
    Compare single vs batch prediction performance:
    1. Implement single prediction (loop)
    2. Implement batch prediction (vectorized)
    3. Measure performance difference
    
    Expected Output:
    {
        "single_prediction_time_ms": float,
        "batch_prediction_time_ms": float,
        "speedup_factor": float,
        "memory_usage_mb": Dict[str, float]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 4: Batch Prediction Optimization")
    print("="*60)
    
    # Simulate predictions
    n_samples = 1000
    n_features = 5
    
    # Generate dummy data
    X_single = [np.random.randn(n_features) for _ in range(n_samples)]
    X_batch = np.random.randn(n_samples, n_features)
    
    # TODO: Implement timing comparison
    # 1. Time single predictions (loop)
    # 2. Time batch prediction (matrix)
    # 3. Calculate speedup
    
    return {
        "single_prediction_time_ms": 0.0,
        "batch_prediction_time_ms": 0.0,
        "speedup_factor": 0.0,
        "memory_usage_mb": {
            "single_approach": 0.0,
            "batch_approach": 0.0
        }
    }


def exercise_5_model_versioning_strategy() -> Dict[str, Any]:
    """
    Exercise 5: Model Versioning Strategy
    
    Design a model versioning system:
    1. Semantic versioning for models
    2. Model registry structure
    3. A/B testing routing logic
    
    Expected Output:
    {
        "version_schema": Dict[str, str],
        "registry_structure": List[str],
        "routing_logic": Dict[str, Any],
        "rollback_strategy": str
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 5: Model Versioning Strategy")
    print("="*60)
    
    # Design versioning system
    version_schema = {
        "major": "Breaking changes, retraining with new features",
        "minor": "Improved performance, same feature set",
        "patch": "Bug fixes, metadata updates"
    }
    
    registry_structure = [
        "models/v1.0.0/housing_model.joblib",
        "models/v1.0.0/metadata.json",
        "models/v1.1.0/housing_model.joblib",
        "models/v1.1.0/performance_metrics.json",
        "models/current -> models/v1.1.0"  # Symlink to current version
    ]
    
    return {
        "version_schema": version_schema,
        "registry_structure": registry_structure,
        "routing_logic": {
            "default_version": "v1.1.0",
            "ab_testing": {
                "v1.0.0": 0.3,  # 30% of traffic
                "v1.1.0": 0.7   # 70% of traffic
            },
            "header_based": "X-Model-Version"
        },
        "rollback_strategy": "Automatic rollback if error rate > 5% for 5 minutes"
    }


def exercise_6_docker_containerization() -> Dict[str, Any]:
    """
    Exercise 6: Docker Containerization for ML Services
    
    Design Docker configuration for ML service:
    1. Multi-stage Dockerfile
    2. Environment variables
    3. Health checks
    4. Resource limits
    
    Expected Output:
    {
        "dockerfile_stages": List[Dict[str, str]],
        "environment_vars": List[str],
        "health_check_command": str,
        "resource_limits": Dict[str, str]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 6: Docker Containerization for ML Services")
    print("="*60)
    
    dockerfile_stages = [
        {
            "name": "builder",
            "purpose": "Install dependencies and build application",
            "base_image": "python:3.9-slim"
        },
        {
            "name": "runtime",
            "purpose": "Production runtime with minimal footprint",
            "base_image": "python:3.9-slim"
        }
    ]
    
    return {
        "dockerfile_stages": dockerfile_stages,
        "environment_vars": [
            "MODEL_PATH=/app/models/housing_model.joblib",
            "MODEL_VERSION=v1.0.0",
            "LOG_LEVEL=INFO",
            "WORKERS=4",
            "PORT=8000"
        ],
        "health_check_command": "curl -f http://localhost:8000/health || exit 1",
        "resource_limits": {
            "memory": "1GB",
            "cpus": "2.0",
            "restart_policy": "on-failure:5"
        }
    }


def exercise_7_error_handling_resilience() -> Dict[str, Any]:
    """
    Exercise 7: Error Handling and Resilience
    
    Design error handling for ML service:
    1. Input validation errors
    2. Model loading failures
    3. Prediction errors
    4. Circuit breaker pattern
    
    Expected Output:
    {
        "error_types": List[Dict[str, str]],
        "http_status_codes": Dict[str, int],
        "circuit_breaker_config": Dict[str, Any],
        "retry_strategy": Dict[str, Any]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 7: Error Handling and Resilience")
    print("="*60)
    
    error_types = [
        {
            "error": "ValidationError",
            "cause": "Invalid input data",
            "http_status": 422,
            "recovery": "Client should fix request"
        },
        {
            "error": "ModelNotFoundError",
            "cause": "Model file missing",
            "http_status": 503,
            "recovery": "Admin should deploy model"
        },
        {
            "error": "PredictionError",
            "cause": "Model prediction failed",
            "http_status": 500,
            "recovery": "Retry with exponential backoff"
        }
    ]
    
    return {
        "error_types": error_types,
        "http_status_codes": {err["error"]: err["http_status"] for err in error_types},
        "circuit_breaker_config": {
            "failure_threshold": 5,
            "reset_timeout": 60,
            "half_open_max_requests": 3
        },
        "retry_strategy": {
            "max_retries": 3,
            "backoff_factor": 2.0,
            "retry_on_status": [500, 502, 503, 504]
        }
    }


def exercise_8_monitoring_observability() -> Dict[str, Any]:
    """
    Exercise 8: Monitoring and Observability
    
    Design monitoring for ML service:
    1. Key metrics to track
    2. Logging strategy
    3. Alerting rules
    4. Dashboard design
    
    Expected Output:
    {
        "key_metrics": List[Dict[str, str]],
        "logging_fields": List[str],
        "alert_rules": List[Dict[str, Any]],
        "dashboard_panels": List[str]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 8: Monitoring and Observability")
    print("="*60)
    
    key_metrics = [
        {
            "name": "prediction_requests_total",
            "type": "counter",
            "description": "Total number of prediction requests"
        },
        {
            "name": "prediction_latency_seconds",
            "type": "histogram",
            "description": "Prediction latency distribution"
        },
        {
            "name": "prediction_errors_total",
            "type": "counter",
            "description": "Total number of prediction errors"
        },
        {
            "name": "model_version_usage",
            "type": "gauge",
            "description": "Active model versions and usage"
        }
    ]
    
    return {
        "key_metrics": key_metrics,
        "logging_fields": [
            "timestamp", "level", "message", "model_version",
            "prediction_id", "latency_ms", "input_features", "error"
        ],
        "alert_rules": [
            {
                "name": "HighErrorRate",
                "condition": "rate(prediction_errors_total[5m]) > 0.05",
                "severity": "critical",
                "message": "Error rate exceeds 5%"
            },
            {
                "name": "HighLatency",
                "condition": "histogram_quantile(0.95, prediction_latency_seconds) > 1.0",
                "severity": "warning",
                "message": "95th percentile latency > 1 second"
            }
        ],
        "dashboard_panels": [
            "Request Rate (requests/sec)",
            "Error Rate (%)",
            "Prediction Latency (p50, p95, p99)",
            "Model Version Distribution",
            "Feature Importance Visualization"
        ]
    }


def exercise_9_ci_cd_ml_pipeline() -> Dict[str, Any]:
    """
    Exercise 9: CI/CD for ML Pipeline
    
    Design CI/CD pipeline for ML service:
    1. Testing stages
    2. Model validation
    3. Deployment strategies
    4. Rollback procedures
    
    Expected Output:
    {
        "pipeline_stages": List[Dict[str, Any]],
        "model_validation_tests": List[str],
        "deployment_strategy": str,
        "rollback_triggers": List[str]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 9: CI/CD for ML Pipeline")
    print("="*60)
    
    pipeline_stages = [
        {
            "name": "test",
            "jobs": ["unit_tests", "integration_tests", "model_validation"],
            "artifacts": ["test_results.xml", "coverage_report.html"]
        },
        {
            "name": "build",
            "jobs": ["build_docker_image", "scan_vulnerabilities"],
            "artifacts": ["docker_image.tar", "scan_report.json"]
        },
        {
            "name": "deploy_staging",
            "jobs": ["deploy_to_staging", "run_smoke_tests"],
            "artifacts": ["deployment_logs.txt", "smoke_test_results.json"]
        },
        {
            "name": "deploy_production",
            "jobs": ["canary_deployment", "monitor_metrics"],
            "artifacts": ["canary_analysis.json", "performance_metrics.json"]
        }
    ]
    
    return {
        "pipeline_stages": pipeline_stages,
        "model_validation_tests": [
            "Accuracy > baseline model",
            "No significant bias across demographic groups",
            "Inference latency < 100ms (p95)",
            "Memory usage < 1GB",
            "Feature importance stability check"
        ],
        "deployment_strategy": "Canary deployment with 10% traffic initially",
        "rollback_triggers": [
            "Error rate increase > 5%",
            "Latency increase > 50%",
            "Business metric degradation",
            "Security vulnerability detected"
        ]
    }


def exercise_10_production_readiness_assessment() -> Dict[str, Any]:
    """
    Exercise 10: Production Readiness Assessment
    
    Assess production readiness of ML service:
    1. Checklist items
    2. Risk assessment
    3. Capacity planning
    4. Disaster recovery
    
    Expected Output:
    {
        "readiness_checklist": Dict[str, bool],
        "risk_assessment": List[Dict[str, Any]],
        "capacity_estimates": Dict[str, Any],
        "disaster_recovery_plan": List[str]
    }
    """
    print("\n" + "="*60)
    print("EXERCISE 10: Production Readiness Assessment")
    print("="*60)
    
    readiness_checklist = {
        "Model trained and validated": True,
        "API endpoints documented": True,
        "Error handling implemented": True,
        "Monitoring and logging configured": False,
        "Load testing performed": False,
        "Security review completed": False,
        "Disaster recovery plan exists": False,
        "Runbooks documented": False,
        "Team trained on operations": False,
        "Compliance requirements met": False
    }
    
    return {
        "readiness_checklist": readiness_checklist,
        "risk_assessment": [
            {
                "risk": "Model performance degradation",
                "likelihood": "medium",
                "impact": "high",
                "mitigation": "A/B testing, automatic rollback"
            },
            {
                "risk": "Data drift affecting predictions",
                "likelihood": "high",
                "impact": "medium",
                "mitigation": "Continuous monitoring, retraining pipeline"
            },
            {
                "risk": "API security vulnerabilities",
                "likelihood": "low",
                "impact": "high",
                "mitigation": "Regular security scans, rate limiting"
            }
        ],
        "capacity_estimates": {
            "requests_per_second": 100,
            "memory_per_instance_mb": 1024,
            "cpu_per_instance": 2.0,
            "storage_gb": 10,
            "estimated_monthly_cost": 150.0
        },
        "disaster_recovery_plan": [
            "Backup model artifacts to cloud storage",
            "Maintain previous model version for rollback",
            "Automated failover to secondary region",
            "Database replication for prediction logs",
            "Incident response runbook"
        ]
    }


def main():
    """Run all exercises and display results"""
    print("\n" + "="*60)
    print("PRACTICE EXERCISES: Predictive Service (Week 20)")
    print("="*60)
    
    exercises = [
        ("Model Training Pipeline", exercise_1_model_training_pipeline),
        ("Pydantic Validation", exercise_2_pydantic_validation),
        ("FastAPI Endpoint Design", exercise_3_fastapi_endpoint_design),
        ("Batch Prediction Optimization", exercise_4_batch_prediction_optimization),
        ("Model Versioning Strategy", exercise_5_model_versioning_strategy),
        ("Docker Containerization", exercise_6_docker_containerization),
        ("Error Handling and Resilience", exercise_7_error_handling_resilience),
        ("Monitoring and Observability", exercise_8_monitoring_observability),
        ("CI/CD for ML Pipeline", exercise_9_ci_cd_ml_pipeline),
        ("Production Readiness Assessment", exercise_10_production_readiness_assessment)
    ]
    
    results = {}
    
    for name, func in exercises:
        try:
            print(f"\nRunning: {name}")
            result = func()
            results[name] = result
            
            # Print summary
            print(f"  Status: COMPLETED")
            if isinstance(result, dict):
                print(f"  Keys: {list(result.keys())}")
        except Exception as e:
            print(f"  Status: FAILED - {str(e)}")
            results[name] = {"error": str(e)}
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    completed = sum(1 for r in results.values() if "error" not in r)
    print(f"Exercises completed: {completed}/{len(exercises)}")
    
    # Save results to file
    with open("practice_exercises_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: practice_exercises_results.json")
    print("\nNext steps:")
    print("1. Implement the TODO sections in each exercise")
    print("2. Test your implementations")
    print("3. Compare with the expected outputs")
    print("4. Review the GOTCHAS_BEST_PRACTICES.md file")
    print("5. Study the INTERVIEW_QUESTIONS.md file")
    
    return results


if __name__ == "__main__":
    main()