# Statistics for Data Engineers: Interview Questions

## Overview
This document contains interview questions covering statistical concepts essential for data engineering roles. Questions range from fundamental concepts to advanced applications in data pipelines, monitoring, and machine learning.

## 📊 Fundamental Statistics Questions

### 1. **Descriptive Statistics**
1. **What's the difference between mean, median, and mode? When would you use each?**
   - **Expected Answer**: Mean is average (sensitive to outliers), median is middle value (robust to outliers), mode is most frequent value. Use mean for symmetric distributions, median for skewed data, mode for categorical data.
   - **Follow-up**: In a dataset of household incomes with a few billionaires, which measure best represents "typical" income?

2. **How do you calculate variance and standard deviation? What do they tell you about the data?**
   - **Expected Answer**: Variance measures average squared deviation from mean; standard deviation is square root of variance (in original units). They quantify data spread/dispersion.
   - **Follow-up**: Why use standard deviation instead of variance for interpretation?

3. **What are quartiles and the interquartile range (IQR)? How are they useful?**
   - **Expected Answer**: Quartiles divide data into four equal parts (Q1=25th percentile, Q2=median, Q3=75th percentile). IQR = Q3 - Q1 measures middle 50% spread. Useful for outlier detection and robust statistics.
   - **Follow-up**: How would you use IQR to detect outliers?

### 2. **Distributions**
4. **What is a normal distribution? Why is it important in statistics?**
   - **Expected Answer**: Bell-shaped, symmetric distribution defined by mean and standard deviation. Important because many statistical methods assume normality (Central Limit Theorem).
   - **Follow-up**: What happens when you apply methods assuming normality to non-normal data?

5. **What is skewness? How does it affect statistical analysis?**
   - **Expected Answer**: Skewness measures distribution asymmetry. Positive skew = right tail longer, negative skew = left tail longer. Affects choice of central tendency measure and validity of parametric tests.
   - **Follow-up**: How would you handle positively skewed data in a regression model?

6. **What is kurtosis? What does high/low kurtosis indicate?**
   - **Expected Answer**: Kurtosis measures "tailedness" (peakedness and tail thickness). High kurtosis = heavy tails (more outliers), low kurtosis = light tails (fewer outliers).
   - **Follow-up**: Why is kurtosis important for risk modeling in finance?

### 3. **Outlier Detection**
7. **What methods would you use to detect outliers in a dataset?**
   - **Expected Answer**: IQR method (Q1 - 1.5×IQR, Q3 + 1.5×IQR), Z-score (|z| > 3), DBSCAN clustering, isolation forest, visual methods (box plots, scatter plots).
   - **Follow-up**: When would you prefer IQR over Z-score method?

8. **Should you always remove outliers? Why or why not?**
   - **Expected Answer**: No. Investigate cause first: outliers may be errors (remove) or valuable insights (keep/analyze separately). Consider business context and downstream impact.
   - **Follow-up**: Give an example where outliers should be kept vs. removed.

9. **What is winsorizing? When would you use it?**
   - **Expected Answer**: Winsorizing caps extreme values at specified percentiles (e.g., 5th and 95th). Useful when you want to reduce outlier impact without removing data points entirely.
   - **Follow-up**: Compare winsorizing with trimming (removing outliers).

## 🔬 Statistical Inference & Testing

### 4. **Hypothesis Testing**
10. **Explain the concept of p-value. What does p < 0.05 mean?**
    - **Expected Answer**: P-value = probability of observing data as extreme as actual data, assuming null hypothesis is true. p < 0.05 means <5% chance of observing this data if null is true (reject null at 5% significance).
    - **Follow-up**: What are common misinterpretations of p-values?

11. **What are Type I and Type II errors? How do they relate to significance level and power?**
    - **Expected Answer**: Type I = false positive (reject true null), Type II = false negative (fail to reject false null). Significance level (α) controls Type I error; power (1-β) controls Type II error.
    - **Follow-up**: In an A/B test for a new feature, which error is more costly?

12. **When would you use a t-test vs. z-test?**
    - **Expected Answer**: t-test: small samples (<30) or unknown population variance. z-test: large samples (≥30) with known population variance. t-test uses t-distribution (heavier tails).
    - **Follow-up**: What happens to t-distribution as sample size increases?

### 5. **Confidence Intervals**
13. **What is a confidence interval? How do you interpret a 95% CI?**
    - **Expected Answer**: Range of plausible values for population parameter. 95% CI means if we repeated sampling many times, 95% of intervals would contain true parameter.
    - **Follow-up**: Why is "95% probability that parameter is in the interval" incorrect?

14. **How does sample size affect confidence interval width?**
    - **Expected Answer**: Larger sample size → narrower confidence interval (more precise estimate). Width ∝ 1/√n.
    - **Follow-up**: If you want to halve the CI width, how much must you increase sample size?

