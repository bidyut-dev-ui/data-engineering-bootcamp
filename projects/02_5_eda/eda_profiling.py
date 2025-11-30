import pandas as pd
import numpy as np

def perform_eda():
    print("🚀 Starting Exploratory Data Analysis...")
    
    # 1. Load Data
    df = pd.read_csv('customer_data.csv')
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns.")
    
    # 2. Basic Inspection
    print("\n--- 1. Data Types & Non-Null Counts ---")
    print(df.info())
    
    # 3. Missing Value Analysis
    print("\n--- 2. Missing Values ---")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # 4. Duplicate Analysis
    print("\n--- 3. Duplicates ---")
    dupes = df.duplicated().sum()
    print(f"Found {dupes} duplicate rows.")
    
    # 5. Numerical Distribution (Descriptive Stats)
    print("\n--- 4. Numerical Distribution ---")
    print(df.describe().round(2))
    
    # 6. Categorical Distribution
    print("\n--- 5. Categorical Counts ---")
    print(df['category'].value_counts())
    print("\nMembership:")
    print(df['membership'].value_counts(dropna=False))
    
    # 7. Correlation Analysis
    print("\n--- 6. Correlation Matrix ---")
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    print(corr.round(2))
    
    # 8. Data Quality Checks (The "Janitor" work)
    print("\n--- 7. Data Quality Flags ---")
    
    # Check 1: Negative Ages
    neg_age = df[df['age'] < 0]
    if not neg_age.empty:
        print(f"🚩 FLAG: Found {len(neg_age)} rows with negative age!")
        print(neg_age[['customer_id', 'age']])
        
    # Check 2: High Income Outliers (Z-Score > 3)
    z_scores = (df['income'] - df['income'].mean()) / df['income'].std()
    outliers = df[np.abs(z_scores) > 3]
    if not outliers.empty:
        print(f"🚩 FLAG: Found {len(outliers)} income outliers (Z > 3)!")
        print(outliers[['customer_id', 'income']])

if __name__ == "__main__":
    perform_eda()
