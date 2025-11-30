"""
Tutorial 5: Lambda Functions and Callables
Essential for df.apply(), df.assign(), map(), filter()
"""

# ============================================================================
# 1. WHAT IS A LAMBDA?
# ============================================================================

print("="*60)
print("1. What is a Lambda?")
print("="*60)

# Regular function
def square(x):
    return x ** 2

# Lambda (anonymous function)
square_lambda = lambda x: x ** 2

# They do the same thing
print(f"Regular function: {square(5)}")
print(f"Lambda function: {square_lambda(5)}")

# Lambda syntax: lambda arguments: expression
add = lambda a, b: a + b
print(f"Lambda add: {add(3, 4)}")

# ============================================================================
# 2. WHEN TO USE LAMBDA
# ============================================================================

print("\n" + "="*60)
print("2. When to Use Lambda")
print("="*60)

# Use lambda for: Simple, one-line operations
# Use def for: Complex logic, multiple lines

# Good use of lambda
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(f"Squared: {squared}")

# Bad use of lambda (too complex)
# Don't do this:
# complex_lambda = lambda x: x**2 if x > 0 else -x**2 if x < 0 else 0

# Do this instead:
def complex_function(x):
    if x > 0:
        return x ** 2
    elif x < 0:
        return -x ** 2
    else:
        return 0

# ============================================================================
# 3. MAP, FILTER, REDUCE
# ============================================================================

print("\n" + "="*60)
print("3. Map, Filter, Reduce")
print("="*60)

# map(): Apply function to each element
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Doubled: {doubled}")

# filter(): Keep elements where function returns True
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# reduce(): Combine elements (need to import)
from functools import reduce
total = reduce(lambda a, b: a + b, numbers)
print(f"Sum: {total}")

# ============================================================================
# 4. PANDAS-LIKE PATTERNS
# ============================================================================

print("\n" + "="*60)
print("4. Pandas-Like Patterns")
print("="*60)

# Simulate DataFrame data
data = {
    'price': [100, 200, 150, 300],
    'quantity': [2, 1, 3, 2],
    'rev2024': [1000, 2000, 1500, 3000],
    'rev2025': [1200, 2400, 1800, 3600]
}

# Pattern 1: Apply lambda to calculate new column
# df.assign(total=lambda d: d.price * d.quantity)
totals = [data['price'][i] * data['quantity'][i] for i in range(len(data['price']))]
print(f"Totals: {totals}")

# Pattern 2: Calculate growth rate
# df.assign(growth=lambda d: d.rev2025 / d.rev2024 - 1)
growth = [(data['rev2025'][i] / data['rev2024'][i] - 1) for i in range(len(data['rev2024']))]
print(f"Growth rates: {[f'{g:.1%}' for g in growth]}")

# Pattern 3: Filter with lambda
# df[df['price'].apply(lambda x: x > 150)]
high_prices = [p for p in data['price'] if p > 150]
print(f"High prices: {high_prices}")

# ============================================================================
# 5. LAMBDA WITH MULTIPLE ARGUMENTS
# ============================================================================

print("\n" + "="*60)
print("5. Lambda with Multiple Arguments")
print("="*60)

# Two arguments
multiply = lambda x, y: x * y
print(f"Multiply: {multiply(5, 3)}")

# Three arguments
calculate = lambda x, y, z: (x + y) * z
print(f"Calculate: {calculate(2, 3, 4)}")

# With default arguments
greet = lambda name, greeting="Hello": f"{greeting}, {name}!"
print(greet("Alice"))
print(greet("Bob", "Hi"))

# ============================================================================
# 6. LAMBDA IN SORTING
# ============================================================================

print("\n" + "="*60)
print("6. Lambda in Sorting")
print("="*60)

# Sort by custom key
people = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35}
]

# Sort by age
sorted_by_age = sorted(people, key=lambda x: x['age'])
print("Sorted by age:")
for person in sorted_by_age:
    print(f"  {person['name']}: {person['age']}")

# Sort by name length
sorted_by_name_len = sorted(people, key=lambda x: len(x['name']))
print("\nSorted by name length:")
for person in sorted_by_name_len:
    print(f"  {person['name']}: {len(person['name'])} chars")

