#!/usr/bin/env python3
"""
Python Deep Dive Solutions

Complete implementations for all Python deep dive practice exercises.
These solutions demonstrate advanced Python concepts essential for data engineering.
"""

import sys
import itertools
import collections
import pathlib
import datetime
import copy
import time
import csv
import json
import random
import math
from typing import Dict, List, Tuple, Any, Optional, Generator
from contextlib import contextmanager
from functools import reduce, lru_cache
import os
import tempfile

# ============================================================================
# Exercise 1: Iterators and Generators - SOLUTION
# ============================================================================

def exercise_1_iterators_and_generators_solution():
    """
    Solution for Exercise 1: Iterators and Generators
    """
    print("\n=== Exercise 1: Iterators and Generators ===")
    
    # 1. Custom iterator class Countdown
    class Countdown:
        def __init__(self, start: int):
            self.current = start
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            value = self.current
            self.current -= 1
            return value
    
    print("1. Countdown iterator:")
    countdown = Countdown(5)
    countdown_list = list(countdown)
    print(f"   Countdown from 5: {countdown_list}")
    
    # 2. Fibonacci generator function
    def fibonacci_sequence(n: int) -> Generator[int, None, None]:
        """Generate first n Fibonacci numbers."""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    print("\n2. Fibonacci sequence generator:")
    fib_numbers = list(fibonacci_sequence(10))
    print(f"   First 10 Fibonacci numbers: {fib_numbers}")
    
    # 3. Using enumerate() and zip()
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    
    print("\n3. Using enumerate() and zip():")
    print("   Using enumerate():")
    for i, name in enumerate(names, 1):
        print(f"     {i}. {name}")
    
    print("\n   Using zip():")
    for name, score in zip(names, scores):
        print(f"     {name}: {score}")
    
    # 4. Memory-efficient generator for large sequences
    print("\n4. Memory-efficient large sequence:")
    large_squares = (x**2 for x in range(1, 1001))
    first_five = [next(large_squares) for _ in range(5)]
    print(f"   First 5 squares from generator: {first_five}")
    print("   (Generator doesn't store all 1000 squares in memory)")
    
    return {
        "countdown_result": countdown_list,
        "fibonacci_result": fib_numbers,
        "enumerate_example": list(enumerate(names, 1)),
        "zip_example": list(zip(names, scores)),
        "generator_demo": "Memory-efficient squares generator"
    }

# ============================================================================
# Exercise 2: Advanced Comprehensions - SOLUTION
# ============================================================================

def exercise_2_comprehensions_solution():
    """
    Solution for Exercise 2: Advanced Comprehensions
    """
    print("\n=== Exercise 2: Advanced Comprehensions ===")
    
    # Sample data
    strings = ["data_science", "machine_learning", "data_engineering", 
               "python", "big_data", "data_analysis", "statistics"]
    
    # 1. Dictionary comprehension with condition
    data_dict = {s: len(s) for s in strings if 'data' in s}
    print("1. Dictionary of strings containing 'data':")
    for key, value in data_dict.items():
        print(f"   '{key}': {value}")
    
    # 2. Set comprehension for unique characters
    unique_chars = {char for s in strings for char in s if char != '_'}
    print(f"\n2. Unique characters (excluding underscores): {sorted(unique_chars)}")
    
    # 3. Nested list comprehension to flatten 2D list
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for row in matrix for item in row]
    print(f"\n3. Flattened 2D list: {flattened}")
    
    # 4. Generator expression for memory efficiency
    large_range = range(1, 1001)
    squares_gen = (x**2 for x in large_range)
    
    # Demonstrate memory efficiency
    import sys
    list_size = sys.getsizeof([x**2 for x in range(1, 1001)])
    gen_size = sys.getsizeof((x**2 for x in range(1, 1001)))
    
    print(f"\n4. Memory comparison:")
    print(f"   List comprehension size: {list_size} bytes")
    print(f"   Generator expression size: {gen_size} bytes")
    print(f"   Memory saved: {list_size - gen_size} bytes")
    
    # Get first 5 squares from generator
    first_five_squares = [next(squares_gen) for _ in range(5)]
    print(f"   First 5 squares from generator: {first_five_squares}")
    
    return {
        "data_dict": data_dict,
        "unique_chars_count": len(unique_chars),
        "flattened_matrix": flattened,
        "memory_savings_bytes": list_size - gen_size
    }

