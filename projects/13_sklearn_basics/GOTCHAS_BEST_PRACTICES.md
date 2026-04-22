# Scikit-learn Gotchas & Best Practices

## 🚨 Critical Gotchas (Common Mistakes)

### 1. **Data Leakage in Preprocessing**
**The Problem:** Applying preprocessing (scaling, imputation) before train-test split contaminates test data with information from training data.

```python
# WRONG: Data leakage!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses entire dataset
X_train, X_test = train_test_split(X_scaled, test_size=0.2)  # Test data already seen scaling params

# CORRECT: Fit only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaling params
```

**Best Practice:** Always split data first, then fit preprocessing on training data only.

### 2. **Ignoring Class Imbalance in Classification**
**The Problem:** Accuracy can be misleading when classes are imbalanced (e.g., 95% negative, 5% positive).

```python
# WRONG: Using accuracy only
accuracy = accuracy_score(y_test, y_pred)  # Could be 95% but model predicts all negatives

# CORRECT: Use comprehensive metrics
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba)}")

# Handle imbalance
from sklearn.utils.class_weight import compute_class_weight
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
model = RandomForestClassifier(class_weight='balanced')
```

### 3. **Forgetting to Set random_state**
**The Problem:** Non-reproducible results due to random initialization in algorithms.

```python
# WRONG: Non-reproducible
model = RandomForestClassifier()  # Different results each run
X_train, X_test = train_test_split(X, test_size=0.2)  # Different splits each run

# CORRECT: Set random_state for reproducibility
model = RandomForestClassifier(random_state=42, n_estimators=100)
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
```

**Best Practice:** Always set `random_state` during development for reproducibility. Remove in production if true randomness is needed.

### 4. **Overfitting with Complex Models**
**The Problem:** Using overly complex models without regularization leads to poor generalization.

```python
# WRONG: Overly complex model
model = DecisionTreeClassifier()  # No max_depth limit - can overfit easily

# CORRECT: Use regularization and validation
from sklearn.model_selection import cross_val_score

# Simple model first
model = LogisticRegression(C=1.0, penalty='l2')
scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"CV Accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")

# Tune complexity
from sklearn.model_selection import GridSearchCV
param_grid = {'max_depth': [3, 5, 10, None]}
grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5)
```

### 5. **Misusing Pipeline with Cross-Validation**
**The Problem:** Incorrect pipeline order or missing steps in cross-validation.

```python
# WRONG: Missing preprocessing in pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
# But what about missing values? categorical encoding?

# CORRECT: Comprehensive pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

numeric_features = ['age', 'income']
categorical_features = ['gender', 'education']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])
```

## 🎯 Best Practices for Production

### 1. **Memory Optimization for 8GB RAM**

```python
# Use incremental learning for large datasets
from sklearn.linear_model import SGDClassifier
model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3)

# Process data in chunks
chunk_size = 1000
for i in range(0, len(X), chunk_size):
    chunk = X[i:i+chunk_size]
    model.partial_fit(chunk, y[i:i+chunk_size], classes=np.unique(y))

# Use sparse matrices for high-dimensional data
from scipy.sparse import csr_matrix
X_sparse = csr_matrix(X)

# Monitor memory usage
import psutil
import os
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")
```

### 2. **Feature Engineering Pipeline**
```python
# Create reusable feature engineering functions
def create_features(df):
    """Engineer features from raw data."""
    df = df.copy()
    
    # Date features
    if 'date' in df.columns:
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
    
    # Interaction features
    if all(col in df.columns for col in ['feature1', 'feature2']):
        df['feature1_x_feature2'] = df['feature1'] * df['feature2']
    
    # Statistical features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[f'{col}_log'] = np.log1p(df[col])
        df[f'{col}_squared'] = df[col] ** 2
    
    return df

# Use in pipeline
class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return create_features(X)
```

### 3. **Model Evaluation Strategy**
```python
def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Comprehensive model evaluation."""
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    # Train model
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Regression metrics
    if len(np.unique(y_train)) > 10:  # Assuming regression
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
    # Classification metrics
    else:
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'roc_auc': roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
        }
    
    return metrics
```

### 4. **Hyperparameter Tuning Best Practices**
```python
def tune_hyperparameters(model, param_grid, X_train, y_train):
    """Systematic hyperparameter tuning."""
    from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
    
    # For small parameter spaces
    grid_search = GridSearchCV(
        model, param_grid, cv=5, scoring='accuracy',
        n_jobs=-1, verbose=1, return_train_score=True
    )
    
    # For large parameter spaces
    randomized_search = RandomizedSearchCV(
        model, param_distributions=param_grid, n_iter=50,
        cv=5, scoring='accuracy', n_jobs=-1, verbose=1,
        random_state=42
    )
    
    # Fit and evaluate
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.3f}")
    
    # Analyze results
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df = results_df.sort_values('mean_test_score', ascending=False)
    
    return grid_search.best_estimator_, results_df
```

