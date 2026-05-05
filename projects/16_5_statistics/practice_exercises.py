#!/usr/bin/env python3
"""
Statistics for Data Engineers - Practice Exercises

This file contains 10 exercises covering statistical concepts essential for data engineers.
Focus on descriptive statistics, distributions, outlier detection, and statistical thinking
for data quality and ML preparation.

Note: Following user priority, solutions are deferred. These exercises are designed to test
understanding of statistical concepts and prepare for interviews.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from scipy import stats


def exercise_1_descriptive_statistics() -> Dict[str, Any]:
    """
    Exercise 1: Descriptive Statistics Fundamentals
    
    Calculate and interpret descriptive statistics for a dataset.
    Focus on understanding when to use mean vs median, and the impact of outliers.
    
    Return a dictionary with:
    - "mean_median_diff": Difference between mean and median for given data
    - "outlier_impact": How much outliers affect the mean (percentage change)
    - "interpretation": Brief explanation of when to use each measure
    """
    # Sample data with outliers
    data = [10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 100]  # 100 is an outlier
    
    # TODO: Implement this exercise
    return {
        "description": "Calculate and interpret descriptive statistics",
        "data": data,
        "mean_median_diff": None,
        "outlier_impact": None,
        "interpretation": None
    }


def exercise_2_distribution_analysis() -> Dict[str, Any]:
    """
    Exercise 2: Distribution Analysis
    
    Analyze different types of distributions (normal, skewed, uniform).
    Calculate skewness and kurtosis, and interpret their meaning.
    
    Return a dictionary with:
    - "skewness_values": Skewness for normal, right-skewed, and left-skewed data
    - "kurtosis_values": Kurtosis for each distribution
    - "distribution_types": Classification of each dataset
    """
    # Generate sample distributions
    np.random.seed(42)
    normal_data = np.random.normal(0, 1, 1000)
    right_skewed = np.random.exponential(1, 1000)
    left_skewed = -np.random.exponential(1, 1000) + 2
    
    # TODO: Implement this exercise
    return {
        "description": "Analyze distribution types and shape metrics",
        "normal_data_sample": normal_data[:5].tolist(),
        "right_skewed_sample": right_skewed[:5].tolist(),
        "left_skewed_sample": left_skewed[:5].tolist(),
        "skewness_values": None,
        "kurtosis_values": None,
        "distribution_types": None
    }


def exercise_3_outlier_detection_iqr() -> Dict[str, Any]:
    """
    Exercise 3: Outlier Detection with IQR Method
    
    Implement IQR-based outlier detection and compare with Z-score method.
    Understand the robustness of IQR to extreme values.
    
    Return a dictionary with:
    - "iqr_outliers": List of outliers detected by IQR method
    - "z_score_outliers": List of outliers detected by Z-score method
    - "comparison": Explanation of when each method is appropriate
    """
    # Sample data with known outliers
    data = pd.Series([15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100, 150])
    
    # TODO: Implement this exercise
    return {
        "description": "Implement IQR and Z-score outlier detection",
        "data": data.tolist(),
        "iqr_outliers": None,
        "z_score_outliers": None,
        "comparison": "IQR is robust to extreme values, Z-score assumes normal distribution"
    }


def exercise_4_skewness_and_transformations() -> Dict[str, Any]:
    """
    Exercise 4: Skewness Analysis and Data Transformations
    
    Calculate skewness and apply transformations (log, square root, Box-Cox)
    to normalize skewed data for ML models.
    
    Return a dictionary with:
    - "original_skewness": Skewness of original data
    - "transformed_skewness": Skewness after each transformation
    - "best_transformation": Which transformation worked best
    """
    # Generate right-skewed data
    np.random.seed(42)
    skewed_data = np.random.exponential(2, 1000) + 1  # Add 1 to avoid log(0)
    
    # TODO: Implement this exercise
    return {
        "description": "Analyze skewness and apply normalization transformations",
        "skewed_data_sample": skewed_data[:5].tolist(),
        "original_skewness": None,
        "transformed_skewness": {},
        "best_transformation": None
    }


def exercise_5_correlation_analysis() -> Dict[str, Any]:
    """
    Exercise 5: Correlation Analysis for Feature Selection
    
    Calculate different correlation coefficients (Pearson, Spearman, Kendall)
    and understand when to use each for feature selection in ML pipelines.
    
    Return a dictionary with:
    - "correlation_matrix": DataFrame with correlation coefficients
    - "strong_correlations": Pairs with |correlation| > 0.7
    - "interpretation": When to use each correlation measure
    """
    # Generate correlated data
    np.random.seed(42)
    n = 100
    x = np.random.normal(0, 1, n)
    y_linear = 2 * x + np.random.normal(0, 0.5, n)  # Linear relationship
    y_monotonic = np.exp(x) + np.random.normal(0, 0.5, n)  # Monotonic but not linear
    
    # TODO: Implement this exercise
    return {
        "description": "Calculate and interpret correlation coefficients",
        "data_shape": (n, 3),
        "correlation_matrix": None,
        "strong_correlations": None,
        "interpretation": None
    }


def exercise_6_confidence_intervals() -> Dict[str, Any]:
    """
    Exercise 6: Confidence Intervals for Data Quality
    
    Calculate confidence intervals for population parameters.
    Understand how sample size affects interval width and precision.
    
    Return a dictionary with:
    - "confidence_intervals": 95% CI for mean of different sample sizes
    - "sample_size_impact": How interval width changes with sample size
    - "interpretation": Practical implications for data quality monitoring
    """
    # Generate population data
    np.random.seed(42)
    population = np.random.normal(100, 15, 10000)
    
    # TODO: Implement this exercise
    return {
        "description": "Calculate confidence intervals and understand sample size impact",
        "population_mean": np.mean(population),
        "population_std": np.std(population),
        "confidence_intervals": None,
        "sample_size_impact": None,
        "interpretation": None
    }


def exercise_7_hypothesis_testing() -> Dict[str, Any]:
    """
    Exercise 7: Hypothesis Testing for A/B Testing
    
    Implement statistical tests (t-test, chi-square, ANOVA) for A/B testing scenarios.
    Understand p-values, significance levels, and practical vs statistical significance.
    
    Return a dictionary with:
    - "test_results": Results of different hypothesis tests
    - "p_values": P-values for each test
    - "conclusions": Whether to reject null hypothesis for each test
    """
    # Generate A/B test data
    np.random.seed(42)
    group_a = np.random.normal(100, 15, 500)
    group_b = np.random.normal(105, 15, 500)  # Slightly different mean
    
    # TODO: Implement this exercise
    return {
        "description": "Implement hypothesis tests for A/B testing scenarios",
        "group_a_mean": np.mean(group_a),
        "group_b_mean": np.mean(group_b),
        "test_results": None,
        "p_values": None,
        "conclusions": None
    }


def exercise_8_statistical_power() -> Dict[str, Any]:
    """
    Exercise 8: Statistical Power and Sample Size Calculation
    
    Calculate statistical power and determine required sample sizes for experiments.
    Understand trade-offs between power, effect size, and sample size.
    
    Return a dictionary with:
    - "power_analysis": Power for different sample sizes and effect sizes
    - "required_sample_size": Sample needed for 80% power with given effect size
    - "tradeoffs": Explanation of power vs sample size vs effect size
    """
    # Parameters for power analysis
    effect_sizes = [0.2, 0.5, 0.8]  # Small, medium, large
    sample_sizes = [50, 100, 200, 500]
    
    # TODO: Implement this exercise
    return {
        "description": "Analyze statistical power and sample size requirements",
        "effect_sizes": effect_sizes,
        "sample_sizes": sample_sizes,
        "power_analysis": None,
        "required_sample_size": None,
        "tradeoffs": None
    }


def exercise_9_time_series_statistics() -> Dict[str, Any]:
    """
    Exercise 9: Time Series Statistics for Monitoring
    
    Calculate time-series statistics (autocorrelation, stationarity, seasonality).
    Apply statistical tests for trend detection and anomaly detection in time series.
    
    Return a dictionary with:
    - "autocorrelation": Autocorrelation at different lags
    - "stationarity_test": Results of Dickey-Fuller test
    - "seasonality_detection": Evidence of seasonal patterns
    """
    # Generate time series data with trend and seasonality
    np.random.seed(42)
    n = 365  # Daily data for one year
    time = np.arange(n)
    trend = 0.05 * time
    seasonality = 10 * np.sin(2 * np.pi * time / 30)  # Monthly seasonality
    noise = np.random.normal(0, 5, n)
    time_series = trend + seasonality + noise
    
    # TODO: Implement this exercise
    return {
        "description": "Analyze time series statistics for monitoring applications",
        "time_series_length": n,
        "autocorrelation": None,
        "stationarity_test": None,
        "seasonality_detection": None
    }


def exercise_10_statistical_thinking_data_engineering() -> Dict[str, Any]:
    """
    Exercise 10: Statistical Thinking for Data Engineering
    
    Apply statistical thinking to real data engineering scenarios:
    - Data quality monitoring with control charts
    - Anomaly detection in data pipelines
    - Statistical sampling for big data
    - ML feature engineering statistics
    
    Return a dictionary with:
    - "scenario_analysis": Analysis of each data engineering scenario
    - "statistical_methods": Recommended statistical methods for each
    - "implementation_considerations": Practical considerations for production
    """
    # TODO: Implement this exercise
    return {
        "description": "Apply statistical thinking to data engineering scenarios",
        "scenarios": [
            "Data quality monitoring with control charts",
            "Anomaly detection in streaming data pipelines",
            "Statistical sampling for big data validation",
            "Feature statistics for ML model training"
        ],
        "scenario_analysis": None,
        "statistical_methods": None,
        "implementation_considerations": [
            "8GB RAM constraints for large datasets",
            "Real-time processing requirements",
            "Production monitoring and alerting",
            "Cost-effective sampling strategies"
        ]
    }


def main():
    """Run all exercises and print summaries"""
    print("=== Statistics for Data Engineers Practice Exercises ===\n")
    print("This file contains 10 exercises covering statistical concepts for data engineers.")
    print("Following user priority: exercises without solutions, focusing on interview preparation.\n")
    
    exercises = [
        ("1. Descriptive Statistics Fundamentals", exercise_1_descriptive_statistics),
        ("2. Distribution Analysis", exercise_2_distribution_analysis),
        ("3. Outlier Detection with IQR Method", exercise_3_outlier_detection_iqr),
        ("4. Skewness Analysis and Data Transformations", exercise_4_skewness_and_transformations),
        ("5. Correlation Analysis for Feature Selection", exercise_5_correlation_analysis),
        ("6. Confidence Intervals for Data Quality", exercise_6_confidence_intervals),
        ("7. Hypothesis Testing for A/B Testing", exercise_7_hypothesis_testing),
        ("8. Statistical Power and Sample Size Calculation", exercise_8_statistical_power),
        ("9. Time Series Statistics for Monitoring", exercise_9_time_series_statistics),
        ("10. Statistical Thinking for Data Engineering", exercise_10_statistical_thinking_data_engineering)
    ]
    
    for title, func in exercises:
        print(f"\n{title}")
        print("-" * len(title))
        try:
            result = func()
            print(f"✓ Exercise defined: {result.get('description', 'No description')}")
            if "data" in result:
                print(f"  Data sample: {result.get('data', [])[:5] if isinstance(result.get('data'), list) else 'N/A'}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Exercises completed. Remember:")
    print("1. These are practice exercises without solutions (per user priority)")
    print("2. Focus on understanding statistical concepts for data engineering")
    print("3. Prepare for interview questions about data quality, outlier detection, and ML preparation")
    print("4. Consider 8GB RAM constraints when implementing statistical methods on large datasets")
    print("\nNext steps: Implement solutions after completing all educational frameworks.")


if __name__ == "__main__":
    main()