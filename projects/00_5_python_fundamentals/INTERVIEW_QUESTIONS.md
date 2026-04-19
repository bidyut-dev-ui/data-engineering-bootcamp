# Python Fundamentals Interview Questions

## 📋 Table of Contents
1. [Basic Python Concepts](#basic-python-concepts)
2. [Data Structures](#data-structures)
3. [Functions and Scope](#functions-and-scope)
4. [Object-Oriented Programming](#object-oriented-programming)
5. [File Handling and I/O](#file-handling-and-io)
6. [Error Handling](#error-handling)
7. [Modules and Packages](#modules-and-packages)
8. [Pythonic Code](#pythonic-code)
9. [Memory Management](#memory-management)
10. [Problem-Solving Questions](#problem-solving-questions)

---

## Basic Python Concepts

### 1. **What is Python? What are its key features?**
**Answer:** Python is a high-level, interpreted, dynamically-typed programming language known for:
- Readable and clean syntax
- Dynamic typing (no need to declare variable types)
- Automatic memory management (garbage collection)
- Extensive standard library
- Support for multiple programming paradigms (OOP, functional, procedural)
- Platform independence
- Large community and ecosystem

### 2. **Explain the difference between Python 2 and Python 3**
**Answer:**
- **Print statement:** Python 2 uses `print "Hello"`, Python 3 uses `print("Hello")`
- **Integer division:** Python 2 returns integer for `5/2` (2), Python 3 returns float (2.5)
- **Unicode:** Python 2 has ASCII strings by default, Python 3 uses Unicode
- **xrange vs range:** Python 2 has both, Python 3's `range` works like `xrange`
- **Error handling:** Python 3 uses `except Exception as e` syntax
- **Iterators:** Python 3's `dict.keys()`, `dict.values()`, `dict.items()` return views, not lists

### 3. **What are Python's built-in data types?**
**Answer:**
- **Numeric:** `int`, `float`, `complex`
- **Sequence:** `str`, `list`, `tuple`, `range`
- **Mapping:** `dict`
- **Set:** `set`, `frozenset`
- **Boolean:** `bool`
- **Binary:** `bytes`, `bytearray`, `memoryview`
- **None:** `NoneType`

### 4. **Explain mutable vs immutable types in Python**
**Answer:**
- **Mutable:** Can be changed after creation
  - Examples: `list`, `dict`, `set`, `bytearray`
  - `my_list.append(5)` modifies the original list
- **Immutable:** Cannot be changed after creation
  - Examples: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`
  - `new_string = old_string + "!"` creates a new string

### 5. **What is the difference between `is` and `==`?**
**Answer:**
- `==` checks for **value equality** (are the values the same?)
- `is` checks for **identity equality** (are they the same object in memory?)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - same values
print(a is b)  # False - different objects
print(a is c)  # True - same object
```

### 6. **Explain Python's garbage collection**
**Answer:** Python uses automatic garbage collection with:
1. **Reference counting:** Each object has a count of references; when it reaches 0, memory is freed
2. **Cyclic garbage collector:** Detects and collects cycles of objects that reference each other
3. **Generational garbage collection:** Objects are grouped by age; younger objects are collected more frequently

### 7. **What are Python decorators?**
**Answer:** Decorators are functions that modify the behavior of other functions. They use the `@decorator` syntax.

```python
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    import time
    time.sleep(1)
    return "Done"
```

---

## Data Structures

### 8. **Compare lists, tuples, sets, and dictionaries**
**Answer:**

| Feature | List | Tuple | Set | Dictionary |
|---------|------|-------|-----|------------|
| **Mutable** | Yes | No | Yes | Yes (keys immutable) |
| **Ordered** | Yes | Yes | No (Python 3.7+ ordered) | Yes (Python 3.7+ ordered) |
| **Indexed** | Yes | Yes | No | By key |
| **Duplicates** | Allowed | Allowed | Not allowed | Keys unique, values can duplicate |
| **Use Case** | Sequence of items | Fixed data, coordinates | Unique items, membership tests | Key-value pairs |

### 9. **What are list comprehensions? Provide an example**
**Answer:** List comprehensions provide a concise way to create lists.

```python
# Traditional approach
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
```

### 10. **Explain dictionary comprehensions**
**Answer:** Similar to list comprehensions but for dictionaries.

```python
# Create dictionary of squares
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Swap keys and values
original = {'a': 1, 'b': 2, 'c': 3}
swapped = {value: key for key, value in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
```

### 11. **What is the difference between `append()` and `extend()` for lists?**
**Answer:**
- `append()` adds its argument as a single element
- `extend()` iterates over its argument and adds each element

```python
list1 = [1, 2, 3]
list2 = [4, 5]

list1.append(list2)
print(list1)  # [1, 2, 3, [4, 5]]

list1 = [1, 2, 3]
list1.extend(list2)
print(list1)  # [1, 2, 3, 4, 5]
```

### 12. **How do you copy a list?**
**Answer:**
```python
import copy

original = [1, 2, [3, 4]]

# Shallow copy (copies references to nested objects)
shallow = original.copy()  # or shallow = original[:]
shallow[2][0] = 99
print(original)  # [1, 2, [99, 4]] - nested list changed!

# Deep copy (creates new objects for nested structures)
original = [1, 2, [3, 4]]
deep = copy.deepcopy(original)
deep[2][0] = 99
print(original)  # [1, 2, [3, 4]] - original unchanged
```

---

## Functions and Scope

### 13. **Explain `*args` and `**kwargs`**
**Answer:**
- `*args` collects positional arguments into a tuple
- `**kwargs` collects keyword arguments into a dictionary

```python
def example_function(*args, **kwargs):
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

example_function(1, 2, 3, name="Alice", age=30)
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'Alice', 'age': 30}
```

### 14. **What is the difference between local and global variables?**
**Answer:**
- **Local variables:** Defined inside a function, accessible only within that function
- **Global variables:** Defined outside functions, accessible throughout the module

```python
x = 10  # Global variable

def func():
    y = 20  # Local variable
    global x  # Declare we're using the global x
    x = 30   # Modifies global x
    
func()
print(x)  # 30
# print(y)  # Error: y is not defined
```

### 15. **What are lambda functions?**
**Answer:** Anonymous functions defined with the `lambda` keyword.

```python
# Regular function
def add(x, y):
    return x + y

# Lambda function
add_lambda = lambda x, y: x + y

# Common use case: sorting
students = [("Alice", 25), ("Bob", 20), ("Charlie", 30)]
students.sort(key=lambda student: student[1])  # Sort by age
```

### 16. **Explain the `map()`, `filter()`, and `reduce()` functions**
**Answer:**
- `map()`: Applies a function to all items in an input list
- `filter()`: Creates a list of elements for which a function returns true
- `reduce()`: Applies a rolling computation to sequential pairs of values

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map: square each number
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]

# filter: keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# reduce: calculate product
product = reduce(lambda x, y: x * y, numbers)  # 120
```

### 17. **What are generators? How do they differ from lists?**
**Answer:** Generators are functions that use `yield` to produce a sequence of values lazily.

```python
# Generator function
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

# Generator expression
squares_gen = (x**2 for x in range(1000000))  # Memory efficient

# Differences:
# - Generators produce values on-the-fly (lazy evaluation)
# - Generators are memory efficient (don't store all values)
# - Generators can only be iterated once
# - Generators use `yield`, functions use `return`
```

---

## Object-Oriented Programming

### 18. **Explain the four pillars of OOP in Python**
**Answer:**
1. **Encapsulation:** Bundling data and methods that operate on that data
2. **Abstraction:** Hiding complex implementation details
3. **Inheritance:** Creating new classes from existing ones
4. **Polymorphism:** Objects of different classes responding to the same method

### 19. **What is the difference between `__init__` and `__new__`?**
**Answer:**
- `__new__` is a static method that creates and returns a new instance
- `__init__` is an instance method that initializes the newly created object

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        print("Creating instance")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, value):
        print("Initializing instance")
        self.value = value
```

### 20. **Explain method types in Python classes**
**Answer:**
1. **Instance methods:** Operate on instance data, receive `self` as first parameter
2. **Class methods:** Operate on class-level data, receive `cls` as first parameter, use `@classmethod` decorator
3. **Static methods:** Don't operate on instance or class data, use `@staticmethod` decorator

```python
class MyClass:
    class_var = "class value"
    
    def __init__(self, value):
        self.instance_var = value
    
    def instance_method(self):
        return f"Instance: {self.instance_var}"
    
    @classmethod
    def class_method(cls):
        return f"Class: {cls.class_var}"
    
    @staticmethod
    def static_method():
        return "Static method"
```

### 21. **What are properties in Python?**
**Answer:** Properties allow you to use getter/setter methods while maintaining attribute syntax.

```python
class Person:
    def __init__(self, name):
        self._name = name  # Private attribute
    
    @property
    def name(self):
        print("Getting name")
        return self._name
    
    @name.setter
    def name(self, value):
        print("Setting name")
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

person = Person("Alice")
print(person.name)  # Calls getter
person.name = "Bob"  # Calls setter
```

### 22. **Explain multiple inheritance and the MRO (Method Resolution Order)**
**Answer:** Python uses C3 Linearization algorithm for MRO.

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

print(D.mro())  # [D, B, C, A, object]
d = D()
print(d.method())  # "B" (from class B)
```

---

## File Handling and I/O

### 23. **How do you read a file in Python?**
**Answer:**
```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Read all lines into list
with open("file.txt", "r") as f:
    lines = f.readlines()
```

### 24. **What is the difference between `read()`, `readline()`, and `readlines()`?**
**Answer:**
- `read()`: Reads entire file as a single string
- `readline()`: Reads next line as a string
- `readlines()`: Reads all lines as a list of strings

### 25. **Explain context managers and the `with` statement**
**Answer:** Context managers ensure resources are properly managed (opened/closed).

```python
# Using with statement (automatically closes file)
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed here

# Creating custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name):
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end-start:.2f} seconds")

with timer("My function"):
    # Code to time
    import time
    time.sleep(1)
```

---

## Error Handling

### 26. **Explain Python's exception hierarchy**
**Answer:**
```
BaseException
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    └── OverflowError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── TypeError
      ├── ValueError
      ├── FileNotFoundError
      └── ... many more
```

### 27. **What is the difference between `try-except`, `try-finally`, and `try-except-finally`?**
**Answer:**
- `try-except`: Catches and handles exceptions
- `try-finally`: Always executes cleanup code, even if exception occurs
- `try-except-finally`: Handles exceptions and always executes cleanup

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("This always executes")
```

### 28. **How do you create custom exceptions?**
**Answer:**
```python
class ValidationError(Exception):
    """Custom exception for validation errors"""
    
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field
    
    def __str__(self):
        if self.field:
            return f"Validation error in {self.field}: {self.args[0]}"
        return f"Validation error: {self.args[0]}"

# Usage
def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative", field="age")
    if age > 150:
        raise ValidationError("Age is unrealistic", field="age")
```

---

## Modules and Packages

### 29. **What is the difference between a module and a package?**
**Answer:**
- **Module:** A single Python file (.py) containing code
- **Package:** A directory containing multiple modules and an `__init__.py` file

### 30. **Explain `__name__ == "__main__"`**
**Answer:** This check allows code to run only when the module is executed directly, not when imported.

```python
# mymodule.py
def my_function():
    return "Hello"

if __name__ == "__main__":
    # This runs only when executing: python mymodule.py
    print("Running as main program")
    print(my_function())
```

### 31. **How does Python find modules?**
**Answer:** Python searches for modules in:
1. Current directory
2. Directories in `PYTHONPATH` environment variable
3. Installation-dependent default paths (site-packages)

---

## Pythonic Code

### 32. **What does "Pythonic" mean?**
**Answer:** Code that follows Python idioms and conventions, making it:
- Readable and clear
- Simple and explicit
- Using Python's features effectively
- Following PEP 8 style guide

### 33. **Give examples of Pythonic vs non-Pythonic code**
**Answer:**
```python
# Non-Pythonic
for i in range(len(my_list)):
    print(my_list[i])

# Pythonic
for item in my_list:
    print(item)

# Even more Pythonic with enumerate
for i, item in enumerate(my_list):
    print(f"{i}: {item}")
```

### 34. **What are some common Python idioms?**
**Answer:**
- **Swapping variables:** `a, b = b, a`
- **List comprehension:** `[x**2 for x in range(10)]`
- **Dictionary get with default:** `value = my_dict.get(key, default)`
- **String joining:** `", ".join(items)` instead of loop with `+=`
- **Context managers:** `with open(...) as f:`
- **Multiple assignment:** `x, y, z = coordinates`

---

## Memory Management

### 35. **How does Python manage memory for large datasets?**
**Answer:**
1. **Use generators** instead of lists for large sequences
2. **Process data in chunks** rather than loading everything at once
3. **Delete unused variables** with `del` keyword
4. **Use `sys.getsizeof()`** to check memory usage
5. **Consider using `array` or `numpy`** for numerical data

```python
import sys

# Process large file in chunks
def process_large_file(filename, chunk_size=10000):
    with open(filename, 'r') as f:
        while True:
            chunk = f.readlines(chunk_size)
            if not chunk:
                break
            process_chunk(chunk)
```

### 36. **What is the Global Interpreter Lock (GIL)?**
**Answer:** The GIL is a mutex that allows only one thread to execute Python bytecode at a time in CPython. This means:
- Python threads cannot run in parallel on multiple CPU cores
- I/O-bound tasks can still benefit from threading
- CPU-bound tasks are better with multiprocessing
- Some Python implementations (Jython, IronPython) don't have GIL

---

## Problem-Solving Questions

### 37. **Reverse a string**
```python
def reverse_string(s):
    return s[::-1]

# Test
print(reverse_string("hello"))  # "olleh"
```

### 38. **Find the most frequent element in a list**
```python
from collections import Counter

def most_frequent(lst):
    if not lst:
        return None
    return Counter(lst).most_common(1)[0][0]

# Without Counter
def most_frequent_manual(lst):
    if not lst:
        return None
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    return max(freq, key=freq.get)
```

### 39. **Check if two strings are anagrams**
```python
def are_anagrams(str1, str2):
    return sorted(str1.lower().replace(" ", "")) == sorted(str2.lower().replace(" ", ""))

# Test
print(are_anagrams("listen", "silent"))  # True
print(are_anagrams("hello", "world"))    # False
```

### 40. **Find the first non-repeating character in a string**
```python
from collections import Counter

def first_non_repeating_char(s):
    freq = Counter(s)
    for char in s:
        if freq[char] == 1:
            return char
    return None

# Test
print(first_non_repeating_char("swiss"))  # "w"
print(first_non_repeating_char("aabb"))   # None
```

### 41. **Implement a stack using lists**
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

### 42. **Merge two sorted lists**
```python
def merge_sorted_lists(list1, list2):
    merged = []
    i = j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    
    # Add remaining elements
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    
    return merged

# Test
print(merge_sorted_lists([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]
```

### 43. **Find the missing number in a list of 1 to n**
```python
def find_missing_number(nums, n):
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum

# Test
print(find_missing_number([1, 2, 4, 5], 5))  # 3
```

### 44. **Check for balanced parentheses**
```python
def is_balanced(expression):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                return False
    
    return len(stack) == 0

# Test
print(is_balanced("({[]})"))  # True
print(is_balanced("({[})"))   # False
```

### 45. **Find all pairs in a list that sum to a target**
```python
def find_pairs(nums, target):
    seen = set()
    pairs = []
    
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    
    return pairs

# Test
print(find_pairs([1, 2, 3, 4, 5], 6))  # [(2, 4), (1, 5)]
```

---

## 🎯 Interview Preparation Tips

### 1. **Before the Interview**
- Review Python fundamentals thoroughly
- Practice coding problems on platforms like LeetCode, HackerRank
- Understand time and space complexity
- Prepare examples of your Python projects

### 2. **During the Interview**
- **Clarify requirements:** Ask questions before coding
- **Think aloud:** Explain your thought process
- **Start simple:** Provide a brute-force solution first, then optimize
- **Test your code:** Walk through examples and edge cases
- **Discuss trade-offs:** Explain time/space complexity

### 3. **Common Mistakes to Avoid**
- Not handling edge cases (empty lists, None values)
- Using `==` instead of `is` for None/True/False comparisons
- Modifying lists while iterating over them
- Not using context managers for file operations
- Ignoring Python's built-in functions and libraries

### 4. **Questions to Ask the Interviewer**
- "What Python version does the team use?"
- "What Python libraries/frameworks are commonly used?"
- "How is the codebase structured (monolith, microservices)?"
- "What's the team's development workflow?"
- "What opportunities are there for learning and growth?"

---

## 📚 Resources for Further Learning

### Books
- "Python Crash Course" by Eric Matthes (beginners)
- "Fluent Python" by Luciano Ramalho (intermediate/advanced)
- "Effective Python" by Brett Slatkin (best practices)

### Online Courses
- Coursera: "Python for Everybody"
- Real Python tutorials
- Codecademy Python course

### Practice Platforms
- LeetCode (filter by Python problems)
- HackerRank (Python domain)
- Codewars (Python katas)
- Exercism (Python track)

### Documentation
- [Python Official Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Standard Library](https://docs.python.org/3/library/index.html)

---

**Remember:** Python interviews test not just syntax, but problem-solving skills, understanding of Python's philosophy, and ability to write clean, efficient, and maintainable code. Practice regularly and build projects to solidify your understanding.