# ============================================================================
# Exercise 3: Unpacking, *args, and **kwargs - SOLUTION
# ============================================================================

def exercise_3_unpacking_and_args_solution():
    """
    Solution for Exercise 3: Unpacking, *args, and **kwargs
    """
    print("\n=== Exercise 3: Unpacking, *args, and **kwargs ===")
    
    # 1. Merge multiple dictionaries
    def merge_dicts(*dicts: Dict) -> Dict:
        """Merge multiple dictionaries, later dicts override earlier ones."""
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    dict3 = {"c": 5, "d": 6}
    
    merged = merge_dicts(dict1, dict2, dict3)
    print("1. Merged dictionaries:")
    print(f"   dict1: {dict1}")
    print(f"   dict2: {dict2}")
    print(f"   dict3: {dict3}")
    print(f"   merged: {merged}")
    
    # 2. Function with variable positional arguments
    def process_data(first, *middle, last):
        """Process data with variable positional arguments."""
        return {
            "first": first,
            "middle": middle,
            "last": last,
            "total_args": 2 + len(middle)
        }
    
    result = process_data("start", "data1", "data2", "data3", "end")
    print(f"\n2. Variable positional arguments:")
    print(f"   Result: {result}")
    
    # 3. Unpacking to transpose matrix
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transposed = list(zip(*matrix))
    print(f"\n3. Matrix transposition using unpacking:")
    print(f"   Original: {matrix}")
    print(f"   Transposed: {transposed}")
    
    # 4. Function with both *args and **kwargs
    def log_arguments(*args, **kwargs):
        """Log all arguments with metadata."""
        return {
            "args": args,
            "kwargs": kwargs,
            "args_count": len(args),
            "kwargs_count": len(kwargs),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    logged = log_arguments(1, 2, 3, name="Alice", age=30, city="NYC")
    print(f"\n4. Function with *args and **kwargs:")
    print(f"   Logged data: {logged}")
    
    # 5. Extended unpacking examples
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    first, *middle, last = numbers
    print(f"\n5. Extended unpacking:")
    print(f"   Numbers: {numbers}")
    print(f"   First: {first}, Middle: {middle}, Last: {last}")
    
    return {
        "merged_dict": merged,
        "process_data_result": result,
        "transposed_matrix": transposed,
        "log_result": logged,
        "unpacking_demo": {"first": first, "middle_len": len(middle), "last": last}
    }

# ============================================================================
# Exercise 4: Context Managers - SOLUTION
# ============================================================================

def exercise_4_context_managers_solution():
    """
    Solution for Exercise 4: Context Managers
    """
    print("\n=== Exercise 4: Context Managers ===")
    
    # 1. Timer context manager class
    class Timer:
        def __init__(self, name: str = "Operation"):
            self.name = name
            self.start_time = None
            self.end_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            print(f"⏱️  Starting {self.name}...")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.time()
            elapsed = self.end_time - self.start_time
            print(f"✅ {self.name} completed in {elapsed:.4f} seconds")
            if exc_type:
                print(f"⚠️  Exception occurred: {exc_type.__name__}: {exc_val}")
            return False  # Don't suppress exceptions
    
    # 2. FileHandler context manager
    class FileHandler:
        def __init__(self, filename: str, mode: str = 'r'):
            self.filename = filename
            self.mode = mode
            self.file = None
        
        def __enter__(self):
            try:
                self.file = open(self.filename, self.mode)
                print(f"📄 Opened file: {self.filename}")
                return self.file
            except Exception as e:
                print(f"❌ Error opening file: {e}")
                raise
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.file:
                self.file.close()
                print(f"📂 Closed file: {self.filename}")
            if exc_type:
                print(f"⚠️  Exception in file operation: {exc_type.__name__}")
            return False  # Don't suppress exceptions
    
    # 3. Generator-based context manager using contextlib
    @contextmanager
    def temporary_directory_change(new_dir: str):
        """Temporarily change working directory."""
        original_dir = os.getcwd()
        try:
            os.chdir(new_dir)
            print(f"📁 Changed directory to: {new_dir}")
            yield new_dir
        finally:
            os.chdir(original_dir)
            print(f"📁 Restored directory to: {original_dir}")
    
    # 4. Memory profiling context manager
    @contextmanager
    def memory_profiler(label: str = "Memory Usage"):
        """Profile memory usage within a context."""
        import psutil
        process = psutil.Process()
        
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        print(f"🧠 {label} - Before: {memory_before:.2f} MB")
        
        try:
            yield
        finally:
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_diff = memory_after - memory_before
            print(f"🧠 {label} - After: {memory_after:.2f} MB")
            print(f"🧠 {label} - Difference: {memory_diff:+.2f} MB")
    
    # Demonstrate usage
    print("1. Timer context manager:")
    with Timer("Heavy Computation"):
        # Simulate heavy computation
        sum(range(1000000))
    
    print("\n2. FileHandler context manager:")
    try:
        with FileHandler("test_file.txt", "w") as f:
            f.write("Test content for context manager demonstration\n")
            print("   File written successfully")
    except Exception as e:
        print(f"   File operation failed: {e}")
    
    print("\n3. Temporary directory change:")
    with temporary_directory_change("/tmp"):
        print("   Working in temporary directory")
        # Simulate some file operations
        temp_files = os.listdir(".")[:3]
        print(f"   First 3 files: {temp_files}")
    
    print("\n4. Memory profiler:")
    with memory_profiler("List Creation"):
        # Create a large list to show memory usage
        large_list = [i for i in range(100000)]
        print(f"   Created list with {len(large_list)} elements")
    
    # Clean up test file
    if os.path.exists("test_file.txt"):
        os.remove("test_file.txt")
        print("\n🧹 Cleaned up test_file.txt")
    
    return {
        "timer_demo": "Completed",
        "file_handler_demo": "File created and closed",
        "directory_change": "Temporary directory changed and restored",
        "memory_profiling": "Memory usage tracked"
    }

# ============================================================================
# Exercise 5: Lambda Functions and Functional Programming - SOLUTION
# ============================================================================

def exercise_5_lambdas_and_functional_solution():
    """
    Solution for Exercise 5: Lambda Functions and Functional Programming
    """
    print("\n=== Exercise 5: Lambda Functions and Functional Programming ===")
    
    # 1. Lambda with sorted()
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 22), ("Diana", 35)]
    sorted_by_age = sorted(data, key=lambda x: x[1])
    print("1. Sorted by age (second element):")
    for name, age in sorted_by_age:
        print(f"   {name}: {age}")
    
    # 2. Map and lambda for temperature conversion
    celsius_temps = [0, 10, 20, 30, 40]
    fahrenheit_temps = list(map(lambda c: (c * 9/5) + 32, celsius_temps))
    print(f"\n2. Temperature conversion (Celsius to Fahrenheit):")
    for c, f in zip(celsius_temps, fahrenheit_temps):
        print(f"   {c}°C = {f:.1f}°F")
    
    # 3. Filter and lambda for even numbers
    numbers = list(range(1, 21))
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"\n3. Even numbers from 1-20: {even_numbers}")
    
    # 4. Reduce for sum of squares
    from functools import reduce
    numbers = [1, 2, 3, 4, 5]
    sum_of_squares = reduce(lambda x, y: x + y**2, numbers, 0)
    print(f"\n4. Sum of squares of {numbers}: {sum_of_squares}")
    print(f"   Manual calculation: {sum([x**2 for x in numbers])}")
    
    # 5. Closure that generates multiplier functions
    def make_multiplier(factor: int):
        """Create a multiplier function."""
        def multiplier(x: int) -> int:
            return x * factor
        return multiplier
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    
    print("\n5. Closure examples:")
    print(f"   double(5) = {double(5)}")
    print(f"   triple(5) = {triple(5)}")
    
    # 6. Practical example: Processing data with functional programming
    transactions = [
        {"amount": 100, "category": "food"},
        {"amount": 200, "category": "entertainment"},
        {"amount": 50, "category": "food"},
        {"amount": 300, "category": "transport"},
        {"amount": 150, "category": "food"},
    ]
    
    # Filter food transactions
    food_transactions = list(filter(lambda t: t["category"] == "food", transactions))
    
    # Extract amounts
    food_amounts = list(map(lambda t: t["amount"], food_transactions))
    
    # Calculate total
    total_food = reduce(lambda x, y: x + y, food_amounts, 0)
    
    print("\n6. Practical example - Transaction processing:")
    print(f"   All transactions: {transactions}")
    print(f"   Food transactions: {food_transactions}")
    print(f"   Food amounts: {food_amounts}")
    print(f"   Total food spending: ${total_food}")
    
    return {
        "sorted_data": sorted_by_age,
        "temperature_conversion": dict(zip(celsius_temps, fahrenheit_temps)),
        "even_numbers": even_numbers,
        "sum_of_squares": sum_of_squares,
        "multiplier_demo": {"double(5)": double(5), "triple(5)": triple(5)},
        "transaction_analysis": {
            "food_transactions": len(food_transactions),
            "total_food_spending": total_food
        }
    }

