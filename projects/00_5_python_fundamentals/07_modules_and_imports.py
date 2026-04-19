"""
Tutorial 07: Modules and Imports in Python
===========================================

Modules allow you to organize code into reusable units.
This tutorial covers:
1. Creating and using modules
2. Import statements (import, from, as)
3. Package structure and __init__.py
4. Standard library modules
5. Third-party packages (pip)
6. Module search path (sys.path)
7. Relative vs absolute imports
8. Module attributes (__name__, __file__)
9. Creating executable scripts

Learning Objectives:
- Create and organize Python modules and packages
- Use different import styles effectively
- Understand Python's module search path
- Work with standard library modules
- Install and use third-party packages
- Create both importable modules and executable scripts

Prerequisites:
- Tutorial 01: Variables and Types
- Tutorial 02: Control Flow
- Tutorial 03: Data Structures
- Tutorial 04: Functions
- Tutorial 05: File I/O
- Tutorial 06: Error Handling
"""

print("=" * 60)
print("TUTORIAL 07: MODULES AND IMPORTS")
print("=" * 60)

import sys
import os
from pathlib import Path

# ============================================================================
# 1. BASIC MODULE CREATION AND USAGE
# ============================================================================
print("\n1. BASIC MODULE CREATION AND USAGE")
print("-" * 40)

# Create a simple module file for demonstration
module_content = '''
"""
math_operations.py - A simple module for math operations.
"""

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the quotient of two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Module-level variable
PI = 3.14159

# This runs when module is executed directly
if __name__ == "__main__":
    print("Math operations module running in standalone mode")
    print(f"2 + 3 = {add(2, 3)}")
'''

# Write the module file
with open("math_operations.py", "w") as f:
    f.write(module_content)

print("Created math_operations.py module")

# ============================================================================
# 2. IMPORT STATEMENTS
# ============================================================================
print("\n2. IMPORT STATEMENTS")
print("-" * 40)

# Method 1: Import entire module
print("Method 1: Import entire module")
import math_operations

print(f"Using math_operations.add(5, 3): {math_operations.add(5, 3)}")
print(f"Module variable PI: {math_operations.PI}")

# Method 2: Import specific functions
print("\nMethod 2: Import specific functions")
from math_operations import multiply, divide

print(f"Using multiply(4, 5): {multiply(4, 5)}")
print(f"Using divide(10, 2): {divide(10, 2)}")

# Method 3: Import with alias
print("\nMethod 3: Import with alias")
import math_operations as mo
from math_operations import add as addition

print(f"Using mo.subtract(10, 4): {mo.subtract(10, 4)}")
print(f"Using addition(7, 8): {addition(7, 8)}")

# Method 4: Import everything (not recommended)
print("\nMethod 4: Import everything (use with caution)")
# from math_operations import *  # Usually avoided

# ============================================================================
# 3. STANDARD LIBRARY MODULES
# ============================================================================
print("\n3. STANDARD LIBRARY MODULES")
print("-" * 40)

# math module
import math
print("Math module:")
print(f"  math.sqrt(25) = {math.sqrt(25)}")
print(f"  math.pi = {math.pi}")
print(f"  math.factorial(5) = {math.factorial(5)}")

# datetime module
import datetime
print("\nDatetime module:")
now = datetime.datetime.now()
print(f"  Current datetime: {now}")
print(f"  Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Year: {now.year}, Month: {now.month}, Day: {now.day}")

# random module
import random
print("\nRandom module:")
print(f"  Random integer 1-100: {random.randint(1, 100)}")
print(f"  Random choice from list: {random.choice(['apple', 'banana', 'cherry'])}")
print(f"  Random sample: {random.sample(range(1, 50), 5)}")

# collections module
from collections import Counter, defaultdict, deque
print("\nCollections module:")
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_count = Counter(words)
print(f"  Word counts: {word_count}")
print(f"  Most common: {word_count.most_common(2)}")

# ============================================================================
# 4. PACKAGES AND __init__.py
# ============================================================================
print("\n4. PACKAGES AND __init__.py")
print("-" * 40)

# Create a package structure for demonstration
package_structure = """
my_package/
├── __init__.py
├── utils.py
├── data/
│   ├── __init__.py
│   └── processors.py
└── models/
    ├── __init__.py
    └── predictor.py
"""

print("Package structure example:")
print(package_structure)

# Create the package directory structure
os.makedirs("my_package/data", exist_ok=True)
os.makedirs("my_package/models", exist_ok=True)

# Create __init__.py files
for init_file in [
    "my_package/__init__.py",
    "my_package/data/__init__.py", 
    "my_package/models/__init__.py"
]:
    with open(init_file, "w") as f:
        f.write('"""Package initialization."""\n')
        f.write(f'print(f"Initializing {__name__}")\n')

