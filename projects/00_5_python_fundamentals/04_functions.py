"""
Tutorial 04: Functions in Python
=================================

Functions are reusable blocks of code that perform specific tasks.
This tutorial covers:
1. Function definition and calling
2. Parameters and arguments
3. Return values
4. Scope and namespaces
5. Default parameters and keyword arguments
6. Variable-length arguments (*args, **kwargs)
7. Lambda functions
8. Decorators (introduction)
9. Recursion

Learning Objectives:
- Define and call functions with various parameter types
- Understand variable scope (local vs global)
- Use lambda functions for simple operations
- Apply basic function decorators
- Write recursive functions

Prerequisites:
- Tutorial 01: Variables and Types
- Tutorial 02: Control Flow  
- Tutorial 03: Data Structures
"""

print("=" * 60)
print("TUTORIAL 04: FUNCTIONS")
print("=" * 60)

# ============================================================================
# 1. BASIC FUNCTION DEFINITION
# ============================================================================
print("\n1. BASIC FUNCTION DEFINITION")
print("-" * 40)

# Simple function without parameters
def greet():
    """Print a greeting message."""
    print("Hello, welcome to Python functions!")

# Calling the function
greet()

# Function with parameters
def greet_person(name):
    """Greet a specific person."""
    print(f"Hello, {name}! Nice to meet you.")

greet_person("Alice")
greet_person("Bob")

# Function with multiple parameters
def introduce(name, age, city):
    """Introduce someone with their details."""
    print(f"Meet {name}, {age} years old from {city}.")

introduce("Charlie", 25, "New York")

# ============================================================================
# 2. RETURN VALUES
# ============================================================================
print("\n2. RETURN VALUES")
print("-" * 40)

# Function that returns a value
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

result = add(5, 3)
print(f"add(5, 3) = {result}")

# Function that returns multiple values (as a tuple)
def get_min_max(numbers):
    """Return the minimum and maximum of a list."""
    return min(numbers), max(numbers)

min_val, max_val = get_min_max([3, 1, 4, 1, 5, 9, 2])
print(f"Min: {min_val}, Max: {max_val}")

# Function without explicit return returns None
def do_nothing():
    """This function does nothing."""
    pass

result = do_nothing()
print(f"do_nothing() returns: {result}")

# ============================================================================
# 3. DEFAULT PARAMETERS
# ============================================================================
print("\n3. DEFAULT PARAMETERS")
print("-" * 40)

def greet_with_default(name="Guest"):
    """Greet with a default name."""
    print(f"Hello, {name}!")

greet_with_default("Alice")  # Uses provided name
greet_with_default()         # Uses default name

def create_profile(name, age, city="Unknown", country="Unknown"):
    """Create a user profile with optional location."""
    print(f"Name: {name}, Age: {age}, City: {city}, Country: {country}")

create_profile("Bob", 30)
create_profile("Charlie", 25, "London")
create_profile("Diana", 28, "Paris", "France")

# ============================================================================
# 4. KEYWORD ARGUMENTS
# ============================================================================
print("\n4. KEYWORD ARGUMENTS")
print("-" * 40)

def describe_pet(pet_name, animal_type="dog"):
    """Describe a pet using keyword arguments."""
    print(f"I have a {animal_type} named {pet_name}.")

# Positional arguments (order matters)
describe_pet("Max", "dog")

# Keyword arguments (order doesn't matter)
describe_pet(animal_type="cat", pet_name="Whiskers")

# Mix of positional and keyword arguments
describe_pet("Buddy", animal_type="parrot")

# ============================================================================
# 5. VARIABLE-LENGTH ARGUMENTS (*args, **kwargs)
# ============================================================================
print("\n5. VARIABLE-LENGTH ARGUMENTS (*args, **kwargs)")
print("-" * 40)

# *args: variable number of positional arguments
def sum_all(*args):
    """Sum any number of arguments."""
    total = 0
    for num in args:
        total += num
    return total

print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(10, 20, 30, 40, 50) = {sum_all(10, 20, 30, 40, 50)}")

