# Statistics for Data Engineers: Gotchas & Best Practices

## Overview
This document covers common pitfalls, best practices, and important considerations when applying statistical methods in data engineering workflows. Statistics is foundational for data quality assessment, outlier detection, feature engineering, and ML model preparation.

## 🚨 Critical Gotchas

### 1. **Misusing Mean vs Median**
**Gotcha**: Using mean for skewed data or data with outliers.
- **Why it's bad**: Mean is sensitive to outliers; a single extreme value can distort the central tendency.
- **Example**: In income data where 99% earn $50k and 1% earn $10M, the mean is misleading.
- **Best Practice**: 
  - Use **median** for skewed distributions or when outliers are present.
  - Use **mean** for symmetric, normally distributed data without outliers.
  - Always visualize distribution (histogram, boxplot) before choosing.

### 2. **Assuming Normal Distribution**
**Gotcha**: Applying methods that assume normality (Z-score, parametric tests) to non-normal data.
- **Why it's bad**: Many statistical methods (t-tests, ANOVA, Z-score outlier detection) assume normality. Violating this assumption leads to incorrect conclusions.
- **Best Practice**:
  - Test for normality (Shapiro-Wilk, Q-Q plots).
  - Use non-parametric alternatives (Mann-Whitney U, IQR method for outliers).
  - Consider data transformations (log, Box-Cox) for skewed data.

### 3. **Ignoring Outlier Context**
**Gotcha**: Automatically removing all outliers without understanding their cause.
- **Why it's bad**: Outliers may be legitimate data points (fraud detection, system failures, rare events) that contain valuable information.
- **Best Practice**:
  - Investigate outlier cause before removal.
  - Use domain knowledge to decide: is this a data entry error or a real phenomenon?
  - Consider robust statistics (median, IQR) that are less affected by outliers.

### 4. **Misinterpreting Correlation as Causation**
**Gotcha**: Concluding that because two variables are correlated, one causes the other.
- **Why it's bad**: Correlation ≠ causation. Spurious correlations are common (e.g., ice cream sales and drowning incidents both increase in summer).
- **Best Practice**:
  - Always consider confounding variables.
  - Use experimental design (A/B tests) for causal inference.
  - Apply domain knowledge to interpret relationships.

### 5. **Overlooking Statistical Power**
**Gotcha**: Conducting hypothesis tests with insufficient sample size.
- **Why it's bad**: Low statistical power increases Type II errors (false negatives) – failing to detect real effects.
- **Best Practice**:
  - Calculate required sample size before experiments using power analysis.
  - For A/B tests, ensure adequate sample size for desired effect size and significance level.
  - Monitor confidence intervals, not just p-values.

### 6. **Data Snooping / Multiple Testing**
**Gotcha**: Running many statistical tests without adjusting significance levels.
- **Why it's bad**: With 20 tests at α=0.05, you expect 1 false positive by chance. Uncorrected multiple testing inflates Type I errors.
- **Best Practice**:
  - Use correction methods (Bonferroni, Benjamini-Hochberg) for multiple comparisons.
  - Pre-specify hypotheses before looking at data.
  - Consider false discovery rate (FDR) instead of family-wise error rate (FWER).

### 7. **Ignoring Time Series Properties**
**Gotcha**: Applying cross-sectional statistics to time series data without considering autocorrelation.
- **Why it's bad**: Time series data points are not independent; ignoring autocorrelation violates independence assumptions.
- **Best Practice**:
  - Check for autocorrelation (ACF/PACF plots).
  - Use time series-specific methods (ARIMA, exponential smoothing).
  - Consider seasonality and trend decomposition.

## ✅ Best Practices

### 1. **Descriptive Statistics Workflow**
1. **Always visualize first**: Histogram, boxplot, Q-Q plot.
2. **Check for missing values**: Handle before analysis.
3. **Assess distribution**: Normal, skewed, multimodal?
4. **Choose appropriate measures**:
   - Central tendency: mean (normal), median (skewed), mode (categorical)
   - Dispersion: std dev (normal), IQR (skewed), range
5. **Document assumptions and decisions**.

### 2. **Outlier Detection Strategy**
1. **Use multiple methods**: IQR (robust), Z-score (normal), DBSCAN (clustering-based).
2. **Set context-aware thresholds**: 3σ for normal data, 1.5×IQR for general use.
3. **Investigate before removal**: Are outliers errors or insights?
4. **Consider winsorizing** (capping) instead of removal for mild outliers.