# ============================================================================
# Exercise 6: Copy vs View (Mutation and References) - SOLUTION
# ============================================================================

def exercise_6_copy_vs_view_solution():
    """
    Solution for Exercise 6: Copy vs View
    """
    print("\n=== Exercise 6: Copy vs View ===")
    
    # 1. Shallow vs Deep copy for nested structures
    print("1. Shallow vs Deep copy for nested structures:")
    
    original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    shallow_copy = copy.copy(original)
    deep_copy = copy.deepcopy(original)
    
    # Modify nested list in shallow copy
    shallow_copy[0][0] = 100
    deep_copy[0][0] = 200
    
    print(f"   Original: {original}")
    print(f"   Shallow copy (modified): {shallow_copy}")
    print(f"   Deep copy (modified): {deep_copy}")
    print(f"   Original after shallow copy modification: {original}")
    print("   Note: Shallow copy shares nested references!")
    
    # 2. List slicing creates shallow copy
    print("\n2. List slicing creates shallow copy:")
    list_a = [1, 2, 3, [4, 5]]
    list_b = list_a[:]  # Shallow copy via slicing
    
    list_b[0] = 100  # Modifies only list_b
    list_b[3][0] = 400  # Modifies both list_a and list_b
    
    print(f"   list_a: {list_a}")
    print(f"   list_b: {list_b}")
    print("   Note: Slicing creates shallow copy - nested list is shared!")
    
    # 3. Safe dictionary modification
    print("\n3. Safe dictionary modification:")
    
    def safe_modify_dict(original_dict: Dict, updates: Dict) -> Dict:
        """Return modified copy without affecting original."""
        modified = copy.deepcopy(original_dict)
        modified.update(updates)
        return modified
    
    user_data = {"name": "Alice", "age": 30, "preferences": {"theme": "dark"}}
    updates = {"age": 31, "preferences": {"theme": "light"}}
    
    modified_data = safe_modify_dict(user_data, updates)
    
    print(f"   Original: {user_data}")
    print(f"   Updates: {updates}")
    print(f"   Modified: {modified_data}")
    print(f"   Original unchanged: {user_data}")
    
    # 4. Simulating Pandas SettingWithCopyWarning scenario
    print("\n4. Simulating Pandas SettingWithCopyWarning:")
    
    # Create sample data similar to Pandas DataFrame
    data = {
        "id": [1, 2, 3, 4],
        "value": [10, 20, 30, 40],
        "category": ["A", "B", "A", "B"]
    }
    
    # Problematic pattern (similar to Pandas chained indexing)
    filtered_data = [row for row in zip(data["id"], data["value"], data["category"]) 
                     if row[2] == "A"]
    
    # Try to modify (this would cause SettingWithCopyWarning in Pandas)
    print("   Filtered data (category A):", filtered_data)
    print("   In Pandas, modifying a slice of DataFrame creates a copy warning")
    print("   Solution: Use .loc[] or .copy() explicitly")
    
    # 5. Performance comparison
    print("\n5. Performance comparison (copy vs reference):")
    
    large_list = list(range(1000000))
    
    import time
    
    # Reference assignment (fast)
    start = time.time()
    ref = large_list
    ref_time = time.time() - start
    
    # Shallow copy (slower)
    start = time.time()
    shallow = large_list[:]
    shallow_time = time.time() - start
    
    # Deep copy (slowest)
    start = time.time()
    deep = copy.deepcopy(large_list)
    deep_time = time.time() - start
    
    print(f"   Reference assignment: {ref_time:.6f}s")
    print(f"   Shallow copy: {shallow_time:.6f}s")
    print(f"   Deep copy: {deep_time:.6f}s")
    print(f"   Deep copy is {deep_time/ref_time:.1f}x slower than reference")
    
    return {
        "shallow_copy_demo": {
            "original": original,
            "shallow_modified": shallow_copy,
            "deep_modified": deep_copy
        },
        "slicing_demo": {
            "list_a": list_a,
            "list_b": list_b
        },
        "safe_modification": {
            "original": user_data,
            "modified": modified_data
        },
        "performance_comparison": {
            "reference_time": ref_time,
            "shallow_copy_time": shallow_time,
            "deep_copy_time": deep_time
        }
    }

