"""
Tutorial 05: File I/O in Python
================================

File Input/Output (I/O) allows programs to read from and write to files.
This tutorial covers:
1. Opening and closing files
2. Reading files (entire file, line by line, chunks)
3. Writing files (overwrite, append)
4. File modes (r, w, a, r+, w+, a+, b)
5. Context managers (with statement)
6. Working with different file formats (text, CSV, JSON)
7. File and directory operations (os, pathlib modules)
8. Handling large files efficiently

Learning Objectives:
- Read and write text files using various methods
- Use context managers for safe file handling
- Parse and create CSV and JSON files
- Navigate directories and check file properties
- Handle large files with memory-efficient techniques

Prerequisites:
- Tutorial 01: Variables and Types
- Tutorial 02: Control Flow
- Tutorial 03: Data Structures
- Tutorial 04: Functions
"""

print("=" * 60)
print("TUTORIAL 05: FILE I/O")
print("=" * 60)

import os
import json
import csv
from pathlib import Path

# ============================================================================
# 1. BASIC FILE OPERATIONS
# ============================================================================
print("\n1. BASIC FILE OPERATIONS")
print("-" * 40)

# Create a sample file for demonstration
sample_content = """Line 1: Hello, World!
Line 2: This is a sample file.
Line 3: Python file I/O is powerful.
Line 4: We can read, write, and manipulate files.
Line 5: End of file."""

# Write to a file (creates or overwrites)
with open("sample.txt", "w") as file:
    file.write(sample_content)

print("Created sample.txt with 5 lines of text")

# ============================================================================
# 2. READING FILES
# ============================================================================
print("\n2. READING FILES")
print("-" * 40)

# Method 1: read() - read entire file as string
print("Method 1: read() - Entire file")
with open("sample.txt", "r") as file:
    content = file.read()
    print(f"File size: {len(content)} characters")
    print(f"First 50 chars: {content[:50]}...")

# Method 2: readline() - read one line at a time
print("\nMethod 2: readline() - Line by line")
with open("sample.txt", "r") as file:
    line1 = file.readline()
    line2 = file.readline()
    print(f"Line 1: {line1.strip()}")
    print(f"Line 2: {line2.strip()}")

# Method 3: readlines() - read all lines into list
print("\nMethod 3: readlines() - All lines as list")
with open("sample.txt", "r") as file:
    lines = file.readlines()
    print(f"Total lines: {len(lines)}")
    for i, line in enumerate(lines[:3], 1):
        print(f"  Line {i}: {line.strip()}")

# Method 4: Iterate directly over file object (memory efficient)
print("\nMethod 4: Iterating over file object")
with open("sample.txt", "r") as file:
    line_count = 0
    for line in file:
        line_count += 1
        if line_count <= 2:
            print(f"  Line {line_count}: {line.strip()}")
    print(f"  Total lines processed: {line_count}")

# ============================================================================
# 3. WRITING FILES
# ============================================================================
print("\n3. WRITING FILES")
print("-" * 40)

# Write mode ('w') - creates new file or overwrites existing
print("Write mode ('w') - Overwrites existing file")
with open("output.txt", "w") as file:
    file.write("This is line 1.\n")
    file.write("This is line 2.\n")
    file.write("This is line 3.\n")
print("Created output.txt with 3 lines")

# Append mode ('a') - adds to end of file
print("\nAppend mode ('a') - Adds to existing file")
with open("output.txt", "a") as file:
    file.write("This is line 4 (appended).\n")
    file.write("This is line 5 (appended).\n")
print("Appended 2 more lines to output.txt")

# Read the final file
print("\nFinal content of output.txt:")
with open("output.txt", "r") as file:
    for i, line in enumerate(file, 1):
        print(f"  Line {i}: {line.strip()}")

# ============================================================================
# 4. FILE MODES
# ============================================================================
print("\n4. FILE MODES")
print("-" * 40)

modes = {
    'r': "Read only (default). File must exist.",
    'w': "Write only. Creates file or truncates existing.",
    'a': "Append only. Creates file or appends to existing.",
    'r+': "Read and write. File must exist.",
    'w+': "Read and write. Creates file or truncates existing.",
    'a+': "Read and append. Creates file or appends to existing.",
    'rb': "Read binary mode.",
    'wb': "Write binary mode.",
    'ab': "Append binary mode."
}

print("Common file modes:")
for mode, description in modes.items():
    print(f"  '{mode}': {description}")

