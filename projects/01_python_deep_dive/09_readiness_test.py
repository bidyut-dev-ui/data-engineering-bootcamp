"""
Readiness Test: Are you ready for Pandas?
Try to implement the solutions without looking at the hints!
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Setup dummy data for the test
df = pd.DataFrame({
    'id': [1, 2, 3],
    'rev2024': [100, 200, 300],
    'rev2025': [120, 240, 360],
    'price_usd': [10.5, 20.0, 15.5],
    'cost_usd': [5.0, 10.0, 8.0],
    'category': ['A', 'B', 'A']
})

print("="*60)
print("PANDAS READINESS TEST")
print("="*60)

# ---------------------------------------------------------
# Challenge 1: Comprehension + Unpacking
# Goal: Get a list of columns starting with 'rev', then unpack the first one and the rest
# ---------------------------------------------------------
print("\n1. Comprehension + Unpacking")
try:
    # TODO: Write your code here
    # cols = ...
    # first, *others = ...
    
    # SOLUTION:
    cols = [c for c in df.columns if c.startswith('rev')]
    first, *others = cols
    
    print(f"✅ Success! First: {first}, Others: {others}")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 2: Context Manager + Lambda
# Goal: Write a CSV where you calculate 'growth' ((rev2025/rev2024) - 1)
# using assign() and a lambda, inside a with block
# ---------------------------------------------------------
print("\n2. Context Manager + Lambda")
try:
    # TODO: Write your code here
    # with ...:
    #    (df.assign(...) ...)
    
    # SOLUTION:
    with open('report_test.csv', 'w') as f:
        (df
         .assign(growth=lambda d: d.rev2025 / d.rev2024 - 1)
         .loc[:, ['id', 'growth']]
         .to_csv(f, index=False)
        )
    print("✅ Success! report_test.csv created.")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 3: Generator Expression
# Goal: Calculate sum of squares of range(1000) using a generator
# ---------------------------------------------------------
print("\n3. Generator Expression")
try:
    # TODO: Write your code here
    # total = ...
    
    # SOLUTION:
    total = sum(x**2 for x in range(1000))
    
    print(f"✅ Success! Total: {total}")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 4: Dict Comprehension
# Goal: Create a dict mapping column names to their dtype
# ---------------------------------------------------------
print("\n4. Dict Comprehension")
try:
    # TODO: Write your code here
    # col_types = ...
    
    # SOLUTION:
    col_types = {col: df[col].dtype for col in df.columns}
    
    print(f"✅ Success! Types: {col_types}")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 5: Unpacking in Function Call
# Goal: Pass a list of values to a function using unpacking
# ---------------------------------------------------------
print("\n5. Unpacking in Function Call")
def calculate_volume(length, width, height):
    return length * width * height

dims = [10, 5, 2]

try:
    # TODO: Write your code here
    # volume = ...
    
    # SOLUTION:
    volume = calculate_volume(*dims)
    
    print(f"✅ Success! Volume: {volume}")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 6: Filter with Lambda
# Goal: Filter rows where price_usd > 15 using apply and lambda
# ---------------------------------------------------------
print("\n6. Filter with Lambda")
try:
    # TODO: Write your code here
    # high_price = ...
    
    # SOLUTION:
    # Note: In real pandas we'd use df[df['price_usd'] > 15], but this tests lambda knowledge
    high_price = df[df['price_usd'].apply(lambda x: x > 15)]
    
    print(f"✅ Success! Found {len(high_price)} rows.")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 7: Identity Check (is None)
# Goal: Check if a value is None using the correct operator
# ---------------------------------------------------------
print("\n7. Identity Check")
missing_val = None
try:
    # TODO: Write your code here
    # if ...:
    
    # SOLUTION:
    if missing_val is None:
        print("✅ Success! Correctly identified None.")
    else:
        print("❌ Failed: Should have identified None.")
except Exception as e:
    print(f"❌ Failed: {e}")

# ---------------------------------------------------------
# Challenge 8: Pathlib
# Goal: Check if 'report_test.csv' exists using pathlib
# ---------------------------------------------------------
print("\n8. Pathlib")
try:
    # TODO: Write your code here
    # p = ...
    # if ...:
    
    # SOLUTION:
    p = Path('report_test.csv')
    if p.exists():
        print("✅ Success! File found using pathlib.")
        # Cleanup
        p.unlink()
    else:
        print("❌ Failed: File not found.")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print("If you saw 8 Success messages, you are READY for Pandas!")
