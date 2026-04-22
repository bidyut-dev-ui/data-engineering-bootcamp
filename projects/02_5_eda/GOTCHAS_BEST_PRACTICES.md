# EDA Gotchas & Best Practices for Data Engineers

## 🚨 Critical Gotchas (Common Mistakes)

### 1. **Memory Explosion with Large Datasets**
**Problem**: Loading entire dataset into memory for EDA on 8GB RAM machine.
```python
# WRONG: Loading 10GB CSV directly
df = pd.read_csv('10gb_file.csv')  # MemoryError!

# CORRECT: Use chunking or sampling
df_sample = pd.read_csv('10gb_file.csv', nrows=100000)  # Sample first 100k rows
# OR
chunks = pd.read_csv('10gb_file.csv', chunksize=100000)
for chunk in chunks:
    # Process each chunk
    pass
```

### 2. **Ignoring Data Types During Loading**
**Problem**: Pandas inferring wrong data types, causing memory bloat.
```python
# WRONG: Letting pandas infer everything
df = pd.read_csv('data.csv')

# CORRECT: Specify dtypes upfront
dtype_spec = {
    'customer_id': 'int32',
    'age': 'int8',
    'income': 'float32',
    'category': 'category'
}
df = pd.read_csv('data.csv', dtype=dtype_spec)
```

### 3. **Missing Value Analysis Pitfalls**
**Problem**: Treating all missing values the same.
```python
# WRONG: Simple missing count
missing = df.isnull().sum()

# CORRECT: Analyze missing patterns
# Check if missingness is random or systematic
missing_matrix = df.isnull()
# Visualize missing patterns
sns.heatmap(missing_matrix, cbar=False)
plt.savefig('missing_patterns.png')

# Check correlation of missingness
missing_corr = missing_matrix.corr()
```

### 4. **Outlier Detection Oversights**
**Problem**: Using only one method for outlier detection.
```python
# WRONG: Relying only on IQR
Q1 = df['income'].quantile(0.25)
Q3 = df['income'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['income'] < (Q1 - 1.5 * IQR)) | (df['income'] > (Q3 + 1.5 * IQR))]

# CORRECT: Multiple methods
# 1. IQR method (for symmetric distributions)
# 2. Z-score method (for normal distributions)
# 3. Percentile method (for skewed distributions)
# 4. Domain knowledge (e.g., age > 120 is impossible)
```

### 5. **Correlation Misinterpretation**
**Problem**: Assuming correlation implies causation.
```python
# WRONG: High correlation = causal relationship
corr = df.corr()
high_corr_pairs = corr[abs(corr) > 0.8]

# CORRECT: Consider spurious correlations
# 1. Check sample size (small n → unreliable correlation)
# 2. Look for confounding variables
# 3. Use partial correlation for multivariate analysis
# 4. Remember: correlation ≠ causation
```

### 6. **Visualization Deception**
**Problem**: Misleading visualizations due to scaling or binning.
```python
# WRONG: Default histogram with wrong bins
plt.hist(df['income'])
plt.show()  # May hide important patterns

# CORRECT: Thoughtful visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# Left: Histogram with optimal bins (Freedman-Diaconis rule)
axes[0].hist(df['income'], bins='fd', edgecolor='black')
axes[0].set_title('Income Distribution (FD bins)')

# Right: Log scale for skewed data
axes[1].hist(df['income'], bins='fd', edgecolor='black', log=True)
axes[1].set_title('Income Distribution (Log scale)')
plt.tight_layout()
```

### 7. **Categorical Data Mishandling**
**Problem**: Treating high-cardinality categoricals as regular columns.
```python
# WRONG: One-hot encoding everything
df_encoded = pd.get_dummies(df, columns=['city'])  # Creates 1000+ columns!

# CORRECT: Handle high cardinality
# 1. Group rare categories into 'Other'
category_counts = df['city'].value_counts()
rare_categories = category_counts[category_counts < 10].index
df['city_grouped'] = df['city'].apply(lambda x: 'Other' if x in rare_categories else x)

# 2. Use target encoding for ML
# 3. Use frequency encoding
```

### 8. **Time Series EDA Neglect**
**Problem**: Ignoring temporal patterns in time-stamped data.
```python
# WRONG: Treating time as regular column
df['timestamp'] = pd.to_datetime(df['timestamp'])
# Missing seasonality analysis

# CORRECT: Comprehensive time series EDA
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['month'] = df['timestamp'].dt.month

# Analyze seasonality
hourly_avg = df.groupby('hour')['value'].mean()
daily_avg = df.groupby('day_of_week')['value'].mean()
```

