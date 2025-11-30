import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

def main():
    print("=== Model Evaluation Tutorial ===\n")
    
    # Load data
    df = pd.read_csv('../13_sklearn_basics/housing_data.csv')
    X = df.drop('price', axis=1)
    y = df['price']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 1. Cross-Validation
    print("1. Cross-Validation (5-fold)...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    cv_scores = cross_val_score(
        pipeline, X_train, y_train,
        cv=5,
        scoring='neg_mean_squared_error'
    )
    
    cv_rmse = np.sqrt(-cv_scores)
    print(f"CV RMSE scores: {cv_rmse}")
    print(f"Mean CV RMSE: ${cv_rmse.mean():,.2f}")
    print(f"Std CV RMSE: ${cv_rmse.std():,.2f}")
    
    # 2. Hyperparameter Tuning
    print("\n2. Hyperparameter Tuning with GridSearchCV...")
    param_grid = {
        'regressor__n_estimators': [50, 100, 200],
        'regressor__max_depth': [10, 20, None],
        'regressor__min_samples_split': [2, 5, 10]
    }
    
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=3,
        scoring='neg_mean_squared_error',
        verbose=1,
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"\nBest parameters: {grid_search.best_params_}")
    print(f"Best CV RMSE: ${np.sqrt(-grid_search.best_score_):,.2f}")
    
    # 3. Final Model Evaluation
    print("\n3. Final Model Evaluation...")
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Test Set Metrics:")
    print(f"  RMSE: ${rmse:,.2f}")
    print(f"  MAE: ${mae:,.2f}")
    print(f"  R² Score: {r2:.4f}")
    
    # 4. Residual Analysis
    print("\n4. Residual Analysis...")
    residuals = y_test - y_pred
    print(f"Mean residual: ${residuals.mean():,.2f}")
    print(f"Std residual: ${residuals.std():,.2f}")
    print(f"Max overestimation: ${residuals.min():,.2f}")
    print(f"Max underestimation: ${residuals.max():,.2f}")
    
    # 5. Save Model
    print("\n5. Saving model...")
    joblib.dump(best_model, 'housing_model.joblib')
    print("Model saved to 'housing_model.joblib'")
    
    # 6. Load and Test
    print("\n6. Loading model and testing...")
    loaded_model = joblib.load('housing_model.joblib')
    test_prediction = loaded_model.predict(X_test.iloc[0:1])
    print(f"Loaded model prediction: ${test_prediction[0]:,.2f}")
    print(f"Actual price: ${y_test.iloc[0]:,.2f}")
    
    print("\n✓ Model ready for deployment!")

if __name__ == "__main__":
    main()
