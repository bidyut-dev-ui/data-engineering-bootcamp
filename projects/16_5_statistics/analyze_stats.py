import pandas as pd
import numpy as np

def analyze_stats():
    df = pd.read_csv('stats_data.csv')
    
    print("=== DATASET STATISTICS ===")
    print(f"Total Rows: {len(df)}")
    
    # 1. Basic Stats
    print("\n--- 1. Descriptive Statistics ---")
    print(df.describe().round(2))
    
    # 2. Skewness
    print("\n--- 2. Skewness ---")
    # 0 = Symmetrical, >0 = Right skewed (tail right), <0 = Left skewed
    skew = df.skew().round(2)
    print(skew)
    print("\nInterpretation:")
    print(f"Normal Val Skew: {skew['normal_val']} (Close to 0 = Symmetrical)")
    print(f"Skewed Val Skew: {skew['skewed_val']} (High positive = Right tail)")
    
    # 3. Outlier Detection (IQR Method)
    print("\n--- 3. Outlier Detection (IQR Method) ---")
    col = 'dirty_val'
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"Column: {col}")
    print(f"IQR: {IQR:.2f}")
    print(f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
    print(f"Found {len(outliers)} outliers:")
    print(outliers.values)
    
    # 4. Z-Score Method
    print("\n--- 4. Outlier Detection (Z-Score Method) ---")
    mean = df[col].mean()
    std = df[col].std()
    z_scores = (df[col] - mean) / std
    
    # Usually Z > 3 or Z < -3 is an outlier
    z_outliers = df[np.abs(z_scores) > 3][col]
    print(f"Found {len(z_outliers)} outliers (Z > 3):")
    print(z_outliers.values)

if __name__ == "__main__":
    analyze_stats()
