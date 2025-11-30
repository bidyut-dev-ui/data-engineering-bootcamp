"""
Tutorial 3: Unpacking, Star Args, and Advanced Assignment
Essential for working with MultiIndex and flexible function calls
"""

# ============================================================================
# 1. BASIC UNPACKING
# ============================================================================

print("="*60)
print("1. Basic Unpacking")
print("="*60)

# Tuple unpacking
point = (10, 20)
x, y = point
print(f"x={x}, y={y}")

# List unpacking
data = [1, 2, 3]
a, b, c = data
print(f"a={a}, b={b}, c={c}")

# Dict unpacking (keys only)
person = {'name': 'Alice', 'age': 25}
# Can't directly unpack dict, but can unpack .items()
for key, value in person.items():
    print(f"{key}: {value}")

# ============================================================================
# 2. STAR (*) UNPACKING
# ============================================================================

print("\n" + "="*60)
print("2. Star (*) Unpacking")
print("="*60)

# Capture "rest" of items
numbers = [1, 2, 3, 4, 5]
first, *rest = numbers
print(f"first={first}, rest={rest}")

# Capture middle
first, *middle, last = numbers
print(f"first={first}, middle={middle}, last={last}")

# Pandas-like: Split columns
df_columns = ['id', 'name', 'price', 'quantity', 'total']
id_col, *feature_cols = df_columns
print(f"ID column: {id_col}")
print(f"Feature columns: {feature_cols}")

# Ignore values with _
first, *_, last = numbers
print(f"first={first}, last={last} (ignored middle)")

# ============================================================================
# 3. DOUBLE STAR (**) UNPACKING
# ============================================================================

print("\n" + "="*60)
print("3. Double Star (**) Unpacking")
print("="*60)

# Merge dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
merged = {**dict1, **dict2}
print(f"Merged: {merged}")

# Override values
defaults = {'host': 'localhost', 'port': 5432, 'user': 'admin'}
custom = {'port': 3306, 'password': 'secret'}
config = {**defaults, **custom}
print(f"Config: {config}")

# ============================================================================
# 4. FUNCTION ARGUMENTS WITH *args and **kwargs
# ============================================================================

print("\n" + "="*60)
print("4. Function Arguments: *args and **kwargs")
print("="*60)

def flexible_function(*args, **kwargs):
    """Accept any number of positional and keyword arguments"""
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")

flexible_function(1, 2, 3, name='Alice', age=25)

# Real-world example: Pandas-like function
def select_columns(df_dict, *columns, **filters):
    """
    Select columns and apply filters
    Similar to df.loc[:, columns].query(filters)
    """
    print(f"Selecting columns: {columns}")
    print(f"Applying filters: {filters}")
    
    # Simulate filtering
    result = {col: df_dict[col] for col in columns if col in df_dict}
    return result

data = {'id': [1,2,3], 'name': ['A','B','C'], 'age': [25,30,35]}
result = select_columns(data, 'id', 'name', min_age=25, max_age=40)
print(f"Result: {result}")

# ============================================================================
# 5. UNPACKING IN FUNCTION CALLS
# ============================================================================

print("\n" + "="*60)
print("5. Unpacking in Function Calls")
print("="*60)

def calculate(x, y, z):
    return x + y + z

# Unpack list as arguments
values = [10, 20, 30]
result = calculate(*values)
print(f"Sum: {result}")

# Unpack dict as keyword arguments
params = {'x': 10, 'y': 20, 'z': 30}
result = calculate(**params)
print(f"Sum: {result}")

# ============================================================================
# 6. PANDAS MULTIINDEX PATTERNS
# ============================================================================

print("\n" + "="*60)
print("6. Pandas MultiIndex Patterns")
print("="*60)

# Simulating MultiIndex tuple
multi_index = ('2024', 'Q1', 'Sales')
year, quarter, metric = multi_index
print(f"Year: {year}, Quarter: {quarter}, Metric: {metric}")

