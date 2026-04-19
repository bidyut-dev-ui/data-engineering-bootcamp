# Python Deep Dive: Gotchas and Best Practices

## 🚨 Common Gotchas for Advanced Python Concepts

### 1. **Iterator Exhaustion**
**❌ DON'T:**
```python
# Wrong: Reusing exhausted iterator
data = [1, 2, 3, 4, 5]
iterator = iter(data)
list1 = list(iterator)  # [1, 2, 3, 4, 5]
list2 = list(iterator)  # [] - iterator is exhausted!
```

**✅ DO:**
```python
# Correct: Create new iterator or convert to list
data = [1, 2, 3, 4, 5]
list1 = list(data)      # Convert to list
list2 = list(data)      # Fresh conversion

# Or create new iterator
iterator1 = iter(data)
list1 = list(iterator1)
iterator2 = iter(data)  # Fresh iterator
list2 = list(iterator2)
```

**Why:** Iterators are single-use. Once exhausted, they yield no more values. This is especially problematic with generator expressions.

### 2. **Mutable Default Arguments**
**❌ DON'T:**
```python
# Wrong: Using mutable default arguments
def append_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Surprise! List persists
```

**✅ DO:**
```python
# Correct: Use None as default and create new list
def append_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [2] - Fresh list each time
```

**Why:** Default arguments are evaluated once at function definition, not each call. Mutable defaults persist across calls.

### 3. **Shallow vs Deep Copy**
**❌ DON'T:**
```python
# Wrong: Shallow copy for nested structures
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] - Original modified!
```

**✅ DO:**
```python
# Correct: Use deep copy for nested structures
import copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original)  # [[1, 2], [3, 4]] - Original unchanged
print(deep)      # [[99, 2], [3, 4]]
```

**Why:** Shallow copy creates new container but references same nested objects. Deep copy creates entirely new objects.

### 4. **'is' vs '==' Operator Confusion**
**❌ DON'T:**
```python
# Wrong: Using 'is' for value comparison
a = 1000
b = 1000
print(a is b)  # False - Different objects (for large integers)
print(a == b)  # True - Same value

# Wrong: Using '==' for None checks
if x == None:  # Works but not Pythonic
    pass
```

**✅ DO:**
```python
# Correct: Use 'is' for identity, '==' for equality
a = 1000
b = 1000
print(a == b)  # True - Value comparison

# Correct: Use 'is' for None, True, False
if x is None:  # Pythonic way
    pass
if success is True:  # Clear intent
    pass
```

**Why:** 'is' checks object identity (same memory location). '==' checks value equality. Small integers (-5 to 256) are cached, making 'is' work unexpectedly.

### 5. **Generator Memory Trade-offs**
**❌ DON'T:**
```python
# Wrong: Converting large generator to list
def read_large_file():
    with open('huge.csv') as f:
        for line in f:
            yield line

# Memory explosion!
all_lines = list(read_large_file())  # Loads entire file
```

**✅ DO:**
```python
# Correct: Process generator incrementally
def process_large_file():
    with open('huge.csv') as f:
        for line in f:
            # Process line immediately
            processed = line.strip().split(',')
            yield processed

# Memory efficient
for row in process_large_file():
    process_row(row)
```

**Why:** Generators produce values lazily, saving memory. Converting to list defeats this benefit.

### 6. **Lambda Scope Issues**
**❌ DON'T:**
```python
# Wrong: Lambda capturing loop variable
functions = []
for i in range(3):
    functions.append(lambda: i * 2)

print([f() for f in functions])  # [4, 4, 4] - All use final i=2
```

**✅ DO:**
```python
# Correct: Capture current value with default argument
functions = []
for i in range(3):
    functions.append(lambda x=i: x * 2)  # Capture i as default

print([f() for f in functions])  # [0, 2, 4] - Correct
```

**Why:** Lambda captures variables by reference, not value. By the time lambda is called, loop has finished.

### 7. **Context Manager Resource Leaks**
**❌ DON'T:**
```python
# Wrong: Manual resource management
f = open('data.txt', 'r')
data = f.read()
# What if exception occurs here?
f.close()  # Might not execute
```

**✅ DO:**
```python
# Correct: Use context manager
with open('data.txt', 'r') as f:
    data = f.read()
# File automatically closed

# For custom resources
from contextlib import contextmanager

@contextmanager
def database_connection(url):
    conn = create_connection(url)
    try:
        yield conn
    finally:
        conn.close()
```

**Why:** Context managers ensure resources are properly released even with exceptions.

### 8. **Unpacking Errors**
**❌ DON'T:**
```python
# Wrong: Unpacking mismatched sizes
a, b = [1, 2, 3]  # ValueError: too many values to unpack
```

