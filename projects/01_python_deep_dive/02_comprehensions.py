"""
Tutorial 2: Comprehensions & Generator Expressions
Critical for efficient data filtering and transformation
"""

# ============================================================================
# 1. LIST COMPREHENSIONS
# ============================================================================

print("="*60)
print("1. List Comprehensions")
print("="*60)

# Basic syntax: [expression for item in iterable]
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(f"Squared: {squared}")

# With condition: [expression for item in iterable if condition]
even_squared = [x**2 for x in numbers if x % 2 == 0]
print(f"Even squared: {even_squared}")

# Pandas-like: Filter columns
columns = ['id', 'name', 'price', 'quantity', 'total_price', 'unit_price']
price_cols = [col for col in columns if 'price' in col]
print(f"Price columns: {price_cols}")

# Transform column names
upper_cols = [col.upper() for col in columns]
print(f"Uppercase: {upper_cols}")

# Conditional transformation
cleaned_cols = [col.replace('_', '') if '_' in col else col for col in columns]
print(f"Cleaned: {cleaned_cols}")

# ============================================================================
# 2. DICT COMPREHENSIONS
# ============================================================================

print("\n" + "="*60)
print("2. Dict Comprehensions")
print("="*60)

# Create dict from lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
my_dict = {k: v for k, v in zip(keys, values)}
print(f"Dict from zip: {my_dict}")

# Filter dict
data = {'name': 'Alice', 'age': 25, 'city': 'NYC', 'country': 'USA'}
filtered = {k: v for k, v in data.items() if isinstance(v, str)}
print(f"String values only: {filtered}")

# Transform dict
squared_dict = {k: v**2 for k, v in {'a': 2, 'b': 3, 'c': 4}.items()}
print(f"Squared values: {squared_dict}")

# ============================================================================
# 3. SET COMPREHENSIONS
# ============================================================================

print("\n" + "="*60)
print("3. Set Comprehensions")
print("="*60)

# Get unique values
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = {x for x in numbers}
print(f"Unique: {unique}")

# Unique first letters
words = ['apple', 'banana', 'apricot', 'blueberry']
first_letters = {word[0] for word in words}
print(f"First letters: {first_letters}")

# ============================================================================
# 4. GENERATOR EXPRESSIONS (Memory Efficient!)
# ============================================================================

print("\n" + "="*60)
print("4. Generator Expressions")
print("="*60)

# Syntax: (expression for item in iterable)
# Uses () instead of []

# List comprehension - creates entire list in memory
list_comp = [x**2 for x in range(1000000)]
print(f"List size: {len(list_comp)} items")

# Generator expression - lazy evaluation
gen_exp = (x**2 for x in range(1000000))
print(f"Generator object: {gen_exp}")
print(f"First value: {next(gen_exp)}")
print(f"Second value: {next(gen_exp)}")

# Pandas-like: Transform columns lazily
columns = ['id', 'name', 'price', 'quantity']
upper_gen = (col.upper() for col in columns)
print(f"Generator: {upper_gen}")
print(f"Materialized: {list(upper_gen)}")

# ============================================================================
# 5. NESTED COMPREHENSIONS
# ============================================================================

print("\n" + "="*60)
print("5. Nested Comprehensions")
print("="*60)

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
flattened = [item for sublist in nested for item in sublist]
print(f"Flattened: {flattened}")

# Matrix operations
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"Transposed: {transposed}")

# ============================================================================
# 6. PRACTICAL PANDAS-LIKE EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("6. Practical Pandas-Like Examples")
print("="*60)

# Example 1: Filter and transform column names
df_columns = ['user_id', 'user_name', 'user_age', 'product_id', 'product_price']

# Get all user columns
user_cols = [col for col in df_columns if col.startswith('user_')]
print(f"User columns: {user_cols}")

# Remove prefix
cleaned = [col.replace('user_', '') for col in user_cols]
print(f"Cleaned: {cleaned}")

# Example 2: Create column mapping
old_cols = ['id', 'nm', 'pr', 'qty']
new_cols = ['order_id', 'name', 'price', 'quantity']
col_mapping = {old: new for old, new in zip(old_cols, new_cols)}
print(f"Column mapping: {col_mapping}")

# Example 3: Filter numeric columns (simulated)
columns_with_types = [
    ('id', int),
    ('name', str),
    ('price', float),
    ('quantity', int),
    ('description', str)
]
numeric_cols = [col for col, dtype in columns_with_types if dtype in (int, float)]
print(f"Numeric columns: {numeric_cols}")

# ============================================================================
# 7. WHEN TO USE EACH
# ============================================================================

print("\n" + "="*60)
print("7. When to Use Each")
print("="*60)

# List comprehension: Need the full list immediately
filtered_data = [x for x in range(100) if x % 10 == 0]
print(f"List comp (need all): {filtered_data}")

# Generator expression: Processing one at a time, large dataset
total = sum(x**2 for x in range(1000000))  # Memory efficient!
print(f"Sum of squares (generator): {total}")

# Dict comprehension: Creating lookup tables
id_to_name = {1: 'Alice', 2: 'Bob', 3: 'Charlie'}
name_to_id = {v: k for k, v in id_to_name.items()}
print(f"Reversed dict: {name_to_id}")

# ============================================================================
# 8. COMMON PITFALLS
# ============================================================================

print("\n" + "="*60)
print("8. Common Pitfalls")
print("="*60)

# Pitfall 1: Generator exhaustion
gen = (x for x in range(3))
print(f"First pass: {list(gen)}")
print(f"Second pass: {list(gen)}")  # Empty! Generator exhausted

# Pitfall 2: Modifying list while iterating
numbers = [1, 2, 3, 4, 5]
# DON'T: for x in numbers: numbers.remove(x)  # Dangerous!
# DO: Use comprehension
numbers = [x for x in numbers if x != 3]
print(f"Safely filtered: {numbers}")

# ============================================================================
# 9. CHALLENGE EXERCISES
# ============================================================================

print("\n" + "="*60)
print("9. Challenge Exercises")
print("="*60)

# Exercise 1: Filter columns
all_columns = ['id', 'name', 'price', 'cost', 'profit', 'quantity', 'price_usd']
# Get columns containing 'price' or 'cost'
result = [col for col in all_columns if 'price' in col or 'cost' in col]
print(f"Exercise 1: {result}")

# Exercise 2: Create dict of column -> length
col_lengths = {col: len(col) for col in all_columns}
print(f"Exercise 2: {col_lengths}")

# Exercise 3: Lazy transformation
# Transform column names but don't materialize until needed
transformed = (col.upper().replace('_', '') for col in all_columns)
print(f"Exercise 3 (first 3): {[next(transformed) for _ in range(3)]}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. List comprehension: [expr for x in iter if cond]
   - Use when you need the full list
   - Pandas: [col for col in df.columns if 'price' in col]

2. Dict comprehension: {k: v for k, v in iter}
   - Use for creating mappings
   - Pandas: {col: df[col].dtype for col in df.columns}

3. Generator expression: (expr for x in iter)
   - Use for large datasets (memory efficient)
   - Pandas: (f(col) for col in df.columns)

4. Nested comprehensions: [x for sublist in nested for x in sublist]
   - Use for flattening or matrix operations

5. Comprehensions are FASTER than loops in Python
   - More Pythonic
   - More readable (once you're used to them)
   - Better performance

In Pandas, you'll use comprehensions constantly:
- Filtering columns
- Renaming columns
- Creating column mappings
- Applying transformations
""")