# Example with r+ mode (read and write)
print("\nExample with 'r+' mode (read and write):")
with open("sample.txt", "r+") as file:
    # Read first line
    first_line = file.readline()
    print(f"  Original first line: {first_line.strip()}")
    
    # Move back to beginning
    file.seek(0)
    
    # Write new first line
    file.write("UPDATED: This is the new first line.\n")
    
    # Read the updated line
    file.seek(0)
    updated_line = file.readline()
    print(f"  Updated first line: {updated_line.strip()}")

# ============================================================================
# 5. CONTEXT MANAGERS (WITH STATEMENT)
# ============================================================================
print("\n5. CONTEXT MANAGERS (with statement)")
print("-" * 40)

print("Without context manager (risky):")
print("  file = open('temp.txt', 'w')")
print("  try:")
print("      file.write('Some data')")
print("  finally:")
print("      file.close()")

print("\nWith context manager (recommended):")
print("  with open('temp.txt', 'w') as file:")
print("      file.write('Some data')")
print("  # File automatically closed")

# Multiple files in one with statement
print("\nMultiple files in one with statement:")
with open("source.txt", "w") as source, open("destination.txt", "w") as dest:
    source.write("Data from source file.\n")
    dest.write("Data copied to destination.\n")
print("Created both source.txt and destination.txt")

# ============================================================================
# 6. WORKING WITH CSV FILES
# ============================================================================
print("\n6. WORKING WITH CSV FILES")
print("-" * 40)

# Create sample CSV data
csv_data = [
    ["Name", "Age", "City", "Salary"],
    ["Alice", "28", "New York", "75000"],
    ["Bob", "32", "San Francisco", "85000"],
    ["Charlie", "25", "Chicago", "65000"],
    ["Diana", "30", "Boston", "80000"]
]

