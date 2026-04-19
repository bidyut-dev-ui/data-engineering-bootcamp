"""
Tutorial 03: Data Structures in Python
=======================================

Data structures are containers that organize and group data.
This tutorial covers Python's built-in data structures:
1. Lists - Ordered, mutable sequences
2. Tuples - Ordered, immutable sequences  
3. Dictionaries - Key-value mappings
4. Sets - Unordered collections of unique elements

Learning Objectives:
- Create and manipulate lists, tuples, dictionaries, and sets
- Understand when to use each data structure
- Perform common operations (adding, removing, searching)
- Use list comprehensions for concise transformations
- Work with nested data structures

Prerequisites:
- Tutorial 01: Variables and Types
- Tutorial 02: Control Flow
"""

print("=" * 60)
print("TUTORIAL 03: DATA STRUCTURES")
print("=" * 60)

# ============================================================================
# 1. LISTS
# ============================================================================
print("\n1. LISTS (Ordered, Mutable Sequences)")
print("-" * 40)

# Creating lists
fruits = ["apple", "banana", "cherry", "date"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty_list = []

print(f"fruits: {fruits}")
print(f"numbers: {numbers}")
print(f"mixed: {mixed}")
print(f"empty_list: {empty_list}")

# Accessing elements (zero-indexed)
print(f"\nFirst fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")
print(f"Second fruit: {fruits[1]}")
print(f"Slice fruits[1:3]: {fruits[1:3]}")  # From index 1 to 2 (3 exclusive)

# Modifying lists (lists are mutable)
fruits[1] = "blueberry"
print(f"\nAfter fruits[1] = 'blueberry': {fruits}")

# List methods
fruits.append("elderberry")  # Add to end
print(f"After append('elderberry'): {fruits}")

fruits.insert(2, "cantaloupe")  # Insert at index 2
print(f"After insert(2, 'cantaloupe'): {fruits}")

removed_fruit = fruits.pop()  # Remove and return last item
print(f"After pop(): {fruits} (removed: {removed_fruit})")

fruits.remove("blueberry")  # Remove first occurrence
print(f"After remove('blueberry'): {fruits}")

# List operations
more_fruits = ["fig", "grape"]
combined = fruits + more_fruits  # Concatenation
print(f"\nfruits + more_fruits: {combined}")

repeated = numbers * 2  # Repetition
print(f"numbers * 2: {repeated}")

# List length and membership
print(f"\nLength of fruits: {len(fruits)}")
print(f"'cherry' in fruits: {'cherry' in fruits}")
print(f"'watermelon' in fruits: {'watermelon' in fruits}")

# Sorting
numbers_to_sort = [5, 2, 8, 1, 9]
numbers_to_sort.sort()  # In-place sort
print(f"\nSorted numbers (ascending): {numbers_to_sort}")

numbers_to_sort.sort(reverse=True)  # Descending sort
print(f"Sorted numbers (descending): {numbers_to_sort}")

# ============================================================================
# 2. LIST COMPREHENSIONS
# ============================================================================
print("\n2. LIST COMPREHENSIONS (Concise List Creation)")
print("-" * 40)

# Basic comprehension: [expression for item in iterable]
squares = [x**2 for x in range(1, 6)]
print(f"Squares of 1-5: {squares}")

# With condition: [expression for item in iterable if condition]
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Even squares (2,4,6,8,10): {even_squares}")

# Transform strings
fruits_upper = [fruit.upper() for fruit in fruits]
print(f"Fruits in uppercase: {fruits_upper}")

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")

# ============================================================================
# 3. TUPLES
# ============================================================================
print("\n3. TUPLES (Ordered, Immutable Sequences)")
print("-" * 40)

# Creating tuples
coordinates = (10, 20)
rgb_color = (255, 128, 0)
single_element = (42,)  # Note the comma!
empty_tuple = ()

print(f"coordinates: {coordinates}")
print(f"rgb_color: {rgb_color}")
print(f"single_element: {single_element}")
print(f"empty_tuple: {empty_tuple}")

# Accessing tuple elements (same as lists)
print(f"\nFirst coordinate: {coordinates[0]}")
print(f"Last color component: {rgb_color[-1]}")

# Tuples are immutable (cannot be changed)
# coordinates[0] = 15  # This would raise TypeError!

# Tuple unpacking
x, y = coordinates
print(f"\nTuple unpacking: x={x}, y={y}")

# Multiple assignment using tuples
a, b, c = 1, 2, 3
print(f"Multiple assignment: a={a}, b={b}, c={c}")

# Swapping variables using tuples
x, y = 5, 10
print(f"\nBefore swap: x={x}, y={y}")
x, y = y, x  # Tuple packing/unpacking
print(f"After swap: x={x}, y={y}")

# Returning multiple values from functions (preview)
def get_min_max(numbers):
    return min(numbers), max(numbers)

result = get_min_max([3, 1, 4, 1, 5, 9, 2])
print(f"\nMin and max of [3,1,4,1,5,9,2]: {result}")

# ============================================================================
# 4. DICTIONARIES
# ============================================================================
print("\n4. DICTIONARIES (Key-Value Mappings)")
print("-" * 40)

# Creating dictionaries
student = {
    "name": "Alice",
    "age": 21,
    "major": "Computer Science",
    "gpa": 3.8
}

empty_dict = {}
grades = {"Math": "A", "Science": "B+", "History": "A-"}

print(f"student: {student}")
print(f"grades: {grades}")

# Accessing values
print(f"\nStudent name: {student['name']}")
print(f"Student age: {student['age']}")

# Using get() method (safer, returns None if key doesn't exist)
print(f"Student major: {student.get('major')}")
print(f"Student minor: {student.get('minor')}")  # Returns None
print(f"Student minor (default): {student.get('minor', 'Not declared')}")

# Adding/updating entries
student["year"] = "Senior"  # Add new key
print(f"\nAfter adding 'year': {student}")

student["gpa"] = 3.9  # Update existing key
print(f"After updating GPA: {student}")

# Removing entries
removed_value = student.pop("year")  # Remove and return value
print(f"\nAfter pop('year'): {student} (removed: {removed_value})")

# Dictionary methods
print(f"\nAll keys: {list(student.keys())}")
print(f"All values: {list(student.values())}")
print(f"All items (key-value pairs): {list(student.items())}")

# Dictionary comprehension
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"\nSquares dictionary: {squares_dict}")

