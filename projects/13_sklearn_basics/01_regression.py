import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def main():
    print("=== Regression Tutorial ===\n")
    
    # 1. Load Data
    print("1. Loading data...")
    df = pd.read_csv('housing_data.csv')
    print(f"Dataset shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    
    # 2. Prepare Features and Target
    print("\n2. Preparing features and target...")
    X = df.drop('price', axis=1)
    y = df['price']
    print(f"Features: {list(X.columns)}")
    print(f"Target: price")
    
    # 3. Split Data
    print("\n3. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # 4. Create Pipeline
    print("\n4. Creating ML pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Normalize features
        ('regressor', LinearRegression())  # Linear regression model
    ])
    print("Pipeline steps:")
    print("  - StandardScaler: Normalize features to mean=0, std=1")
    print("  - LinearRegression: Fit linear model")
    
    # 5. Train Model
    print("\n5. Training model...")
    pipeline.fit(X_train, y_train)
    print("Training complete!")
    
    # 6. Make Predictions
    print("\n6. Making predictions...")
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)
    
    # 7. Evaluate
    print("\n7. Evaluating model...")
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print(f"\nTraining Set:")
    print(f"  RMSE: ${train_rmse:,.2f}")
    print(f"  R² Score: {train_r2:.4f}")
    
    print(f"\nTest Set:")
    print(f"  RMSE: ${test_rmse:,.2f}")
    print(f"  R² Score: {test_r2:.4f}")
    
    # 8. Feature Importance
    print("\n8. Feature coefficients:")
    model = pipeline.named_steps['regressor']
    for feature, coef in zip(X.columns, model.coef_):
        print(f"  {feature}: {coef:,.2f}")
    
    # 9. Example Prediction
    print("\n9. Example prediction:")
    example = X_test.iloc[0:1]
    print(f"Input features:\n{example}")
    prediction = pipeline.predict(example)[0]
    actual = y_test.iloc[0]
    print(f"\nPredicted price: ${prediction:,.2f}")
    print(f"Actual price: ${actual:,.2f}")
    print(f"Error: ${abs(prediction - actual):,.2f}")

if __name__ == "__main__":
    main()
