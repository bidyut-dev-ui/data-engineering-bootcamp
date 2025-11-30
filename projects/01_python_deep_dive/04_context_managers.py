"""
Tutorial 4: Context Managers and the 'with' Statement
Essential for file handling and resource management in Pandas
"""

# ============================================================================
# 1. THE PROBLEM: Manual Resource Management
# ============================================================================

print("="*60)
print("1. The Problem: Manual Resource Management")
print("="*60)

# Bad way: Manual file handling
def read_file_bad(filename):
    """Risky - file might not close if error occurs"""
    f = open(filename, 'r')
    data = f.read()
    f.close()  # Might not execute if error above!
    return data

# What if an error occurs?
# try:
#     read_file_bad('nonexistent.txt')
# except FileNotFoundError:
#     print("File not found - but file handle might still be open!")

# ============================================================================
# 2. THE SOLUTION: Context Managers (with statement)
# ============================================================================

print("\n" + "="*60)
print("2. The Solution: Context Managers")
print("="*60)

# Good way: Context manager
def read_file_good(filename):
    """Safe - file automatically closes even if error occurs"""
    with open(filename, 'r') as f:
        data = f.read()
    # File is automatically closed here
    return data

# Create a test file
with open('test.txt', 'w') as f:
    f.write('Hello, World!')

# Read it back
with open('test.txt', 'r') as f:
    content = f.read()
    print(f"Content: {content}")

# File is closed here automatically
print(f"File closed: {f.closed}")

# ============================================================================
# 3. PANDAS FILE OPERATIONS
# ============================================================================

print("\n" + "="*60)
print("3. Pandas File Operations")
print("="*60)

# Create sample CSV
import csv

with open('sample_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'price'])
    writer.writerow([1, 'Apple', 1.5])
    writer.writerow([2, 'Banana', 0.8])
    writer.writerow([3, 'Orange', 1.2])

print("Created sample_data.csv")

# Pandas pattern: Read CSV with context manager
# This is common when you need to process the file object
with open('sample_data.csv', 'r') as f:
    # In real Pandas: df = pd.read_csv(f)
    lines = f.readlines()
    print(f"Read {len(lines)} lines")

# Pandas pattern: Write CSV with context manager
data_to_write = [
    ['id', 'value'],
    [1, 100],
    [2, 200]
]

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data_to_write)
    # In real Pandas: df.to_csv(f, index=False)

print("Wrote output.csv")

# ============================================================================
# 4. MULTIPLE CONTEXT MANAGERS
# ============================================================================

print("\n" + "="*60)
print("4. Multiple Context Managers")
print("="*60)

# Open multiple files at once
with open('sample_data.csv', 'r') as input_file, \
     open('processed.csv', 'w', newline='') as output_file:
    
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    
    # Process and write
    for row in reader:
        writer.writerow(row)
    
    print("Processed data from input to output")

# Both files are closed here

# ============================================================================
# 5. CUSTOM CONTEXT MANAGERS
# ============================================================================

print("\n" + "="*60)
print("5. Custom Context Managers")
print("="*60)

from contextlib import contextmanager

@contextmanager
def timer(name):
    """Context manager to time code execution"""
    import time
    start = time.time()
    print(f"Starting {name}...")
    
    yield  # Code block runs here
    
    end = time.time()
    print(f"Finished {name} in {end - start:.4f} seconds")

# Use it
with timer("Data Processing"):
    # Simulate processing
    total = sum(range(1000000))
    print(f"Computed sum: {total}")

# ============================================================================
# 6. COMMON PANDAS PATTERNS
# ============================================================================

print("\n" + "="*60)
print("6. Common Pandas Patterns")
print("="*60)

# Pattern 1: Read CSV
print("\nPattern 1: Read CSV")
with open('sample_data.csv', 'r') as f:
    # df = pd.read_csv(f)
    print(f"File object: {f}")
    print(f"File name: {f.name}")

