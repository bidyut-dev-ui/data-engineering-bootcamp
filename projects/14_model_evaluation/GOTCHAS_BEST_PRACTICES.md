# Model Evaluation & Serialization: Gotchas & Best Practices

## 🚨 Critical Gotchas in Model Evaluation

### 1. **Data Leakage in Cross-Validation**
**WRONG:** Preprocessing entire dataset before cross-validation
```python
# WRONG: Data leakage!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Fits on ALL data
cv_scores = cross_val_score(model, X_scaled, y, cv=5)
```

**CORRECT:** Use Pipeline to keep preprocessing within each fold
```python
# CORRECT: No data leakage
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestRegressor())
])
cv_scores = cross_val_score(pipeline, X, y, cv=5)
```

**Why it matters:** Scaling with statistics from the entire dataset leaks information about the test fold into training, giving overly optimistic performance estimates.

### 2. **Memory Explosion with GridSearchCV**
**WRONG:** Using `n_jobs=-1` with large parameter grids on 8GB RAM
```python
# WRONG: Could crash on 8GB RAM
param_grid = {
    'n_estimators': [50, 100, 200, 300, 500],
    'max_depth': [5, 10, 20, 30, 50, None],
    'min_samples_split': [2, 5, 10, 20]
}
# 5 * 6 * 4 = 120 combinations, each with 5-fold CV = 600 model fits
grid = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)  # Memory disaster!
```

**CORRECT:** Use RandomizedSearchCV with limited parallelism
```python
# CORRECT: Memory-safe approach
from sklearn.model_selection import RandomizedSearchCV
param_dist = {
    'n_estimators': [50, 100, 150, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}
# Sample 20 combinations instead of all 120
random_search = RandomizedSearchCV(
    model, param_dist, n_iter=20, cv=3,  # Reduced CV folds
    n_jobs=2,  # Limited parallelism
    random_state=42
)
```

**8GB RAM Optimization:** 
- Use `n_jobs=2` instead of `-1`
- Reduce CV folds from 5 to 3 for large datasets
- Use `RandomizedSearchCV` instead of `GridSearchCV`
- Implement early stopping with memory monitoring

### 3. **Misleading R² Scores**
**WRONG:** Trusting R² without understanding its limitations
```python
# WRONG: High R² doesn't mean good model
r2 = r2_score(y_test, y_pred)
print(f"R²: {r2:.4f}")  # Could be 0.95 but predictions still terrible
```

**CORRECT:** Use multiple metrics and visualize residuals
```python
# CORRECT: Comprehensive evaluation
metrics = {
    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
    'MAE': mean_absolute_error(y_test, y_pred),
    'R²': r2_score(y_test, y_pred),
    'MAPE': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
}

# Check residual patterns
residuals = y_test - y_pred
print(f"Residual mean: {residuals.mean():.2f}")  # Should be near 0
print(f"Residual std: {residuals.std():.2f}")
```

**Why it matters:** R² can be high even with systematic errors. Always check residuals for patterns.

### 4. **Serialization Version Incompatibility**
**WRONG:** Saving models without version tracking
```python
# WRONG: No version info, hard to debug later
joblib.dump(model, 'model.joblib')
```

**CORRECT:** Include metadata and versioning
```python
# CORRECT: Versioned serialization
import joblib
from datetime import datetime
import json

metadata = {
    'model_version': '1.0.0',
    'sklearn_version': sklearn.__version__,
    'python_version': sys.version,
    'trained_at': datetime.now().isoformat(),
    'features': list(X.columns),
    'metrics': metrics,
    'hyperparameters': model.get_params()
}

# Save model with version in filename
version = 'v1_0_0'
model_path = f'model_{version}.joblib'
metadata_path = f'model_metadata_{version}.json'

joblib.dump(model, model_path, compress=3)
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2, default=str)
```

### 5. **Memory Leaks in Large-Scale Evaluation**
**WRONG:** Keeping all intermediate results in memory
```python
# WRONG: Memory grows with each fold
all_predictions = []
all_true_values = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    
    all_predictions.append(preds)  # Memory keeps growing!
    all_true_values.append(y_val)
```

**CORRECT:** Process and aggregate incrementally
```python
# CORRECT: Memory-efficient aggregation
total_rmse = 0
total_mae = 0
n_samples = 0

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    
    # Calculate metrics for this fold
    fold_rmse = np.sqrt(mean_squared_error(y_val, preds))
    fold_mae = mean_absolute_error(y_val, preds)
    
    # Weighted aggregation
    weight = len(y_val)
    total_rmse += fold_rmse * weight
    total_mae += fold_mae * weight
    n_samples += weight
    
    # Clean up to free memory
    del X_train, X_val, y_train, y_val, preds
    gc.collect()

final_rmse = total_rmse / n_samples
final_mae = total_mae / n_samples
```

## 🏆 Best Practices for Production Model Evaluation