# Nested dictionaries
company = {
    "name": "TechCorp",
    "employees": {
        "engineering": 50,
        "sales": 20,
        "hr": 5
    },
    "locations": ["New York", "San Francisco", "London"]
}

print(f"\nNested dictionary - company: {company}")
print(f"Engineering employees: {company['employees']['engineering']}")
print(f"First location: {company['locations'][0]}")

# ============================================================================
# 5. SETS
# ============================================================================
print("\n5. SETS (Unordered Collections of Unique Elements)")
print("-" * 40)

# Creating sets
fruits_set = {"apple", "banana", "cherry", "apple"}  # Duplicates removed
numbers_set = set([1, 2, 3, 4, 5, 5, 5])  # From list
empty_set = set()  # Note: {} creates empty dict, not empty set!

print(f"fruits_set: {fruits_set}")  # Note: order may vary
print(f"numbers_set: {numbers_set}")
print(f"empty_set: {empty_set}")

# Set operations
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"\nset_a: {set_a}")
print(f"set_b: {set_b}")

print(f"Union (a | b): {set_a | set_b}")  # All elements in either set
print(f"Intersection (a & b): {set_a & set_b}")  # Elements in both sets
print(f"Difference (a - b): {set_a - set_b}")  # Elements in a but not b
print(f"Symmetric Difference (a ^ b): {set_a ^ set_b}")  # Elements in either but not both

# Set methods
set_a.add(6)
print(f"\nAfter add(6): {set_a}")

set_a.remove(6)  # Raises KeyError if element doesn't exist
print(f"After remove(6): {set_a}")

set_a.discard(10)  # Doesn't raise error if element doesn't exist
print(f"After discard(10): {set_a}")

# Set comprehension
even_squares_set = {x**2 for x in range(1, 11) if x % 2 == 0}
print(f"\nEven squares as set: {even_squares_set}")

# ============================================================================
# 6. CHOOSING THE RIGHT DATA STRUCTURE
# ============================================================================
print("\n6. CHOOSING THE RIGHT DATA STRUCTURE")
print("-" * 40)

print("Use LISTS when:")
print("  - You need ordered collection")
print("  - You need to modify elements (add, remove, change)")
print("  - You need to access elements by position (index)")
print("  - Example: Shopping cart items, to-do list")

print("\nUse TUPLES when:")
print("  - You need ordered collection that shouldn't change")
print("  - You're returning multiple values from a function")
print("  - You need dictionary keys (tuples are hashable)")
print("  - Example: Coordinates (x, y), RGB colors")

print("\nUse DICTIONARIES when:")
print("  - You need to map keys to values")
print("  - You need fast lookups by key")
print("  - You need to store structured data")
print("  - Example: User profiles, configuration settings")

print("\nUse SETS when:")
print("  - You need to store unique elements")
print("  - You need to perform set operations (union, intersection)")
print("  - Order doesn't matter")
print("  - Example: Tags, unique visitors, stop words")

# ============================================================================
# 7. PRACTICE EXERCISES
# ============================================================================
print("\n7. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: List Manipulation")
print("Create a list of numbers 1-10, then:")
print("  - Remove all even numbers")
print("  - Double each remaining number")
print("  - Sort in descending order")
print("  - Find the sum of all elements")

print("\nExercise 2: Word Frequency Counter")
print("Given a string, create a dictionary that counts:")
print("  - Frequency of each word")
print("  - Frequency of each character (ignoring spaces)")
print("  - Top 3 most common words")