# Pattern 2: Write CSV
print("\nPattern 2: Write CSV")
with open('report.csv', 'w', newline='') as f:
    # df.to_csv(f, index=False)
    writer = csv.writer(f)
    writer.writerow(['metric', 'value'])
    writer.writerow(['total_sales', 10000])

# Pattern 3: Chained operations
print("\nPattern 3: Chained operations")
with open('sample_data.csv', 'r') as f:
    # In real Pandas:
    # (df
    #  .assign(tax=lambda d: d.price * 0.1)
    #  .loc[:, ['name', 'price', 'tax']]
    #  .to_csv(output_file, index=False)
    # )
    print("Would process and write in one chain")

# ============================================================================
# 7. ERROR HANDLING WITH CONTEXT MANAGERS
# ============================================================================

print("\n" + "="*60)
print("7. Error Handling with Context Managers")
print("="*60)

# Context manager ensures cleanup even on error
try:
    with open('sample_data.csv', 'r') as f:
        data = f.read()
        # Simulate error
        # raise ValueError("Something went wrong!")
        print("Processing data...")
except ValueError as e:
    print(f"Error occurred: {e}")
finally:
    # File is still closed!
    print(f"File closed even with error: {f.closed}")

# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "="*60)
print("8. Practical Examples")
print("="*60)

# Example 1: Safe file processing
def process_csv_safe(input_file, output_file):
    """Process CSV safely with context managers"""
    with open(input_file, 'r') as f_in, \
         open(output_file, 'w', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=['id', 'name', 'price_with_tax'])
        writer.writeheader()
        
        for row in reader:
            # Add tax
            price = float(row['price'])
            row['price_with_tax'] = price * 1.1
            writer.writerow({
                'id': row['id'],
                'name': row['name'],
                'price_with_tax': row['price_with_tax']
            })

process_csv_safe('sample_data.csv', 'with_tax.csv')
print("Created with_tax.csv")

# Example 2: Temporary file context
import tempfile

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
    tmp.write('id,value\n')
    tmp.write('1,100\n')
    tmp_name = tmp.name
    print(f"Created temporary file: {tmp_name}")

# File is closed but not deleted (delete=False)
print(f"Temp file exists: {True}")  # Would check with os.path.exists()

# ============================================================================
# 9. CONTEXT MANAGER PROTOCOL
# ============================================================================

print("\n" + "="*60)
print("9. Context Manager Protocol")
print("="*60)

class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening connection to {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        print(f"Closing connection to {self.db_name}")
        self.connection = None
        # Return False to propagate exceptions
        return False

# Use it
with DatabaseConnection('sales_db') as conn:
    print(f"Using {conn}")
    # Do database operations

# Connection is closed here

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n" + "="*60)
print("KEY TAKEAWAYS")
print("="*60)
print("""
1. Always use 'with' for file operations:
   with open('file.txt') as f:
       data = f.read()

2. Files are automatically closed, even on errors

3. Multiple context managers:
   with open('in.csv') as f_in, open('out.csv', 'w') as f_out:
       # Process

4. Pandas patterns:
   with open('data.csv') as f:
       df = pd.read_csv(f)
   
   with open('output.csv', 'w') as f:
       df.to_csv(f, index=False)

5. Custom context managers:
   @contextmanager
   def my_context():
       # setup
       yield
       # cleanup

6. Benefits:
   - Automatic cleanup
   - Exception safe
   - Cleaner code
   - No resource leaks

In Pandas, you'll use 'with' constantly for:
- Reading CSV/Excel files
- Writing processed data
- Database connections
- Temporary files
""")

# Cleanup
import os
for f in ['test.txt', 'sample_data.csv', 'output.csv', 'processed.csv', 
          'report.csv', 'with_tax.csv']:
    if os.path.exists(f):
        os.remove(f)
print("\nCleaned up test files")
