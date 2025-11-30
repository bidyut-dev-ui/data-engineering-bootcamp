import numpy as np
import pandas as pd

def generate_data():
    np.random.seed(42)
    
    # 1. Normal Distribution (Gaussian)
    # Mean=50, StdDev=10, N=1000
    normal_data = np.random.normal(loc=50, scale=10, size=1000)
    
    # 2. Skewed Distribution (Exponential)
    # Simulates things like income, website latency (long tail)
    skewed_data = np.random.exponential(scale=10, size=1000)
    
    # 3. Add some Outliers to the normal data
    # Add 5 extreme values
    outliers = np.array([150, 160, -20, 200, 180])
    data_with_outliers = np.concatenate([normal_data, outliers])
    
    # Save to CSV
    df = pd.DataFrame({
        'normal_val': np.resize(normal_data, 1005), # Resize to match length
        'skewed_val': np.resize(skewed_data, 1005),
        'dirty_val': data_with_outliers
    })
    
    df.to_csv('stats_data.csv', index=False)
    print("✅ Generated stats_data.csv with 1005 rows.")

if __name__ == "__main__":
    generate_data()