# ============================================================================
# Exercise 7: Identity vs Equality Operators - SOLUTION
# ============================================================================

def exercise_7_identity_equality_operators_solution():
    """
    Solution for Exercise 7: Identity vs Equality Operators
    """
    print("\n=== Exercise 7: Identity vs Equality Operators ===")
    
    # 1. 'is' vs '==' with different scenarios
    print("1. 'is' vs '==' examples:")
    
    # Integers (small integers are cached in Python)
    a = 256
    b = 256
    print(f"   a = 256, b = 256")
    print(f"   a == b: {a == b}")  # True - same value
    print(f"   a is b: {a is b}")  # True - same object (cached)
    
    a = 257
    b = 257
    print(f"\n   a = 257, b = 257")
    print(f"   a == b: {a == b}")  # True - same value
    print(f"   a is b: {a is b}")  # False - different objects (not cached)
    
    # Strings (some are interned)
    s1 = "hello"
    s2 = "hello"
    s3 = "hello world"
    s4 = "hello world"
    
    print(f"\n   s1 = 'hello', s2 = 'hello'")
    print(f"   s1 == s2: {s1 == s2}")  # True
    print(f"   s1 is s2: {s1 is s2}")  # True (string interning)
    
    print(f"\n   s3 = 'hello world', s4 = 'hello world'")
    print(f"   s3 == s4: {s3 == s4}")  # True
    print(f"   s3 is s4: {s3 is s4}")  # May be True or False (implementation dependent)
    
    # 2. Proper None checks
    print("\n2. Proper None checks:")
    
    def process_value(value):
        """Demonstrate proper None checking."""
        # WRONG: if value == None:  # Avoid this
        # CORRECT:
        if value is None:
            return "Value is None"
        elif value is True:
            return "Value is True (identity check)"
        elif value == True:
            return "Value equals True (value check)"
        else:
            return f"Value is {value}"
    
    test_values = [None, True, 1, "hello"]
    for val in test_values:
        result = process_value(val)
        print(f"   process_value({repr(val)}) = {result}")
    
    # 3. 'in' operator for lists vs sets
    print("\n3. 'in' operator performance (list vs set):")
    
    # Create large list and set
    large_list = list(range(1000000))
    large_set = set(large_list)
    
    import time
    
    # Test membership at beginning
    start = time.time()
    result_list_start = 0 in large_list
    list_start_time = time.time() - start
    
    start = time.time()
    result_set_start = 0 in large_set
    set_start_time = time.time() - start
    
    # Test membership at end
    start = time.time()
    result_list_end = 999999 in large_list
    list_end_time = time.time() - start
    
    start = time.time()
    result_set_end = 999999 in large_set
    set_end_time = time.time() - start
    
    print(f"   List 'in' (start): {list_start_time:.6f}s")
    print(f"   Set 'in' (start): {set_start_time:.6f}s")
    print(f"   List 'in' (end): {list_end_time:.6f}s")
    print(f"   Set 'in' (end): {set_end_time:.6f}s")
    print(f"   Set is {list_end_time/set_end_time:.0f}x faster for end lookup")
    
    # 4. Operator chaining
    print("\n4. Operator chaining:")
    
    x, y, z = 5, 10, 15
    print(f"   x = {x}, y = {y}, z = {z}")
    print(f"   x < y < z: {x < y < z}")  # Equivalent to (x < y) and (y < z)
    print(f"   5 <= x <= 10: {5 <= x <= 10}")
    print(f"   'a' < 'b' < 'c': {'a' < 'b' < 'c'}")
    
    # 5. Custom class with __eq__ and __hash__
    print("\n5. Custom class with __eq__ and __hash__:")
    
    class Product:
        def __init__(self, id: int, name: str, price: float):
            self.id = id
            self.name = name
            self.price = price
        
        def __eq__(self, other):
            if not isinstance(other, Product):
                return False
            return self.id == other.id and self.name == other.name
        
        def __hash__(self):
            return hash((self.id, self.name))
        
        def __repr__(self):
            return f"Product(id={self.id}, name='{self.name}', price={self.price})"
    
    p1 = Product(1, "Laptop", 999.99)
    p2 = Product(1, "Laptop", 899.99)  # Same id and name, different price
    p3 = Product(2, "Mouse", 49.99)
    
    print(f"   p1: {p1}")
    print(f"   p2: {p2}")
    print(f"   p3: {p3}")
    print(f"   p1 == p2: {p1 == p2}")  # True (same id and name)
    print(f"   p1 == p3: {p1 == p3}")  # False
    
    # Using in sets (requires __hash__)
    product_set = {p1, p2, p3}
    print(f"   Set of products (duplicates removed): {product_set}")
    print(f"   Set size: {len(product_set)} (p1 and p2 are equal, so only one)")
    
    return {
        "identity_vs_equality": {
            "256_is_same": 256 is 256,
            "257_is_same": 257 is 257,
            "hello_is_same": "hello" is "hello"
        },
        "none_check_demo": [process_value(v) for v in test_values],
        "performance_comparison": {
            "list_in_start": list_start_time,
            "set_in_start": set_start_time,
            "list_in_end": list_end_time,
            "set_in_end": set_end_time
        },
        "operator_chaining": {
            "x_lt_y_lt_z": x < y < z,
            "range_check": 5 <= x <= 10
        },
        "custom_class_demo": {
            "p1_eq_p2": p1 == p2,
            "p1_eq_p3": p1 == p3,
            "set_size": len(product_set)
        }
    }