# **kwargs: variable number of keyword arguments
def print_profile(**kwargs):
    """Print a profile with any number of key-value pairs."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_profile(name="Alice", age=25, city="NYC")
print_profile(name="Bob", occupation="Engineer", hobby="Reading")

# Combining *args and **kwargs
def mixed_args(*args, **kwargs):
    """Accept both positional and keyword arguments."""
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

mixed_args(1, 2, 3, name="Alice", age=25)

# ============================================================================
# 6. SCOPE AND NAMESPACES
# ============================================================================
print("\n6. SCOPE AND NAMESPACES")
print("-" * 40)

# Global variable
global_var = "I'm global"

def demonstrate_scope():
    """Demonstrate local vs global scope."""
    # Local variable
    local_var = "I'm local"
    
    # Can access global variables
    print(f"Inside function - global_var: {global_var}")
    print(f"Inside function - local_var: {local_var}")
    
    # Modifying global variable (requires global keyword)
    global global_var
    global_var = "Modified global"
    
    # Nested function
    def inner_function():
        inner_var = "I'm in inner function"
        print(f"  Inside inner - inner_var: {inner_var}")
        print(f"  Inside inner - local_var (from outer): {local_var}")
    
    inner_function()

print(f"Outside function - global_var: {global_var}")
demonstrate_scope()
print(f"Outside function - global_var after modification: {global_var}")

# Cannot access local_var outside the function
# print(local_var)  # This would raise NameError

# ============================================================================
# 7. LAMBDA FUNCTIONS (ANONYMOUS FUNCTIONS)
# ============================================================================
print("\n7. LAMBDA FUNCTIONS (Anonymous Functions)")
print("-" * 40)

# Regular function
def square(x):
    return x ** 2

# Equivalent lambda function
square_lambda = lambda x: x ** 2

print(f"square(5) = {square(5)}")
print(f"square_lambda(5) = {square_lambda(5)}")

# Lambda with multiple parameters
add_lambda = lambda a, b: a + b
print(f"add_lambda(3, 4) = {add_lambda(3, 4)}")

# Lambda with conditional
is_even = lambda x: x % 2 == 0
print(f"is_even(4) = {is_even(4)}")
print(f"is_even(7) = {is_even(7)}")

# Using lambda with map()
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"Numbers: {numbers}")
print(f"Squared (using map+lambda): {squared}")

# Using lambda with filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers (using filter+lambda): {evens}")

# ============================================================================
# 8. FUNCTION DECORATORS (INTRODUCTION)
# ============================================================================
print("\n8. FUNCTION DECORATORS (Introduction)")
print("-" * 40)

# Simple decorator
def timer_decorator(func):
    """Decorator to measure function execution time."""
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper

# Using the decorator
@timer_decorator
def slow_function():
    """A function that takes some time."""
    import time
    time.sleep(0.5)  # Simulate work
    return "Done"

print("Calling decorated function:")
result = slow_function()
print(f"Result: {result}")

# Decorator with arguments
def repeat(n_times):
    """Decorator to repeat a function n times."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n_times):
                print(f"Call {i + 1}/{n_times}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

print("\nCalling repeat decorator:")
say_hello()

# ============================================================================
# 9. RECURSION
# ============================================================================
print("\n9. RECURSION")
print("-" * 40)

# Factorial using recursion
def factorial(n):
    """Calculate factorial using recursion."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

print(f"factorial(5) = {factorial(5)}")
print(f"factorial(0) = {factorial(0)}")

# Fibonacci sequence using recursion
def fibonacci(n):
    """Calculate nth Fibonacci number using recursion."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print(f"Fibonacci sequence (first 10 numbers):")
for i in range(10):
    print(f"  fibonacci({i}) = {fibonacci(i)}")

# Recursive directory traversal (simplified)
def count_files(depth, current_depth=0):
    """Simulate counting files in nested directories."""
    if current_depth > depth:
        return 0
    
    # Simulate files in current directory
    files_in_current = 3
    
    # Simulate subdirectories
    subdir_files = 0
    if current_depth < depth:
        for i in range(2):  # 2 subdirectories
            subdir_files += count_files(depth, current_depth + 1)
    
    return files_in_current + subdir_files

print(f"\nSimulated file count (depth=2): {count_files(2)}")

# ============================================================================
# 10. DOCSTRINGS AND TYPE HINTS
# ============================================================================
print("\n10. DOCSTRINGS AND TYPE HINTS")
print("-" * 40)

def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Parameters:
    -----------
    length : float
        The length of the rectangle
    width : float
        The width of the rectangle
    
    Returns:
    --------
    float
        The area of the rectangle (length * width)
    
    Examples:
    ---------
    >>> calculate_area(5, 3)
    15.0
    >>> calculate_area(2.5, 4.0)
    10.0
    """
    return length * width

# Accessing docstring
print("Function docstring:")
print(calculate_area.__doc__)

# Using the function
area = calculate_area(5, 3)
print(f"\nArea of rectangle (5 x 3): {area}")

# Type hints in practice
def process_data(data: list[int], multiplier: int = 1) -> list[int]:
    """Process a list of integers."""
    return [x * multiplier for x in data]

result = process_data([1, 2, 3], 2)
print(f"process_data([1, 2, 3], 2): {result}")

# ============================================================================
# 11. PRACTICE EXERCISES
# ============================================================================
print("\n11. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: Calculator Functions")
print("Create functions for basic operations:")
print("  - add(a, b): returns sum")
print("  - subtract(a, b): returns difference")
print("  - multiply(a, b): returns product")
print("  - divide(a, b): returns quotient (handle division by zero)")
print("  - calculator(operation, a, b): uses the above functions")

print("\nExercise 2: Password Strength Checker")
print("Create a function that checks password strength:")
print("  - At least 8 characters")
print("  - Contains uppercase and lowercase letters")
print("  - Contains at least one digit")
print("  - Contains at least one special character")
print("  - Return a score (0-4) and suggestions for improvement")

print("\nExercise 3: Recursive Directory Size")
print("Write a recursive function to calculate total size:")
print("  - Simulate a directory tree with file sizes")
print("  - Each directory can have files and subdirectories")
print("  - Return total size of all files in directory and subdirectories")

print("\nExercise 4: Decorator for Logging")
print("Create a decorator that:")
print("  - Logs function name and arguments before execution")
print("  - Logs return value after execution")
print("  - Logs execution time")
print("  - Can be turned on/off with a parameter")

# ============================================================================
# 12. COMMON GOTCHAS
# ============================================================================
print("\n12. COMMON GOTCHAS")
print("-" * 40)

print("1. Mutable default arguments")
print("   ❌ def add_item(item, items=[]):")
print("          items.append(item)")
print("          return items")
print("   ✅ def add_item(item, items=None):")
print("          if items is None:")
print("              items = []")
print("          items.append(item)")
print("          return items")

print("\n2. Forgetting return statement")
print("   ❌ def process_data(data):")
print("          result = data * 2")
print("   ✅ def process_data(data):")
print("          result = data * 2")
print("          return result")

print("\n3. Modifying global variables without global keyword")
print("   ❌ counter = 0")
print("      def increment():")
print("          counter += 1  # UnboundLocalError")
print("   ✅ counter = 0")
print("      def increment():")
print("          global counter")
print("          counter += 1")

print("\n4. Confusing *args with **kwargs")
print("   ❌ def func(*args, **args):  # Syntax error")
print("   ✅ def func(*args, **kwargs):")

print("\n5. Infinite recursion")
print("   ❌ def recursive_func(n):")
print("          return recursive_func(n)  # No base case!")
print("   ✅ def recursive_func(n):")
print("          if n <= 0: return 0")
print("          return recursive_func(n-1)")

# ============================================================================
# 13. BEST PRACTICES
# ============================================================================
print("\n13. BEST PRACTICES")
print("-" * 40)

print("1. Use descriptive function names")
print("   ❌ def f(x, y):")
print("   ✅ def calculate_distance(x1, y1, x2, y2):")

print("\n2. Keep functions small and focused (Single Responsibility)")
print("   ❌ def process_user_data(user):")
print("          # 100 lines doing validation, saving, emailing...")
print("   ✅ def validate_user(user):")
print("   ✅ def save_user_to_db(user):")
print("   ✅ def send_welcome_email(user):")

print("\n3. Use type hints for clarity")
print("   ❌ def process(data, count):")
print("   ✅ def process(data: list[str], count: int) -> dict:")

print("\n4. Write comprehensive docstrings")
print("   ✅ \"\"\"Process user data and return statistics.")
print("   ")
print("   Parameters:")
print("   -----------")
print("   users : list of dict")
print("       List of user dictionaries")
print("   ")
print("   Returns:")
print("   --------")
print("   dict")
print("       Statistics about users")
print("   \"\"\"")

print("\n5. Use lambda for simple, one-line operations")
print("   ❌ def square(x):")
print("          return x * x")
print("   ✅ square = lambda x: x * x")

# ============================================================================
# 14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE
# ============================================================================
print("\n14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE")
print("-" * 40)

def read_data(filename: str) -> list[str]:
    """Read data from a file."""
    # Simulated data reading
    return ["apple,5", "banana,3", "cherry,8", "date,2"]

def parse_line(line: str) -> tuple[str, int]:
    """Parse a line into (item, quantity)."""
    item, quantity_str = line.split(",")
    return item, int(quantity_str)

def filter_low_quantity(items: list[tuple[str, int]], min_qty: int = 3) -> list[tuple[str, int]]:
    """Filter items with quantity below minimum."""
    return [(item, qty) for item, qty in items if qty >= min_qty]

def calculate_total(items: list[tuple[str, int]]) -> dict[str, int]:
    """Calculate total quantity per item."""
    totals = {}
    for item, qty in items:
        totals[item] = totals.get(item, 0) + qty
    return totals

def format_report(totals: dict[str, int]) -> str:
    """Format totals into a readable report."""
    report_lines = ["INVENTORY REPORT", "=" * 40]
    for item, total in sorted(totals.items()):
        report_lines.append(f"{item:10} : {total:3d}")
    report_lines.append(f"\nTotal items: {len(totals)}")
    return "\n".join(report_lines)

# Decorator for logging pipeline steps
def log_step(step_name: str):
    """Decorator to log pipeline step execution."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[STEP] {step_name}: Starting...")
            result = func(*args, **kwargs)
            print(f"[STEP] {step_name}: Completed")
            return result
        return wrapper
    return decorator