### 6. **Correlation & Regression**
15. **What's the difference between correlation and causation?**
    - **Expected Answer**: Correlation measures association; causation implies one variable directly affects another. Correlation ≠ causation due to confounding variables, reverse causality, coincidence.
    - **Follow-up**: Give an example of spurious correlation.

16. **When would you use Pearson vs. Spearman correlation?**
    - **Expected Answer**: Pearson: linear relationships, interval/ratio data, normal distribution. Spearman: monotonic relationships, ordinal data, non-normal distributions, robust to outliers.
    - **Follow-up**: If data has outliers, which correlation coefficient is more appropriate?

17. **What is R-squared in regression? What are its limitations?**
    - **Expected Answer**: R² = proportion of variance in dependent variable explained by model. Limitations: increases with more predictors (even irrelevant ones), doesn't indicate causation, sensitive to outliers.
    - **Follow-up**: Why might a high R² not indicate a good model?

## 🏗️ Statistics in Data Engineering

### 7. **Data Quality & Monitoring**
18. **How would you use statistics to monitor data pipeline health?**
    - **Expected Answer**: Track descriptive statistics (mean, median, std dev) over time, set control limits (3σ), monitor for distribution shifts, detect anomalies with statistical tests.
    - **Follow-up**: What statistical methods would you use for real-time anomaly detection?

19. **What statistical metrics would you track for data quality?**
    - **Expected Answer**: Completeness (missing rate), consistency (value distributions over time), accuracy (error rate vs ground truth), uniqueness (duplicate rate), validity (out-of-range values).
    - **Follow-up**: How would you statistically test if data quality has degraded?

20. **How would you handle missing data statistically?**
    - **Expected Answer**: Assess missingness pattern (MCAR, MAR, MNAR). Options: deletion (if MCAR and small %), imputation (mean/median/mode, regression, KNN), model-based methods (MICE).
    - **Follow-up**: When is mean imputation inappropriate?

### 8. **A/B Testing & Experimentation**
21. **How do you determine sample size for an A/B test?**
    - **Expected Answer**: Based on desired significance level (α), power (1-β), minimum detectable effect (MDE), and baseline conversion rate. Use power analysis formulas or calculators.
    - **Follow-up**: What happens if you run a test with insufficient sample size?

