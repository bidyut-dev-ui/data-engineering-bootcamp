"""
Tutorial 1: Iterables, Iterators, and the Iterator Protocol
Essential for understanding how Pandas loops over columns/indexes
"""

# ============================================================================
# 1. ITERABLES vs ITERATORS
# ============================================================================

print("="*60)
print("1. Understanding Iterables vs Iterators")
print("="*60)

# Iterable: Any object you can loop over
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)
my_string = "abc"

# All are iterables - you can use them in for loops
for item in my_list:
    print(item, end=" ")
print()

# Iterator: Object that produces values one at a time
# Get an iterator from an iterable using iter()
my_iterator = iter(my_list)
print(f"\nIterator object: {my_iterator}")

# Use next() to get values one by one
print(next(my_iterator))  # 1
print(next(my_iterator))  # 2
print(next(my_iterator))  # 3
# print(next(my_iterator))  # Would raise StopIteration

# ============================================================================
# 2. THE ITERATOR PROTOCOL
# ============================================================================

print("\n" + "="*60)
print("2. The Iterator Protocol")
print("="*60)

# What happens under the hood in a for loop:
# for item in my_list:
#     print(item)
#
# Is equivalent to:
iterator = iter(my_list)
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break

# ============================================================================
# 3. COMMON ITERATOR FUNCTIONS
# ============================================================================

print("\n" + "="*60)
print("3. Common Iterator Functions")
print("="*60)

# enumerate() - get index and value
columns = ['name', 'age', 'salary']
for idx, col in enumerate(columns):
    print(f"Column {idx}: {col}")

# zip() - iterate over multiple iterables together
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
salaries = [50000, 60000, 70000]

for name, age, salary in zip(names, ages, salaries):
    print(f"{name} is {age} years old and earns ${salary}")

# dict.items() - iterate over dictionary key-value pairs
data = {'name': 'Alice', 'age': 25, 'city': 'NYC'}
for key, value in data.items():
    print(f"{key}: {value}")

# ============================================================================
# 4. PANDAS-LIKE ITERATION PATTERNS
# ============================================================================

print("\n" + "="*60)
print("4. Pandas-Like Iteration Patterns")
print("="*60)

# Simulating DataFrame columns
df_columns = ['id', 'name', 'price', 'quantity', 'total_price']

# Filter columns containing 'price'
price_columns = [col for col in df_columns if 'price' in col]
print(f"Price columns: {price_columns}")

# Iterate with index (like df.iterrows())
data_rows = [
    {'id': 1, 'name': 'Apple', 'price': 1.5},
    {'id': 2, 'name': 'Banana', 'price': 0.8},
]

for idx, row in enumerate(data_rows):
    print(f"Row {idx}: {row}")

# ============================================================================
# 5. LAZY EVALUATION WITH ITERATORS
# ============================================================================

print("\n" + "="*60)
print("5. Lazy Evaluation (Memory Efficient)")
print("="*60)

# range() is an iterator - doesn't create list in memory
# Good for large datasets
for i in range(1000000):
    if i >= 3:
        break
    print(i)

# map() returns an iterator
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)
print(f"map object: {squared}")  # Not evaluated yet
print(f"Converted to list: {list(squared)}")  # Now evaluated

# filter() returns an iterator
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(f"Even numbers: {list(even_numbers)}")

# ============================================================================
# 6. PRACTICAL EXERCISE
# ============================================================================

print("\n" + "="*60)
print("6. Practical Exercise")
print("="*60)

# Simulate processing a large dataset efficiently
def process_large_dataset():
    """Generator function - yields one row at a time"""
    for i in range(5):
        yield {'id': i, 'value': i * 10}

# Process without loading everything into memory
for row in process_large_dataset():
    print(f"Processing: {row}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. Iterable: Can be looped over (list, tuple, string, dict)
2. Iterator: Produces values one at a time (iter(), next())
3. enumerate(): Get index + value
4. zip(): Combine multiple iterables
5. dict.items(): Get key-value pairs
6. Lazy evaluation: Iterators don't compute until needed (memory efficient)

These concepts are EVERYWHERE in Pandas:
- df.iterrows() → iterator over rows
- df.columns → iterable of column names
- df.items() → iterator over (column_name, Series) pairs
""")