**✅ DO:**
```python
# Correct: Use extended unpacking
a, b, *rest = [1, 2, 3, 4, 5]
print(a, b)    # 1 2
print(rest)    # [3, 4, 5]

# Or unpack with star for function arguments
def sum_numbers(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
result = sum_numbers(*numbers)  # Unpacks list
```

**Why:** Extended unpacking (*) handles variable numbers of elements gracefully.

## 🏆 Best Practices for Python Deep Dive

### 1. **Use Type Hints for Clarity**
```python
from typing import List, Dict, Optional, Iterator

def process_data(
    data: List[Dict[str, float]],
    threshold: Optional[float] = None
) -> Iterator[Dict[str, float]]:
    """Process data with optional threshold filter."""
    for record in data:
        if threshold is None or record['value'] > threshold:
            yield record
```

**Benefit:** Improves code readability, enables IDE autocomplete, and catches type errors early.

### 2. **Leverage Standard Library**
```python
# Instead of manual implementations, use:
from collections import defaultdict, Counter, deque
from itertools import chain, groupby, product
from functools import lru_cache, partial
from pathlib import Path
from datetime import datetime, timedelta
```

**Benefit:** Battle-tested, optimized, and Pythonic solutions.

### 3. **Memory-Efficient Patterns**
```python
# Use generators for large datasets
def read_large_file_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Use comprehensions for transformation
squared = (x**2 for x in range(1000000))  # Generator expression
filtered = [x for x in data if x > 0]     # List comprehension
```

**Benefit:** Reduces memory footprint for 8GB RAM constraints.

### 4. **Error Handling with Context**
```python
# Provide context in exceptions
try:
    result = risky_operation()
except ValueError as e:
    # Add context without losing original traceback
    raise RuntimeError(f"Failed to process data: {e}") from e

# Use specific exceptions
except (FileNotFoundError, PermissionError) as e:
    logger.error(f"File access failed: {e}")
    raise
```

**Benefit:** Easier debugging and better error messages.

### 5. **Functional Programming Wisely**
```python
# Use map/filter for simple transformations
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)

# But prefer comprehensions for complex logic
squared = [x**2 for x in numbers if x % 2 == 0]

# Use functools for function composition
from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
```

**Benefit:** Clean, readable code that expresses intent clearly.

### 6. **Optimize for Pandas Compatibility**
```python
# Write Python that translates well to Pandas
# Good: List comprehensions
column_names = [f"col_{i}" for i in range(10)]

# Good: Dictionary operations
config = {'threshold': 0.5, 'max_items': 100}
filtered = {k: v for k, v in config.items() if v}

# Good: Generator expressions for large data
large_sequence = (process(x) for x in read_stream())
```

**Benefit:** Skills directly transfer to data engineering with Pandas.

### 7. **Profile Before Optimizing**
```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function's performance."""
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args, **kwargs)
    pr.disable()
    
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())
    
    return result
```

**Benefit:** Focus optimization efforts where they matter most.

### 8. **Write Testable Code**
```python
# Pure functions are easier to test
def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """Calculate basic statistics."""
    return {
        'mean': sum(data) / len(data),
        'min': min(data),
        'max': max(data)
    }

# Use dependency injection
def process_with_deps(data, transformer=None, validator=None):
    """Process data with injectable dependencies."""
    transformer = transformer or default_transformer
    validator = validator or default_validator
    # ...
```

**Benefit:** Enables unit testing and modular design.

## 🔧 Performance Tips for 8GB RAM

### Memory Optimization
1. **Use generators** instead of lists for large sequences
2. **Process files in chunks** rather than loading entirely
3. **Use `array` module** for numeric data instead of lists
4. **Delete references** when done: `del large_object`
5. **Use `sys.getsizeof()`** to measure object memory

### CPU Optimization
1. **Use built-in functions** (C-optimized) over Python loops
2. **Leverage `itertools`** for efficient iteration
3. **Cache expensive computations** with `functools.lru_cache`
4. **Use local variables** in loops (faster access)
5. **Consider `numba` or `cython`** for critical paths

### I/O Optimization
1. **Buffer I/O operations** (read/write in chunks)
2. **Use `pathlib`** for filesystem operations
3. **Compress data** when storing/transmitting
4. **Use binary formats** (pickle, parquet) for Python objects
5. **Async I/O** for network operations

## 📚 Further Reading

1. **Python Documentation**: https://docs.python.org/3/
2. **Fluent Python** by Luciano Ramalho
3. **Effective Python** by Brett Slatkin
4. **Python Cookbook** by David Beazley & Brian K. Jones

---

*Last Updated: 2026-04-19*  
*Next Review: Quarterly*