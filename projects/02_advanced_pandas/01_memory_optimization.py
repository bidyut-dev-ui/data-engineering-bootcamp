import pandas as pd
import numpy as np
import os

def get_memory_usage(df):
    """Returns memory usage in MB"""
    return df.memory_usage(deep=True).sum() / (1024 * 1024)

def main():
    print("=== Memory Optimization Tutorial ===")
    
    # 1. Naive Load
    print("\n1. Loading CSV naively...")
    try:
        df = pd.read_csv('large_sales.csv')
    except FileNotFoundError:
        print("Error: 'large_sales.csv' not found. Run generate_large_data.py first!")
        return

    initial_mem = get_memory_usage(df)
    print(f"Initial Memory Usage: {initial_mem:.2f} MB")
    print("\nData Types:")
    print(df.dtypes)
    
    # 2. Optimization: Downcasting Numerics
    print("\n2. Optimizing Numerics...")
    # 'transaction_id' fits in int32 (up to 2B)
    df['transaction_id'] = pd.to_numeric(df['transaction_id'], downcast='integer')
    # 'quantity' fits in int8 or int16
    df['quantity'] = pd.to_numeric(df['quantity'], downcast='integer')
    # 'price' fits in float32
    df['price'] = pd.to_numeric(df['price'], downcast='float')
    
    mem_after_numeric = get_memory_usage(df)
    print(f"Memory after numeric optimization: {mem_after_numeric:.2f} MB")
    
    # 3. Optimization: Categoricals
    print("\n3. Optimizing Strings to Categoricals...")
    # 'category' has low cardinality (only 5 unique values)
    print(f"Unique categories: {df['category'].nunique()}")
    df['category'] = df['category'].astype('category')
    
    # 'sub_category' has medium cardinality (50)
    print(f"Unique sub-categories: {df['sub_category'].nunique()}")
    df['sub_category'] = df['sub_category'].astype('category')
    
    # 'description' is high cardinality/unique, so category won't help much (and might hurt if all unique),
    # but here it is repeated, so let's see.
    # In real life, free text is hard to optimize unless you drop it.
    
    final_mem = get_memory_usage(df)
    print(f"Final Memory Usage: {final_mem:.2f} MB")
    
    savings = (initial_mem - final_mem) / initial_mem * 100
    print(f"\nTotal Savings: {savings:.1f}%")

if __name__ == "__main__":
    main()