# Create utils.py
utils_content = '''
"""Utility functions for the package."""

def format_name(first, last):
    """Format a full name."""
    return f"{first.title()} {last.title()}"

def calculate_average(numbers):
    """Calculate average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
'''

with open("my_package/utils.py", "w") as f:
    f.write(utils_content)

# Create processors.py in data subpackage
processors_content = '''
"""Data processing functions."""

def clean_text(text):
    """Clean text by removing extra whitespace."""
    return ' '.join(text.strip().split())

def normalize_numbers(numbers, target_range=(0, 1)):
    """Normalize numbers to target range."""
    if not numbers:
        return []
    min_val, max_val = min(numbers), max(numbers)
    if min_val == max_val:
        return [target_range[0]] * len(numbers)
    
    scale = target_range[1] - target_range[0]
    return [
        target_range[0] + (x - min_val) / (max_val - min_val) * scale
        for x in numbers
    ]
'''

with open("my_package/data/processors.py", "w") as f:
    f.write(processors_content)

print("Created my_package with subpackages")

# Demonstrate package imports
print("\nDemonstrating package imports:")
import my_package.utils
from my_package.data import processors

print(f"  my_package.utils.format_name('john', 'doe'): {my_package.utils.format_name('john', 'doe')}")
print(f"  processors.clean_text('  hello   world  '): '{processors.clean_text('  hello   world  ')}'")

# ============================================================================
# 5. MODULE SEARCH PATH (sys.path)
# ============================================================================
print("\n5. MODULE SEARCH PATH (sys.path)")
print("-" * 40)

print("Python searches for modules in these locations (in order):")
for i, path in enumerate(sys.path[:5], 1):  # Show first 5
    print(f"  {i}. {path}")

print("\nAdding current directory to path (if not already there):")
current_dir = os.path.abspath(".")
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"  Added: {current_dir}")

# Create a module in a custom location
custom_dir = "custom_modules"
os.makedirs(custom_dir, exist_ok=True)

custom_module = '''
"""Custom module in a custom directory."""

def custom_function():
    return "Hello from custom module!"
'''

with open(f"{custom_dir}/custom_mod.py", "w") as f:
    f.write(custom_module)

# Add custom directory to path
sys.path.append(os.path.abspath(custom_dir))

print(f"\nAdded custom directory to path: {custom_dir}")

# Now we can import from custom directory
import custom_mod
print(f"  custom_mod.custom_function(): {custom_mod.custom_function()}")

# ============================================================================
# 6. RELATIVE VS ABSOLUTE IMPORTS
# ============================================================================
print("\n6. RELATIVE VS ABSOLUTE IMPORTS")
print("-" * 40)

print("Absolute imports (recommended):")
print("  import my_package.utils")
print("  from my_package.data import processors")

print("\nRelative imports (within a package):")
print("  from . import utils          # Import from same package")
print("  from .. import other_module  # Import from parent package")
print("  from .subpackage import func # Import from subpackage")

# Create a module with relative imports for demonstration
relative_module = '''
"""Module demonstrating relative imports."""

# These would be in a real package structure
# from . import sibling_module
# from .. import parent_module
# from .subpackage import function

def demonstrate():
    return "Relative imports are for use within packages"
'''

with open("my_package/relative_demo.py", "w") as f:
    f.write(relative_module)

print("\nNote: Relative imports only work within packages")
print("and when the module is imported, not run as a script.")

# ============================================================================
# 7. MODULE ATTRIBUTES
# ============================================================================
print("\n7. MODULE ATTRIBUTES")
print("-" * 40)

print("Important module attributes:")
print(f"  math_operations.__name__: {math_operations.__name__}")
print(f"  math_operations.__file__: {math_operations.__file__}")
print(f"  math_operations.__doc__: {math_operations.__doc__[:50]}...")

# List functions in a module
print("\nFunctions in math_operations module:")
for name in dir(math_operations):
    if not name.startswith("_"):  # Skip private attributes
        attr = getattr(math_operations, name)
        if callable(attr):
            print(f"  {name}()")

# Check if module has specific attribute
print(f"\nHas 'add' attribute? {hasattr(math_operations, 'add')}")
print(f"Has 'non_existent' attribute? {hasattr(math_operations, 'non_existent')}")

# ============================================================================
# 8. __name__ AND __main__ PATTERN
# ============================================================================
print("\n8. __name__ AND __main__ PATTERN")
print("-" * 40)

