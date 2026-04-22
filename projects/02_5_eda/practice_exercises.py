#!/usr/bin/env python3
"""
Practice Exercises for Week 2.5: Exploratory Data Analysis (EDA)

This module provides 10 practice exercises covering essential EDA techniques
for data engineers, with a focus on identifying data quality issues,
understanding distributions, and preparing data for downstream processing.

All exercises are designed to run within 8GB RAM constraints.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Tuple
import warnings
warnings.filterwarnings('ignore')


def exercise_1_basic_data_profiling() -> Dict[str, Any]:
    """
    Exercise 1: Basic Data Profiling
    Load the customer_data.csv file and perform basic profiling.
    
    Tasks:
    1. Load the dataset and print shape, columns, and dtypes
    2. Calculate missing values percentage for each column
    3. Identify duplicate rows
    4. Generate basic statistics for numerical columns
    
    Returns:
        Dictionary with profiling results
    """
    # TODO: Implement this exercise
    # Hint: Use pd.read_csv(), df.info(), df.isnull().sum(), df.duplicated().sum(), df.describe()
    
    return {
        "shape": None,
        "columns": None,
        "missing_values": None,
        "duplicates": None,
        "numerical_stats": None
    }


def exercise_2_outlier_detection() -> Dict[str, Any]:
    """
    Exercise 2: Outlier Detection using IQR Method
    Detect outliers in numerical columns using the Interquartile Range method.
    
    Tasks:
    1. For each numerical column, calculate Q1, Q3, and IQR
    2. Identify outliers (values < Q1 - 1.5*IQR or > Q3 + 1.5*IQR)
    3. Count outliers per column
    4. Calculate percentage of outliers
    
    Returns:
        Dictionary with outlier statistics
    """
    # TODO: Implement this exercise
    # Hint: Use df.select_dtypes(include=[np.number]), df.quantile()
    
    return {
        "outlier_counts": None,
        "outlier_percentages": None,
        "columns_with_most_outliers": None
    }


def exercise_3_correlation_analysis() -> Dict[str, Any]:
    """
    Exercise 3: Correlation Analysis and Heatmap Generation
    Analyze relationships between numerical variables.
    
    Tasks:
    1. Calculate correlation matrix for numerical columns
    2. Identify highly correlated pairs (|correlation| > 0.7)
    3. Generate a heatmap visualization (save to file)
    4. Identify multicollinearity issues
    
    Returns:
        Dictionary with correlation analysis results
    """
    # TODO: Implement this exercise
    # Hint: Use df.corr(), sns.heatmap(), plt.savefig()
    
    return {
        "correlation_matrix": None,
        "highly_correlated_pairs": None,
        "heatmap_path": "correlation_heatmap.png"
    }


def exercise_4_categorical_analysis() -> Dict[str, Any]:
    """
    Exercise 4: Categorical Variable Analysis
    Analyze categorical columns for cardinality, distribution, and issues.
    
    Tasks:
    1. Identify categorical columns (object dtype)
    2. Calculate cardinality (unique values) for each categorical column
    3. Check for high cardinality columns (> 50 unique values)
    4. Analyze value distributions and identify rare categories (< 1% frequency)
    
    Returns:
        Dictionary with categorical analysis results
    """
    # TODO: Implement this exercise
    # Hint: Use df.select_dtypes(include=['object']), df[col].nunique(), df[col].value_counts(normalize=True)
    
    return {
        "categorical_columns": None,
        "cardinality": None,
        "high_cardinality_columns": None,
        "rare_categories": None
    }


def exercise_5_data_quality_checks() -> Dict[str, Any]:
    """
    Exercise 5: Comprehensive Data Quality Checks
    Implement data quality validation rules.
    
    Tasks:
    1. Check for negative values in age, income, purchase_amount
    2. Validate categorical values against expected domains
    3. Check for impossible combinations (e.g., age < 18 but membership = 'premium')
    4. Validate date ranges and logical consistency
    
    Returns:
        Dictionary with data quality issues found
    """
    # TODO: Implement this exercise
    # Hint: Use df[df['age'] < 0], df[~df['category'].isin(expected_categories)]
    
    return {
        "negative_values": None,
        "invalid_categories": None,
        "impossible_combinations": None,
        "date_inconsistencies": None
    }


def exercise_6_missing_value_patterns() -> Dict[str, Any]:
    """
    Exercise 6: Missing Value Pattern Analysis
    Analyze patterns in missing data and imputation strategies.
    
    Tasks:
    1. Create missing value matrix (heatmap of null values)
    2. Analyze if missingness is random or follows a pattern
    3. Test different imputation strategies (mean, median, mode, forward fill)
    4. Compare imputation impact on correlation structure
    
    Returns:
        Dictionary with missing value analysis
    """
    # TODO: Implement this exercise
    # Hint: Use df.isnull(), sns.heatmap(df.isnull()), df.fillna()
    
    return {
        "missing_pattern": None,
        "imputation_comparison": None,
        "recommended_strategy": None
    }


def exercise_7_distribution_visualization() -> Dict[str, Any]:
    """
    Exercise 7: Distribution Visualization
    Create comprehensive visualizations for data understanding.
    
    Tasks:
    1. Create histograms for all numerical columns
    2. Create box plots for outlier visualization
    3. Create bar charts for categorical distributions
    4. Create pairplot for multivariate relationships
    5. Save all visualizations to files
    
    Returns:
        Dictionary with visualization file paths
    """
    # TODO: Implement this exercise
    # Hint: Use plt.hist(), sns.boxplot(), sns.countplot(), sns.pairplot()
    
    return {
        "histogram_paths": [],
        "boxplot_paths": [],
        "barchart_paths": [],
        "pairplot_path": "pairplot.png"
    }


def exercise_8_memory_optimization() -> Dict[str, Any]:
    """
    Exercise 8: Memory Optimization for Large Datasets
    Optimize DataFrame memory usage for 8GB RAM constraints.
    
    Tasks:
    1. Calculate current memory usage of DataFrame
    2. Convert object dtypes to category where appropriate
    3. Downcast numerical columns to smaller dtypes
    4. Measure memory savings achieved
    5. Implement chunked processing for very large files
    
    Returns:
        Dictionary with memory optimization results
    """
    # TODO: Implement this exercise
    # Hint: Use df.memory_usage(deep=True), df[col].astype('category'), pd.to_numeric(df[col], downcast='integer')
    
    return {
        "original_memory_mb": None,
        "optimized_memory_mb": None,
        "memory_saving_percentage": None,
        "chunk_processing_plan": None
    }


def exercise_9_automated_eda_report() -> Dict[str, Any]:
    """
    Exercise 9: Automated EDA Report Generation
    Create a comprehensive EDA report in markdown format.
    
    Tasks:
    1. Generate summary statistics table
    2. Create data quality scorecard
    3. Include visualization summaries
    4. Generate actionable recommendations
    5. Save report to markdown file
    
    Returns:
        Dictionary with report generation results
    """
    # TODO: Implement this exercise
    # Hint: Use f-strings for markdown generation, write to .md file
    
    return {
        "report_path": "eda_report.md",
        "summary_statistics": None,
        "data_quality_score": None,
        "key_findings": [],
        "recommendations": []
    }


def exercise_10_production_ready_eda_pipeline() -> Dict[str, Any]:
    """
    Exercise 10: Production-Ready EDA Pipeline
    Create a reusable EDA pipeline class for production use.
    
    Tasks:
    1. Create EDA class with configurable parameters
    2. Implement methods for profiling, visualization, and reporting
    3. Add logging and error handling
    4. Create unit tests for the pipeline
    5. Optimize for performance on 8GB RAM
    
    Returns:
        Dictionary with pipeline implementation details
    """
    # TODO: Implement this exercise
    # Hint: Create a class with __init__, profile(), visualize(), generate_report() methods
    
    return {
        "pipeline_class": "EDA_Pipeline",
        "methods_implemented": [],
        "performance_metrics": None,
        "test_coverage": None
    }


def main():
    """Run all EDA practice exercises in sequence."""
    exercises = [
        ("Basic Data Profiling", exercise_1_basic_data_profiling),
        ("Outlier Detection", exercise_2_outlier_detection),
        ("Correlation Analysis", exercise_3_correlation_analysis),
        ("Categorical Analysis", exercise_4_categorical_analysis),
        ("Data Quality Checks", exercise_5_data_quality_checks),
        ("Missing Value Patterns", exercise_6_missing_value_patterns),
        ("Distribution Visualization", exercise_7_distribution_visualization),
        ("Memory Optimization", exercise_8_memory_optimization),
        ("Automated EDA Report", exercise_9_automated_eda_report),
        ("Production-Ready EDA Pipeline", exercise_10_production_ready_eda_pipeline)
    ]
    
    print("🚀 Starting EDA Practice Exercises...")
    print("=" * 60)
    
    results = {}
    
    for name, func in exercises:
        print(f"\n📊 Exercise: {name}")
        print("-" * 40)
        
        try:
            result = func()
            results[name] = result
            print(f"✅ {name} completed successfully")
            # Print key insights
            if isinstance(result, dict):
                for key, value in list(result.items())[:3]:  # Show first 3 items
                    if value is not None:
                        print(f"   • {key}: {value}")
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            results[name] = {"error": str(e)}
    
    print("\n" + "=" * 60)
    print("🎯 All exercises completed!")
    print(f"📈 Total exercises run: {len(exercises)}")
    print(f"✅ Successful: {sum(1 for r in results.values() if 'error' not in r)}")
    print(f"❌ Failed: {sum(1 for r in results.values() if 'error' in r)}")
    
    return results


if __name__ == "__main__":
    main()