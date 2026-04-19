# Python Fundamentals: Gotchas and Best Practices

## 🚨 Common Gotchas for Python Beginners

### 1. **Mutable Default Arguments**
**❌ DON'T:**
```python
def add_item(item, items=[]):  # BAD: Default list is created once
    items.append(item)
    return items
```

**✅ DO:**
```python
def add_item(item, items=None):  # GOOD: Create new list each time
    if items is None:
        items = []
    items.append(item)
    return items
```

**Why:** Default arguments are evaluated only once when the function is defined, not each time it's called.

### 2. **Variable Scope Confusion**
**❌ DON'T:**
```python
x = 10

def modify():
    x = 20  # Creates a new local variable, doesn't modify global x
    print(f"Inside: {x}")

modify()
print(f"Outside: {x}")  # Still 10!
```

**✅ DO:**
```python
x = 10

def modify():
    global x  # Explicitly declare global variable
    x = 20
    print(f"Inside: {x}")

modify()
print(f"Outside: {x}")  # Now 20
```

**Alternative (Better):** Pass values as parameters and return results:
```python
def modify(value):
    return value * 2

x = 10
x = modify(x)  # Clear data flow
```

### 3. **String vs. List Modification**
**❌ DON'T:**
```python
text = "hello"
text[0] = "H"  # TypeError: 'str' object does not support item assignment
```

**✅ DO:**
```python
text = "hello"
text = "H" + text[1:]  # Create new string
# OR
text_list = list(text)
text_list[0] = "H"
text = "".join(text_list)
```

**Why:** Strings are immutable in Python; lists are mutable.

### 4. **Integer Division in Python 3**
**❌ DON'T:**
```python
result = 5 / 2  # Returns 2.5 (float), not 2
```

**✅ DO:**
```python
# For integer division (floor division):
result = 5 // 2  # Returns 2

# For float division:
result = 5 / 2  # Returns 2.5

# For explicit type conversion:
result = int(5 / 2)  # Returns 2
```

### 5. **Copy vs. Reference**
**❌ DON'T:**
```python
original = [1, 2, 3]
copy = original  # This is a reference, not a copy!
copy.append(4)
print(original)  # [1, 2, 3, 4] - Oops!
```

**✅ DO:**
```python
import copy

# Shallow copy (for simple lists):
original = [1, 2, 3]
copy = original.copy()  # or copy = original[:]
copy.append(4)

# Deep copy (for nested structures):
nested = [[1, 2], [3, 4]]
deep_copy = copy.deepcopy(nested)
```

### 6. **`is` vs `==` Operator**
**❌ DON'T:**
```python
x = [1, 2, 3]
y = [1, 2, 3]
print(x is y)  # False - Different objects in memory
```

**✅ DO:**
```python
x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)  # True - Same values

# Use `is` for None, True, False, or identity checks:
if x is None:
    pass
if y is True:
    pass
```

### 7. **Dictionary Key Existence**
**❌ DON'T:**
```python
data = {"name": "Alice", "age": 30}
if data["city"]:  # KeyError if key doesn't exist
    print(data["city"])
```

**✅ DO:**
```python
data = {"name": "Alice", "age": 30}

# Method 1: Use `in` operator
if "city" in data:
    print(data["city"])

# Method 2: Use `get()` with default
city = data.get("city", "Unknown")
print(city)

# Method 3: Use `setdefault()` to set if missing
data.setdefault("city", "New York")
```

### 8. **File Handling Without Context Managers**
**❌ DON'T:**
```python
file = open("data.txt", "r")
content = file.read()
# What if an exception occurs here?
file.close()  # Might not execute!
```

**✅ DO:**
```python
# Use context manager (automatically closes file)
with open("data.txt", "r") as file:
    content = file.read()
# File is automatically closed here, even if exceptions occur
```

### 9. **Infinite Recursion**
**❌ DON'T:**
```python
def factorial(n):
    return n * factorial(n - 1)  # No base case = infinite recursion
```

**✅ DO:**
```python
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)
```

