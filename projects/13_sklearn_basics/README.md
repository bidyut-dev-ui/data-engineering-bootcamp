# Week 17: Scikit-learn Basics

**Goal**: Learn the fundamentals of machine learning using scikit-learn: regression, classification, preprocessing, and pipelines.

## Scenario
You are a Data Scientist tasked with building predictive models. You need to predict housing prices (regression) and customer churn (classification) using historical data.

## Concepts Covered
1. **Supervised Learning**: Regression vs Classification
2. **Train/Test Split**: Preventing overfitting
3. **Preprocessing**: StandardScaler for normalization
4. **Pipelines**: Chaining transformers and estimators
5. **Model Training**: fit() and predict()
6. **Evaluation Metrics**: RMSE, R², Accuracy, Precision, Recall
7. **Feature Importance**: Understanding model decisions

## Structure
- `generate_data.py`: Creates synthetic datasets
- `01_regression.py`: Linear regression tutorial (housing prices)
- `02_classification.py`: Random forest classification (customer churn)
- `housing_data.csv`: Generated regression dataset
- `customer_churn.csv`: Generated classification dataset

## Instructions

### 1. Setup
```bash
cd projects/13_sklearn_basics
source ../00_setup_and_refresher/venv/bin/activate
pip install scikit-learn matplotlib
```

### 2. Generate Data
```bash
python generate_data.py
```

**Expected Output**:
- `housing_data.csv` (1000 samples, 5 features + price)
- `customer_churn.csv` (1000 samples, 4 features + churn label)

### 3. Run Regression Tutorial
```bash
python 01_regression.py
```

**Expected Output**:
- Training/Test RMSE and R² scores
- Feature coefficients showing impact on price
- Example prediction with actual vs predicted price

**What to Look For**:
- R² score close to 1.0 indicates good fit
- Test RMSE should be similar to training RMSE (no overfitting)

### 4. Run Classification Tutorial
```bash
python 02_classification.py
```

**Expected Output**:
- Accuracy score
- Classification report (precision, recall, F1-score)
- Confusion matrix
- Feature importance rankings

**What to Look For**:
- Accuracy > 0.80 is good
- Precision and recall should be balanced
- Feature importance shows which factors predict churn

## Homework / Challenge

### Challenge 1: Improve Regression
Modify `01_regression.py`:
1. Try different models: Ridge, Lasso, DecisionTreeRegressor
2. Add polynomial features: `PolynomialFeatures(degree=2)`
3. Compare RMSE scores - which model performs best?

### Challenge 2: Hyperparameter Tuning
Create `03_challenge.py`:
1. Use `GridSearchCV` to tune RandomForest parameters
2. Test different values for: `n_estimators`, `max_depth`, `min_samples_split`
3. Report the best parameters and improved accuracy

### Challenge 3: Real Data
Download a real dataset from [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php):
1. Load the data with pandas
2. Build a complete pipeline (preprocessing + model)
3. Evaluate and report results

## Expected Learning Outcomes
- ✅ Understand regression vs classification
- ✅ Build scikit-learn pipelines
- ✅ Evaluate model performance
- ✅ Interpret feature importance
- ✅ Avoid common pitfalls (data leakage, overfitting)
