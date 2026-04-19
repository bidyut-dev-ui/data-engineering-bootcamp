# Python Deep Dive Interview Questions

## 📋 Table of Contents
1. [Iterators & Generators](#iterators--generators)
2. [Comprehensions & Functional Programming](#comprehensions--functional-programming)
3. [Unpacking & Argument Handling](#unpacking--argument-handling)
4. [Context Managers & Resource Management](#context-managers--resource-management)
5. [Copy vs View & Object References](#copy-vs-view--object-references)
6. [Identity vs Equality & Operators](#identity-vs-equality--operators)
7. [Standard Library Mastery](#standard-library-mastery)
8. [Memory Optimization & Performance](#memory-optimization--performance)
9. [Advanced Python Patterns](#advanced-python-patterns)
10. [Scenario-Based Questions](#scenario-based-questions)

---

## Iterators & Generators

### 1. **Explain the iterator protocol in Python**
**Answer:** The iterator protocol consists of two methods:
- `__iter__()`: Returns the iterator object itself
- `__next__()`: Returns the next item, raising `StopIteration` when exhausted

```python
class Countdown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Usage
for num in Countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

**Follow-up:** How do generators relate to iterators?

### 2. **What's the difference between `iterable`, `iterator`, and `generator`?**
**Answer:**
- **Iterable**: Any object that can be looped over (implements `__iter__()`)
- **Iterator**: Object that produces values one at a time (implements `__iter__()` and `__next__()`)
- **Generator**: Special type of iterator created using `yield` or generator expressions

```python
# Iterable
my_list = [1, 2, 3]          # Has __iter__()

# Iterator
my_iterator = iter(my_list)  # Has __next__()

# Generator
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
```

**Follow-up:** When would you use a generator instead of a list?

### 3. **How does `yield` differ from `return`?**
**Answer:**
- `return`: Ends function execution and returns a single value
- `yield`: Pauses function execution, returns a value, and remembers state for next call

```python
def simple_return():
    return [1, 2, 3]  # Returns entire list

def simple_yield():
    yield 1  # Returns 1, pauses
    yield 2  # Returns 2, pauses  
    yield 3  # Returns 3, done

# return: All memory used at once
# yield: Memory efficient, produces values lazily
```

**Follow-up:** What is generator exhaustion and how do you handle it?

## Comprehensions & Functional Programming

### 4. **Compare list comprehension, generator expression, and map/filter**
**Answer:**
```python
# List comprehension: Creates list immediately
squares = [x**2 for x in range(10)]  # Memory: O(n)

# Generator expression: Creates iterator
squares_gen = (x**2 for x in range(10))  # Memory: O(1)

# map/filter: Functional style
squares_map = map(lambda x: x**2, range(10))  # Returns iterator
```

**Memory implications:**
- List comprehension: Stores all results (use for small datasets)
- Generator expression: Produces values on demand (use for large datasets)
- map/filter: Returns iterator (similar to generator expression)

**Follow-up:** When would you prefer map/filter over comprehensions?

### 5. **Explain the use of `lambda` functions and their limitations**
**Answer:** Lambda functions are anonymous, single-expression functions:
```python
# Syntax: lambda arguments: expression
add = lambda x, y: x + y

# Common use with sorted()
students = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
sorted_students = sorted(students, key=lambda x: x[1])  # Sort by score
```

**Limitations:**
- Single expression only (no statements)
- No type annotations
- Harder to debug (no function name)
- Can't have docstrings

**Follow-up:** What's a closure and how does it relate to lambda?

### 6. **How do you handle mutable default arguments in functions?**
**Answer:** This is a classic Python gotcha:
```python
# ❌ WRONG: Mutable default argument
def append_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Surprise!

# ✅ CORRECT: Use None as default
def append_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list
```

**Why:** Default arguments are evaluated once at function definition time, not each call.

**Follow-up:** What other function argument patterns should you be aware of?

## Unpacking & Argument Handling

### 7. **Explain `*args` and `**kwargs` with examples**
**Answer:**
- `*args`: Collects positional arguments into a tuple
- `**kwargs`: Collects keyword arguments into a dictionary

```python
def process_data(*args, **kwargs):
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")

process_data(1, 2, 3, name='Alice', age=30)
# Output:
# Positional args: (1, 2, 3)
# Keyword args: {'name': 'Alice', 'age': 30}
```

**Common use cases:**
- Wrapper/decorator functions
- Function composition
- API wrappers with variable parameters

**Follow-up:** How would you forward `*args` and `**kwargs` to another function?

### 8. **What is extended unpacking and when is it useful?**
**Answer:** Extended unpacking uses `*` to capture multiple elements:
```python
# Basic unpacking
first, second = [1, 2]

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5

# Useful for variable-length sequences
def sum_first_last(*numbers):
    first, *middle, last = numbers
    return first + last
```

**Follow-up:** How does unpacking work with dictionaries?

## Context Managers & Resource Management

### 9. **What problem do context managers solve?**
**Answer:** Context managers ensure proper resource acquisition and release:
```python
# ❌ Without context manager (error-prone)
f = open('data.txt', 'r')
try:
    data = f.read()
finally:
    f.close()  # Easy to forget

# ✅ With context manager (auto cleanup)
with open('data.txt', 'r') as f:
    data = f.read()
# File automatically closed
```

**Benefits:**
- Automatic cleanup (files, connections, locks)
- Exception safety
- Cleaner, more readable code

**Follow-up:** How would you create a custom context manager?

### 10. **Create a context manager that measures execution time**
**Answer:**
```python
import time
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{name} took {end - start:.2f} seconds")

# Usage
with timer("Data processing"):
    # Your code here
    process_large_dataset()
```

**Follow-up:** What's the difference between class-based and decorator-based context managers?

## Copy vs View & Object References

### 11. **Explain shallow copy vs deep copy with examples**
**Answer:**
```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy: New container, same nested objects
shallow = copy.copy(original)
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] - Modified!

# Deep copy: Entirely new objects
deep = copy.deepcopy(original)
deep[0][0] = 100
print(original)  # [[99, 2], [3, 4]] - Unchanged
```

**When to use:**
- Shallow copy: Simple, flat structures
- Deep copy: Nested structures with mutable elements

**Follow-up:** How does list slicing relate to copying?

### 12. **What is the "SettingWithCopyWarning" in Pandas and its Python roots?**
**Answer:** This warning occurs when modifying what appears to be a copy of data:
```python
# Python equivalent issue
original = [[1, 2], [3, 4]]
view = original[:]  # Shallow copy
view[0][0] = 99     # Modifies original[0][0] too!

# Pandas version
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3]})
subset = df[df['A'] > 1]  # This is a view, not a copy
subset['A'] = 0           # SettingWithCopyWarning!
```

**Solution:** Use `.copy()` explicitly when you need a true copy.

**Follow-up:** How can you check if two variables reference the same object?

## Identity vs Equality & Operators

### 13. **When should you use `is` vs `==`?**
**Answer:**
- `is`: Checks object identity (same memory location)
- `==`: Checks value equality (same content)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - Same values
print(a is b)  # False - Different objects
print(a is c)  # True - Same object

# Special cases: None, True, False
if x is None:    # ✅ Correct
if x == None:    # ❌ Avoid
```

**Follow-up:** Why do small integers (-5 to 256) behave differently with `is`?

### 14. **Explain operator chaining and precedence**
**Answer:** Python supports natural operator chaining:
```python
# Valid chaining
if 0 < x < 10:          # Equivalent to (0 < x) and (x < 10)
    pass

# Complex chaining  
if a == b == c != d:    # All must be True
    pass

# Precedence matters
result = 2 + 3 * 4      # 14, not 20
result = (2 + 3) * 4    # 20
```

**Common precedence (high to low):**
1. `()` parentheses
2. `**` exponentiation  
3. `* / // %` multiplication/division
4. `+ -` addition/subtraction
5. `== != < > <= >=` comparisons
6. `is`, `is not`, `in`, `not in`
7. `not` boolean NOT
8. `and` boolean AND
9. `or` boolean OR

**Follow-up:** How does the `in` operator work with different data types?

## Standard Library Mastery

### 15. **Which `collections` module classes are most useful for data engineering?**
**Answer:**
- `defaultdict`: Dictionary with default values
- `Counter`: Count hashable objects
- `deque`: Double-ended queue for efficient appends/pops
- `OrderedDict`: Dictionary that remembers insertion order (Python 3.7+ dicts do this)
- `namedtuple`: Lightweight object with named fields

```python
from collections import defaultdict, Counter

# defaultdict example
word_counts = defaultdict(int)
for word in text.split():
    word_counts[word] += 1  # No KeyError

# Counter example
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counts = Counter(words)  # {'apple': 3, 'banana': 2, 'orange': 1}
```

**Follow-up:** When would you use `deque` instead of `list`?

### 16. **How do `itertools` functions improve performance?**
**Answer:** `itertools` provides memory-efficient iterator tools:
```python
import itertools

# Infinite sequences
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7...

# Combinations and permutations
combos = itertools.combinations([1, 2, 3, 4], 2)  # (1,2), (1,3), (1,4)...

# Grouping data
for key, group in itertools.groupby(data, key=lambda x: x['category']):
    process_group(list(group))
```

**Benefits:**
- Lazy evaluation (memory efficient)
- C-optimized implementations
- Clean, functional patterns

**Follow-up:** What's the difference between `itertools.chain` and nested loops?

## Memory Optimization & Performance

### 17. **How would you process a 10GB CSV file on an 8GB RAM machine?**
**Answer:** Use chunking and streaming:
```python
import pandas as pd

# Process in chunks
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)  # Process each chunk independently
    del chunk  # Free memory

# Alternative: Use generators
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        header = f.readline()
        for line in f:
            yield line.strip().split(',')

for row in read_large_file('large_file.csv'):
    process_row(row)
```

**Follow-up:** What tools would you use to profile memory usage?

### 18. **Explain the Global Interpreter Lock (GIL) and its impact**
**Answer:** The GIL is a mutex that allows only one thread to execute Python bytecode at a time.

**Impact:**
- CPU-bound Python code doesn't benefit from multiple threads
- I/O-bound code can still benefit (threads release GIL during I/O)
- Use multiprocessing for CPU parallelism

```python
# Threading (limited by GIL for CPU work)
import threading

# Multiprocessing (bypasses GIL)
import multiprocessing

# Async I/O (efficient for I/O bound)
import asyncio
```

**Follow-up:** How does this affect data engineering workloads?

## Advanced Python Patterns

### 19. **What are decorators and how do they work?**
**Answer:** Decorators are functions that modify other functions:
```python
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer_decorator
def expensive_computation():
    # Some expensive operation
    pass

# Equivalent to: expensive_computation = timer_decorator(expensive_computation)
```

**Common uses:**
- Logging
- Timing
- Authentication
- Caching
- Validation

**Follow-up:** How would you create a decorator with arguments?

### 20. **Explain metaclasses and their practical use cases**
**Answer:** Metaclasses are classes of classes that control class creation:
```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = create_connection()
```

**Practical uses:**
- Singleton pattern
- ORM class registration
- API schema validation
- Automatic property creation

**Follow-up:** When should you avoid metaclasses?

## Scenario-Based Questions

### 21. **You need to process real-time streaming data. Which Python features would you use?**
**Answer:**
```python
# 1. Generators for lazy processing
def stream_data(source):
    while True:
        chunk = source.get_chunk()
        if not chunk:
            break
        yield process(chunk)

# 2. Async/await for I/O efficiency
async def process_stream():
    async for data in async_stream():
        await process_async(data)

# 3. Queue for producer-consumer pattern
from queue import Queue
from threading import Thread

def producer(q):
    while True:
        data = get_data()
        q.put(data)

def consumer(q):
    while True:
        data = q.get()
        process(data)
        q.task_done()
```

**Follow-up:** How would you handle backpressure?

### 22. **Design a memory-efficient data pipeline for processing 1TB of logs**
**Answer:**
```python
# Architecture:
# 1. Chunked reading with generators
# 2. Streaming transformations
# 3. Disk-based intermediate storage
# 4. Parallel processing with multiprocessing

import multiprocessing
from pathlib import Path

def process_logs_parallel(log_files, num_workers=4):
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.imap_unordered(process_single_log, log_files)
        for result in results:
            store_result(result)

def process_single_log(log_file):
    # Process one file at a time
    with open(log_file, 'r') as f:
        for line in f:
            yield parse_log_line(line)
```

**Follow-up:** How would you monitor memory usage during execution?

### 23. **Debug a memory leak in a long-running Python service**
**Answer:**
```python
# 1. Use memory profiler
import tracemalloc

tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)

# 2. Check for reference cycles
import gc
gc.collect()
print(f"Objects: {len(gc.get_objects())}")

# 3. Common culprits:
# - Cached data growing unbounded
# - Unclosed file handles/connections
# - Global variables accumulating data
# - Circular references
```

**Follow-up:** What tools would you use for production monitoring?

### 24. **Optimize a slow data transformation function**
**Answer:**
```python
# Before optimization
def slow_transform(data):
    result = []
    for item in data:
        transformed = complex_calculation(item)
        if filter_condition(transformed):
            result.append(transformed)
    return result

# After optimization
def fast_transform(data):
    # 1. Use vectorized operations if possible
    # 2. Use list comprehensions
    # 3. Use built-in functions
    # 4. Profile to find bottlenecks
    
    return [
        transformed 
        for item in data 
        if filter_condition(transformed := complex_calculation(item))
    ]

# Further optimization: Use numpy/pandas for numerical data
import numpy as np
def vectorized_transform(data):
    arr = np.array(data)
    return arr[arr > threshold] * multiplier
```

**Follow-up:** How would you benchmark the improvements?

### 25. **Implement a retry mechanism for unreliable external APIs**
**Answer:**
```python
import time
from functools import wraps
import random

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    
                    # Exponential backoff with jitter
                    sleep_time = current_delay * (backoff ** (attempts - 1))
                    sleep_time += random.uniform(0, 0.1 * sleep_time)  # Jitter
                    time.sleep(sleep_time)
            
            return func(*args, **kwargs)  # Final attempt
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2, backoff=2, exceptions=(ConnectionError, TimeoutError))
def call_unreliable_api():
    # API call here
    pass
```

**Follow-up:** How would you implement circuit breaker pattern?

---

## 🎯 Quick Reference

### Key Concepts to Master
1. **Iterators vs Generators**: Know when to use each
2. **Memory Management**: Generators, chunking, profiling
3. **Function Design**: Args/kwargs, decorators, closures
4. **Object Model**: Copy vs reference, identity vs equality
5. **Standard Library**: collections, itertools, functools, contextlib

### Common Interview Patterns
- "Explain the difference between X and Y"
- "How would you optimize this code for memory/performance?"
- "Design a system to handle scenario Z"
- "Debug this common Python gotcha"

### Preparation Tips
1. Practice writing generators and decorators from memory
2. Understand the memory implications of different data structures
3. Be ready to discuss real-world applications
4. Prepare examples from your experience

---

*Last Updated: 2026-04-19*  
*Total Questions: 25+ with follow-ups*  
*Estimated Study Time: 8-12 hours*