# Create a module that can be both imported and run
main_module = '''
"""
main_demo.py - Demonstrates __name__ == "__main__" pattern.
"""

def helper_function():
    """A function that's always available."""
    return "I'm a helper function"

def main():
    """Main function that runs when script is executed directly."""
    print("Running as main script")
    print(f"Helper function says: {helper_function()}")
    print("Doing some work...")
    return "Work completed"

# This code runs only when the module is executed directly
if __name__ == "__main__":
    result = main()
    print(f"Result: {result}")
'''

with open("main_demo.py", "w") as f:
    f.write(main_module)

print("Created main_demo.py with __name__ == '__main__' pattern")
print("\nWhen imported: helper_function is available, main() doesn't run")
print("When run directly: main() executes")

# Demonstrate importing it
import main_demo
print(f"\nImported main_demo, helper_function: {main_demo.helper_function()}")

# ============================================================================
# 9. THIRD-PARTY PACKAGES (pip)
# ============================================================================
print("\n9. THIRD-PARTY PACKAGES (pip)")
print("-" * 40)

print("Common pip commands:")
print("  pip install package_name          # Install a package")
print("  pip install package_name==1.2.3   # Install specific version")
print("  pip install -r requirements.txt   # Install from requirements file")
print("  pip list                          # List installed packages")
print("  pip show package_name             # Show package info")
print("  pip freeze > requirements.txt     # Save installed packages")

print("\nVirtual environments (best practice):")
print("  python -m venv venv               # Create virtual environment")
print("  source venv/bin/activate          # Activate (Linux/Mac)")
print("  venv\\Scripts\\activate           # Activate (Windows)")
print("  deactivate                        # Deactivate")

print("\nPopular third-party packages for data engineering:")
print("  - pandas: Data manipulation and analysis")
print("  - numpy: Numerical computing")
print("  - requests: HTTP requests")
print("  - sqlalchemy: Database ORM")
print("  - fastapi: Web framework")
print("  - pyspark: Big data processing")
print("  - airflow: Workflow orchestration")

# ============================================================================
# 10. CREATING EXECUTABLE SCRIPTS
# ============================================================================
print("\n10. CREUTING EXECUTABLE SCRIPTS")
print("-" * 40)