### 10. **Modifying List While Iterating**
**❌ DON'T:**
```python
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Modifying list while iterating = unexpected behavior
```

**✅ DO:**
```python
numbers = [1, 2, 3, 4, 5]

# Method 1: Create new list
filtered = [num for num in numbers if num % 2 != 0]

# Method 2: Iterate over copy
for num in numbers.copy():
    if num % 2 == 0:
        numbers.remove(num)

# Method 3: Use while loop
i = 0
while i < len(numbers):
    if numbers[i] % 2 == 0:
        numbers.pop(i)
    else:
        i += 1
```

## 🏆 Best Practices

### 1. **Use Descriptive Variable Names**
```python
# ❌ Bad
a = 10
b = 20
c = a + b

# ✅ Good
base_price = 10
tax = 20
total_price = base_price + tax
```

### 2. **Follow PEP 8 Style Guide**
- Use 4 spaces per indentation level
- Limit lines to 79 characters
- Use blank lines to separate functions and classes
- Use spaces around operators and after commas

### 3. **Write Docstrings for Functions**
```python
def calculate_discount(price, discount_percent):
    """
    Calculate the final price after applying discount.
    
    Args:
        price (float): Original price
        discount_percent (float): Discount percentage (0-100)
    
    Returns:
        float: Final price after discount
    
    Raises:
        ValueError: If discount_percent is not between 0 and 100
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    return price * (1 - discount_percent / 100)
```

### 4. **Use List Comprehensions Wisely**
```python
# ✅ Good for simple transformations
squares = [x**2 for x in range(10)]

# ❌ Avoid complex logic in comprehensions
# Instead, use a regular loop
results = []
for x in range(10):
    if x % 2 == 0:
        results.append(x**2)
    else:
        results.append(x**3)
```

### 5. **Handle Exceptions Gracefully**
```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Invalid input: {e}")
    result = default_value
except FileNotFoundError:
    print("File not found, using default data")
    result = load_default_data()
except Exception as e:
    print(f"Unexpected error: {e}")
    raise  # Re-raise if you can't handle it
finally:
    cleanup_resources()  # Always executes
```

### 6. **Use `enumerate()` for Index-Value Pairs**
```python
fruits = ["apple", "banana", "cherry"]

# ✅ Good
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# ❌ Bad
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")
```

### 7. **Use `zip()` to Iterate Over Multiple Sequences**
```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

# ✅ Good
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
```

### 8. **Prefer `pathlib` Over `os.path`**
```python
from pathlib import Path

# ✅ Modern approach
file_path = Path("data") / "subfolder" / "file.txt"
if file_path.exists():
    content = file_path.read_text()
```

### 9. **Use Type Hints (Python 3.5+)**
```python
from typing import List, Dict, Optional

def process_data(
    items: List[str],
    config: Optional[Dict[str, int]] = None
) -> Dict[str, List[str]]:
    """Process data with type hints for clarity."""
    config = config or {}
    # ... implementation
    return {"processed": items}
```

### 10. **Keep Functions Small and Focused**
```python
# ❌ Bad: One function doing too much
def process_user_data(user_data):
    # Validate data
    # Clean data
    # Transform data
    # Save to database
    # Send notification
    # Generate report
    pass

# ✅ Good: Separate concerns
def validate_user_data(data):
    pass

def clean_user_data(data):
    pass

def transform_user_data(data):
    pass

def save_user_data(data):
    pass
```

## 🔧 Debugging Tips

### 1. **Use `print()` Debugging Effectively**
```python
def complex_function(x, y):
    print(f"[DEBUG] Entering complex_function with x={x}, y={y}")
    result = x * y
    print(f"[DEBUG] Intermediate result: {result}")
    # ... more code
    print(f"[DEBUG] Returning: {result}")
    return result
```

### 2. **Leverage Python's Debugger (pdb)**
```python
import pdb

def buggy_function():
    x = 10
    pdb.set_trace()  # Execution pauses here
    y = x / 0  # Bug!
    return y
```

Common pdb commands:
- `n` (next line)
- `s` (step into function)
- `c` (continue)
- `p variable` (print variable)
- `q` (quit)