22. **What is sequential testing and why is it useful?**
    - **Expected Answer**: Evaluating results as data accumulates, stopping early if significant. Useful for reducing sample size/time while controlling Type I error (using methods like SPRT, O'Brien-Fleming).
    - **Follow-up**: What's the risk of "peeking" at results without proper sequential testing?

23. **How would you analyze an A/B test with multiple metrics?**
    - **Expected Answer**: Use multiple testing correction (Bonferroni, Benjamini-Hochberg) to control family-wise error rate or false discovery rate. Pre-specify primary vs secondary metrics.
    - **Follow-up**: What's the difference between FWER and FDR control?

### 9. **Time Series Analysis**
24. **What statistical properties are unique to time series data?**
    - **Expected Answer**: Autocorrelation (correlation with past values), seasonality, trend, non-stationarity. Requires specialized methods (ARIMA, exponential smoothing).
    - **Follow-up**: Why can't you use regular correlation for time series?

25. **How would you detect seasonality in time series data?**
    - **Expected Answer**: Visual methods (time series plot, seasonal subseries plot), autocorrelation function (ACF) showing peaks at seasonal lags, decomposition methods (STL, seasonal decomposition).
    - **Follow-up**: What statistical test would you use for seasonality?

## 🤖 Statistics for Machine Learning

### 10. **Feature Engineering & Selection**
26. **How would you use statistics for feature selection?**
    - **Expected Answer**: Correlation analysis (remove highly correlated features), statistical tests (t-test, ANOVA for categorical targets), mutual information, variance threshold (remove low-variance features).
    - **Follow-up**: What's the problem with using correlation for feature selection with non-linear relationships?

27. **What is feature scaling and why is it important?**
    - **Expected Answer**: Scaling features to comparable ranges (standardization: mean=0, std=1; normalization: min=0, max=1). Important for distance-based algorithms (k-means, SVM, neural networks).
    - **Follow-up**: When would you use standardization vs. normalization?

### 11. **Model Evaluation**
28. **What statistical metrics would you use to evaluate classification models?**
    - **Expected Answer**: Accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix. Choose based on business objective (e.g., precision for spam detection, recall for medical diagnosis).
    - **Follow-up**: Why is accuracy misleading for imbalanced datasets?

29. **How would you statistically compare two machine learning models?**
    - **Expected Answer**: Use paired statistical tests: paired t-test for performance metrics, McNemar's test for classification errors, Wilcoxon signed-rank test for non-normal differences.
    - **Follow-up**: What's the null hypothesis when comparing two models?

### 12. **Bias-Variance Tradeoff**
30. **Explain the bias-variance tradeoff in statistical terms.**
    - **Expected Answer**: Total error = bias² + variance + irreducible error. High bias = underfitting (model too simple), high variance = overfitting (model too complex). Tradeoff: reducing one increases the other.
    - **Follow-up**: How does regularization affect bias and variance?

## 💼 Behavioral & Scenario Questions

### 13. **Problem-Solving Scenarios**
31. **You notice a sudden spike in error rates in your data pipeline. How would you investigate using statistics?**
    - **Expected Answer**: Check if spike is statistically significant (control chart, hypothesis test). Compare distributions before/after spike. Analyze correlated metrics. Use root cause analysis with statistical evidence.
    - **Evaluation**: Looks for systematic approach, use of statistical methods, consideration of multiple factors.

32. **A stakeholder claims a new feature increased conversion by 5%. How would you validate this statistically?**
    - **Expected Answer**: Check A/B test design (randomization, sample size, duration). Calculate statistical significance (p-value, confidence interval). Consider multiple testing if looking at multiple metrics. Assess practical significance (effect size).
    - **Evaluation**: Looks for understanding of experimental design, statistical testing, and business context.

33. **You're building a monitoring system for data quality. What statistical thresholds would you set and why?**
    - **Expected Answer**: Use control limits (3σ for normally distributed metrics), percentiles (p95, p99 for latency), IQR-based thresholds for skewed data. Consider false positive rate and alert fatigue.
    - **Evaluation**: Looks for practical application of statistical methods to real-world monitoring.

### 14. **Communication & Interpretation**
34. **How would you explain a confidence interval to a non-technical stakeholder?**
    - **Expected Answer**: "We're 95% confident that the true value lies between X and Y. If we repeated this measurement 100 times, about 95 of those intervals would contain the actual value."
    - **Evaluation**: Clear, accurate, avoids technical jargon.

35. **A data scientist presents a model with p < 0.001. What questions would you ask?**
    - **Expected Answer**: Effect size? Practical significance? Sample size? Assumptions met? Multiple testing corrected? Business impact?
    - **Evaluation**: Critical thinking beyond statistical significance.

## 📈 Advanced Topics

### 15. **Bayesian Statistics**
36. **What's the difference between frequentist and Bayesian statistics?**
    - **Expected Answer**: Frequentist: probability as long-run frequency, fixed parameters. Bayesian: probability as degree of belief, parameters as random variables with prior distributions updated to posteriors via Bayes' theorem.
    - **Follow-up**: When would you prefer Bayesian methods?

37. **What is a prior in Bayesian statistics? How does it affect results?**
    - **Expected Answer**: Prior represents initial beliefs about parameters before seeing data. Strong priors dominate with small samples; weak priors have less influence. Results are posterior distribution combining prior and likelihood.
    - **Follow-up**: What's the difference between informative and non-informative priors?

### 16. **Non-Parametric Statistics**
38. **When would you use non-parametric statistical methods?**
    - **Expected Answer**: When data doesn't meet parametric assumptions (normality, equal variance, interval scale), with small samples, ordinal data, or when robustness to outliers is needed.
    - **Follow-up**: Give examples of non-parametric alternatives to common parametric tests.

### 17. **Statistical Power**
39. **What factors affect statistical power?**
    - **Expected Answer**: Sample size (↑n → ↑power), effect size (↑effect → ↑power), significance level (↑α → ↑power), variability (↑σ → ↓power), test type (one-tailed vs two-tailed).
    - **Follow-up**: How would you increase power without increasing sample size?

## 🎯 Preparation Tips

### Technical Preparation
1. **Review fundamental concepts**: Descriptive statistics, distributions, hypothesis testing, confidence intervals.
2. **Practice calculations**: Mean, median, variance, standard deviation, correlation coefficients.
3. **Understand assumptions**: Know when different statistical methods are appropriate.
4. **Study real applications**: A/B testing, anomaly detection, monitoring, data quality.

### Interview Strategy
1. **Think aloud**: Explain your reasoning process.
2. **Ask clarifying questions**: Understand the problem context before answering.
3. **Consider multiple approaches**: Mention alternative methods and tradeoffs.
4. **Connect to business impact**: Explain why statistical findings matter.
5. **Admit uncertainty**: It's okay to say "I would look up that specific formula" or "I'd consult a statistician for advanced methods."

### Common Pitfalls to Avoid
1. **Confusing correlation with causation**.
2. **Misinterpreting p-values** (e.g., "p=0.04 means there's a 96% chance the alternative is true").
3. **Ignoring assumptions** of statistical tests.
4. **Overlooking practical significance** (statistical ≠ practical significance).
5. **Not considering multiple testing** when evaluating multiple metrics.

## 📚 Resources for Further Study
- **Books**: "Practical Statistics for Data Scientists", "Naked Statistics", "Statistics for Data Science"
- **Online courses**: Coursera "Statistics with Python", Khan Academy Statistics
- **Practice**: LeetCode statistics problems, real-world datasets on Kaggle
- **Tools**: Python (pandas, scipy, statsmodels), R, Jupyter notebooks for experimentation