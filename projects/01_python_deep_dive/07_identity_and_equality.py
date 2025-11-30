"""
Tutorial 7: Identity (is) vs Equality (==) and 'in' Operator
Critical for None checks, pd.isna(), and filtering
"""

print("="*60)
print("Identity (is) vs Equality (==)")
print("="*60)

# == checks VALUE equality
# is checks OBJECT IDENTITY (same object in memory)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a == b: {a == b}")  # True - same values
print(f"a is b: {a is b}")  # False - different objects
print(f"a is c: {a is c}")  # True - same object

# ============================================================================
# NONE CHECKS (CRITICAL!)
# ============================================================================

print("\n" + "="*60)
print("None Checks")
print("="*60)

value = None

# ✅ CORRECT: Use 'is' for None
if value is None:
    print("Value is None (correct way)")

# ❌ WRONG: Don't use == for None
if value == None:
    print("Value is None (works but not Pythonic)")

# Why? None is a singleton - only one None object exists
print(f"id(None): {id(None)}")
none1 = None
none2 = None
print(f"none1 is none2: {none1 is none2}")  # Always True

# ============================================================================
# PANDAS PATTERNS
# ============================================================================

print("\n" + "="*60)
print("Pandas Patterns")
print("="*60)

# Check for None/NaN
value = None
if value is None:
    print("Missing value")

# In Pandas, use pd.isna() for NaN/None
# if pd.isna(value):
#     print("Missing value")

# Filter DataFrame
# df[df['column'].isna()]  # Get rows with missing values
# df[df['column'].notna()]  # Get rows without missing values

# ============================================================================
# THE 'in' OPERATOR
# ============================================================================

print("\n" + "="*60)
print("The 'in' Operator")
print("="*60)

# Check membership
fruits = ['apple', 'banana', 'orange']
print(f"'apple' in fruits: {'apple' in fruits}")
print(f"'grape' in fruits: {'grape' in fruits}")

# Check substring
text = "Hello, World!"
print(f"'World' in text: {'World' in text}")

# Check dict keys
person = {'name': 'Alice', 'age': 25}
print(f"'name' in person: {'name' in person}")
print(f"'email' in person: {'email' in person}")

# Pandas: Check if column exists
columns = ['id', 'name', 'price']
if 'price' in columns:
    print("Has price column")

# Filter columns
price_cols = [col for col in columns if 'price' in col]
print(f"Price columns: {price_cols}")

# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("Practical Examples")
print("="*60)

# Example 1: Validate data
def validate_row(row):
    """Check for missing required fields"""
    required = ['id', 'name', 'price']
    missing = [field for field in required if field not in row]
    
    if missing:
        print(f"Missing fields: {missing}")
        return False
    
    if row.get('price') is None:
        print("Price is None")
        return False
    
    return True

row1 = {'id': 1, 'name': 'Apple', 'price': 1.5}
row2 = {'id': 2, 'name': 'Banana'}  # Missing price
row3 = {'id': 3, 'name': 'Orange', 'price': None}

print(f"Row 1 valid: {validate_row(row1)}")
print(f"Row 2 valid: {validate_row(row2)}")
print(f"Row 3 valid: {validate_row(row3)}")

# Example 2: Category membership
def categorize_price(price):
    """Categorize by price range"""
    if price is None:
        return 'unknown'
    elif price < 50:
        return 'cheap'
    elif price in range(50, 200):  # 'in' with range
        return 'moderate'
    else:
        return 'expensive'

prices = [25, 100, 300, None]
for p in prices:
    print(f"Price {p}: {categorize_price(p)}")

# ============================================================================
# COMMON PITFALLS
# ============================================================================

print("\n" + "="*60)
print("Common Pitfalls")
print("="*60)

# Pitfall 1: Using == for None
value = None
# if value == None:  # Works but not Pythonic
if value is None:  # Correct way
    print("Use 'is' for None checks")

# Pitfall 2: Confusing 'in' with dict values
person = {'name': 'Alice', 'age': 25}
print(f"'Alice' in person: {'Alice' in person}")  # False - checks keys!
print(f"'Alice' in person.values(): {'Alice' in person.values()}")  # True

# Pitfall 3: Using 'is' for value comparison
a = 1000
b = 1000
print(f"a == b: {a == b}")  # True
print(f"a is b: {a is b}")  # Might be False! (CPython caches small ints)

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. is vs ==:
   - is: Checks object identity (same object)
   - ==: Checks value equality (same value)

2. None checks:
   ✅ if value is None:
   ❌ if value == None:

3. 'in' operator:
   - Lists: 'apple' in fruits
   - Strings: 'World' in text
   - Dicts: 'key' in dict (checks keys, not values!)
   - Ranges: 5 in range(1, 10)

4. Pandas patterns:
   - if 'price' in df.columns:
   - if pd.isna(value):
   - df[df['col'].isna()]
   - [c for c in df.columns if 'price' in c]

5. When to use each:
   - Use 'is' for: None, True, False
   - Use '==' for: Everything else
   - Use 'in' for: Membership testing

Remember:
- None is a singleton (only one exists)
- Use 'is' for None checks (faster and correct)
- Use 'in' to check column existence
- Use pd.isna() for missing data in Pandas
""")
