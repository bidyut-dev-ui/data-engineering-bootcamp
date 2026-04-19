"""
Practice Exercises for Python Deep Dive Project

This file contains hands-on exercises to reinforce advanced Python concepts
that are essential for working with Pandas and data engineering.
These exercises are designed for 8GB RAM laptops with no GPU.
"""

import sys
import itertools
import collections
import pathlib
import datetime
import copy

def exercise_1_iterators_and_generators():
    """
    Exercise 1: Iterators and Generators
    
    Task: Implement a custom iterator class and a generator function.
    
    Requirements:
    1. Create a class `Countdown` that implements the iterator protocol:
       - __init__(self, start): Initialize with start value
       - __iter__(self): Return self
       - __next__(self): Return current value and decrement until 0, then raise StopIteration
    
    2. Create a generator function `fibonacci_sequence(n)` that yields the first n
       Fibonacci numbers.
    
    3. Use enumerate() and zip() to process two lists simultaneously.
    
    Memory Constraint: Use generators for large sequences to avoid memory overhead.
    """
    # TODO: Implement this function
    pass

def exercise_2_comprehensions():
    """
    Exercise 2: Advanced Comprehensions
    
    Task: Use list, dict, and set comprehensions to solve data processing problems.
    
    Requirements:
    1. Given a list of strings, create a dictionary where keys are strings and
       values are their lengths, but only for strings containing 'data'.
    
    2. Create a set of all unique characters from a list of strings, excluding spaces.
    
    3. Use nested list comprehension to flatten a 2D list.
    
    4. Create a generator expression that yields squares of numbers 1-1000
       without storing all results in memory.
    
    Memory Constraint: Use generator expressions for large ranges.
    """
    # TODO: Implement this function
    pass

def exercise_3_unpacking_and_args():
    """
    Exercise 3: Unpacking, *args, and **kwargs
    
    Task: Master unpacking techniques for flexible function design.
    
    Requirements:
    1. Write a function `merge_dicts(*dicts)` that merges multiple dictionaries.
       Later dictionaries should override earlier ones for conflicting keys.
    
    2. Implement a function `process_data(first, *middle, last)` that handles
       variable positional arguments.
    
    3. Use unpacking to transpose a matrix represented as list of lists.
    
    4. Create a function with both *args and **kwargs that logs all arguments.
    """
    # TODO: Implement this function
    pass

def exercise_4_context_managers():
    """
    Exercise 4: Context Managers
    
    Task: Create custom context managers for resource management.
    
    Requirements:
    1. Implement a context manager `Timer` that measures execution time.
    
    2. Create a context manager `FileHandler` that safely opens a file,
       ensures it's closed, and handles exceptions.
    
    3. Use contextlib.contextmanager decorator to create a generator-based
       context manager for temporary directory changes.
    
    4. Implement a context manager that profiles memory usage.
    """
    # TODO: Implement this function
    pass

def exercise_5_lambdas_and_functional():
    """
    Exercise 5: Lambda Functions and Functional Programming
    
    Task: Use lambda functions, map, filter, and reduce effectively.
    
    Requirements:
    1. Use lambda with sorted() to sort a list of tuples by second element.
    
    2. Use map() and lambda to convert a list of temperatures from Celsius to Fahrenheit.
    
    3. Use filter() and lambda to extract even numbers from a list.
    
    4. Implement a simple reduce operation (sum of squares) without using loops.
    
    5. Create a closure that generates multiplier functions.
    """
    # TODO: Implement this function
    pass

def exercise_6_copy_vs_view():
    """
    Exercise 6: Copy vs View (Mutation and References)
    
    Task: Understand object references, shallow vs deep copy, and mutation.
    
    Requirements:
    1. Demonstrate the difference between shallow and deep copy for nested structures.
    
    2. Show how list slicing creates a shallow copy.
    
    3. Create a function that safely modifies a dictionary without affecting the original.
    
    4. Demonstrate the "SettingWithCopyWarning" scenario that occurs in Pandas.
    
    Memory Constraint: Use copy.deepcopy() judiciously for large objects.
    """
    # TODO: Implement this function
    pass

def exercise_7_identity_equality_operators():
    """
    Exercise 7: Identity vs Equality Operators
    
    Task: Master 'is' vs '==', None checks, and operator behavior.
    
    Requirements:
    1. Write examples showing when `is` and `==` give different results.
    
    2. Create proper None checks using `is` operator.
    
    3. Demonstrate the difference between `in` operator for lists vs sets.
    
    4. Show how operator chaining works (e.g., `a < b < c`).
    
    5. Implement a custom class with __eq__ and __hash__ methods.
    """
    # TODO: Implement this function
    pass

def exercise_8_stdlib_glue():
    """
    Exercise 8: Standard Library Glue Code
    
    Task: Use Python's standard library for common data engineering tasks.
    
    Requirements:
    1. Use pathlib to recursively find all .csv files in a directory tree.
    
    2. Use datetime to calculate business days between two dates.
    
    3. Use collections.Counter to find the most common words in a text.
    
    4. Use itertools to generate combinations and permutations.
    
    5. Use functools.lru_cache to memoize expensive function calls.
    """
    # TODO: Implement this function
    pass

def exercise_9_integration_challenge():
    """
    Exercise 9: Integration Challenge
    
    Task: Combine multiple concepts to solve a real-world data problem.
    
    Scenario: You're processing a dataset of sales transactions.
    
    Requirements:
    1. Read a CSV file using a context manager.
    2. Use generator to process rows one by one (memory-efficient).
    3. Use comprehensions to filter and transform data.
    4. Use itertools to group data by category.
    5. Use collections to aggregate results.
    6. Write results using pathlib.
    
    Memory Constraint: Process file in chunks, don't load entire file into memory.
    """
    # TODO: Implement this function
    pass

def main():
    """
    Main function to run all exercises.
    """
    print("Python Deep Dive Practice Exercises")
    print("=" * 50)
    
    exercises = [
        ("Iterators and Generators", exercise_1_iterators_and_generators),
        ("Comprehensions", exercise_2_comprehensions),
        ("Unpacking and Args", exercise_3_unpacking_and_args),
        ("Context Managers", exercise_4_context_managers),
        ("Lambdas and Functional", exercise_5_lambdas_and_functional),
        ("Copy vs View", exercise_6_copy_vs_view),
        ("Identity vs Equality", exercise_7_identity_equality_operators),
        ("Stdlib Glue", exercise_8_stdlib_glue),
        ("Integration Challenge", exercise_9_integration_challenge),
    ]
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * 30)
        try:
            func()
            print(f"  Exercise function called successfully")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("All exercises completed (stubs implemented)")

if __name__ == "__main__":
    main()