# ============================================================================
# 7. LAMBDA WITH PANDAS METHODS
# ============================================================================

print("\n" + "="*60)
print("7. Lambda with Pandas Methods")
print("="*60)

# Simulating common Pandas operations

# apply(): Apply function to each element
prices = [100, 200, 150, 300]
with_tax = list(map(lambda x: x * 1.1, prices))
print(f"Prices with tax: {with_tax}")

# applymap(): Apply to entire DataFrame (element-wise)
# In real Pandas: df.applymap(lambda x: x * 2)
matrix = [[1, 2], [3, 4]]
doubled_matrix = [[x * 2 for x in row] for row in matrix]
print(f"Doubled matrix: {doubled_matrix}")

# assign(): Create new column
# df.assign(log_price=lambda d: np.log(d.price))
import math
log_prices = [math.log(p) for p in prices]
print(f"Log prices: {[f'{lp:.2f}' for lp in log_prices]}")

# ============================================================================
# 8. CALLABLES (Any Object You Can Call)
# ============================================================================

print("\n" + "="*60)
print("8. Callables")
print("="*60)

# Functions are callable
def my_function():
    return "I'm a function"

# Lambdas are callable
my_lambda = lambda: "I'm a lambda"

# Classes can be callable
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        return x * self.factor

# All are callable
print(f"Function: {my_function()}")
print(f"Lambda: {my_lambda()}")

multiply_by_3 = Multiplier(3)
print(f"Callable class: {multiply_by_3(5)}")

# Check if callable
print(f"\nIs function callable? {callable(my_function)}")
print(f"Is lambda callable? {callable(my_lambda)}")
print(f"Is class instance callable? {callable(multiply_by_3)}")

# ============================================================================
# 9. PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("9. Practical Examples")
print("="*60)

# Example 1: Data transformation pipeline
data = [1, 2, 3, 4, 5]

# Chain operations
result = list(
    map(lambda x: x ** 2,           # Square
    filter(lambda x: x % 2 == 0,    # Keep evens
    data))
)
print(f"Evens squared: {result}")

# Example 2: Column name transformation
columns = ['user_id', 'user_name', 'user_age']
cleaned = list(map(lambda x: x.replace('user_', ''), columns))
print(f"Cleaned columns: {cleaned}")

# Example 3: Conditional transformation
prices = [50, 150, 200, 80]
discounted = list(map(
    lambda x: x * 0.9 if x > 100 else x,
    prices
))
print(f"Discounted prices: {discounted}")

# ============================================================================
# 10. LAMBDA VS COMPREHENSION
# ============================================================================

print("\n" + "="*60)
print("10. Lambda vs Comprehension")
print("="*60)

numbers = [1, 2, 3, 4, 5]

# Using lambda + map
squared_lambda = list(map(lambda x: x**2, numbers))

# Using comprehension (more Pythonic!)
squared_comp = [x**2 for x in numbers]

print(f"Lambda + map: {squared_lambda}")
print(f"Comprehension: {squared_comp}")
print("Both give same result, but comprehension is more readable!")

# When to use each:
# - Comprehension: When you control the code (more readable)
# - Lambda: When passing to functions (df.apply, sorted, etc.)

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. Lambda syntax: lambda args: expression
   square = lambda x: x**2

2. Use lambda for simple, one-line operations
   Use def for complex logic

3. Common with map, filter, sorted:
   map(lambda x: x*2, numbers)
   filter(lambda x: x > 0, numbers)
   sorted(people, key=lambda x: x['age'])

4. Pandas patterns:
   df.assign(total=lambda d: d.price * d.qty)
   df['price'].apply(lambda x: x * 1.1)
   df[df['price'].apply(lambda x: x > 100)]

5. Callables: Anything you can call with ()
   - Functions
   - Lambdas
   - Classes with __call__

6. Lambda vs comprehension:
   - Lambda: When passing to functions
   - Comprehension: When you control the code

In Pandas, lambda is EVERYWHERE:
- df.apply(lambda x: ...)
- df.assign(col=lambda d: ...)
- df.sort_values(key=lambda x: ...)
- df.groupby(...).apply(lambda g: ...)
""")