### 1. **Comprehensive Evaluation Framework**
```python
def evaluate_model(model, X_train, X_test, y_train, y_test, 
                   cv_folds=5, memory_limit_gb=6):
    """
    Comprehensive model evaluation with memory constraints.
    """
    results = {}
    
    # 1. Cross-validation with memory monitoring
    cv_scores = cross_val_score(
        model, X_train, y_train, 
        cv=min(cv_folds, 3),  # Reduce folds if memory constrained
        scoring='neg_mean_squared_error',
        n_jobs=1  # Single job to control memory
    )
    results['cv_rmse'] = np.sqrt(-cv_scores)
    
    # 2. Test set evaluation
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    results['test_metrics'] = {
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'mae': mean_absolute_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'mape': calculate_mape(y_test, y_pred)
    }
    
    # 3. Residual analysis
    residuals = y_test - y_pred
    results['residual_stats'] = {
        'mean': residuals.mean(),
        'std': residuals.std(),
        'skew': skew(residuals),
        'kurtosis': kurtosis(residuals)
    }
    
    # 4. Memory usage tracking
    results['memory_usage_mb'] = get_memory_usage()
    
    return results
```

### 2. **Memory-Efficient Hyperparameter Tuning**
```python
def memory_safe_hyperparameter_tuning(model, param_grid, X, y, 
                                      max_memory_gb=6, timeout_hours=2):
    """
    Hyperparameter tuning with memory and time constraints.
    """
    from sklearn.model_selection import RandomizedSearchCV
    import psutil
    
    # Monitor memory
    process = psutil.Process()
    
    def memory_callback(estimator, parameters, score):
        """Callback to check memory during search"""
        memory_gb = process.memory_info().rss / 1024**3
        if memory_gb > max_memory_gb:
            raise MemoryError(f"Memory limit exceeded: {memory_gb:.1f}GB")
        return True
    
    # Use RandomizedSearchCV with limited iterations
    search = RandomizedSearchCV(
        model, param_grid,
        n_iter=10,  # Limited iterations for memory
        cv=3,       # Reduced CV folds
        scoring='neg_mean_squared_error',
        n_jobs=1,   # Single job
        random_state=42,
        pre_dispatch='1*n_jobs',  # Control parallelism
        error_score='raise'
    )
    
    # Fit with timeout
    import signal
    class TimeoutException(Exception):
        pass
    
    def timeout_handler(signum, frame):
        raise TimeoutException("Hyperparameter tuning timed out")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_hours * 3600)
    
    try:
        search.fit(X, y)
    except (MemoryError, TimeoutException) as e:
        print(f"Tuning stopped: {e}")
        # Return partial results if available
        if hasattr(search, 'cv_results_'):
            return search
        else:
            raise
    finally:
        signal.alarm(0)  # Disable alarm
    
    return search
```

### 3. **Production-Ready Model Serialization**
```python
class ModelSerializer:
    """Production-ready model serialization with versioning."""
    
    def __init__(self, base_path='models', compress_level=3):
        self.base_path = Path(base_path)
        self.compress_level = compress_level
        self.base_path.mkdir(exist_ok=True)
    
    def save(self, model, metadata, version=None):
        """Save model with metadata and versioning."""
        if version is None:
            version = self._generate_version()
        
        # Create version directory
        version_dir = self.base_path / version
        version_dir.mkdir(exist_ok=True)
        
        # Save model
        model_path = version_dir / 'model.joblib'
        joblib.dump(model, model_path, compress=self.compress_level)
        
        # Save metadata
        metadata_path = version_dir / 'metadata.json'
        full_metadata = {
            **metadata,
            'model_path': str(model_path),
            'saved_at': datetime.now().isoformat(),
            'file_size_mb': model_path.stat().st_size / 1024**2
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(full_metadata, f, indent=2, default=str)
        
        # Update latest symlink
        latest_path = self.base_path / 'latest'
        if latest_path.exists():
            latest_path.unlink()
        latest_path.symlink_to(version_dir)
        
        return version
    
    def load(self, version='latest'):
        """Load model and metadata."""
        if version == 'latest':
            version_path = self.base_path / 'latest'
            if not version_path.exists():
                raise FileNotFoundError("No latest model found")
            version_dir = version_path.resolve()
        else:
            version_dir = self.base_path / version
        
        model_path = version_dir / 'model.joblib'
        metadata_path = version_dir / 'metadata.json'
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load model
        model = joblib.load(model_path)
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return model, metadata
    
    def _generate_version(self):
        """Generate semantic version based on existing versions."""
        import re
        versions = []
        for d in self.base_path.iterdir():
            if d.is_dir() and re.match(r'v\d+\.\d+\.\d+', d.name):
                versions.append(d.name)
        
        if not versions:
            return 'v1.0.0'
        
        # Parse and increment patch version
        latest = sorted(versions)[-1]
        major, minor, patch = map(int, latest[1:].split('.'))
        return f'v{major}.{minor}.{patch + 1}'
```

