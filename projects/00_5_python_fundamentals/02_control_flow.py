"""
Tutorial 02: Control Flow in Python
====================================

Control flow determines the order in which statements are executed in a program.
This tutorial covers:
1. Conditional statements (if, elif, else)
2. Loops (for, while)
3. Loop control (break, continue, pass)
4. Logical operators (and, or, not)
5. Comparison operators
6. Ternary conditional expressions

Learning Objectives:
- Write conditional logic to make decisions
- Use loops to repeat operations
- Control loop execution with break/continue
- Combine conditions with logical operators
- Write clean, readable control flow

Prerequisites:
- Tutorial 01: Variables and Types
- Basic understanding of Python syntax
"""

print("=" * 60)
print("TUTORIAL 02: CONTROL FLOW")
print("=" * 60)

# ============================================================================
# 1. COMPARISON OPERATORS
# ============================================================================
print("\n1. COMPARISON OPERATORS")
print("-" * 40)

# Comparison operators return True or False
a = 10
b = 20

print(f"a = {a}, b = {b}")
print(f"a == b: {a == b}")      # Equal to
print(f"a != b: {a != b}")      # Not equal to
print(f"a < b: {a < b}")        # Less than
print(f"a > b: {a > b}")        # Greater than
print(f"a <= b: {a <= b}")      # Less than or equal to
print(f"a >= b: {a >= b}")      # Greater than or equal to

# Strings can also be compared (lexicographically)
name1 = "Alice"
name2 = "Bob"
print(f"\nname1 = '{name1}', name2 = '{name2}'")
print(f"name1 == name2: {name1 == name2}")
print(f"name1 < name2: {name1 < name2}")  # 'A' comes before 'B'

# ============================================================================
# 2. LOGICAL OPERATORS
# ============================================================================
print("\n2. LOGICAL OPERATORS (and, or, not)")
print("-" * 40)

# Logical operators combine boolean expressions
age = 25
has_license = True
is_student = False

print(f"age = {age}, has_license = {has_license}, is_student = {is_student}")

# AND: True only if both conditions are True
can_drive = age >= 18 and has_license
print(f"age >= 18 AND has_license: {can_drive}")

# OR: True if at least one condition is True
gets_discount = age < 18 or is_student
print(f"age < 18 OR is_student: {gets_discount}")

# NOT: Inverts the boolean value
cannot_drive = not can_drive
print(f"NOT can_drive: {cannot_drive}")

# Complex logical expressions
is_eligible = (age >= 18 and has_license) or (age >= 16 and is_student)
print(f"(age >= 18 AND has_license) OR (age >= 16 AND is_student): {is_eligible}")

# ============================================================================
# 3. CONDITIONAL STATEMENTS (if, elif, else)
# ============================================================================
print("\n3. CONDITIONAL STATEMENTS (if, elif, else)")
print("-" * 40)

# Basic if statement
temperature = 28
print(f"Temperature: {temperature}°C")

if temperature > 30:
    print("It's hot outside!")
elif temperature > 20:
    print("It's warm outside.")
elif temperature > 10:
    print("It's cool outside.")
else:
    print("It's cold outside!")

# Nested if statements
score = 85
attendance = 0.95  # 95%

print(f"\nScore: {score}, Attendance: {attendance*100}%")

if score >= 80:
    if attendance >= 0.9:
        print("Grade: A (Excellent performance with good attendance)")
    else:
        print("Grade: B (Good performance but attendance needs improvement)")
elif score >= 60:
    print("Grade: C (Passing grade)")
else:
    print("Grade: F (Needs improvement)")

# ============================================================================
# 4. TERNARY CONDITIONAL EXPRESSIONS
# ============================================================================
print("\n4. TERNARY CONDITIONAL EXPRESSIONS")
print("-" * 40)

# Ternary syntax: value_if_true if condition else value_if_false
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Age {age}: {status}")

# Multiple conditions in ternary (not recommended for complex logic)
score = 75
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
print(f"Score {score}: Grade {grade}")

# ============================================================================
# 5. FOR LOOPS
# ============================================================================
print("\n5. FOR LOOPS")
print("-" * 40)

# Loop through a list
fruits = ["apple", "banana", "cherry", "date"]
print("Fruits in the basket:")
for fruit in fruits:
    print(f"  - {fruit}")

# Loop with index using enumerate()
print("\nFruits with their positions:")
for index, fruit in enumerate(fruits):
    print(f"  {index + 1}. {fruit}")

# Loop through a string
word = "Python"
print(f"\nLetters in '{word}':")
for letter in word:
    print(f"  {letter}")

# Loop through a range of numbers
print("\nCounting from 1 to 5:")
for i in range(1, 6):  # range(start, stop) - stop is exclusive
    print(f"  {i}")

print("\nEven numbers from 2 to 10:")
for i in range(2, 11, 2):  # range(start, stop, step)
    print(f"  {i}")

# ============================================================================
# 6. WHILE LOOPS
# ============================================================================
print("\n6. WHILE LOOPS")
print("-" * 40)

# Basic while loop
count = 1
print("Counting up to 5:")
while count <= 5:
    print(f"  Count: {count}")
    count += 1  # Don't forget to increment!

# While loop with user input simulation
print("\nSimulating login attempts:")
max_attempts = 3
attempts = 0
password = "secret123"
logged_in = False