# Create an executable script
script_content = '''#!/usr/bin/env python3
"""
data_processor.py - A command-line data processing script.
"""

import sys
import argparse
from pathlib import Path

def process_file(input_file, output_file=None):
    """Process a data file."""
    print(f"Processing {input_file}...")
    
    # Read input
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Simple processing: convert to uppercase
    processed = content.upper()
    
    # Determine output file
    if output_file is None:
        output_file = Path(input_file).stem + "_processed.txt"
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(processed)
    
    print(f"Saved to {output_file}")
    return output_file

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Process data files")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Verbose mode enabled")
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
    
    try:
        output = process_file(args.input, args.output)
        print(f"Successfully processed {args.input}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''

with open("data_processor.py", "w") as f:
    f.write(script_content)

# Make it executable (Unix-like systems)
os.chmod("data_processor.py", 0o755)

print("Created data_processor.py as an executable script")
print("\nUsage examples:")
print("  python data_processor.py input.txt")
print("  python data_processor.py input.txt -o output.txt")
print("  python data_processor.py input.txt -v")

# Create a test input file
with open("test_input.txt", "w") as f:
    f.write("Hello, World!\nThis is a test file.\n")

print("\nTest the script:")
print("  Created test_input.txt")

# ============================================================================
# 11. PRACTICE EXERCISES
# ============================================================================
print("\n11. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: Create a Utility Package")
print("Create a package called 'myutils' with:")
print("  - file_utils.py: functions for file operations")
print("  - string_utils.py: functions for string manipulation")
print("  - math_utils.py: advanced math functions")
print("  - __init__.py that exposes key functions")
print("  - setup.py for installation")
print("  - tests/ directory with test modules")

print("\nExercise 2: Command-Line Tool")
print("Create a command-line tool that:")
print("  - Uses argparse for command-line arguments")
print("  - Can be installed with pip install -e .")
print("  - Has multiple subcommands (like git)")
print("  - Includes help text and examples")
print("  - Logs to a file with different verbosity levels")

print("\nExercise 3: Plugin System")
print("Create a plugin system where:")
print("  - Main program discovers plugins dynamically")
print("  - Plugins are separate modules or packages")
print("  - Each plugin implements a standard interface")
print("  - Plugins can be enabled/disabled via config")
print("  - New plugins can be added without modifying main code")

print("\nExercise 4: Configuration Manager")
print("Create a configuration system that:")
print("  - Loads config from multiple sources (file, env vars, CLI)")
print("  - Supports different environments (dev, test, prod)")
print("  - Validates configuration values")
print("  - Provides defaults for missing values")
print("  - Can be imported and used by any module")

# ============================================================================
# 12. COMMON GOTCHAS
# ============================================================================
print("\n12. COMMON GOTCHAS")
print("-" * 40)

print("1. Circular imports")
print("   ❌ module_a imports module_b, module_b imports module_a")
print("   ✅ Restructure code to avoid circular dependencies")
print("   ✅ Use local imports inside functions")

print("\n2. Shadowing standard library modules")
print("   ❌ Naming your file 'json.py' or 'os.py'")
print("   ✅ Use descriptive, unique names for your modules")

print("\n3. Modifying sys.path incorrectly")
print("   ❌ sys.path.append('..')  # Can cause confusion")
print("   ✅ Use proper package structure")
print("   ✅ Use absolute imports")

print("\n4. Forgetting __init__.py in packages")
print("   ❌ mypackage/subpackage/  # Missing __init__.py")
print("   ✅ mypackage/subpackage/__init__.py  # Makes it a package")

print("\n5. Importing inside functions (performance)")
print("   ❌ def process_data():")
print("          import pandas as pd  # Import on every call!")
print("   ✅ import pandas as pd")
print("      def process_data():")
print("          # use pd")

print("\n6. Not handling import errors")
print("   ❌ import non_existent_module  # Crashes program")
print("   ✅ try:")
print("          import optional_module")
print("      except ImportError:")
print("          optional_module = None")

# ============================================================================
# 13. BEST PRACTICES
# ============================================================================
print("\n13. BEST PRACTICES")
print("-" * 40)

print("1. Use absolute imports (from package import module)")
print("   ✅ from mypackage.utils import helper")
print("   ❌ from ..utils import helper  # Hard to understand")

print("\n2. Organize imports logically")
print("   ✅ # Standard library imports")
print("   ✅ import os")
print("   ✅ import sys")
print("   ✅ # Third-party imports")
print("   ✅ import pandas as pd")
print("   ✅ import numpy as np")
print("   ✅ # Local application imports")
print("   ✅ from . import utils")
print("   ✅ from .models import predictor")

print("\n3. Use __init__.py to control package exports")
print("   ✅ # In __init__.py")
print("   ✅ from .core import main_function")
print("   ✅ from .utils import helper_function")
print("   ✅ __all__ = ['main_function', 'helper_function']")

print("\n4. Create setup.py for installable packages")
print("   ✅ from setuptools import setup, find_packages")
print("   ✅ setup(")
print("          name='mypackage',")
print("          version='1.0.0',")
print("          packages=find_packages(),")
print("          install_requires=['requests>=2.25'])")

print("\n5. Use virtual environments for isolation")
print("   ✅ python -m venv venv")
print("   ✅ source venv/bin/activate")
print("   ✅ pip install -r requirements.txt")

print("\n6. Document your modules and functions")
print("   ✅ \"\"\"Module for data processing.")
print("   ")
print("   This module provides functions for cleaning")
print("   and transforming data.")
print("   \"\"\"")

print("\n7. Test your modules")
print("   ✅ import unittest")
print("   ✅ from mymodule import myfunction")
print("   ✅ class TestMyModule(unittest.TestCase):")
print("   ✅     def test_myfunction(self):")
print("   ✅         result = myfunction(input)")
print("   ✅         self.assertEqual(result, expected)")

# ============================================================================
# 14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE PACKAGE
# ============================================================================
print("\n14. REAL-WORLD EXAMPLE: DATA PROCESSING PIPELINE PACKAGE")
print("-" * 40)

print("Creating a complete data processing package structure:")

pipeline_structure = """
data_pipeline/
├── __init__.py
├── cli.py              # Command-line interface
├── config.py           # Configuration management
├── pipeline.py         # Main pipeline logic
├── processors/         # Data processors
│   ├── __init__.py
│   ├── csv_processor.py
│   ├── json_processor.py
│   └── transformer.py
├── utils/              # Utilities
│   ├── __init__.py
│   ├── file_utils.py
│   ├── logging_utils.py
│   └── validation.py
├── tests/              # Tests
│   ├── __init__.py
│   ├── test_pipeline.py
│   └── test_processors.py
├── requirements.txt    # Dependencies
├── setup.py           # Installation script
└── README.md          # Documentation
"""

print(pipeline_structure)

# Create a simplified version for demonstration
os.makedirs("demo_pipeline/processors", exist_ok=True)
os.makedirs("demo_pipeline/utils", exist_ok=True)
os.makedirs("demo_pipeline/tests", exist_ok=True)

# Create __init__.py files
for init_file in [
    "demo_pipeline/__init__.py",
    "demo_pipeline/processors/__init__.py",
    "demo_pipeline/utils/__init__.py",
    "demo_pipeline/tests/__init__.py"
]:
    with open(init_file, "w") as f:
        f.write('"""Package initialization."""\n\n__version__ = "1.0.0"\n')

# Create a simple processor
csv_processor = '''
"""CSV processor module."""

