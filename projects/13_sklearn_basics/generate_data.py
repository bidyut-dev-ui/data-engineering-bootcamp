import pandas as pd
import numpy as np
from sklearn.datasets import make_regression, make_classification

def generate_regression_data():
    """Generate synthetic housing price data"""
    print("Generating regression dataset...")
    
    # Create features
    X, y = make_regression(
        n_samples=1000,
        n_features=5,
        noise=10,
        random_state=42
    )
    
    # Create DataFrame with meaningful names
    df = pd.DataFrame(X, columns=[
        'square_feet',
        'bedrooms',
        'bathrooms',
        'age_years',
        'distance_to_city'
    ])
    
    # Scale features to realistic ranges
    df['square_feet'] = (df['square_feet'] * 500 + 1500).astype(int)
    df['bedrooms'] = (df['bedrooms'] * 1 + 3).clip(1, 6).astype(int)
    df['bathrooms'] = (df['bathrooms'] * 0.5 + 2).clip(1, 4).astype(int)
    df['age_years'] = (df['age_years'] * 10 + 15).clip(0, 50).astype(int)
    df['distance_to_city'] = (df['distance_to_city'] * 5 + 10).clip(1, 30)
    
    # Scale target to realistic prices
    df['price'] = (y * 50000 + 300000).clip(100000, 1000000)
    
    df.to_csv('housing_data.csv', index=False)
    print(f"Created housing_data.csv with {len(df)} samples")
    return df

def generate_classification_data():
    """Generate synthetic customer churn data"""
    print("\nGenerating classification dataset...")
    
    X, y = make_classification(
        n_samples=1000,
        n_features=4,
        n_informative=3,
        n_redundant=1,
        random_state=42
    )
    
    df = pd.DataFrame(X, columns=[
        'tenure_months',
        'monthly_charges',
        'total_charges',
        'support_calls'
    ])
    
    # Scale to realistic ranges
    df['tenure_months'] = (df['tenure_months'] * 12 + 24).clip(1, 72).astype(int)
    df['monthly_charges'] = (df['monthly_charges'] * 20 + 50).clip(20, 150)
    df['total_charges'] = df['tenure_months'] * df['monthly_charges']
    df['support_calls'] = (df['support_calls'] * 2 + 3).clip(0, 10).astype(int)
    df['churned'] = y
    
    df.to_csv('customer_churn.csv', index=False)
    print(f"Created customer_churn.csv with {len(df)} samples")
    return df

if __name__ == "__main__":
    generate_regression_data()
    generate_classification_data()
    print("\nData generation complete!")