print("\nExercise 3: Student Gradebook")
print("Create a nested dictionary for students:")
print("  - Each student has name, grades (list), and attendance")
print("  - Calculate average grade for each student")
print("  - Find students with attendance > 90%")
print("  - Sort students by average grade")

print("\nExercise 4: Set Operations for Data Analysis")
print("Given two sets of customer IDs:")
print("  - Set A: Customers who bought product X")
print("  - Set B: Customers who bought product Y")
print("  - Find: Customers who bought both products")
print("  - Find: Customers who bought only product X")
print("  - Find: Total unique customers")

# ============================================================================
# 8. COMMON GOTCHAS
# ============================================================================
print("\n8. COMMON GOTCHAS")
print("-" * 40)

print("1. Modifying list while iterating")
print("   ❌ for item in my_list:")
print("          if condition:")
print("              my_list.remove(item)")
print("   ✅ Create a copy: for item in my_list.copy():")

print("\n2. Confusing [] and {}")
print("   ❌ my_dict = []  # This is a list!")
print("   ✅ my_dict = {}  # This is a dictionary")

print("\n3. Forgetting that sets are unordered")
print("   ❌ Assuming set elements maintain insertion order")
print("   ✅ Use lists if order matters")

print("\n4. Using mutable objects as dictionary keys")
print("   ❌ my_dict = {[1,2]: 'value'}  # List is mutable!")
print("   ✅ my_dict = {(1,2): 'value'}  # Tuple is immutable")

print("\n5. Shallow vs deep copy")
print("   ❌ list2 = list1  # Both reference same list")
print("   ✅ list2 = list1.copy()  # Creates shallow copy")
print("   ✅ import copy; list2 = copy.deepcopy(list1)")

# ============================================================================
# 9. BEST PRACTICES
# ============================================================================
print("\n9. BEST PRACTICES")
print("-" * 40)

print("1. Use list comprehensions for simple transformations")
print("   ❌ result = []")
print("      for x in range(10):")
print("          result.append(x**2)")
print("   ✅ result = [x**2 for x in range(10)]")

print("\n2. Use dictionary.get() for safe access")
print("   ❌ value = my_dict[key]  # Raises KeyError if missing")
print("   ✅ value = my_dict.get(key, default_value)")

print("\n3. Use tuples for heterogeneous data")
print("   ❌ point = [x, y]  # List implies homogeneous")
print("   ✅ point = (x, y)  # Tuple implies fixed structure")

print("\n4. Use sets for membership testing")
print("   ❌ if item in my_list:  # O(n) for lists")
print("   ✅ if item in my_set:   # O(1) for sets")

print("\n5. Use collections module for advanced needs")
print("   ✅ from collections import defaultdict, Counter")
print("   ✅ word_counts = Counter(text.split())")

# ============================================================================
# 10. REAL-WORLD EXAMPLE
# ============================================================================
print("\n10. REAL-WORLD EXAMPLE: E-commerce Cart")
print("-" * 40)

# Simulating an e-commerce shopping cart
cart = {
    "user_id": 12345,
    "items": [
        {"product_id": 101, "name": "Laptop", "price": 999.99, "quantity": 1},
        {"product_id": 202, "name": "Mouse", "price": 29.99, "quantity": 2},
        {"product_id": 303, "name": "Keyboard", "price": 79.99, "quantity": 1}
    ],
    "discount_codes": {"SAVE10", "FREESHIP"},
    "shipping_address": ("123 Main St", "New York", "NY", "10001")
}

print("Shopping Cart Structure:")
print(f"User ID: {cart['user_id']}")
print(f"Number of items: {len(cart['items'])}")

# Calculate total
total = sum(item["price"] * item["quantity"] for item in cart["items"])
print(f"Subtotal: ${total:.2f}")

# Apply discount if any code is valid
valid_codes = {"SAVE10", "BLACKFRIDAY"}
applied_discount = any(code in valid_codes for code in cart["discount_codes"])
if applied_discount:
    total *= 0.9  # 10% discount
    print(f"Discount applied! Total: ${total:.2f}")

# Shipping address
address = cart["shipping_address"]
print(f"Shipping to: {address[0]}, {address[1]}, {address[2]} {address[3]}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Lists: Ordered, mutable sequences - use for collections that change
2. Tuples: Ordered, immutable sequences - use for fixed data
3. Dictionaries: Key-value mappings - use for structured data with labels
4. Sets: Unordered unique collections - use for membership testing
5. List comprehensions: Concise way to create/transform lists
6. Each structure has specific use cases - choose based on needs

Memory & Performance:
- Lists: O(1) access by index, O(n) search
- Dictionaries: O(1) access by key (average case)
- Sets: O(1) membership testing
- Tuples: More memory efficient than lists

Next Steps:
- Practice with the exercises above
- Move to Tutorial 04: Functions
- Try building a small program using multiple data structures
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 03")
print("=" * 60)