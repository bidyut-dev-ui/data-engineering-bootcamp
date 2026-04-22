#!/usr/bin/env python3
"""
Model Evaluation & Serialization Practice Exercises

This file contains 10 practice exercises covering:
1. Cross-validation techniques
2. Hyperparameter tuning
3. Evaluation metrics
4. Residual analysis
5. Model serialization
6. Model versioning
7. Memory-efficient evaluation
8. Production deployment considerations
9. Model monitoring
10. A/B testing for models

Each exercise focuses on practical implementation with 8GB RAM constraints.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Exercise 1: Cross-Validation Implementation
def exercise_1_cross_validation() -> Dict[str, Any]:
    """
    Implement k-fold cross-validation for model evaluation.
    
    Requirements:
    1. Load sample housing data (or generate synthetic data)
    2. Implement 5-fold cross-validation manually (without sklearn's cross_val_score)
    3. Calculate RMSE for each fold
    4. Return mean and standard deviation of RMSE across folds
    5. Handle edge cases (empty folds, missing values)
    
    Focus on memory efficiency for 8GB RAM.
    """
    print("=== Exercise 1: Cross-Validation Implementation ===")
    print("Implement k-fold cross-validation for robust model evaluation.")
    
    # Sample data generation (in practice, load from file)
    np.random.seed(42)
    n_samples = 1000
    X = np.random.randn(n_samples, 5)  # 5 features
    y = 2.5 * X[:, 0] + 1.8 * X[:, 1] - 0.9 * X[:, 2] + np.random.randn(n_samples) * 0.5
    
    # TODO: Implement 5-fold cross-validation
    # 1. Split data into 5 folds
    # 2. For each fold:
    #    - Use as validation set
    #    - Train on remaining folds
    #    - Calculate RMSE on validation set
    # 3. Return statistics
    
    return {
        "description": "Implement k-fold cross-validation manually",
        "data_shape": (n_samples, 5),
        "expected_output_keys": ["fold_scores", "mean_rmse", "std_rmse", "fold_indices"],
        "memory_constraint": "Process one fold at a time to stay under 8GB RAM",
        "hint": "Use np.array_split for creating folds, implement simple linear regression for prediction"
    }

# Exercise 2: Hyperparameter Tuning with GridSearchCV
def exercise_2_hyperparameter_tuning() -> Dict[str, Any]:
    """
    Implement hyperparameter tuning using GridSearchCV.
    
    Requirements:
    1. Define a parameter grid for RandomForestRegressor
    2. Use GridSearchCV with 3-fold cross-validation
    3. Track memory usage during grid search
    4. Implement early stopping if memory exceeds 6GB
    5. Return best parameters and corresponding score
    
    Optimize for 8GB RAM environment.
    """
    print("=== Exercise 2: Hyperparameter Tuning ===")
    print("Implement GridSearchCV with memory constraints.")
    
    # Parameter grid example
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10]
    }
    
    # TODO: Implement GridSearchCV with memory monitoring
    # 1. Monitor memory usage with psutil or resource module
    # 2. Implement checkpointing to save intermediate results
    # 3. Use n_jobs carefully (parallelism increases memory usage)
    
    return {
        "description": "Hyperparameter tuning with GridSearchCV and memory constraints",
        "parameter_grid_size": len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split']),
        "expected_output_keys": ["best_params", "best_score", "memory_usage_mb", "grid_search_results"],
        "memory_constraint": "Limit n_jobs based on available memory, use incremental fitting if needed",
        "hint": "Consider using RandomizedSearchCV for larger parameter spaces to save memory"
    }

# Exercise 3: Evaluation Metrics for Regression
def exercise_3_evaluation_metrics() -> Dict[str, Any]:
    """
    Implement comprehensive evaluation metrics for regression models.
    
    Requirements:
    1. Calculate RMSE, MAE, R², MAPE, and RMSLE
    2. Implement confidence intervals for metrics using bootstrapping
    3. Create visualizations of prediction vs actual (without plotting libraries)
    4. Calculate residual statistics (mean, std, skewness, kurtosis)
    5. Detect heteroscedasticity in residuals
    
    All calculations should be memory-efficient.
    """
    print("=== Exercise 3: Evaluation Metrics ===")
    print("Implement comprehensive regression evaluation metrics.")
    
    # Generate sample predictions and actual values
    np.random.seed(42)
    n = 500
    y_true = np.random.uniform(100000, 500000, n)
    y_pred = y_true + np.random.normal(0, 30000, n)  # Predictions with noise
    
    # TODO: Implement evaluation metrics
    # 1. Calculate basic metrics (RMSE, MAE, R²)
    # 2. Implement bootstrapping for confidence intervals
    # 3. Calculate residual statistics
    # 4. Detect patterns in residuals
    
    return {
        "description": "Comprehensive regression evaluation metrics",
        "sample_size": n,
        "expected_output_keys": ["rmse", "mae", "r2", "mape", "rmsle", "residual_stats", "confidence_intervals"],
        "memory_constraint": "Use streaming calculations for large datasets, avoid storing all residuals at once",
        "hint": "Implement Welford's algorithm for streaming variance calculation"
    }

# Exercise 4: Residual Analysis and Diagnostics
def exercise_4_residual_analysis() -> Dict[str, Any]:
    """
    Perform residual analysis to diagnose model issues.
    
    Requirements:
    1. Calculate residuals (y_true - y_pred)
    2. Test for normality (Shapiro-Wilk, QQ plots conceptually)
    3. Detect autocorrelation (Durbin-Watson statistic)
    4. Identify outliers using Cook's distance
    5. Check for homoscedasticity (Breusch-Pagan test conceptually)
    
    Implement memory-efficient statistical tests.
    """
    print("=== Exercise 4: Residual Analysis ===")
    print("Diagnose model issues through residual analysis.")
    
    # TODO: Implement residual diagnostics
    # 1. Calculate and analyze residuals
    # 2. Implement statistical tests
    # 3. Identify problematic observations
    # 4. Suggest corrective actions
    
    return {
        "description": "Residual analysis and model diagnostics",
        "expected_output_keys": ["residuals", "normality_test", "autocorrelation", "outliers", "homoscedasticity_test", "diagnostic_summary"],
        "memory_constraint": "Process residuals in chunks for large datasets",
        "hint": "For Cook's distance, use the formula that avoids matrix inversion for memory efficiency"
    }

# Exercise 5: Model Serialization with Joblib
def exercise_5_model_serialization() -> Dict[str, Any]:
    """
    Implement model serialization with versioning and metadata.
    
    Requirements:
    1. Save model using joblib with compression
    2. Create metadata JSON with model info, training date, metrics
    3. Implement model versioning (v1.0.0, v1.0.1, etc.)
    4. Add checksum verification for model files
    5. Implement model loading with validation
    
    Focus on production-ready serialization.
    """
    print("=== Exercise 5: Model Serialization ===")
    print("Implement production-ready model serialization with versioning.")
    
    # TODO: Implement model serialization system
    # 1. Save model with joblib.dump
    # 2. Create metadata file
    # 3. Implement versioning scheme
    # 4. Add validation on load
    
    return {
        "description": "Model serialization with versioning and metadata",
        "expected_output_keys": ["model_path", "metadata_path", "model_version", "checksum", "serialization_time_seconds"],
        "memory_constraint": "Use compression to reduce disk I/O and memory usage",
        "hint": "Consider using SHA-256 for checksums, store metadata in separate JSON for easy inspection"
    }

# Exercise 6: Memory-Efficient Cross-Validation
def exercise_6_memory_efficient_cv() -> Dict[str, Any]:
    """
    Implement memory-efficient cross-validation for large datasets.
    
    Requirements:
    1. Process data in chunks during cross-validation
    2. Use incremental learning algorithms when possible
    3. Implement out-of-core cross-validation
    4. Monitor and log memory usage throughout
    5. Compare performance with standard CV
    
    Specifically designed for 8GB RAM constraints.
    """
    print("=== Exercise 6: Memory-Efficient Cross-Validation ===")
    print("Implement CV that works with datasets larger than available RAM.")
    
    # TODO: Implement memory-efficient cross-validation
    # 1. Use generators/yield for data streaming
    # 2. Implement incremental learning
    # 3. Monitor memory usage
    # 4. Compare with traditional approach
    
    return {
        "description": "Memory-efficient cross-validation for large datasets",
        "expected_output_keys": ["cv_scores", "memory_usage_profile", "processing_time", "comparison_with_standard_cv"],
        "memory_constraint": "Keep peak memory under 6GB for safety margin",
        "hint": "Use sklearn's partial_fit with SGDRegressor for incremental learning"
    }

# Exercise 7: Model Versioning and Registry
def exercise_7_model_versioning() -> Dict[str, Any]:
    """
    Implement a simple model versioning and registry system.
    
    Requirements:
    1. Track model versions with semantic versioning
    2. Store metadata for each version (metrics, training data, hyperparameters)
    3. Implement rollback capability
    4. Add model comparison functionality
    5. Create a model registry API (conceptual)
    
    Design for production deployment.
    """
    print("=== Exercise 7: Model Versioning and Registry ===")
    print("Implement a model versioning system with rollback capability.")
    
    # TODO: Implement model versioning system
    # 1. Design versioning schema
    # 2. Implement registry storage
    # 3. Add rollback functionality
    # 4. Create comparison methods
    
    return {
        "description": "Model versioning and registry system",
        "expected_output_keys": ["registry_structure", "version_list", "current_version", "rollback_procedure", "comparison_matrix"],
        "memory_constraint": "Store metadata separately from model binaries",
        "hint": "Use a simple SQLite database or JSON files for the registry"
    }

# Exercise 8: Production Model Monitoring
def exercise_8_model_monitoring() -> Dict[str, Any]:
    """
    Implement model monitoring for production deployment.
    
    Requirements:
    1. Track prediction drift over time
    2. Monitor feature distribution changes
    3. Implement performance degradation alerts
    4. Calculate data quality metrics
    5. Create monitoring dashboard (conceptual design)
    
    Focus on lightweight monitoring suitable for 8GB RAM.
    """
    print("=== Exercise 8: Production Model Monitoring ===")
    print("Implement monitoring for model performance and data drift.")
    
    # TODO: Implement model monitoring
    # 1. Track predictions over time
    # 2. Monitor feature distributions
    # 3. Implement alerting logic
    # 4. Design monitoring system
    
    return {
        "description": "Production model monitoring system",
        "expected_output_keys": ["drift_metrics", "performance_trends", "alert_conditions", "monitoring_dashboard_design"],
        "memory_constraint": "Use rolling windows for statistics, avoid storing all historical data",
        "hint": "Implement KS-test for distribution comparison, use exponentially weighted moving averages for trends"
    }

# Exercise 9: A/B Testing for Models
def exercise_9_ab_testing() -> Dict[str, Any]:
    """
    Implement A/B testing framework for model comparison.
    
    Requirements:
    1. Design A/B test for two model versions
    2. Implement statistical significance testing
    3. Calculate sample size requirements
    4. Analyze test results with confidence intervals
    5. Make deployment recommendations
    
    Include memory-efficient statistical calculations.
    """
    print("=== Exercise 9: A/B Testing for Models ===")
    print("Implement A/B testing framework to compare model versions.")
    
    # TODO: Implement A/B testing framework
    # 1. Design experiment
    # 2. Calculate statistical significance
    # 3. Analyze results
    # 4. Make recommendations
    
    return {
        "description": "A/B testing framework for model comparison",
        "expected_output_keys": ["experiment_design", "sample_size_calculation", "test_results", "statistical_significance", "recommendation"],
        "memory_constraint": "Process test results incrementally",
        "hint": "Use sequential testing methods to reduce required sample size"
    }

# Exercise 10: End-to-End Model Evaluation Pipeline
def exercise_10_end_to_end_pipeline() -> Dict[str, Any]:
    """
    Implement an end-to-end model evaluation pipeline.
    
    Requirements:
    1. Integrate all previous exercises into a cohesive pipeline
    2. Add logging and error handling
    3. Implement configuration management
    4. Add performance benchmarking
    5. Create deployment-ready evaluation report
    
    Optimize for 8GB RAM throughout the pipeline.
    """
    print("=== Exercise 10: End-to-End Evaluation Pipeline ===")
    print("Implement complete model evaluation pipeline with production readiness.")
    
    # TODO: Implement end-to-end pipeline
    # 1. Integrate all components
    # 2. Add configuration and logging
    # 3. Generate comprehensive report
    # 4. Optimize for production
    
    return {
        "description": "End-to-end model evaluation pipeline",
        "expected_output_keys": ["pipeline_stages", "configuration", "evaluation_report", "performance_metrics", "memory_usage_summary"],
        "memory_constraint": "Pipeline must complete within 8GB RAM limit",
        "hint": "Use context managers for resource cleanup, implement checkpointing for long-running evaluations"
    }

def main():
    """Run all exercises and print summaries."""
    print("Model Evaluation & Serialization Practice Exercises")
    print("=" * 60)
    print("This module contains 10 exercises covering:")
    print("1. Cross-validation techniques")
    print("2. Hyperparameter tuning")
    print("3. Evaluation metrics")
    print("4. Residual analysis")
    print("5. Model serialization")
    print("6. Memory-efficient evaluation")
    print("7. Model versioning")
    print("8. Production monitoring")
    print("9. A/B testing")
    print("10. End-to-end pipeline")
    print("\nEach exercise is designed with 8GB RAM constraints.")
    print("Implement the TODO sections in each function.")
    
    # Exercise summaries
    exercises = [
        exercise_1_cross_validation,
        exercise_2_hyperparameter_tuning,
        exercise_3_evaluation_metrics,
        exercise_4_residual_analysis,
        exercise_5_model_serialization,
        exercise_6_memory_efficient_cv,
        exercise_7_model_versioning,
        exercise_8_model_monitoring,
        exercise_9_ab_testing,
        exercise_10_end_to_end_pipeline
    ]
    
    print("\n" + "=" * 60)
    print("Exercise Summaries:")
    for i, exercise_func in enumerate(exercises, 1):
        result = exercise_func()
        print(f"\n{i}. {result['description']}")
        print(f"   Expected outputs: {', '.join(result['expected_output_keys'])}")
        print(f"   Memory constraint: {result['memory_constraint']}")
    
    print("\n" + "=" * 60)
    print("Implementation Notes:")
    print("- All exercises should be implemented with 8GB RAM constraints")
    print("- Use streaming algorithms for large datasets")
    print("- Implement proper error handling and logging")
    print("- Focus on production-ready code patterns")
    print("- Test with both small and large datasets")
    
    return {"status": "exercises_defined", "count": len(exercises)}

if __name__ == "__main__":
    main()