# ============================================================================
# Exercise 8: Standard Library Glue Code - SOLUTION
# ============================================================================

def exercise_8_stdlib_glue_solution():
    """
    Solution for Exercise 8: Standard Library Glue Code
    """
    print("\n=== Exercise 8: Standard Library Glue Code ===")
    
    import tempfile
    import shutil
    
    # 1. pathlib to find CSV files
    print("1. Finding CSV files with pathlib:")
    
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = pathlib.Path(tmpdir)
        
        # Create test files
        (tmp_path / "data1.csv").write_text("col1,col2,col3\n1,2,3")
        (tmp_path / "data2.txt").write_text("Not a CSV")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "data3.csv").write_text("a,b,c\n4,5,6")
        (tmp_path / "data4.CSV").write_text("uppercase extension")
        
        # Find all CSV files recursively
        csv_files = list(tmp_path.rglob("*.csv")) + list(tmp_path.rglob("*.CSV"))
        print(f"   Found {len(csv_files)} CSV files:")
        for f in csv_files:
            print(f"     - {f.relative_to(tmp_path)}")
    
    # 2. datetime for business days calculation
    print("\n2. Business days between dates:")
    
    def business_days_between(start_date, end_date):
        """Calculate business days between two dates (exclusive)."""
        from datetime import timedelta
        
        business_days = 0
        current_date = start_date + timedelta(days=1)
        
        while current_date < end_date:
            if current_date.weekday() < 5:  # Monday=0, Friday=4
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    
    start = datetime.date(2024, 1, 1)  # Monday
    end = datetime.date(2024, 1, 10)   # Wednesday (9 days later)
    
    bd = business_days_between(start, end)
    total_days = (end - start).days - 1
    print(f"   From {start} to {end}:")
    print(f"   Total days (exclusive): {total_days}")
    print(f"   Business days: {bd}")
    print(f"   Weekend days: {total_days - bd}")
    
    # 3. collections.Counter for word frequency
    print("\n3. Most common words with collections.Counter:")
    
    text = """
    Python is an interpreted high-level general-purpose programming language. 
    Python's design philosophy emphasizes code readability with its notable 
    use of significant indentation. Its language constructs as well as its 
    object-oriented approach aim to help programmers write clear, logical 
    code for small and large-scale projects.
    """
    
    # Clean and count words
    words = text.lower().split()
    words = [word.strip('.,!?;:"\'') for word in words if word.strip('.,!?;:"\'')]
    
    word_counts = collections.Counter(words)
    most_common = word_counts.most_common(5)
    
    print(f"   Text sample: {text[:50]}...")
    print(f"   Top 5 most common words:")
    for word, count in most_common:
        print(f"     '{word}': {count}")
    
    # 4. itertools combinations and permutations
    print("\n4. itertools combinations and permutations:")
    
    items = ['A', 'B', 'C']
    
    print("   Combinations of 2 (order doesn't matter):")
    for combo in itertools.combinations(items, 2):
        print(f"     {combo}")
    
    print("\n   Permutations of 2 (order matters):")
    for perm in itertools.permutations(items, 2):
        print(f"     {perm}")
    
    # 5. functools.lru_cache for memoization
    print("\n5. functools.lru_cache for expensive calculations:")
    
    @lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number with memoization."""
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # First call (computes recursively)
    start = time.time()
    fib_30 = fibonacci(30)
    first_time = time.time() - start
    
    # Second call (from cache)
    start = time.time()
    fib_30_cached = fibonacci(30)
    cached_time = time.time() - start
    
    print(f"   fibonacci(30) = {fib_30}")
    print(f"   First computation: {first_time:.6f}s")
    print(f"   Cached computation: {cached_time:.6f}s")
    print(f"   Speedup: {first_time/cached_time:.0f}x")
    
    # 6. Practical example: Processing log files
    print("\n6. Practical example: Processing simulated log files")
    
    # Create sample log data
    logs = [
        "2024-01-01 INFO: User login successful",
        "2024-01-01 ERROR: Database connection failed",
        "2024-01-01 WARNING: High memory usage",
        "2024-01-02 INFO: Backup completed",
        "2024-01-02 ERROR: File not found",
        "2024-01-02 INFO: User logout",
        "2024-01-03 WARNING: Disk space low",
        "