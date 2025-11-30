import sys
sys.path.append('../13_sklearn_basics')
sys.path.append('../14_model_evaluation')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

def train_model():
    """Train and save the housing price model"""
    print("Training housing price prediction model...\n")
    
    # Load data
    print("1. Loading data...")
    df = pd.read_csv('../13_sklearn_basics/housing_data.csv')
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Split
    print("2. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create pipeline
    print("3. Creating pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            random_state=42
        ))
    ])
    
    # Train
    print("4. Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    print("5. Evaluating...")
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    print(f"   Train R²: {train_score:.4f}")
    print(f"   Test R²: {test_score:.4f}")
    
    # Save
    print("6. Saving model...")
    joblib.dump(pipeline, 'housing_model.joblib')
    print("   Saved to housing_model.joblib")
    
    print("\n✓ Training complete!")

if __name__ == "__main__":
    train_model()
