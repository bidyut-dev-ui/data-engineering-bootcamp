"""
Tutorial 1: Variables, Data Types, and Basic Operations
Essential foundation for all Python programming
"""

print("=" * 60)
print("TUTORIAL 1: VARIABLES, DATA TYPES, AND BASIC OPERATIONS")
print("=" * 60)

# ============================================================================
# 1. VARIABLES AND ASSIGNMENT
# ============================================================================

print("\n" + "=" * 40)
print("1. Variables and Assignment")
print("=" * 40)

# Variables store values
name = "Alice"
age = 30
height = 5.8
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")
print(f"Is student: {is_student}")

# Variables can be reassigned
age = 31  # Alice had a birthday!
print(f"Updated age: {age}")

# Multiple assignment
x, y, z = 1, 2, 3
print(f"x={x}, y={y}, z={z}")

# ============================================================================
# 2. BASIC DATA TYPES
# ============================================================================

print("\n" + "=" * 40)
print("2. Basic Data Types")
print("=" * 40)

# Integers (whole numbers)
count = 42
temperature = -10
print(f"Integer examples: {count}, {temperature}")
print(f"Type of count: {type(count)}")

# Floats (decimal numbers)
price = 19.99
pi = 3.14159
print(f"Float examples: {price}, {pi}")
print(f"Type of price: {type(price)}")

# Strings (text)
greeting = "Hello, World!"
name = 'Alice'
multiline = """This is a
multi-line string"""
print(f"String examples: {greeting}, {name}")
print(f"Type of greeting: {type(greeting)}")

# Booleans (True/False)
is_raining = False
has_permission = True
print(f"Boolean examples: {is_raining}, {has_permission}")
print(f"Type of is_raining: {type(is_raining)}")

# ============================================================================
# 3. TYPE CONVERSION
# ============================================================================

print("\n" + "=" * 40)
print("3. Type Conversion")
print("=" * 40)

# Convert between types
number_str = "42"
number_int = int(number_str)  # Convert string to integer
print(f"String '42' converted to integer: {number_int}")

float_str = "3.14"
float_num = float(float_str)  # Convert string to float
print(f"String '3.14' converted to float: {float_num}")

int_to_str = str(100)  # Convert integer to string
print(f"Integer 100 converted to string: '{int_to_str}'")

# Boolean conversion
print(f"bool(0): {bool(0)}")      # False
print(f"bool(1): {bool(1)}")      # True
print(f"bool(''): {bool('')}")    # False (empty string)
print(f"bool('hello'): {bool('hello')}")  # True

# ============================================================================
# 4. ARITHMETIC OPERATORS
# ============================================================================

print("\n" + "=" * 40)
print("4. Arithmetic Operators")
print("=" * 40)

a = 10
b = 3

print(f"a = {a}, b = {b}")
print(f"Addition (a + b): {a + b}")
print(f"Subtraction (a - b): {a - b}")
print(f"Multiplication (a * b): {a * b}")
print(f"Division (a / b): {a / b}")
print(f"Floor Division (a // b): {a // b}")  # Rounds down
print(f"Modulus (a % b): {a % b}")  # Remainder
print(f"Exponentiation (a ** b): {a ** b}")  # 10^3

# Compound assignment
c = 5
c += 3  # Same as c = c + 3
print(f"c += 3: {c}")

# ============================================================================
# 5. COMPARISON OPERATORS
# ============================================================================

print("\n" + "=" * 40)
print("5. Comparison Operators")
print("=" * 40)

x = 10
y = 20

print(f"x = {x}, y = {y}")
print(f"Equal (x == y): {x == y}")
print(f"Not equal (x != y): {x != y}")
print(f"Greater than (x > y): {x > y}")
print(f"Less than (x < y): {x < y}")
print(f"Greater than or equal (x >= y): {x >= y}")
print(f"Less than or equal (x <= y): {x <= y}")

# String comparison
name1 = "Alice"
name2 = "Bob"
print(f"'Alice' == 'Bob': {name1 == name2}")
print(f"'Alice' != 'Bob': {name1 != name2}")

# ============================================================================
# 6. STRING OPERATIONS
# ============================================================================

print("\n" + "=" * 40)
print("6. String Operations")
print("=" * 40)

first_name = "John"
last_name = "Doe"

# Concatenation
full_name = first_name + " " + last_name
print(f"Full name: {full_name}")

# Repetition
separator = "-" * 20
print(f"Separator: {separator}")

# String methods
text = "  Hello, Python!  "
print(f"Original: '{text}'")
print(f"Upper case: '{text.upper()}'")
print(f"Lower case: '{text.lower()}'")
print(f"Strip whitespace: '{text.strip()}'")
print(f"Replace 'Python' with 'World': '{text.replace('Python', 'World')}'")
print(f"Starts with 'Hello': {text.strip().startswith('Hello')}")
print(f"Ends with '!': {text.strip().endswith('!')}")

# String formatting (f-strings)
name = "Alice"
score = 95.5
formatted = f"Student: {name}, Score: {score:.1f}%"
print(f"Formatted string: {formatted}")

# ============================================================================
# 7. PRACTICE EXERCISES
# ============================================================================

print("\n" + "=" * 40)
print("7. Practice Exercises")
print("=" * 40)

print("\nTry these exercises (solutions in solutions/01_solution.py):")
print("1. Create variables for a product: name, price, and quantity in stock")
print("2. Calculate the total value (price * quantity)")
print("3. Convert the price to a string with a dollar sign")
print("4. Check if the quantity is greater than 0")
print("5. Create a formatted string describing the product")

# Example solution structure
print("\nExample structure:")
product_name = "Laptop"
product_price = 999.99
product_quantity = 5

total_value = product_price * product_quantity
price_str = f"${product_price:.2f}"
has_stock = product_quantity > 0
description = f"{product_name}: {price_str} each, {product_quantity} in stock, total value: ${total_value:.2f}"

print(f"\nProduct: {product_name}")
print(f"Price: {price_str}")
print(f"Quantity: {product_quantity}")
print(f"Total value: ${total_value:.2f}")
print(f"Has stock: {has_stock}")
print(f"Description: {description}")

print("\n" + "=" * 60)
print("END OF TUTORIAL 1")
print("=" * 60)
print("\nNext: Run 'python 02_control_flow.py' to learn about if/else and loops!")