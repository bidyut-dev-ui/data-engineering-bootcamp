import pandas as pd
import numpy as np
import random

def create_messy_dataset():
    np.random.seed(42)
    n_rows = 1000
    
    # 1. Base Data
    data = {
        'customer_id': range(1, n_rows + 1),
        'age': np.random.normal(35, 10, n_rows).astype(int),
        'income': np.random.exponential(50000, n_rows),
        'purchase_amount': np.random.uniform(10, 1000, n_rows),
        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], n_rows),
        'membership': np.random.choice(['Gold', 'Silver', 'Bronze', None], n_rows, p=[0.1, 0.3, 0.5, 0.1])
    }
    
    df = pd.DataFrame(data)
    
    # 2. Add Correlations (Rich get richer)
    # Higher income -> Higher purchase amount
    df['purchase_amount'] += df['income'] * 0.01
    
    # 3. Inject Messiness
    
    # Missing Values
    df.loc[np.random.choice(df.index, 50), 'age'] = np.nan
    df.loc[np.random.choice(df.index, 20), 'income'] = np.nan
    
    # Duplicates
    duplicates = df.sample(20)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Bad Data (Negative Age)
    df.loc[np.random.choice(df.index, 5), 'age'] = -5
    
    # Bad Data (Outliers in Income)
    df.loc[np.random.choice(df.index, 3), 'income'] = 10_000_000
    
    # Save
    df.to_csv('customer_data.csv', index=False)
    print(f"✅ Created customer_data.csv with {len(df)} rows.")

if __name__ == "__main__":
    create_messy_dataset()