## ✅ Best Practices

### 1. **Systematic EDA Workflow**
```python
def systematic_eda_pipeline(df, output_dir='eda_results'):
    """Comprehensive EDA pipeline."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    steps = [
        ('1_data_loading', validate_data_loading),
        ('2_missing_analysis', analyze_missing_values),
        ('3_outlier_detection', detect_outliers),
        ('4_distribution_analysis', analyze_distributions),
        ('5_correlation_analysis', analyze_correlations),
        ('6_categorical_analysis', analyze_categorical),
        ('7_time_series_analysis', analyze_time_series),
        ('8_data_quality_report', generate_quality_report)
    ]
    
    results = {}
    for step_name, step_func in steps:
        print(f"Running {step_name}...")
        results[step_name] = step_func(df)
    
    return results
```

### 2. **Memory-Efficient EDA for 8GB RAM**
```python
class MemoryEfficientEDA:
    """EDA optimized for 8GB RAM constraints."""
    
    def __init__(self, max_memory_gb=6):
        self.max_memory_bytes = max_memory_gb * 1024**3
        
    def estimate_memory_needed(self, df):
        """Estimate if analysis will fit in memory."""
        estimated_memory = df.memory_usage(deep=True).sum()
        return estimated_memory < self.max_memory_bytes
    
    def chunked_analysis(self, filepath, chunksize=100000):
        """Perform EDA on large files using chunking."""
        results_accumulator = {
            'row_count': 0,
            'column_stats': {},
            'missing_counts': None,
            'min_max_values': {}
        }
        
        for chunk in pd.read_csv(filepath, chunksize=chunksize):
            # Update accumulator with chunk statistics
            results_accumulator['row_count'] += len(chunk)
            # Merge statistics intelligently
        
        return results_accumulator
```

### 3. **Automated Data Quality Scoring**
```python
def calculate_data_quality_score(df):
    """Calculate comprehensive data quality score (0-100)."""
    scores = {}
    
    # 1. Completeness (30 points)
    completeness = 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))
    scores['completeness'] = completeness * 30
    
    # 2. Validity (30 points)
    validity_checks = [
        ('age', lambda x: (x >= 0) & (x <= 120), 10),
        ('income', lambda x: x >= 0, 10),
        ('purchase_date', lambda x: pd.to_datetime(x, errors='coerce').notna().all(), 10)
    ]
    
    validity_score = 0
    for col, check_func, points in validity_checks:
        if col in df.columns:
            valid_percentage = check_func(df[col]).mean()
            validity_score += valid_percentage * points
    
    scores['validity'] = validity_score
    
    # 3. Consistency (20 points)
    # Check for logical consistency (e.g., registration_date <= purchase_date)
    
    # 4. Uniqueness (20 points)
    duplicate_score = (1 - (df.duplicated().sum() / len(df))) * 20
    scores['uniqueness'] = duplicate_score
    
    total_score = sum(scores.values())
    return {
        'total_score': total_score,
        'breakdown': scores,
        'grade': 'A' if total_score >= 90 else 'B' if total_score >= 80 else 'C' if total_score >= 70 else 'D'
    }
```

### 4. **Production-Ready EDA Configuration**
```python
EDAPipelineConfig = {
    'memory_limits': {
        'max_rows_in_memory': 1000000,
        'max_columns_in_memory': 100,
        'chunk_size': 100000
    },
    'quality_thresholds': {
        'missing_value_threshold': 0.3,  # Drop columns with >30% missing
        'outlier_threshold': 0.05,  # Flag if >5% outliers
        'correlation_threshold': 0.8,  # Flag high correlations
        'cardinality_threshold': 50  # Flag high cardinality categoricals
    },
    'visualization_settings': {
        'figure_size': (12, 8),
        'dpi': 100,
        'color_palette': 'viridis',
        'save_format': 'png'
    },
    'reporting': {
        'generate_html_report': True,
        'generate_markdown_report': True,
        'include_visualizations': True,
        'summary_level': 'detailed'
    }
}
```

### 5. **Performance Optimization Tips**
```python
# BEFORE OPTIMIZATION (Slow)
df = pd.read_csv('large_file.csv')
result = df.groupby('category')['value'].apply(lambda x: x.rolling(7).mean())

# AFTER OPTIMIZATION (Fast)
# 1. Use efficient dtypes
dtypes = {'category': 'category', 'value': 'float32'}
df = pd.read_csv('large_file.csv', dtype=dtypes, usecols=['category', 'value'])

# 2. Use vectorized operations
result = df.groupby('category')['value'].transform(lambda x: x.rolling(7).mean())

# 3. Use categorical optimization
if df['category'].nunique() < 100:
    df['category'] = df['category'].astype('category')

# 4. Memory monitoring
import psutil
def check_memory_usage():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024**2
    print(f"Memory usage: {memory_mb:.2f} MB")
    return memory_mb < 6000  # Stay under 6GB
```

