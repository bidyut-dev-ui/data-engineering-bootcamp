# Week 16.5: Statistics for Data Engineers

**Goal**: Understand the data you are processing before feeding it to ML models.

## Scenario
You are preparing a dataset for a Machine Learning model. If you feed it "dirty" data with extreme outliers or heavy skew, the model will fail. You need to statistically profile the data first.

## Concepts Covered
1. **Descriptive Statistics**: Mean, Median, Mode, Std Dev.
2. **Distributions**: Normal vs Skewed.
3. **Outlier Detection**:
   - **IQR Method**: Robust to extreme values.
   - **Z-Score**: Assumes normal distribution.
4. **Skewness**: Measure of asymmetry.

## Instructions

### 1. Setup
```bash
cd projects/16_5_statistics
```

### 2. Generate Data
Create a synthetic dataset with known properties (normal, skewed, and outliers).
```bash
python generate_distribution.py
```

### 3. Analyze Data
Run the statistical profiling script.
```bash
python analyze_stats.py
```

**Expected Output**:
- **Descriptive Stats**: Summary of the data.
- **Skewness**: `skewed_val` should have high positive skew.
- **Outliers**: The script should detect the manual outliers (150, 160, -20, etc.) using both IQR and Z-Score methods.

## Deep Dive

### **Mean vs Median**
- **Mean**: Average. Sensitive to outliers.
- **Median**: Middle value. Robust to outliers.
- *Example*: If Bill Gates walks into a bar, the average (mean) wealth skyrockets, but the median wealth stays roughly the same.

### **IQR (Interquartile Range)**
- `Q1`: 25th percentile
- `Q3`: 75th percentile
- `IQR = Q3 - Q1`
- Outliers are anything outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`

## Interview Questions

**Q: How do you handle missing values?**
A: Depends on the data.
- **Drop**: If rows are few.
- **Impute Mean/Median**: If data is numerical (Median is safer for skewed data).
- **Impute Mode**: For categorical data.
- **Forward Fill**: For time-series.

**Q: What is the difference between Type I and Type II errors?**
A:
- **Type I (False Positive)**: Alarm goes off, but no fire.
- **Type II (False Negative)**: Fire, but no alarm.

**Q: Why is normalization/scaling important for ML?**
A: Many algorithms (like KNN, SVM, Neural Nets) calculate distances. If one feature is 0-1 and another is 0-10000, the large feature will dominate.

## Homework / Challenge
1. Create a script `visualize.py` (if you have matplotlib installed) to plot histograms of the 3 columns.
2. Implement a "Winsorization" function to cap outliers at the 99th percentile instead of removing them.