### 3. **Statistical Testing Protocol**
1. **Formulate clear hypotheses** (H₀, H₁) before testing.
2. **Check assumptions**: normality, independence, equal variance.
3. **Choose appropriate test**:
   - Parametric (t-test, ANOVA): when assumptions met
   - Non-parametric (Mann-Whitney, Kruskal-Wallis): when assumptions violated
4. **Report effect size** (Cohen's d, η²) not just p-value.
5. **Interpret with confidence intervals**.

### 4. **Correlation Analysis**
1. **Use appropriate correlation coefficient**:
   - Pearson's r: linear relationships, normal data
   - Spearman's ρ: monotonic relationships, ordinal/rank data
   - Kendall's τ: small samples, many tied ranks
2. **Visualize with scatter plots**.
3. **Check for non-linear relationships** (scatter plot smoothing).
4. **Be aware of Simpson's paradox** (aggregation hiding true relationships).

### 5. **Data Transformation Guidelines**
1. **Log transformation**: Right-skewed data, multiplicative effects.
2. **Square root transformation**: Count data, mild skew.
3. **Box-Cox transformation**: Automatically finds optimal transformation.
4. **Standardization (z-score)**: For algorithms requiring comparable scales.
5. **Min-max scaling**: For bounded ranges (e.g., neural networks).

### 6. **Statistical Thinking for Data Engineering**
1. **Design for reproducibility**: Set random seeds, document all steps.
2. **Quantify uncertainty**: Confidence intervals, prediction intervals.
3. **Validate assumptions**: Continuously check statistical assumptions.
4. **Communicate effectively**: Use visualizations, avoid jargon, highlight practical implications.

## 🔧 Practical Implementation Tips

### Python Libraries
- **NumPy/SciPy**: Basic statistics, distributions, hypothesis tests.
- **Pandas**: Descriptive statistics, correlation, data manipulation.
- **Statsmodels**: Advanced statistical models, hypothesis testing.
- **Scikit-learn**: Preprocessing, feature selection metrics.

### Common Patterns
```python
# Robust descriptive statistics
def robust_summary(df, column):
    return {
        'count': df[column].count(),
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std': df[column].std(),
        'iqr': df[column].quantile(0.75) - df[column].quantile(0.25),
        'skewness': df[column].skew(),
        'outliers_iqr': detect_outliers_iqr(df[column])
    }

# Outlier detection with IQR
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return series[(series < lower_bound) | (series > upper_bound)]
```

### Performance Considerations
- **Large datasets**: Use approximate statistics (streaming algorithms).
- **Distributed computing**: Implement statistical operations in Spark (approxQuantile, summary statistics).
- **Memory efficiency**: Use chunked processing for statistics on large files.

## 📊 Real-World Examples

### Example 1: Monitoring Data Pipeline
**Scenario**: Monitoring latency metrics with occasional spikes.
- **Gotcha**: Using mean latency alerts triggers false alarms due to outliers.
- **Solution**: Use 95th percentile (p95) for alerting, median for trend analysis.
- **Implementation**: `np.percentile(latencies, 95)` instead of `np.mean(latencies)`.

### Example 2: A/B Test Analysis
**Scenario**: Comparing conversion rates between two website versions.
- **Gotcha**: Running test until p < 0.05 (peeking) inflates Type I error.
- **Solution**: Pre-determine sample size, use sequential testing with correction.
- **Implementation**: Calculate required sample size using power analysis before test.

### Example 3: Data Quality Check
**Scenario**: Validating sensor data for anomalies.
- **Gotcha**: Using fixed thresholds fails when data distribution changes.
- **Solution**: Use statistical process control (control charts) with moving averages.
- **Implementation**: Shewhart control charts with 3σ limits.

## 🎯 Key Takeaways
1. **Statistics is not just math** – it requires domain knowledge and critical thinking.
2. **Always visualize** before calculating.
3. **Understand assumptions** behind statistical methods.
4. **Consider the business context** when interpreting results.
5. **Communicate uncertainty** – point estimates are incomplete without confidence intervals.

## 📚 Further Reading
- "Naked Statistics" by Charles Wheelan
- "Statistics for Data Scientists" by Peter Bruce
- "Practical Statistics for Data Scientists" by Peter Bruce & Andrew Bruce
- Scipy documentation: Statistical functions
- Pandas documentation: Descriptive statistics