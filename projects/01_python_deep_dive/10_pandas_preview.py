"""
Pandas Preview: See how Python concepts map to Pandas code
This script demonstrates why you learned all those "boring" Python concepts!
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("="*60)
print("PANDAS PREVIEW: PYTHON CONCEPTS IN ACTION")
print("="*60)

# 1. SETUP: Using Context Managers & Pathlib
# ==========================================
print("\n1. Context Managers & Pathlib")
# Why you learned: with open(...), Path()

data_path = Path('dummy_sales.csv')

# Create dummy data safely
with open(data_path, 'w') as f:
    f.write("order_id,product,price,qty,date\n")
    f.write("1001,Widget A,10.0,5,2024-01-01\n")
    f.write("1002,Widget B,20.0,2,2024-01-02\n")
    f.write("1003,Widget A,10.0,10,2024-01-03\n")
    f.write("1004,Widget C,50.0,1,2024-01-04\n")

print("Created dummy CSV using context manager.")

# 2. LOADING: Using Callables (read_csv)
# ======================================
print("\n2. Loading Data")
df = pd.read_csv(data_path)
print(f"Loaded DataFrame shape: {df.shape}")

# 3. COMPREHENSIONS: Filtering Columns
# ====================================
print("\n3. Comprehensions")
# Why you learned: [x for x in list if condition]

# Get numeric columns only
numeric_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
print(f"Numeric columns: {numeric_cols}")

# 4. LAMBDA FUNCTIONS: Transformations
# ====================================
print("\n4. Lambda Functions")
# Why you learned: lambda x: x + 1

# Add a 'total' column
# assign() takes a callable (lambda) that receives the DataFrame
df = df.assign(
    total=lambda d: d['price'] * d['qty'],
    is_large_order=lambda d: d['qty'] > 5
)
print("Added 'total' and 'is_large_order' columns using lambdas.")
print(df[['order_id', 'total', 'is_large_order']].head(2))

# 5. UNPACKING: Splitting Data
# ============================
print("\n5. Unpacking")
# Why you learned: a, *b = list

# Split columns into ID and Features
id_col, *features = df.columns
print(f"ID Column: {id_col}")
print(f"Feature Columns: {features}")

# 6. ITERATORS: Looping over Rows
# ===============================
print("\n6. Iterators")
# Why you learned: iter(), next(), tuples

# iterrows returns an iterator yielding (index, row) tuples
print("First 2 rows via iterator:")
row_iter = df.iterrows()
print(next(row_iter))
print(next(row_iter))

# 7. IDENTITY vs EQUALITY: Missing Data
# =====================================
print("\n7. Identity vs Equality")
# Why you learned: is None vs == None

# Introduce a missing value
df.loc[0, 'price'] = None  # Pandas converts this to NaN for floats

# Check for missing values (Pandas uses isna(), but Python concept is 'is None')
has_missing = df['price'].isna().any()
print(f"Has missing prices? {has_missing}")

# 8. STANDARD LIBRARY: Datetime
# =============================
print("\n8. Standard Library (datetime)")
# Why you learned: datetime objects

# Convert string to datetime objects
df['date'] = pd.to_datetime(df['date'])
print(f"Date column type: {df['date'].dtype}")
print(f"First date year: {df['date'].dt.year.iloc[0]}")

# CLEANUP
if data_path.exists():
    data_path.unlink()
    print("\nCleaned up dummy file.")

print("\n" + "="*60)
print("See? You used ALL the Python concepts!")
print("Now you are ready to dive deep into Pandas in Week 2.")
print("="*60)