### 5. **Model Persistence and Versioning**
```python
import joblib
import json
from datetime import datetime
import hashlib

def save_model(model, feature_names, metrics, version='1.0'):
    """Save model with metadata."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_id = f"model_{timestamp}"
    
    # Create model metadata
    metadata = {
        'model_id': model_id,
        'version': version,
        'timestamp': timestamp,
        'feature_names': feature_names,
        'metrics': metrics,
        'model_type': type(model).__name__,
        'model_params': model.get_params() if hasattr(model, 'get_params') else {}
    }
    
    # Save model
    model_filename = f"{model_id}.joblib"
    joblib.dump(model, model_filename)
    
    # Save metadata
    metadata_filename = f"{model_id}_metadata.json"
    with open(metadata_filename, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Create hash for verification
    with open(model_filename, 'rb') as f:
        model_hash = hashlib.md5(f.read()).hexdigest()
    
    metadata['model_hash'] = model_hash
    
    print(f"Model saved: {model_filename}")
    print(f"Metadata saved: {metadata_filename}")
    
    return model_filename, metadata_filename

def load_model(model_filename, metadata_filename):
    """Load model with verification."""
    # Load metadata
    with open(metadata_filename, 'r') as f:
        metadata = json.load(f)
    
    # Verify model hash
    with open(model_filename, 'rb') as f:
        current_hash = hashlib.md5(f.read()).hexdigest()
    
    if current_hash != metadata.get('model_hash'):
        print("Warning: Model file may have been modified!")
    
    # Load model
    model = joblib.load(model_filename)
    
    return model, metadata
```

## 🔧 Performance Optimization

### 1. **Vectorized Operations**
```python
# WRONG: Looping through DataFrame
for i in range(len(df)):
    df.loc[i, 'new_feature'] = some_function(df.loc[i, 'old_feature'])

# CORRECT: Vectorized operations
df['new_feature'] = df['old_feature'].apply(some_function)
# Even better if function supports vectorization
df['new_feature'] = np.log1p(df['old_feature'])
```

### 2. **Efficient Cross-Validation**
```python
# Use cross_val_score for quick evaluation
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model, X, y, 
    cv=5,  # 5-fold CV
    scoring='accuracy',
    n_jobs=-1  # Parallel processing
)

# For time series, use TimeSeriesSplit
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X, y, cv=tscv, scoring='neg_mean_squared_error')
```

### 3. **Early Stopping for Iterative Algorithms**
```python
# Use early stopping to save computation
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=1000,  # Set high initial value
    learning_rate=0.1,
    subsample=0.8,
    validation_fraction=0.1,  # Use 10% for validation
    n_iter_no_change=10,  # Stop if no improvement for 10 iterations
    tol=1e-4  # Tolerance for improvement
)
```

### 4. **Memory-Efficient Data Types**
```python
# Reduce memory usage with appropriate dtypes
def reduce_memory_usage(df):
    """Reduce DataFrame memory usage."""
    start_mem = df.memory_usage().sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                else:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')
    
    end_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory reduced from {start_mem:.2f} MB to {end_mem:.2f} MB ({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)")
    
    return df
```

## 📊 Monitoring and Maintenance

### 1. **Model Drift Detection**
```python
def detect_model_drift(current_data, reference_data, model, threshold=0.05):
    """Detect if model performance has drifted."""
    from scipy import stats
    
    # Predict on both datasets
    current_pred = model.predict(current_data)
    reference_pred = model.predict(reference_data)
    
    # Compare distributions
    if len(np.unique(current_pred)) > 10:  # Regression
        current_mean = np.mean(current_pred)
        reference_mean = np.mean(reference_pred)
        drift = abs(current_mean - reference_mean) / reference_mean
    else:  # Classification
        current_probs = np.mean(current_pred)
        reference_probs = np.mean(reference_pred)
        drift = abs(current_probs - reference_probs)
    
    # Statistical test
    if len(current_pred) > 30 and len(reference_pred) > 30:
        t_stat, p_value = stats.ttest_ind(current_pred, reference_pred)
        significant_drift = p_value < 0.05
    else:
        significant_drift = drift > threshold
    
    return {
        'drift_detected': significant_drift,
        'drift_magnitude': drift,
        'p_value': p_value if 'p_value' in locals() else None,
        'threshold': threshold
    }
```

### 2. **Feature Importance Monitoring**
```python
def monitor_feature_importance(model, feature_names, top_n=10):
    """Track feature importance over time."""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_).flatten()
    else:
        return None
    
    # Create importance DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    # Track top features
    top_features = importance_df.head(top_n)
    
    # Visualize (if matplotlib available)
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance')
        plt.title('Top Feature Importances')
        plt.tight_layout()
        plt.savefig('feature_importance.png')
        plt.close()
    except ImportError:
        pass
    
    return importance_df
```

## 🚀 Quick Reference Checklist

### Before Training:
- [ ] Split data into train/validation/test sets
- [ ] Handle missing values appropriately
- [ ] Encode categorical variables
- [ ] Scale numerical features
- [ ] Check for class imbalance
- [ ] Set random_state for reproducibility

### During Training:
- [ ] Use cross-validation for robust evaluation
- [ ] Start with simple models (linear/logistic regression)
- [ ] Regularize complex models to prevent overfitting
- [ ] Monitor training progress and convergence
- [ ] Save intermediate models for comparison

### After Training:
- [ ] Evaluate on held-out test set
- [ ] Analyze feature importance
- [ ] Check for bias and fairness issues
- [ ] Document model performance and parameters
- [ ] Save model with metadata and versioning

### For Production:
- [ ] Implement monitoring for model drift
- [ ] Set up retraining pipeline
- [ ] Create A/B testing framework
- [ ] Document deployment process
- [ ] Plan for model rollback if needed

## 📚 Further Reading

1. **Scikit-learn Documentation**: https://scikit-learn.org/stable/
2. **Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow** by Aurélien Géron
3. **Python Data Science Handbook** by Jake VanderPlas
4. **Machine Learning Yearning** by Andrew Ng
5. **Interpretable Machine Learning** by Christoph Molnar

---
*Last Updated: 2026-04-20*  
*Use this guide to avoid common pitfalls and follow best practices in your scikit-learn projects.*