### 4. **Model Monitoring and Drift Detection**
```python
class ModelMonitor:
    """Monitor model performance and data drift in production."""
    
    def __init__(self, reference_data, model, window_size=1000):
        self.reference_data = reference_data
        self.model = model
        self.window_size = window_size
        self.predictions = []
        self.actuals = []
        self.feature_stats = []
    
    def log_prediction(self, features, actual=None):
        """Log a prediction for monitoring."""
        prediction = self.model.predict([features])[0]
        
        # Store in rolling window
        self.predictions.append(prediction)
        if actual is not None:
            self.actuals.append(actual)
        
        # Store feature statistics
        feature_stats = {
            'mean': np.mean(features),
            'std': np.std(features),
            'min': np.min(features),
            'max': np.max(features)
        }
        self.feature_stats.append(feature_stats)
        
        # Maintain window size
        if len(self.predictions) > self.window_size:
            self.predictions.pop(0)
            if len(self.actuals) > self.window_size:
                self.actuals.pop(0)
            self.feature_stats.pop(0)
        
        return prediction
    
    def check_drift(self):
        """Check for prediction drift and data drift."""
        if len(self.predictions) < 100:
            return {"status": "insufficient_data"}
        
        results = {}
        
        # 1. Prediction drift (if we have actuals)
        if len(self.actuals) >= 100:
            recent_mae = mean_absolute_error(
                self.actuals[-100:], 
                self.predictions[-100:]
            )
            baseline_mae = mean_absolute_error(
                self.actuals[:100], 
                self.predictions[:100]
            )
            drift_ratio = recent_mae / baseline_mae
            results['prediction_drift'] = {
                'recent_mae': recent_mae,
                'baseline_mae': baseline_mae,
                'drift_ratio': drift_ratio,
                'drift_detected': drift_ratio > 1.5
            }
        
        # 2. Feature drift (Kolmogorov-Smirnov test)
        if len(self.feature_stats) >= 100:
            recent_features = self.feature_stats[-100:]
            baseline_features = self.feature_stats[:100]
            
            # Compare distributions for each feature stat
            for stat in ['mean', 'std']:
                recent_vals = [f[stat] for f in recent_features]
                baseline_vals = [f[stat] for f in baseline_features]
                
                # Simple threshold-based drift detection
                recent_mean = np.mean(recent_vals)
                baseline_mean = np.mean(baseline_vals)
                change_pct = abs(recent_mean - baseline_mean) / baseline_mean * 100
                
                results[f'feature_{stat}_drift'] = {
                    'change_percent': change_pct,
                    'drift_detected': change_pct > 20
                }
        
        return results
```

### 5. **8GB RAM Optimization Checklist**

#### ✅ **DO: Memory-Efficient Practices**
- Use `RandomizedSearchCV` instead of `GridSearchCV`
- Set `n_jobs=1` or `n_jobs=2` for parallel processing
- Reduce CV folds from 5 to 3 for large datasets
- Use incremental learning algorithms (`partial_fit`)
- Process data in chunks with generators
- Clear memory between folds with `del` and `gc.collect()`
- Use compressed serialization (`compress=3` in joblib)

#### ❌ **DON'T: Memory-Hungry Practices**
- Don't use `n_jobs=-1` with large parameter grids
- Don't store all intermediate predictions in memory
- Don't use 10-fold CV with large datasets
- Don't load entire dataset if you can process in chunks
- Don't use memory-inefficient data structures (lists of dicts)

#### 📊 **Memory Monitoring Tools**
```python
import psutil
import resource

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024**2

def check_memory_limit(limit_mb=6000):
    """Check if memory usage exceeds limit."""
    current_mb = get_memory_usage()
    if current_mb > limit_mb:
        raise MemoryError(f"Memory limit exceeded: {current_mb:.0f}MB > {limit_mb}MB")
    return current_mb
```

## 🎯 Key Takeaways

1. **Always use Pipelines** to prevent data leakage in cross-validation
2. **Monitor memory usage** during hyperparameter tuning and evaluation
3. **Use multiple evaluation metrics** - never rely on R² alone
4. **Implement versioned serialization** with comprehensive metadata
5. **Design for 8GB RAM constraints** from the beginning
6. **Monitor models in production** for performance drift
7. **Test serialization/deserialization** as part of your CI/CD pipeline
8. **Keep evaluation reproducible** by saving random seeds and configurations

## 🔧 Quick Reference Commands

```bash
# Monitor memory usage during evaluation
python -m memory_profiler your_evaluation_script.py

# Test model serialization/deserialization
python -c "import joblib; model = joblib.load('model.joblib'); print('Model loaded successfully')"

# Profile evaluation performance
python -m cProfile -o eval_profile.prof your_evaluation_script.py

# Check for serialization compatibility
python -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
```

By following these best practices and avoiding common gotchas, you'll build robust, production-ready model evaluation and serialization pipelines that work reliably within 8GB RAM constraints.