import csv
from pathlib import Path

def read_csv(filepath):
    """Read a CSV file and return data as list of dictionaries."""
    data = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def write_csv(data, filepath, fieldnames=None):
    """Write data to a CSV file."""
    if not data:
        return
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    return filepath
'''

with open("demo_pipeline/processors/csv_processor.py", "w") as f:
    f.write(csv_processor)

# Create a utility module
file_utils = '''
"""File utility functions."""

import os
from pathlib import Path

def ensure_directory(path):
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def get_file_extension(filepath):
    """Get the file extension (without dot)."""
    return Path(filepath).suffix[1:].lower()

def find_files(directory, pattern="*"):
    """Find files matching a pattern in a directory."""
    return list(Path(directory).glob(pattern))
'''

with open("demo_pipeline/utils/file_utils.py", "w") as f:
    f.write(file_utils)

# Create main pipeline module
pipeline = '''
"""Main pipeline module."""

from .processors import csv_processor
from .utils import file_utils

class DataPipeline:
    """A simple data processing pipeline."""
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        file_utils.ensure_directory(output_dir)
    
    def process_csv_files(self):
        """Process all CSV files in input directory."""
        import glob
        csv_files = glob.glob(f"{self.input_dir}/*.csv")
        
        results = []
        for csv_file in csv_files:
            print(f"Processing {csv_file}...")
            
            # Read data
            data = csv_processor.read_csv(csv_file)
            
            # Simple transformation: add processed timestamp
            import datetime
            for row in data:
                row['processed_at'] = datetime.datetime.now().isoformat()
            
            # Write to output
            output_file = f"{self.output_dir}/{Path(csv_file).name}"
            csv_processor.write_csv(data, output_file)
            
            results.append({
                'input': csv_file,
                'output': output_file,
                'records': len(data)
            })
        
        return results
'''

with open("demo_pipeline/pipeline.py", "w") as f:
    f.write(pipeline)

# Create __init__.py that exports the main class
with open("demo_pipeline/__init__.py", "a") as f:
    f.write('\nfrom .pipeline import DataPipeline\n')
    f.write('__all__ = ["DataPipeline"]\n')

print("\nCreated demo_pipeline package with:")
print("  - DataPipeline class in pipeline.py")
print("  - CSV processor in processors/csv_processor.py")
print("  - File utilities in utils/file_utils.py")
print("  - Proper __init__.py files")

# Demonstrate using the package
print("\nDemonstrating package usage:")
import sys
sys.path.insert(0, ".")

from demo_pipeline import DataPipeline
print("  Imported DataPipeline from demo_pipeline")

# Clean up demonstration files
print("\nCleaning up demonstration files...")
import shutil

files_to_remove = [
    "math_operations.py",
    "main_demo.py", 
    "data_processor.py",
    "test_input.txt",
    "custom_mod.py"
]

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)

# Remove directories
dirs_to_remove = [
    "my_package",
    "custom_modules",
    "demo_pipeline"
]

for directory in dirs_to_remove:
    if os.path.exists(directory):
        shutil.rmtree(directory)

print("Cleanup complete!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Modules are single .py files, packages are directories with __init__.py
2. Use import to load modules, from ... import for specific items
3. Python searches for modules in directories listed in sys.path
4. __name__ == "__main__" lets code run when executed directly
5. Organize large projects into packages with clear structure
6. Use virtual environments to manage dependencies
7. Document modules with docstrings at the top of files
8. Test modules independently

Module Organization Principles:
- Single Responsibility: Each module should have one clear purpose
- Flat is better than nested: Avoid deep package hierarchies
- Explicit is better than implicit: Use clear import statements
- Readability counts: Name modules and functions descriptively

Common Patterns:
1. Library modules: Meant to be imported, not run directly
2. Script modules: Can be both imported and run as scripts
3. Package __init__.py: Controls what's exported from the package
4. if __name__ == "__main__": Code that runs only when script is executed

Next Steps:
- Practice creating your own modules and packages
- Explore Python's standard library modules
- Learn about setuptools for creating distributable packages
- Study popular third-party packages in your domain
- Move to Tutorial 08: Practice Exercises to consolidate learning
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 07")
print("=" * 60)