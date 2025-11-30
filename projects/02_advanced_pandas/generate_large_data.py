import pandas as pd
import numpy as np
import os

def generate_large_dataset(rows=1_000_000):
    print(f"Generating {rows} rows of data... this might take a moment.")
    
    # Using numpy for faster generation
    ids = np.arange(rows)
    # Random categories
    categories = np.random.choice(['Electronics', 'Clothing', 'Home', 'Garden', 'Toys'], rows)
    # Random sub-categories (more cardinality)
    sub_cats = np.random.choice([f'Item_{i}' for i in range(50)], rows)
    # Random floats
    prices = np.random.uniform(10.0, 1000.0, rows)
    # Random ints
    quantities = np.random.randint(1, 100, rows)
    
    df = pd.DataFrame({
        'transaction_id': ids,
        'category': categories,
        'sub_category': sub_cats,
        'price': prices,
        'quantity': quantities,
        'description': ['Detailed description of the item goes here ' * 5] * rows # Long string to bloat memory
    })
    
    # Save as CSV
    file_path = 'large_sales.csv'
    print(f"Saving to {file_path}...")
    df.to_csv(file_path, index=False)
    
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Done! File size: {file_size:.2f} MB")

if __name__ == "__main__":
    generate_large_dataset()
