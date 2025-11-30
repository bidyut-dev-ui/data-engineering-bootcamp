"""
Tutorial 6: Copy vs View and Mutation
Critical for avoiding SettingWithCopyWarning in Pandas
"""

# ============================================================================
# 1. MUTABLE VS IMMUTABLE OBJECTS
# ============================================================================

print("="*60)
print("1. Mutable vs Immutable Objects")
print("="*60)

# Immutable: Cannot be changed after creation
# int, float, str, tuple, frozenset
x = 5
y = x
x = 10
print(f"x={x}, y={y}")  # y is still 5

# Mutable: Can be changed after creation
# list, dict, set
list1 = [1, 2, 3]
list2 = list1  # Reference, not copy!
list1.append(4)
print(f"list1={list1}, list2={list2}")  # Both changed!

# ============================================================================
# 2. REFERENCE VS COPY
# ============================================================================

print("\n" + "="*60)
print("2. Reference vs Copy")
print("="*60)

# Reference (same object)
original = [1, 2, 3]
reference = original
reference.append(4)
print(f"Original: {original}")  # [1, 2, 3, 4]
print(f"Reference: {reference}")  # [1, 2, 3, 4]
print(f"Same object? {original is reference}")  # True

# Shallow copy (new object, same contents)
original = [1, 2, 3]
shallow = original.copy()  # or list(original) or original[:]
shallow.append(4)
print(f"\nOriginal: {original}")  # [1, 2, 3]
print(f"Shallow copy: {shallow}")  # [1, 2, 3, 4]
print(f"Same object? {original is shallow}")  # False

# ============================================================================
# 3. SHALLOW VS DEEP COPY
# ============================================================================

print("\n" + "="*60)
print("3. Shallow vs Deep Copy")
print("="*60)

# Shallow copy: Copies outer container, but not nested objects
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
shallow[0].append(999)  # Modifies nested list
print(f"Original: {nested}")  # [[1, 2, 999], [3, 4]]
print(f"Shallow: {shallow}")  # [[1, 2, 999], [3, 4]]

# Deep copy: Copies everything recursively
import copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
deep[0].append(999)
print(f"\nOriginal: {nested}")  # [[1, 2], [3, 4]]
print(f"Deep: {deep}")  # [[1, 2, 999], [3, 4]]

# ============================================================================
# 4. VIEWS IN NUMPY/PANDAS
# ============================================================================

print("\n" + "="*60)
print("4. Views (NumPy/Pandas Concept)")
print("="*60)

# View: Different way to look at same data (no copy)
# Modifying view modifies original

# Simulating with list slicing
original = [1, 2, 3, 4, 5]

# List slicing creates a COPY (not a view)
slice_copy = original[1:4]
slice_copy[0] = 999
print(f"Original: {original}")  # [1, 2, 3, 4, 5] - unchanged
print(f"Slice: {slice_copy}")  # [999, 3, 4]

# NumPy arrays can create views
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]  # This is a VIEW, not a copy
view[0] = 999
print(f"\nNumPy original: {arr}")  # [1, 999, 3, 4, 5] - changed!
print(f"NumPy view: {view}")  # [999, 3, 4]

# ============================================================================
# 5. THE SETTINGWITHCOPYWARNING PROBLEM
# ============================================================================

print("\n" + "="*60)
print("5. The SettingWithCopyWarning Problem")
print("="*60)

# This is why Pandas shows SettingWithCopyWarning
# Simulating the problem:

# Bad: Chained assignment
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
# df[df['A'] > 1]['B'] = 999  # Is this modifying a view or a copy?

# The problem: You don't know if you're modifying:
# 1. The original DataFrame
# 2. A copy of a subset
# 3. A view of a subset

# Good: Use .loc for assignment
# df.loc[df['A'] > 1, 'B'] = 999  # Clear: modifying original

# ============================================================================
# 6. WHEN DOES PANDAS CREATE A COPY VS VIEW?
# ============================================================================

print("\n" + "="*60)
print("6. When Does Pandas Create Copy vs View?")
print("="*60)

