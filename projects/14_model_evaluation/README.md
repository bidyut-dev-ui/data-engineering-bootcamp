# Week 18: Model Evaluation & Serialization

**Goal**: Learn how to properly evaluate ML models using cross-validation, tune hyperparameters, and save/load models for production use.

## Scenario
You've built a model, but how do you know if it's good enough? You need to evaluate it rigorously, optimize its parameters, and prepare it for deployment.

## Concepts Covered
1. **Cross-Validation**: K-fold CV for robust evaluation
2. **Hyperparameter Tuning**: GridSearchCV and RandomizedSearchCV
3. **Evaluation Metrics**: RMSE, MAE, R² for regression
4. **Residual Analysis**: Understanding prediction errors
5. **Model Serialization**: Saving with joblib and pickle
6. **Model Versioning**: Tracking model versions
7. **Metadata Management**: Storing model information

## Structure
- `01_evaluation.py`: Cross-validation and hyperparameter tuning
- `02_serialization.py`: Saving, loading, and versioning models
- `housing_model.joblib`: Saved model file
- `model_metadata.json`: Model tracking information

## Instructions

### 1. Setup
```bash
cd projects/14_model_evaluation
source ../00_setup_and_refresher/venv/bin/activate
pip install scikit-learn joblib
```

### 2. Run Evaluation Tutorial
```bash
python 01_evaluation.py
```

**Expected Output**:
- 5-fold cross-validation scores
- GridSearchCV progress (testing 27 parameter combinations)
- Best parameters found
- Final test set metrics
- Saved model file: `housing_model.joblib`

**What to Look For**:
- CV scores should be consistent (low std deviation)
- Best model should improve over baseline
- Test RMSE should match CV RMSE (no overfitting)

### 3. Run Serialization Tutorial
```bash
python 02_serialization.py
```

**Expected Output**:
- Loaded model confirmation
- Predictions on new data
- Metadata JSON file created
- Versioned model saved

## Homework / Challenge

### Challenge 1: Compare Models
Create `03_challenge.py`:
1. Train 3 different models: LinearRegression, RandomForest, GradientBoosting
2. Use cross-validation to compare them
3. Save the best model with appropriate metadata

### Challenge 2: Custom Scoring
Modify `01_evaluation.py`:
1. Create a custom scorer that penalizes overestimation more than underestimation
2. Use it in GridSearchCV
3. Compare results with standard RMSE

### Challenge 3: Model Registry
Create `model_registry.py`:
1. Build a simple model registry (dict or SQLite)
2. Store: model_id, version, metrics, file_path, created_at
3. Functions: register_model(), get_best_model(), list_models()

## Expected Learning Outcomes
- ✅ Perform robust model evaluation
- ✅ Tune hyperparameters systematically
- ✅ Save and load models correctly
- ✅ Track model versions and metadata
- ✅ Understand when a model is production-ready