while attempts < max_attempts and not logged_in:
    attempts += 1
    # Simulating incorrect password for first two attempts
    if attempts < 3:
        print(f"  Attempt {attempts}: Incorrect password")
    else:
        print(f"  Attempt {attempts}: Correct password!")
        logged_in = True

if logged_in:
    print("  Login successful!")
else:
    print("  Too many failed attempts. Account locked.")

# ============================================================================
# 7. LOOP CONTROL: break, continue, pass
# ============================================================================
print("\n7. LOOP CONTROL (break, continue, pass)")
print("-" * 40)

# break: Exit the loop immediately
print("Finding the first number divisible by 7:")
for num in range(1, 21):
    if num % 7 == 0:
        print(f"  Found: {num}")
        break  # Exit the loop
    print(f"  Checking {num}...")

# continue: Skip to the next iteration
print("\nPrinting odd numbers from 1 to 10:")
for num in range(1, 11):
    if num % 2 == 0:  # Skip even numbers
        continue
    print(f"  {num}")

# pass: Do nothing (placeholder)
print("\nChecking numbers (pass example):")
for num in range(1, 6):
    if num == 3:
        pass  # We'll implement this later
    else:
        print(f"  Processing {num}")

# ============================================================================
# 8. PRACTICE EXERCISES
# ============================================================================
print("\n8. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: FizzBuzz")
print("Write a program that prints numbers from 1 to 20:")
print("  - For multiples of 3, print 'Fizz'")
print("  - For multiples of 5, print 'Buzz'")
print("  - For multiples of both 3 and 5, print 'FizzBuzz'")
print("  - Otherwise, print the number")

print("\nExercise 2: Password Validator")
print("Write a program that validates passwords:")
print("  - At least 8 characters long")
print("  - Contains at least one uppercase letter")
print("  - Contains at least one digit")
print("  - Contains at least one special character (!@#$%^&*)")

print("\nExercise 3: Number Guessing Game")
print("Create a number guessing game:")
print("  - Computer picks a random number between 1-100")
print("  - User has 7 attempts to guess")
print("  - After each guess, tell if it's too high or too low")
print("  - If guessed correctly, congratulate the user")

print("\nExercise 4: Multiplication Table")
print("Generate a multiplication table:")
print("  - Ask user for a number (n)")
print("  - Print multiplication table from 1 to 10 for n")
print("  - Format it nicely with proper alignment")

# ============================================================================
# 9. COMMON GOTCHAS
# ============================================================================
print("\n9. COMMON GOTCHAS")
print("-" * 40)

print("1. Forgetting colon (:) after if/for/while")
print("   ❌ if x > 5")
print("   ✅ if x > 5:")

print("\n2. Using = instead of == in conditions")
print("   ❌ if x = 5:  # This is assignment!")
print("   ✅ if x == 5: # This is comparison")

print("\n3. Infinite while loops (forgetting to update condition)")
print("   ❌ while x > 0:  # x never changes")
print("   ✅ while x > 0:")
print("        x -= 1  # Update the condition")

print("\n4. Off-by-one errors with range()")
print("   ❌ range(5) gives 0,1,2,3,4 (not 5)")
print("   ✅ Use range(1, 6) for 1,2,3,4,5")

print("\n5. Modifying list while iterating")
print("   ❌ for item in my_list:")
print("          my_list.remove(item)")
print("   ✅ Create a copy: for item in my_list.copy():")

# ============================================================================
# 10. BEST PRACTICES
# ============================================================================
print("\n10. BEST PRACTICES")
print("-" * 40)

print("1. Keep conditions simple and readable")
print("   ❌ if not (x < 5 or y > 10) and z == 0:")
print("   ✅ is_valid = (x >= 5 and y <= 10) or z != 0")
print("   ✅ if is_valid:")

print("\n2. Use meaningful variable names in conditions")
print("   ❌ if a > 18 and b:")
print("   ✅ if age >= 18 and has_license:")

print("\n3. Avoid deep nesting (use early returns)")
print("   ❌ if condition1:")
print("        if condition2:")
print("            if condition3:")
print("                # Do something")
print("   ✅ if not condition1: return")
print("   ✅ if not condition2: return")
print("   ✅ # Do something")

print("\n4. Use for loops over while when possible")
print("   ❌ i = 0")
print("      while i < len(items):")
print("          print(items[i])")
print("          i += 1")
print("   ✅ for item in items:")
print("          print(item)")

print("\n5. Comment complex logic")
print("   ✅ # Check if user is eligible for discount")
print("   ✅ # (Students OR seniors) AND first_time_customer")
print("   ✅ if (is_student or is_senior) and first_time:")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Comparison operators (==, !=, <, >, <=, >=) return True/False
2. Logical operators (and, or, not) combine boolean expressions
3. if/elif/else statements control program flow based on conditions
4. for loops iterate over sequences (lists, strings, ranges)
5. while loops repeat while a condition is True
6. Use break to exit loops, continue to skip iterations
7. Ternary expressions: x if condition else y
8. Avoid common pitfalls: infinite loops, off-by-one errors

Next Steps:
- Practice with the exercises above
- Move to Tutorial 03: Data Structures
- Try building small programs using control flow
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 02")
print("=" * 60)