### 3. **Use Assertions for Sanity Checks**
```python
def calculate_average(numbers):
    assert len(numbers) > 0, "Cannot calculate average of empty list"
    assert all(isinstance(n, (int, float)) for n in numbers), "All items must be numbers"
    
    return sum(numbers) / len(numbers)
```

### 4. **Log Instead of Print for Production Code**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data[:10]}...")
    try:
        result = complex_operation(data)
        logger.info(f"Successfully processed {len(data)} items")
        return result
    except Exception as e:
        logger.error(f"Failed to process data: {e}")
        raise
```

## 📚 Memory Management for 8GB RAM

### 1. **Use Generators for Large Datasets**
```python
# ✅ Good: Processes one line at a time
def read_large_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# ❌ Bad: Loads entire file into memory
def read_entire_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()
```

### 2. **Delete Unused Variables**
```python
large_data = load_huge_dataset()
# Process data
processed = process_data(large_data)

# Free memory
del large_data
import gc
gc.collect()
```

### 3. **Use `sys.getsizeof()` to Check Memory Usage**
```python
import sys

data = [i for i in range(1000000)]
print(f"Memory usage: {sys.getsizeof(data) / 1024 / 1024:.2f} MB")
```

### 4. **Chunk Large Operations**
```python
def process_large_dataset(filename, chunk_size=10000):
    results = []
    
    with open(filename, 'r') as f:
        chunk = []
        for line in f:
            chunk.append(line.strip())
            if len(chunk) >= chunk_size:
                results.extend(process_chunk(chunk))
                chunk = []  # Clear chunk to free memory
        
        # Process remaining items
        if chunk:
            results.extend(process_chunk(chunk))
    
    return results
```

## 🎯 Interview Preparation Focus

### 1. **Must-Know Concepts**
- List vs. Tuple vs. Set vs. Dictionary
- Mutable vs. Immutable types
- Shallow copy vs. Deep copy
- `*args` and `**kwargs`
- Decorators and their use cases
- Context managers (`with` statement)
- Generators and `yield`

### 2. **Common Interview Questions**
- Reverse a string/list
- Find duplicates in a list
- Check if two strings are anagrams
- Implement a stack/queue
- Find the most frequent element
- Merge two sorted lists
- Validate parentheses

### 3. **Problem-Solving Approach**
1. **Understand the problem**: Ask clarifying questions
2. **Plan your solution**: Write pseudocode, consider edge cases
3. **Implement**: Write clean, readable code
4. **Test**: Use sample inputs, edge cases
5. **Optimize**: Consider time/space complexity

### 4. **Time Complexity Awareness**
- O(1): Constant time (dictionary lookup)
- O(log n): Logarithmic time (binary search)
- O(n): Linear time (iterating through list)
- O(n log n): Linearithmic time (efficient sorting)
- O(n²): Quadratic time (nested loops)
- O(2ⁿ): Exponential time (recursive Fibonacci)

## 🔗 Integration with Other Projects

### 1. **Connecting to Pandas**
```python
import pandas as pd

# Your Python fundamentals help here:
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
}

# Convert to DataFrame
df = pd.DataFrame(data)
print(df)
```

### 2. **Preparing for Data Engineering**
- Practice file I/O with large CSV files
- Learn to work with JSON data
- Understand data validation patterns
- Master error handling for robust pipelines

### 3. **Building Towards APIs**
- Practice function design with clear inputs/outputs
- Learn to handle different data formats
- Understand serialization (JSON, CSV)

## 📝 Final Tips

1. **Practice Daily**: Even 30 minutes of coding helps
2. **Read Others' Code**: Learn from open-source projects
3. **Build Projects**: Apply concepts to real problems
4. **Use Version Control**: Start with Git early
5. **Ask for Help**: Stack Overflow, Python communities
6. **Review Your Code**: Refactor and improve
7. **Stay Curious**: Python ecosystem is vast and growing

Remember: Every expert was once a beginner. The key is consistent practice and learning from mistakes.