"""
Tutorial 8: Standard Library Glue
pathlib, datetime, collections, itertools - Pandas loves these!
"""

# ============================================================================
# 1. PATHLIB - Modern File Path Handling
# ============================================================================

print("="*60)
print("1. pathlib - Modern File Paths")
print("="*60)

from pathlib import Path

# Create paths (works on Windows and Unix!)
data_dir = Path('data')
csv_file = data_dir / 'sales.csv'  # Use / operator!
print(f"CSV path: {csv_file}")

# Path operations
print(f"Exists: {csv_file.exists()}")
print(f"Is file: {csv_file.is_file()}")
print(f"Parent: {csv_file.parent}")
print(f"Name: {csv_file.name}")
print(f"Stem: {csv_file.stem}")  # Filename without extension
print(f"Suffix: {csv_file.suffix}")  # Extension

# Create directory
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)  # Create if doesn't exist
print(f"Created: {output_dir}")

# List files
# for file in data_dir.glob('*.csv'):
#     print(file)

# Pandas pattern
# df = pd.read_csv(data_dir / 'sales.csv')

# ============================================================================
# 2. DATETIME - Date and Time Handling
# ============================================================================

print("\n" + "="*60)
print("2. datetime - Date and Time")
print("="*60)

from datetime import datetime, timedelta, date

# Current datetime
now = datetime.now()
print(f"Now: {now}")
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Parse string to datetime
date_str = '2024-01-15'
parsed = datetime.strptime(date_str, '%Y-%m-%d')
print(f"Parsed: {parsed}")

# Date arithmetic
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
print(f"Tomorrow: {tomorrow.date()}")
print(f"Last week: {last_week.date()}")

# Extract components
print(f"Year: {now.year}")
print(f"Month: {now.month}")
print(f"Day: {now.day}")
print(f"Weekday: {now.strftime('%A')}")

# Pandas pattern
# df['date'] = pd.to_datetime(df['date_str'])
# df['year'] = df['date'].dt.year
# df['month'] = df['date'].dt.month

# ============================================================================
# 3. COLLECTIONS - Specialized Data Structures
# ============================================================================

print("\n" + "="*60)
print("3. collections - Specialized Containers")
print("="*60)

from collections import Counter, defaultdict, namedtuple

# Counter: Count occurrences
categories = ['fruit', 'vegetable', 'fruit', 'meat', 'fruit', 'vegetable']
counts = Counter(categories)
print(f"Counts: {counts}")
print(f"Most common: {counts.most_common(2)}")

# defaultdict: Dict with default values
from collections import defaultdict
sales_by_region = defaultdict(list)
sales_by_region['North'].append(100)
sales_by_region['North'].append(200)
sales_by_region['South'].append(150)
print(f"Sales by region: {dict(sales_by_region)}")

# namedtuple: Lightweight class
Person = namedtuple('Person', ['name', 'age', 'city'])
alice = Person('Alice', 25, 'NYC')
print(f"Person: {alice}")
print(f"Name: {alice.name}, Age: {alice.age}")

# Pandas pattern
# df['category'].value_counts()  # Like Counter
# df.groupby('region')['sales'].sum()  # Like defaultdict

# ============================================================================
# 4. ITERTOOLS - Iterator Tools
# ============================================================================

print("\n" + "="*60)
print("4. itertools - Iterator Tools")
print("="*60)

from itertools import chain, islice, groupby, combinations

# chain: Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flattened = list(chain(*nested))
print(f"Flattened: {flattened}")

# Or use chain.from_iterable
flattened2 = list(chain.from_iterable(nested))
print(f"Flattened (alt): {flattened2}")

# islice: Slice an iterator
numbers = range(100)
first_5 = list(islice(numbers, 5))
print(f"First 5: {first_5}")

# groupby: Group consecutive items
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('A', 5)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")

# combinations: All combinations
items = ['A', 'B', 'C']
pairs = list(combinations(items, 2))
print(f"Pairs: {pairs}")

# Pandas pattern
# pd.concat([df1, df2, df3])  # Like chain
# df.head(5)  # Like islice
# df.groupby('category')  # Like groupby

# ============================================================================
# 5. PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("5. Practical Examples")
print("="*60)

# Example 1: Process all CSV files in directory
from pathlib import Path

data_dir = Path('.')
csv_files = list(data_dir.glob('*.csv'))
print(f"CSV files found: {len(csv_files)}")

# Example 2: Date range for filtering
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=30)
print(f"Date range: {start_date.date()} to {end_date.date()}")

# Pandas: df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Example 3: Count occurrences
from collections import Counter

transactions = [
    {'category': 'food', 'amount': 50},
    {'category': 'transport', 'amount': 30},
    {'category': 'food', 'amount': 40},
    {'category': 'entertainment', 'amount': 60},
    {'category': 'food', 'amount': 35},
]

category_counts = Counter(t['category'] for t in transactions)
print(f"Category counts: {category_counts}")

# Example 4: Flatten nested data
from itertools import chain

nested_data = [
    [{'id': 1}, {'id': 2}],
    [{'id': 3}, {'id': 4}],
    [{'id': 5}]
]

all_items = list(chain.from_iterable(nested_data))
print(f"All items: {all_items}")

# ============================================================================
# 6. PANDAS INTEGRATION
# ============================================================================

print("\n" + "="*60)
print("6. Pandas Integration")
print("="*60)

print("""
Pandas happily accepts these standard library types:

1. pathlib.Path:
   df = pd.read_csv(Path('data') / 'sales.csv')

2. datetime:
   df['date'] = pd.to_datetime(df['date_str'])
   df[df['date'] > datetime(2024, 1, 1)]

3. Counter:
   category_counts = Counter(df['category'])
   # Or: df['category'].value_counts()

4. itertools.chain:
   all_dfs = pd.concat([df1, df2, df3])
   # Like: chain.from_iterable([df1, df2, df3])

5. defaultdict:
   groups = defaultdict(list)
   for idx, row in df.iterrows():
       groups[row['category']].append(row['value'])
   # Or: df.groupby('category')['value'].apply(list)
""")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. pathlib.Path:
   - Modern file path handling
   - Works cross-platform
   - data_dir / 'file.csv'

2. datetime:
   - Parse: datetime.strptime(s, fmt)
   - Format: dt.strftime(fmt)
   - Arithmetic: dt + timedelta(days=1)

3. collections.Counter:
   - Count occurrences
   - most_common(n)

4. collections.defaultdict:
   - Dict with default values
   - No KeyError

5. itertools.chain:
   - Flatten nested lists
   - chain.from_iterable()

6. Why learn these?
   - Pandas uses them internally
   - You'll see them in Pandas code
   - They complement Pandas well

Common patterns:
- Path('data') / 'sales.csv'
- pd.to_datetime(df['date'])
- Counter(df['category'])
- chain.from_iterable(nested_lists)
""")

# Cleanup
output_dir = Path('output')
if output_dir.exists():
    output_dir.rmdir()