print("""
View (shares memory with original):
- Single column selection: df['col']
- Slicing rows: df[10:20]
- Boolean indexing sometimes

Copy (new memory):
- Multiple column selection: df[['col1', 'col2']]
- Most operations: df.groupby(), df.merge(), etc.
- Explicitly: df.copy()

Rule of thumb: If unsure, assume it's a copy!
Use .copy() explicitly when you need a copy.
""")

# ============================================================================
# 7. SAFE PATTERNS
# ============================================================================

print("\n" + "="*60)
print("7. Safe Patterns")
print("="*60)

# Pattern 1: Explicit copy when needed
original_data = [1, 2, 3, 4, 5]
working_copy = original_data.copy()
working_copy.append(6)
print(f"Original: {original_data}")  # [1, 2, 3, 4, 5]
print(f"Working copy: {working_copy}")  # [1, 2, 3, 4, 5, 6]

# Pattern 2: Use .loc for assignment (Pandas)
# df.loc[condition, 'column'] = value  # Safe

# Pattern 3: Chain operations, don't modify intermediate results
# Good: df.query('A > 1').assign(B=999)
# Bad: subset = df.query('A > 1'); subset['B'] = 999

# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("8. Practical Examples")
print("="*60)

# Example 1: Modifying a list
def add_item_bad(lst):
    """Modifies original list - surprising!"""
    lst.append(999)
    return lst

def add_item_good(lst):
    """Returns new list - clear intent"""
    new_lst = lst.copy()
    new_lst.append(999)
    return new_lst

original = [1, 2, 3]
result_bad = add_item_bad(original)
print(f"After bad function: {original}")  # [1, 2, 3, 999] - modified!

original = [1, 2, 3]
result_good = add_item_good(original)
print(f"After good function: {original}")  # [1, 2, 3] - unchanged

# Example 2: Default mutable arguments (common pitfall!)
def append_to_list_bad(item, lst=[]):  # DON'T DO THIS!
    """Default list is shared across calls!"""
    lst.append(item)
    return lst

print(f"\nCall 1: {append_to_list_bad(1)}")  # [1]
print(f"Call 2: {append_to_list_bad(2)}")  # [1, 2] - Surprise!

def append_to_list_good(item, lst=None):
    """Create new list each time"""
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(f"\nCall 1: {append_to_list_good(1)}")  # [1]
print(f"Call 2: {append_to_list_good(2)}")  # [2] - Expected

# ============================================================================
# 9. CHECKING OBJECT IDENTITY
# ============================================================================

print("\n" + "="*60)
print("9. Checking Object Identity")
print("="*60)

a = [1, 2, 3]
b = a
c = a.copy()

print(f"a is b: {a is b}")  # True - same object
print(f"a is c: {a is c}")  # False - different objects
print(f"a == c: {a == c}")  # True - same values

# Get object ID
print(f"\nid(a): {id(a)}")
print(f"id(b): {id(b)}")  # Same as a
print(f"id(c): {id(c)}")  # Different from a

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. Mutable vs Immutable:
   - Mutable: list, dict, set (can change)
   - Immutable: int, str, tuple (cannot change)

2. Reference vs Copy:
   - Reference: b = a (same object)
   - Copy: b = a.copy() (different object)

3. Shallow vs Deep Copy:
   - Shallow: Copies outer, shares nested
   - Deep: Copies everything (copy.deepcopy())

4. Views (NumPy/Pandas):
   - View: Different way to see same data
   - Modifying view modifies original
   - Use .copy() to avoid surprises

5. Pandas SettingWithCopyWarning:
   - Happens when modifying a view/copy ambiguously
   - Fix: Use .loc[condition, 'col'] = value

6. Safe patterns:
   - Explicit .copy() when needed
   - Use .loc for assignment
   - Don't modify intermediate results

7. Common pitfalls:
   - Mutable default arguments
   - Chained assignment
   - Assuming slicing creates copy

In Pandas:
- Always use .loc for assignment
- Use .copy() when you need independent data
- Understand view vs copy to avoid warnings
""")
