# Week 1.5: Python Deep Dive for Pandas

**Goal**: Master the Python concepts that Pandas relies on heavily. Your colleague is right - these are essential before diving into Pandas!

## Why This Matters

Pandas code is full of:
- `[col for col in df.columns if 'price' in col]` → Comprehensions
- `df.apply(lambda x: x**2)` → Lambda functions
- `with open('data.csv') as f: df = pd.read_csv(f)` → Context managers
- `first, *rest = df.columns` → Unpacking
- `df.assign(growth=lambda d: d.rev2025 / d.rev2024 - 1)` → All of the above!

If these look confusing, you'll struggle with Pandas. Master them here first!

## Structure

### Core Tutorials
1. `01_iterators.py` - Iterator protocol, enumerate, zip, dict.items()
2. `02_comprehensions.py` - List/dict/set comprehensions, generators
3. `03_unpacking.py` - Unpacking, *args, **kwargs
4. `04_context_managers.py` - with statement, file handling
5. `05_lambdas_and_callables.py` - Lambda, map, filter, apply
6. `06_copy_vs_view.py` - Mutation, references, SettingWithCopyWarning
7. `07_identity_and_equality.py` - is vs ==, None checks, in operator
8. `08_stdlib_glue.py` - pathlib, datetime, collections, itertools

### Practice
- `09_readiness_test.py` - Can you write these without looking them up?
- `10_pandas_preview.py` - See how these concepts appear in Pandas

## Learning Path

### Day 1: Iteration & Comprehensions
```bash
python 01_iterators.py
python 02_comprehensions.py
```

**Practice**: Write these without looking:
```python
# 1. Filter columns containing 'price'
cols = [c for c in df.columns if 'price' in c]

# 2. Enumerate with index
for idx, col in enumerate(df.columns):
    print(f"{idx}: {col}")

# 3. Zip two lists
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

### Day 2: Unpacking & Context Managers
```bash
python 03_unpacking.py
python 04_context_managers.py
```

**Practice**: Write these without looking:
```python
# 1. Unpack first and rest
first, *rest = df.columns

# 2. Read file with context manager
with open('data.csv') as f:
    df = pd.read_csv(f)

# 3. Merge dicts
config = {**defaults, **user_settings}
```

### Day 3: Lambdas & Callables
```bash
python 05_lambdas_and_callables.py
```

**Practice**: Write these without looking:
```python
# 1. Lambda in assign
df.assign(growth=lambda d: d.rev2025 / d.rev2024 - 1)

# 2. Map function
squared = list(map(lambda x: x**2, numbers))

# 3. Filter with lambda
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### Day 4: Copy/View & Identity
```bash
python 06_copy_vs_view.py
python 07_identity_and_equality.py
```

**Practice**: Understand these:
```python
# 1. Copy vs reference
a = [1, 2, 3]
b = a        # Reference (same object)
c = a.copy() # Copy (different object)

# 2. is vs ==
if value is None:  # Check identity
if value == None:  # Check equality (don't do this!)

# 3. in operator
if 'price' in df.columns:
    print("Has price column")
```

### Day 5: Standard Library
```bash
python 08_stdlib_glue.py
```

**Practice**: Use these libraries:
```python
from pathlib import Path
from datetime import datetime
from collections import Counter
from itertools import chain

# Path handling
data_file = Path('data') / 'sales.csv'

# Date parsing
df['date'] = pd.to_datetime(df['date_str'])

# Count occurrences
counts = Counter(df['category'])

# Flatten lists
all_items = list(chain(*nested_lists))
```

## The Readiness Test

Can you write these **without looking them up**?

```python
# 1. Comprehension + unpacking
cols = [c for c in df.columns if c.startswith('rev')]
first, *others = cols

# 2. Context manager + lambda
with open('report.csv', 'w') as f:
    (df
     .assign(growth=lambda d: d.rev2025 / d.rev2024 - 1)
     .loc[:, ['id', 'growth']]
     .to_csv(f, index=False)
    )

# 3. Generator expression
total = sum(x**2 for x in range(1000000))

# 4. Dict comprehension
col_types = {col: df[col].dtype for col in df.columns}

# 5. Unpacking in function call
def process(a, b, c):
    return a + b + c

values = [1, 2, 3]
result = process(*values)

# 6. Filter with lambda
high_prices = df[df['price'].apply(lambda x: x > 100)]

# 7. is vs == for None
if value is None:
    print("Missing")

# 8. Path handling
from pathlib import Path
data_path = Path('data') / 'sales.csv'
if data_path.exists():
    df = pd.read_csv(data_path)
```

**If you can write all 8 without looking → You're Pandas-ready!**  
**If you struggle with any → Study that tutorial again**

## Common Mistakes to Avoid

### 1. Using == instead of is for None
```python
# ❌ Don't
if value == None:
    pass

# ✅ Do
if value is None:
    pass
```

### 2. Forgetting generators are exhausted
```python
gen = (x for x in range(5))
list(gen)  # [0, 1, 2, 3, 4]
list(gen)  # [] - exhausted!
```

### 3. Modifying list while iterating
```python
# ❌ Don't
for item in my_list:
    my_list.remove(item)  # Dangerous!

# ✅ Do
my_list = [x for x in my_list if condition]
```

### 4. Not using context managers for files
```python
# ❌ Don't
f = open('file.txt')
data = f.read()
f.close()  # Might not run if error occurs

# ✅ Do
with open('file.txt') as f:
    data = f.read()  # Auto-closes even on error
```

### 5. Confusing copy vs reference
```python
# ❌ Don't
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4] - Surprise!

# ✅ Do
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)  # [1, 2, 3] - Expected
```

## How These Appear in Pandas

### Iterators
```python
# Pandas uses iterators everywhere
for col in df.columns:  # df.columns is iterable
    print(col)

for idx, row in df.iterrows():  # Returns iterator
    print(idx, row)
```

### Comprehensions
```python
# Filter columns
price_cols = [col for col in df.columns if 'price' in col]

# Rename columns
df.columns = [col.upper() for col in df.columns]

# Create dict
col_types = {col: df[col].dtype for col in df.columns}
```

### Unpacking
```python
# Split columns
id_col, *feature_cols = df.columns

# MultiIndex
df.loc[(*idx,), :]  # Unpack tuple for row selection
```

### Lambda
```python
# Transform columns
df.assign(log_price=lambda d: np.log(d.price))

# Apply to column
df['price'].apply(lambda x: x * 1.1)

# Filter rows
df[df['price'].apply(lambda x: x > 100)]
```

### Context Managers
```python
# Read file
with open('data.csv') as f:
    df = pd.read_csv(f)

# Write file
with open('output.csv', 'w') as f:
    df.to_csv(f, index=False)
```

## Expected Learning Outcomes

After completing this week, you should be able to:
- ✅ Explain the iterator protocol
- ✅ Write list/dict/generator comprehensions fluently
- ✅ Use unpacking and star args confidently
- ✅ Understand when to use `is` vs `==`
- ✅ Write lambda functions for simple transformations
- ✅ Use context managers for file handling
- ✅ Understand copy vs view semantics
- ✅ Use pathlib, datetime, collections, itertools

## Next Steps

Once you can write the readiness test code without looking:
1. Move to `projects/02_pandas_basics`
2. The Pandas syntax will make much more sense
3. You'll understand WHY Pandas does things a certain way

## Resources

- Python Docs: https://docs.python.org/3/tutorial/
- Real Python: https://realpython.com/
- Python Iterators: https://docs.python.org/3/tutorial/classes.html#iterators
- Comprehensions: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

---