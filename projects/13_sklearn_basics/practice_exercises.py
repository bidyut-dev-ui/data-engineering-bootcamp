#!/usr/bin/env python3
"""
Scikit-learn Practice Exercises

This module contains 10 practice exercises covering fundamental scikit-learn concepts
including regression, classification, preprocessing, pipelines, and model evaluation.
Each exercise is designed to reinforce learning through hands-on implementation.

Memory Considerations:
- All exercises are designed to work within 8GB RAM constraints
- Use incremental learning for large datasets
- Implement proper data splitting and validation
- Monitor memory usage with sklearn's memory profiling
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')


def exercise_1_basic_regression_pipeline() -> Dict[str, Any]:
    """
    Exercise 1: Basic Regression Pipeline
    
    Implement a complete regression pipeline that:
    1. Loads and explores the housing dataset
    2. Splits data into train/test sets
    3. Creates a preprocessing pipeline with scaling
    4. Trains a Linear Regression model
    5. Evaluates using RMSE and R² scores
    6. Returns feature importance (coefficients)
    
    Returns:
        Dictionary with metrics, model coefficients, and sample predictions
    """
    pass


def exercise_2_classification_with_cross_validation() -> Dict[str, Any]:
    """
    Exercise 2: Classification with Cross-Validation
    
    Implement a classification pipeline that:
    1. Loads the customer churn dataset
    2. Handles categorical features with one-hot encoding
    3. Implements k-fold cross-validation (k=5)
    4. Trains a Random Forest Classifier
    5. Evaluates using accuracy, precision, recall, F1-score
    6. Returns feature importance from the model
    
    Returns:
        Dictionary with cross-validation scores, evaluation metrics, and feature importance
    """
    pass


def exercise_3_feature_engineering_and_selection() -> Dict[str, Any]:
    """
    Exercise 3: Feature Engineering and Selection
    
    Implement feature engineering techniques:
    1. Create polynomial features (degree=2) for numerical columns
    2. Handle missing values using multiple imputation strategies
    3. Perform feature selection using correlation analysis
    4. Use recursive feature elimination (RFE)
    5. Compare model performance with vs without feature selection
    
    Returns:
        Dictionary with selected features, performance comparison, and engineering insights
    """
    pass


def exercise_4_hyperparameter_tuning() -> Dict[str, Any]:
    """
    Exercise 4: Hyperparameter Tuning with GridSearchCV
    
    Implement hyperparameter optimization:
    1. Define parameter grid for Random Forest (n_estimators, max_depth, min_samples_split)
    2. Use GridSearchCV with 5-fold cross-validation
    3. Implement RandomizedSearchCV for comparison
    4. Evaluate best model on test set
    5. Visualize parameter performance (if matplotlib available)
    
    Returns:
        Dictionary with best parameters, best score, and search results
    """
    pass


def exercise_5_model_ensemble_techniques() -> Dict[str, Any]:
    """
    Exercise 5: Model Ensemble Techniques
    
    Implement ensemble methods:
    1. Bagging (Random Forest)
    2. Boosting (Gradient Boosting - if available)
    3. Voting Classifier for classification
    4. Stacking with multiple base models
    5. Compare ensemble performance vs single models
    
    Returns:
        Dictionary with ensemble configurations, performance metrics, and comparison results
    """
    pass


def exercise_6_pipeline_with_custom_transformer() -> Dict[str, Any]:
    """
    Exercise 6: Custom Transformer in Pipeline
    
    Create a custom transformer for:
    1. Log transformation of skewed numerical features
    2. Outlier detection and capping
    3. Custom feature interaction creation
    4. Integration into sklearn Pipeline
    5. Comparison with standard preprocessing
    
    Returns:
        Dictionary with custom transformer implementation and performance impact
    """
    pass


def exercise_7_clustering_and_unsupervised_learning() -> Dict[str, Any]:
    """
    Exercise 7: Clustering and Unsupervised Learning
    
    Implement unsupervised techniques:
    1. K-Means clustering for customer segmentation
    2. Determine optimal k using elbow method and silhouette score
    3. PCA for dimensionality reduction and visualization
    4. DBSCAN for density-based clustering
    5. Interpret cluster characteristics
    
    Returns:
        Dictionary with clustering results, optimal k, and cluster profiles
    """
    pass


def exercise_8_time_series_forecasting() -> Dict[str, Any]:
    """
    Exercise 8: Time Series Forecasting with sklearn
    
    Implement time series forecasting:
    1. Create time-based features (lag features, rolling statistics)
    2. Handle seasonality and trend decomposition
    3. Train regression models on time series data
    4. Implement walk-forward validation
    5. Evaluate using time-series specific metrics (MAE, MAPE)
    
    Returns:
        Dictionary with forecasting results, error metrics, and feature importance
    """
    pass


def exercise_9_model_persistence_and_deployment() -> Dict[str, Any]:
    """
    Exercise 9: Model Persistence and Deployment Preparation
    
    Implement model serialization and deployment patterns:
    1. Save trained model using joblib/pickle
    2. Create prediction function with input validation
    3. Implement batch prediction for multiple samples
    4. Create model versioning strategy
    5. Monitor model drift with simple statistical tests
    
    Returns:
        Dictionary with serialized model info, prediction examples, and deployment checklist
    """
    pass


def exercise_10_performance_optimization_for_8gb_ram() -> Dict[str, Any]:
    """
    Exercise 10: Performance Optimization for 8GB RAM
    
    Optimize sklearn workflows for memory-constrained environments:
    1. Use incremental learning with partial_fit
    2. Implement feature selection to reduce dimensionality
    3. Use sparse matrices for high-dimensional data
    4. Implement early stopping for iterative algorithms
    5. Monitor memory usage during training
    6. Compare performance vs memory trade-offs
    
    Returns:
        Dictionary with optimization techniques, memory usage metrics, and performance benchmarks
    """
    pass


def main():
    """Run all scikit-learn practice exercises in sequence."""
    exercises = [
        ("Basic Regression Pipeline", exercise_1_basic_regression_pipeline),
        ("Classification with Cross-Validation", exercise_2_classification_with_cross_validation),
        ("Feature Engineering and Selection", exercise_3_feature_engineering_and_selection),
        ("Hyperparameter Tuning", exercise_4_hyperparameter_tuning),
        ("Model Ensemble Techniques", exercise_5_model_ensemble_techniques),
        ("Pipeline with Custom Transformer", exercise_6_pipeline_with_custom_transformer),
        ("Clustering and Unsupervised Learning", exercise_7_clustering_and_unsupervised_learning),
        ("Time Series Forecasting", exercise_8_time_series_forecasting),
        ("Model Persistence and Deployment", exercise_9_model_persistence_and_deployment),
        ("Performance Optimization for 8GB RAM", exercise_10_performance_optimization_for_8gb_ram),
    ]
    
    results = {}
    
    print("=" * 80)
    print("Scikit-learn Practice Exercises")
    print("=" * 80)
    print(f"Running {len(exercises)} exercises...\n")
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * len(name))
        
        try:
            # Execute the exercise function
            result = func()
            results[name] = result
            
            # Print summary if available
            if isinstance(result, dict):
                if 'success' in result:
                    print(f"  Status: {'✓ Success' if result['success'] else '✗ Failed'}")
                if 'metrics' in result:
                    print(f"  Metrics: {result['metrics']}")
                if 'message' in result:
                    print(f"  Message: {result['message']}")
            else:
                print(f"  Result: {type(result).__name__}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
            results[name] = {"error": str(e)}
    
    print("\n" + "=" * 80)
    print("Exercise Summary:")
    print("=" * 80)
    
    successful = sum(1 for r in results.values() if isinstance(r, dict) and r.get('success', False))
    print(f"\nCompleted: {successful}/{len(exercises)} exercises")
    
    # Return comprehensive results
    return {
        "total_exercises": len(exercises),
        "completed": successful,
        "results": results,
        "timestamp": pd.Timestamp.now().isoformat()
    }


if __name__ == "__main__":
    # Generate sample data if needed
    try:
        # Check if data files exist
        import os
        if not os.path.exists('housing_data.csv') or not os.path.exists('customer_churn.csv'):
            print("Generating sample data...")
            # Import and run generate_data if available
            try:
                from generate_data import main as generate_data_main
                generate_data_main()
            except ImportError:
                print("Warning: Could not generate sample data. Some exercises may fail.")
    except ImportError:
        pass
    
    # Run all exercises
    main()