# Write CSV file
print("Writing CSV file (employees.csv):")
with open("employees.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)
print("Created employees.csv with 5 rows")

# Read CSV file
print("\nReading CSV file:")
with open("employees.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    print(f"  Headers: {headers}")
    
    employees = []
    for row in reader:
        employees.append(row)
        print(f"  Row {len(employees)}: {row}")

# Read CSV as dictionary
print("\nReading CSV as dictionary:")
with open("employees.csv", "r") as csvfile:
    dict_reader = csv.DictReader(csvfile)
    for i, row in enumerate(dict_reader, 1):
        print(f"  Employee {i}: {row['Name']}, {row['Age']} years, {row['City']}")

# ============================================================================
# 7. WORKING WITH JSON FILES
# ============================================================================
print("\n7. WORKING WITH JSON FILES")
print("-" * 40)

# Create sample JSON data
employee_data = {
    "company": "TechCorp",
    "employees": [
        {
            "id": 101,
            "name": "Alice",
            "position": "Software Engineer",
            "skills": ["Python", "JavaScript", "SQL"],
            "active": True
        },
        {
            "id": 102,
            "name": "Bob",
            "position": "Data Scientist",
            "skills": ["Python", "R", "Machine Learning"],
            "active": True
        },
        {
            "id": 103,
            "name": "Charlie",
            "position": "DevOps Engineer",
            "skills": ["Docker", "Kubernetes", "AWS"],
            "active": False
        }
    ],
    "total_employees": 3,
    "locations": ["New York", "San Francisco", "Remote"]
}

# Write JSON file
print("Writing JSON file (company_data.json):")
with open("company_data.json", "w") as jsonfile:
    json.dump(employee_data, jsonfile, indent=2)
print("Created company_data.json with structured data")

# Read JSON file
print("\nReading JSON file:")
with open("company_data.json", "r") as jsonfile:
    loaded_data = json.load(jsonfile)
    print(f"  Company: {loaded_data['company']}")
    print(f"  Total employees: {loaded_data['total_employees']}")
    print(f"  Active employees: {sum(1 for emp in loaded_data['employees'] if emp['active'])}")
    
    print("\n  Employee names:")
    for emp in loaded_data["employees"]:
        print(f"    - {emp['name']} ({emp['position']})")

# ============================================================================
# 8. FILE AND DIRECTORY OPERATIONS (os module)
# ============================================================================
print("\n8. FILE AND DIRECTORY OPERATIONS (os module)")
print("-" * 40)

print("Current working directory:")
print(f"  {os.getcwd()}")

print("\nList files in current directory:")
for file in os.listdir("."):
    if os.path.isfile(file):
        size = os.path.getsize(file)
        print(f"  {file:20} - {size:6} bytes")

print("\nCheck if files exist:")
files_to_check = ["sample.txt", "output.txt", "employees.csv", "nonexistent.txt"]
for filename in files_to_check:
    exists = os.path.exists(filename)
    print(f"  {filename:20} - {'Exists' if exists else 'Does not exist'}")

print("\nFile properties:")
if os.path.exists("sample.txt"):
    stats = os.stat("sample.txt")
    print(f"  sample.txt:")
    print(f"    Size: {stats.st_size} bytes")
    print(f"    Created: {stats.st_ctime}")
    print(f"    Modified: {stats.st_mtime}")

# Create and remove directories
print("\nDirectory operations:")
os.makedirs("test_dir/sub_dir", exist_ok=True)
print("  Created test_dir/sub_dir")

# Create a file in the new directory
with open("test_dir/example.txt", "w") as f:
    f.write("Test file in nested directory")

print("  Created test_dir/example.txt")

# Clean up (remove test directory)
import shutil
shutil.rmtree("test_dir")
print("  Removed test_dir and its contents")

# ============================================================================
# 9. PATHLIB MODULE (Modern path handling)
# ============================================================================
print("\n9. PATHLIB MODULE (Modern path handling)")
print("-" * 40)

# Create Path objects
current_dir = Path(".")
sample_file = Path("sample.txt")
output_file = Path("output.txt")

print(f"Current directory: {current_dir.absolute()}")
print(f"Sample file exists: {sample_file.exists()}")
print(f"Sample file size: {sample_file.stat().st_size} bytes")

# Working with paths
new_path = current_dir / "data" / "processed" / "output.csv"
print(f"\nExample path construction: {new_path}")
print(f"  Parent: {new_path.parent}")
print(f"  Name: {new_path.name}")
print(f"  Stem: {new_path.stem}")
print(f"  Suffix: {new_path.suffix}")

# Create directory structure
data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)
print(f"\nCreated directory: {data_dir}")

# Write to file using pathlib
data_file = data_dir / "data.txt"
data_file.write_text("Data written using pathlib")
print(f"Created file: {data_file}")

# Read from file using pathlib
content = data_file.read_text()
print(f"Read content: {content[:30]}...")

# Clean up
import shutil
shutil.rmtree("data")
print("Cleaned up data directory")

# ============================================================================
# 10. HANDLING LARGE FILES
# ============================================================================
print("\n10. HANDLING LARGE FILES (Memory-efficient techniques)")
print("-" * 40)

# Create a large file for demonstration (1000 lines)
print("Creating large file (large_data.txt) with 1000 lines...")
with open("large_data.txt", "w") as f:
    for i in range(1000):
        f.write(f"Line {i+1}: This is sample data for line {i+1}. "
                f"It contains some random text to simulate a large file.\n")

file_size = os.path.getsize("large_data.txt")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

# Method 1: Process line by line (memory efficient)
print("\nMethod 1: Process line by line")
line_count = 0
with open("large_data.txt", "r") as f:
    for line in f:
        line_count += 1
        if line_count <= 3:
            print(f"  Line {line_count}: {line[:50]}...")
print(f"  Total lines processed: {line_count}")

# Method 2: Read in chunks (for binary files or custom parsing)
print("\nMethod 2: Read in chunks (1024 bytes at a time)")
chunk_size = 1024
total_chars = 0
with open("large_data.txt", "r") as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        total_chars += len(chunk)
print(f"  Total characters read: {total_chars:,}")

# Method 3: Using generators for processing
print("\nMethod 3: Generator function for processing")
def read_large_file(filename):
    """Generator to read large file line by line."""
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

# Process first 5 lines using generator
print("  First 5 lines from generator:")
for i, line in enumerate(read_large_file("large_data.txt")):
    if i < 5:
        print(f"    Line {i+1}: {line[:50]}...")
    if i >= 4:
        break

# Clean up large file
os.remove("large_data.txt")
print("\nCleaned up large_data.txt")

# ============================================================================
# 11. PRACTICE EXERCISES
# ============================================================================
print("\n11. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: Log File Analyzer")
print("Create a program that analyzes a web server log file:")
print("  - Count total requests")
print("  - Find most frequent IP addresses")
print("  - Count requests by HTTP method (GET, POST, etc.)")
print("  - Find the most requested URL")
print("  - Generate a summary report to a new file")

print("\nExercise 2: CSV Data Cleaner")
print("Create a program that cleans a CSV file:")
print("  - Remove duplicate rows")
print("  - Fill missing values with appropriate defaults")
print("  - Convert data types (strings to numbers, dates)")
print("  - Remove outliers based on statistical rules")
print("  - Save cleaned data to a new CSV file")

print("\nExercise 3: Configuration Manager")
print("Create a program that manages application configuration:")
print("  - Read configuration from a JSON file")
print("  - Allow updating configuration values")
print("  - Validate configuration (required fields, data types)")
print("  - Create backup of old configuration before saving")
print("  - Support different environments (dev, prod, test)")

print("\nExercise 4: File Synchronization Tool")
print("Create a program that synchronizes two directories:")
print("  - Compare files in source and destination directories")
print("  - Copy new or modified files from source to destination")
print("  - Delete files in destination that don't exist in source")
print("  - Generate a log of all operations performed")
print("  - Handle large files with progress indicators")

# ============================================================================
# 12. COMMON GOTCHAS
# ============================================================================
print("\n12. COMMON GOTCHAS")
print("-" * 40)

print("1. Forgetting to close files")
print("   ❌ file = open('data.txt', 'r')")
print("      data = file.read()")
print("      # File remains open!")
print("   ✅ with open('data.txt', 'r') as file:")
print("          data = file.read()")

print("\n2. Using wrong file mode")
print("   ❌ with open('data.txt', 'w') as file:")
print("          content = file.read()  # Can't read in write mode!")
print("   ✅ with open('data.txt', 'r') as file:")
print("          content = file.read()")

print("\n3. Not handling file not found errors")
print("   ❌ with open('missing.txt', 'r') as file:")
print("          content = file.read()  # FileNotFoundError!")
print("   ✅ try:")
print("          with open('missing.txt', 'r') as file:")
print("              content = file.read()")
print("      except FileNotFoundError:")
print("          print('File not found')")

print("\n4. Platform-specific path separators")
print("   ❌ path = 'folder\\file.txt'  # Windows only")
print("   ✅ import os")
print("      path = os.path.join('folder', 'file.txt')")
print("   ✅ from pathlib import Path")
print("      path = Path('folder') / 'file.txt'")

print("\n5. Reading entire large file into memory")
print("   ❌ with open('huge.log', 'r') as file:")
print("          lines = file.readlines()  # Memory error!")
print("   ✅ with open('huge.log', 'r') as file:")
print("          for line in file:")
print("              process(line)")

# ============================================================================
# 13. BEST PRACTICES
# ============================================================================
print("\n13. BEST PRACTICES")
print("-" * 40)

print("1. Always use context managers (with statement)")
print("   ✅ with open('file.txt', 'r') as f:")
print("          data = f.read()")

print("\n2. Specify encoding for text files")
print("   ✅ with open('file.txt', 'r', encoding='utf-8') as f:")
print("          data = f.read()")

print("\n3. Use pathlib for modern path handling")
print("   ✅ from pathlib import Path")
print("      file_path = Path('data') / 'input.csv'")
print("      if file_path.exists():")
print("          content = file_path.read_text()")

print("\n4. Handle different line endings")
print("   ✅ with open('file.txt', 'r', newline='') as f:")
print("          # Handles \\n, \\r\\n, \\r correctly")

print("\n5. Use appropriate file modes")
print("   ✅ 'r' for reading, 'w' for writing (overwrites)")
print("   ✅ 'a' for appending, 'x' for exclusive creation")
print("   ✅ 'b' for binary files (images, videos)")

print("\n6. Clean up temporary files")
print("   ✅ import tempfile")
print("      with tempfile.NamedTemporaryFile() as tmp:")
print("          tmp.write(b'data')")
print("          # File automatically deleted")

print("\n7. Validate file operations")
print("   ✅ if not file_path.exists():")
print("          raise FileNotFoundError(f'{file_path} not found')")
print("   ✅ if not file_path.is_file():")
print("          raise ValueError(f'{file_path} is not a file')")

# ============================================================================
# 14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE
# ============================================================================
print("\n14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE")
print("-" * 40)

print("Simulating a data processing pipeline:")
print("1. Read raw data from multiple sources")
print("2. Clean and transform the data")
print("3. Aggregate and analyze")
print("4. Generate reports")
print("5. Archive processed files")

# Step 1: Create sample data files
print("\nStep 1: Creating sample data files...")

# Sales data
sales_data = [
    ["date", "product", "quantity", "price", "customer_id"],
    ["2024-01-01", "Laptop", "2", "999.99", "C001"],
    ["2024-01-01", "Mouse", "5", "29.99", "C002"],
    ["2024-01-02", "Keyboard", "3", "79.99", "C003"],
    ["2024-01-02", "Monitor", "1", "299.99", "C001"],
    ["2024-01-03", "Laptop", "1", "999.99", "C004"]
]

with open("sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(sales_data)

# Customer data
customer_data = {
    "customers": [
        {"id": "C001", "name": "Alice", "email": "alice@example.com", "tier": "gold"},
        {"id": "C002", "name": "Bob", "email": "bob@example.com", "tier": "silver"},
        {"id": "C003", "name": "Charlie", "email": "charlie@example.com", "tier": "bronze"},
        {"id": "C004", "name": "Diana", "email": "diana@example.com", "tier": "gold"}
    ]
}

with open("customers.json", "w") as f:
    json.dump(customer_data, f, indent=2)

print("  Created sales.csv and customers.json")

# Step 2: Process the data
print("\nStep 2: Processing data...")

# Read and process sales data
sales_by_customer = {}
with open("sales.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        customer_id = row["customer_id"]
        quantity = int(row["quantity"])
        price = float(row["price"])
        total = quantity * price
        
        if customer_id not in sales_by_customer:
            sales_by_customer[customer_id] = {
                "total_sales": 0,
                "total_quantity": 0,
                "transactions": 0
            }
        
        sales_by_customer[customer_id]["total_sales"] += total
        sales_by_customer[customer_id]["total_quantity"] += quantity
        sales_by_customer[customer_id]["transactions"] += 1

# Read customer data
with open("customers.json", "r") as f:
    customers = json.load(f)["customers"]

# Step 3: Generate report
print("\nStep 3: Generating report...")

report_data = []
for customer in customers:
    customer_id = customer["id"]
    if customer_id in sales_by_customer:
        sales = sales_by_customer[customer_id]
        report_data.append({
            "customer_id": customer_id,
            "name": customer["name"],
            "tier": customer["tier"],
            "total_sales": round(sales["total_sales"], 2),
            "total_quantity": sales["total_quantity"],
            "transactions": sales["transactions"],
            "avg_transaction": round(sales["total_sales"] / sales["transactions"], 2)
        })

# Write report to CSV
report_file = "sales_report.csv"
with open(report_file, "w", newline="") as f:
    if report_data:
        fieldnames = report_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

print(f"  Generated {report_file} with {len(report_data)} customers")

# Step 4: Create summary
print("\nStep 4: Creating summary...")
total_sales = sum(item["total_sales"] for item in report_data)
avg_sales = total_sales / len(report_data) if report_data else 0

summary = {
    "report_date": "2024-01-03",
    "total_customers": len(report_data),
    "total_sales": round(total_sales, 2),
    "average_sales_per_customer": round(avg_sales, 2),
    "top_customer": max(report_data, key=lambda x: x["total_sales"])["name"] if report_data else "None",
    "files_processed": ["sales.csv", "customers.json"]
}

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("  Created summary.json")

# Step 5: Cleanup
print("\nStep 5: Archiving source files...")
import shutil
os.makedirs("archive", exist_ok=True)
for filename in ["sales.csv", "customers.json"]:
    if os.path.exists(filename):
        shutil.move(filename, f"archive/{filename}")
        print(f"  Archived {filename}")

print("\nPipeline completed successfully!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Use context managers (with statement) for automatic file closing
2. Choose appropriate file modes (r, w, a, r+, etc.) for your needs
3. Read files efficiently: line-by-line for large files, read() for small files
4. Use csv module for CSV files and json module for JSON files
5. os and pathlib modules provide file and directory operations
6. Handle different encodings and line endings properly
7. Always validate file existence and permissions before operations
8. Clean up temporary files and organize file structure

Performance Considerations:
- For large files: iterate line-by-line or read in chunks
- Use generators for memory-efficient processing pipelines
- Binary mode ('b') for non-text files (images, executables)
- Buffer size can be adjusted for performance tuning

Next Steps:
- Practice with the exercises above
- Move to Tutorial 06: Error Handling
- Experiment with building file processing utilities
- Explore advanced topics: memory-mapped files, async file I/O
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 05")
print("=" * 60)

# Clean up created files
files_to_clean = [
    "sample.txt", "output.txt", "employees.csv", "company_data.json",
    "source.txt", "destination.txt", "sales_report.csv", "summary.json"
]

print("\nCleaning up demonstration files...")
for filename in files_to_clean:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"  Removed {filename}")

if os.path.exists("archive"):
    shutil.rmtree("archive")
    print("  Removed archive directory")

print("Cleanup complete!")