# Using star unpacking with MultiIndex
index_tuple = ('2024', 'Q1', 'North', 'Product_A')
year, quarter, *location_product = index_tuple
print(f"Year: {year}, Quarter: {quarter}, Rest: {location_product}")

# Pandas df.loc with tuple unpacking
# df.loc[(*idx,)]  # Unpack tuple as row selector
idx = ('2024', 'Q1')
print(f"Would select: df.loc[{(*idx,)}]")

# ============================================================================
# 7. PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("7. Practical Examples")
print("="*60)

# Example 1: Split DataFrame columns
all_columns = ['id', 'timestamp', 'value1', 'value2', 'value3', 'status']
id_col, time_col, *value_cols, status_col = all_columns
print(f"ID: {id_col}")
print(f"Time: {time_col}")
print(f"Values: {value_cols}")
print(f"Status: {status_col}")

# Example 2: Merge multiple config dicts
default_config = {'batch_size': 32, 'epochs': 10, 'lr': 0.001}
user_config = {'epochs': 20, 'lr': 0.01}
env_config = {'batch_size': 64}

final_config = {**default_config, **user_config, **env_config}
print(f"Final config: {final_config}")

# Example 3: Flexible data loader
def load_data(filepath, *columns, **options):
    """Simulate pd.read_csv with flexible arguments"""
    print(f"Loading: {filepath}")
    print(f"Columns: {columns if columns else 'all'}")
    print(f"Options: {options}")

load_data('data.csv', 'id', 'name', 'price', sep=',', header=0, encoding='utf-8')

# ============================================================================
# 8. COMMON PATTERNS IN PANDAS
# ============================================================================

print("\n" + "="*60)
print("8. Common Patterns in Pandas")
print("="*60)

# Pattern 1: Select first and last columns
columns = ['id', 'name', 'age', 'city', 'country', 'status']
first, *middle, last = columns
print(f"First: {first}, Last: {last}")

# Pattern 2: Group columns by type
id_cols = ['user_id', 'order_id']
feature_cols = ['name', 'price', 'quantity']
target_col = ['total_sales']

all_cols = [*id_cols, *feature_cols, *target_col]
print(f"All columns: {all_cols}")

# Pattern 3: Merge row data
row1 = {'id': 1, 'name': 'Alice'}
row2 = {'age': 25, 'city': 'NYC'}
complete_row = {**row1, **row2}
print(f"Complete row: {complete_row}")

# ============================================================================
# 9. ADVANCED: NESTED UNPACKING
# ============================================================================

print("\n" + "="*60)
print("9. Advanced: Nested Unpacking")
print("="*60)

# Nested structures
data = [
    ('Alice', (25, 'NYC')),
    ('Bob', (30, 'LA'))
]

for name, (age, city) in data:
    print(f"{name} is {age} years old and lives in {city}")

# MultiIndex-like structure
multi_data = [
    (('2024', 'Q1'), 100),
    (('2024', 'Q2'), 150),
]

for (year, quarter), value in multi_data:
    print(f"{year}-{quarter}: {value}")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. Basic unpacking: a, b, c = [1, 2, 3]

2. Star unpacking: first, *rest = [1, 2, 3, 4, 5]
   - Captures remaining items
   - Use _ to ignore: first, *_, last = items

3. Dict unpacking: merged = {**dict1, **dict2}
   - Later dicts override earlier ones

4. Function args:
   - *args: Capture positional arguments
   - **kwargs: Capture keyword arguments

5. Unpacking in calls:
   - func(*list) → unpack list as positional args
   - func(**dict) → unpack dict as keyword args

6. Pandas patterns:
   - first, *rest = df.columns
   - df.loc[(*idx,)] for MultiIndex
   - pd.read_csv(file, **options)

7. Nested unpacking:
   - for (year, quarter), value in multi_index_data

Master these patterns and Pandas code will make much more sense!
""")
