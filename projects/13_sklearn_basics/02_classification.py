import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def main():
    print("=== Classification Tutorial ===\n")
    
    # 1. Load Data
    print("1. Loading data...")
    df = pd.read_csv('customer_churn.csv')
    print(f"Dataset shape: {df.shape}")
    print(f"Churn distribution:\n{df['churned'].value_counts()}")
    
    # 2. Prepare Features and Target
    print("\n2. Preparing features and target...")
    X = df.drop('churned', axis=1)
    y = df['churned']
    
    # 3. Split Data
    print("\n3. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Create Pipeline
    print("\n4. Creating ML pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # 5. Train Model
    print("\n5. Training model...")
    pipeline.fit(X_train, y_train)
    print("Training complete!")
    
    # 6. Make Predictions
    print("\n6. Making predictions...")
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)
    
    # 7. Evaluate
    print("\n7. Evaluating model...")
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Churned', 'Churned']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"True Negatives: {cm[0,0]}")
    print(f"False Positives: {cm[0,1]}")
    print(f"False Negatives: {cm[1,0]}")
    print(f"True Positives: {cm[1,1]}")
    
    # 8. Feature Importance
    print("\n8. Feature importance:")
    model = pipeline.named_steps['classifier']
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"  {feature}: {importance:.4f}")
    
    # 9. Example Prediction
    print("\n9. Example prediction:")
    example = X_test.iloc[0:1]
    print(f"Input features:\n{example}")
    prediction = pipeline.predict(example)[0]
    probability = pipeline.predict_proba(example)[0]
    actual = y_test.iloc[0]
    print(f"\nPredicted: {'Churned' if prediction == 1 else 'Not Churned'}")
    print(f"Probability: {probability[1]:.2%} chance of churn")
    print(f"Actual: {'Churned' if actual == 1 else 'Not Churned'}")

if __name__ == "__main__":
    main()
