# Week 2.5: Exploratory Data Analysis (EDA)

**Goal**: Learn to "see" the data before you process it.

## Why This Matters
If you ingest garbage, you produce garbage. A Data Engineer must profile data to detect schema violations, missing values, and outliers *before* building the pipeline.

## Scenario
You received a `customer_data.csv` file from the marketing team. They claim it's "clean". Your job is to prove them wrong using EDA.

## Concepts Covered
1. **Profiling**: `df.info()`, `df.describe()`, `df.value_counts()`.
2. **Missingness**: Detecting `NaN` patterns.
3. **Correlations**: Understanding relationships (e.g., Income vs Purchase).
4. **Data Quality Flags**: Writing logic to catch impossible values (Age < 0).

## Instructions

### 1. Setup
```bash
cd projects/02_5_eda
```

### 2. Generate Data
Create the "messy" dataset.
```bash
python generate_dataset.py
```

### 3. Perform EDA (Profiling)
Run the profiling script to uncover the issues textually.
```bash
python eda_profiling.py
```

### 4. Perform Visual EDA (Plots)
Generate visualizations to see the patterns.
```bash
pip install -r requirements.txt
python visual_eda.py
```
*Check the `plots/` directory for the generated images.*

**Expected Findings**:
- **Boxplots**: You will see dots outside the whiskers for `income` (Outliers).
- **Heatmap**: You will see a red square (high correlation) between `income` and `purchase_amount`.
- **Pairplot**: You might see clusters of customers based on category.

## Interview Questions

**Q: Why use a Boxplot over a Histogram for outlier detection?**
A: Boxplots explicitly show the IQR and mark outliers as individual points. Histograms can hide outliers in the "long tail".

**Q: What does a Heatmap tell you that `df.corr()` doesn't?**
A: It's the same data, but color-coding makes patterns pop out instantly. You can spot multicollinearity (redundant features) in seconds.

**Q: When would you use a Pairplot?**
A: When exploring a new dataset to see how *every* variable relates to *every other* variable. It's great for spotting linear relationships or clusters.

**Q: How do you handle high cardinality categorical columns?**
A: If a column has too many unique values (e.g., User ID), `value_counts()` is useless. Check `df['col'].nunique()` instead.

**Q: Why is correlation important for a Data Engineer?**
A: It helps identify redundant features (multicollinearity) or validate data relationships (e.g., Tax should correlate with Price).

## Homework / Challenge
1. Create a visualization script using `matplotlib` to plot a Histogram of Age and a Scatter Plot of Income vs Purchase.
2. Write a cleaning function that:
   - Drops duplicates.
   - Fills missing Age with the Median.
   - Replaces negative ages with `NaN` or the Mean.