## 🎯 Interview Preparation Tips

### Common EDA Interview Questions:
1. **"How would you approach EDA for a new dataset with 10 million rows?"**
   - Answer: Start with sampling (1%), check memory constraints, use chunked processing, focus on data quality first.

2. **"What would you do if you find 40% missing values in a critical column?"**
   - Answer: Investigate missing pattern (MCAR, MAR, MNAR), consult domain experts, consider imputation vs. removal, document decision.

3. **"How do you handle skewed distributions in EDA?"**
   - Answer: Use log/box-cox transformations, consider robust statistics (median/IQR instead of mean/std), visualize with appropriate scales.

4. **"What's your process for validating data quality?"**
   - Answer: Implement data quality framework (completeness, validity, consistency, timeliness), create data quality scorecard, automate checks.

### Red Flags to Mention in Interviews:
- "I found correlation of 0.95 between two variables" → Check for data leakage
- "The dataset has no missing values" → Verify if missing values were encoded as special values (-999, 999, etc.)
- "All distributions look normal" → Real-world data is rarely perfectly normal

## 📊 EDA Checklist for Data Engineers

### Phase 1: Initial Assessment
- [ ] Check dataset size and memory requirements
- [ ] Verify column names and data types
- [ ] Calculate basic statistics (min, max, mean, std)
- [ ] Identify missing values pattern

### Phase 2: Deep Dive Analysis
- [ ] Detect and analyze outliers
- [ ] Analyze distributions (histograms, Q-Q plots)
- [ ] Calculate correlations and identify multicollinearity
- [ ] Analyze categorical variables (cardinality, distribution)

### Phase 3: Data Quality Validation
- [ ] Validate against business rules
- [ ] Check for logical inconsistencies
- [ ] Verify date ranges and temporal patterns
- [ ] Test uniqueness constraints

### Phase 4: Documentation & Reporting
- [ ] Generate comprehensive EDA report
- [ ] Create visualization gallery
- [ ] Document data quality issues
- [ ] Provide actionable recommendations

## 🔗 Integration with Downstream Processes

### EDA → Data Cleaning:
```python
def eda_informed_cleaning(df, eda_results):
    """Use EDA findings to guide cleaning decisions."""
    cleaning_steps = []
    
    # Based on missing value analysis
    if eda_results['missing_percentage'] > 0.3:
        cleaning_steps.append(('drop_column', 'high_missing_column'))
    elif eda_results['missing_percentage'] < 0.05:
        cleaning_steps.append(('impute_mean', 'low_missing_column'))
    
    # Based on outlier analysis
    if eda_results['outlier_percentage'] > 0.1:
        cleaning_steps.append(('winsorize', 'outlier_prone_column'))
    
    # Based on correlation analysis
    if eda_results['high_correlation_found']:
        cleaning_steps.append(('remove_collinear', 'redundant_column'))
    
    return cleaning_steps
```

### EDA → Feature Engineering:
```python
def eda_informed_feature_engineering(df, eda_results):
    """Create features based on EDA insights."""
    features = {}
    
    # Create interaction terms from high correlations
    for col1, col2 in eda_results['highly_correlated_pairs']:
        features[f'{col1}_{col2}_interaction'] = df[col1] * df[col2]
    
    # Create outlier flags
    for col in eda_results['outlier_columns']:
        features[f'{col}_is_outlier'] = df[col].apply(
            lambda x: 1 if x in eda_results['outliers'][col] else 0
        )
    
    # Create missing value indicators
    for col in eda_results['missing_columns']:
        features[f'{col}_is_missing'] = df[col].isnull().astype(int)
    
    return pd.DataFrame(features)
```

## 🚀 Quick Reference Commands

### Essential Pandas EDA Commands:
```python
# Basic profiling
df.info(memory_usage='deep')
df.describe(include='all')
df.memory_usage(deep=True).sum() / 1024**2  # MB

# Missing values
df.isnull().sum()
df.isnull().mean() * 100  # Percentage
msno.matrix(df)  # Missingno visualization

# Outliers
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()

# Correlations
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

# Categorical analysis
df.select_dtypes(include=['object']).nunique()
df['category'].value_counts(normalize=True) * 100
```

Remember: EDA is not just about running commands—it's about developing intuition about your data and making informed decisions for downstream processing.