# Apply decorators to pipeline functions
@log_step("Read Data")
def read_data_decorated(filename):
    return read_data(filename)

@log_step("Parse Lines")
def parse_line_decorated(lines):
    return [parse_line(line) for line in lines]

@log_step("Filter Low Quantity")
def filter_low_quantity_decorated(items):
    return filter_low_quantity(items, min_qty=3)

@log_step("Calculate Totals")
def calculate_total_decorated(items):
    return calculate_total(items)

@log_step("Format Report")
def format_report_decorated(totals):
    return format_report(totals)

# Execute the pipeline
print("Executing data processing pipeline:")
print("-" * 40)

lines = read_data_decorated("inventory.csv")
parsed_items = parse_line_decorated(lines)
filtered_items = filter_low_quantity_decorated(parsed_items)
totals = calculate_total_decorated(filtered_items)
report = format_report_decorated(totals)

print("\n" + report)

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Functions encapsulate reusable code with defined inputs/outputs
2. Parameters can be positional, keyword, or variable-length (*args, **kwargs)
3. Functions can return values (including multiple values as tuples)
4. Scope determines variable visibility (local vs global)
5. Lambda functions are anonymous, single-expression functions
6. Decorators modify function behavior without changing source code
7. Recursion solves problems by calling the function itself
8. Docstrings and type hints improve code documentation

Function Design Principles:
- Single Responsibility: Each function should do one thing well
- Pure Functions: Same input → same output, no side effects
- Descriptive Names: Functions should be named by what they do
- Appropriate Parameters: Use default values and type hints
- Clear Return Values: Always return something meaningful

Next Steps:
- Practice with the exercises above
- Move to Tutorial 05: File I/O
- Experiment with building your own function libraries
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 04")
print("=" * 60)