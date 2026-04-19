"""
Tutorial 06: Error Handling in Python
======================================

Error handling allows programs to gracefully handle unexpected situations.
This tutorial covers:
1. Types of errors (syntax, runtime, logical)
2. try/except blocks
3. Handling multiple exceptions
4. else and finally clauses
5. Raising exceptions
6. Creating custom exceptions
7. Exception chaining
8. Best practices for robust error handling

Learning Objectives:
- Identify different types of Python errors
- Use try/except blocks to handle runtime errors
- Raise exceptions with meaningful messages
- Create custom exception classes
- Write robust code that handles edge cases
- Use finally for cleanup operations

Prerequisites:
- Tutorial 01: Variables and Types
- Tutorial 02: Control Flow
- Tutorial 03: Data Structures
- Tutorial 04: Functions
- Tutorial 05: File I/O
"""

print("=" * 60)
print("TUTORIAL 06: ERROR HANDLING")
print("=" * 60)

# ============================================================================
# 1. TYPES OF ERRORS
# ============================================================================
print("\n1. TYPES OF ERRORS")
print("-" * 40)

print("1. Syntax Errors - Detected during parsing")
print("   Example: print('Hello world'  # Missing closing parenthesis")
print("   ❌ This code won't even run")

print("\n2. Runtime Errors (Exceptions) - Occur during execution")
print("   Example: x = 10 / 0  # ZeroDivisionError")
print("   ✅ Can be caught and handled with try/except")

print("\n3. Logical Errors - Code runs but produces wrong results")
print("   Example: average = sum / count (forgot to check if count > 0)")
print("   ✅ Need careful testing and validation")

# ============================================================================
# 2. BASIC TRY/EXCEPT
# ============================================================================
print("\n2. BASIC TRY/EXCEPT BLOCKS")
print("-" * 40)

# Example 1: Handling division by zero
print("Example 1: Handling division by zero")
try:
    numerator = 10
    denominator = 0
    result = numerator / denominator
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")

# Example 2: Handling file not found
print("\nExample 2: Handling file not found")
try:
    with open("nonexistent_file.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found. Creating a new one...")
    with open("nonexistent_file.txt", "w") as file:
        file.write("This file was created because it didn't exist.")
    print("File created successfully!")

# Example 3: Handling multiple error types
print("\nExample 3: Handling multiple error types")
try:
    # This will cause a ValueError
    number = int("not_a_number")
    result = 10 / number
except ValueError:
    print("Error: Invalid number format")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")

# ============================================================================
# 3. ELSE AND FINALLY CLAUSES
# ============================================================================
print("\n3. ELSE AND FINALLY CLAUSES")
print("-" * 40)

# else: runs if no exception occurred
print("Using else clause:")
try:
    number = int("42")  # This will succeed
    result = 100 / number
except ValueError:
    print("Invalid number format")
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print(f"Calculation successful! Result: {result}")

# finally: always runs, used for cleanup
print("\nUsing finally clause for cleanup:")
file = None
try:
    file = open("test_file.txt", "w")
    file.write("Some data")
    # Simulate an error
    x = 1 / 0  # This will raise ZeroDivisionError
except ZeroDivisionError:
    print("Math error occurred")
finally:
    if file:
        file.close()
        print("File closed in finally block")
    print("Cleanup completed")

# Combined example
print("\nCombined try/except/else/finally:")
try:
    data = {"name": "Alice", "age": 30}
    print(f"Name: {data['name']}")
    print(f"City: {data['city']}")  # KeyError!
except KeyError as e:
    print(f"Missing key: {e}")
else:
    print("All data accessed successfully")
finally:
    print("Data access attempt completed")

# ============================================================================
# 4. RAISING EXCEPTIONS
# ============================================================================
print("\n4. RAISING EXCEPTIONS")
print("-" * 40)

# Raising built-in exceptions
def validate_age(age):
    """Validate that age is between 0 and 120."""
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 120:
        raise ValueError("Age seems unrealistic (over 120)")
    return True

print("Testing age validation:")
for test_age in [25, -5, 150]:
    try:
        validate_age(test_age)
        print(f"  Age {test_age}: Valid")
    except ValueError as e:
        print(f"  Age {test_age}: {e}")

# Raising with custom message
def divide_safely(a, b):
    """Divide two numbers with proper error handling."""
    if b == 0:
        raise ZeroDivisionError(f"Cannot divide {a} by zero")
    return a / b

print("\nTesting division with custom messages:")
try:
    result = divide_safely(10, 0)
except ZeroDivisionError as e:
    print(f"Error: {e}")

# Re-raising exceptions
def process_data(data):
    """Process data and re-raise exceptions with context."""
    try:
        return int(data) * 2
    except ValueError:
        print(f"Failed to process: '{data}'")
        raise  # Re-raise the same exception

print("\nTesting re-raising exceptions:")
try:
    process_data("abc")
except ValueError:
    print("Caught re-raised ValueError")

# ============================================================================
# 5. CUSTOM EXCEPTIONS
# ============================================================================
print("\n5. CUSTOM EXCEPTIONS")
print("-" * 40)

# Creating custom exception classes
class InsufficientFundsError(Exception):
    """Exception raised when account has insufficient funds."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.message = f"Insufficient funds: ${balance} available, ${amount} requested"
        super().__init__(self.message)

class InvalidTransactionError(Exception):
    """Exception raised for invalid transactions."""
    pass

# Using custom exceptions
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

print("Testing custom exceptions with bank account:")
account = BankAccount(1000)

# Test valid withdrawal
try:
    new_balance = account.withdraw(500)
    print(f"Withdrew $500. New balance: ${new_balance}")
except (InsufficientFundsError, InvalidTransactionError) as e:
    print(f"Withdrawal failed: {e}")

# Test insufficient funds
try:
    account.withdraw(600)  # Only $500 left now
except InsufficientFundsError as e:
    print(f"Withdrawal failed: {e}")

# Test invalid transaction
try:
    account.withdraw(-50)
except InvalidTransactionError as e:
    print(f"Withdrawal failed: {e}")

# ============================================================================
# 6. EXCEPTION CHAINING
# ============================================================================
print("\n6. EXCEPTION CHAINING")
print("-" * 40)

# Chaining exceptions with 'from'
def read_config_file(filename):
    """Read configuration file."""
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Configuration file '{filename}' not found") from e

def load_configuration():
    """Load application configuration."""
    try:
        config = read_config_file("config.json")
        return json.loads(config)
    except RuntimeError as e:
        print(f"Failed to load configuration: {e}")
        print(f"Original error: {e.__cause__}")

print("Testing exception chaining:")
try:
    load_configuration()
except Exception as e:
    print(f"Top-level error: {type(e).__name__}")

# Using raise ... from None to suppress chain
def process_user_input(user_input):
    """Process user input with suppressed chain."""
    try:
        return int(user_input)
    except ValueError:
        raise ValueError(f"Invalid input: '{user_input}' is not a number") from None

print("\nTesting suppressed exception chain:")
try:
    process_user_input("abc")
except ValueError as e:
    print(f"Error: {e}")
    print(f"Has cause: {e.__cause__ is not None}")

# ============================================================================
# 7. CONTEXT MANAGERS WITH ERROR HANDLING
# ============================================================================
print("\n7. CONTEXT MANAGERS WITH ERROR HANDLING")
print("-" * 40)

# Custom context manager with error handling
class DatabaseConnection:
    """Simulate a database connection with error handling."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        print(f"Connecting to database '{self.db_name}'...")
        # Simulate connection failure 30% of the time
        import random
        if random.random() < 0.3:
            raise ConnectionError(f"Failed to connect to {self.db_name}")
        self.connected = True
        print("Connected successfully!")
        return self
    
    def execute_query(self, query):
        """Execute a database query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"Executing query: {query}")
        # Simulate query execution
        return f"Results for: {query}"
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        self.connected = False
        if exc_type:
            print(f"An error occurred: {exc_type.__name__}: {exc_val}")
            # Return True to suppress the exception, False to re-raise
            return False  # Re-raise the exception
        print("Connection closed successfully")
        return True

print("Testing database connection with error handling:")
try:
    with DatabaseConnection("customers_db") as db:
        result = db.execute_query("SELECT * FROM users")
        print(f"Query result: {result}")
except ConnectionError as e:
    print(f"Database connection failed: {e}")
except RuntimeError as e:
    print(f"Database operation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")

# ============================================================================
# 8. ASSERTIONS FOR DEBUGGING
# ============================================================================
print("\n8. ASSERTIONS FOR DEBUGGING")
print("-" * 40)

# Using assertions for internal consistency checks
def calculate_discount(price, discount_percent):
    """Calculate discounted price with validation."""
    assert 0 <= discount_percent <= 100, f"Discount must be between 0-100, got {discount_percent}"
    assert price >= 0, f"Price cannot be negative, got {price}"
    
    discounted = price * (1 - discount_percent / 100)
    return round(discounted, 2)

print("Testing assertions (debug mode):")
try:
    # Valid case
    result = calculate_discount(100, 20)
    print(f"20% discount on $100: ${result}")
    
    # This will raise AssertionError if assertions are enabled
    # result = calculate_discount(-50, 20)  # Would fail
    # result = calculate_discount(100, 150)  # Would fail
except AssertionError as e:
    print(f"Assertion failed: {e}")

# Assertions can be disabled with -O flag
print("\nNote: Assertions are for debugging and can be disabled.")
print("Use proper validation for production code.")

# ============================================================================
# 9. PRACTICE EXERCISES
# ============================================================================
print("\n9. PRACTICE EXERCISES")
print("-" * 40)
print("Try these exercises to test your understanding:")

print("\nExercise 1: Robust Calculator")
print("Create a calculator that handles:")
print("  - Division by zero")
print("  - Invalid number formats")
print("  - Overflow errors")
print("  - Provide helpful error messages")
print("  - Log all errors to a file")

print("\nExercise 2: File Processor with Error Recovery")
print("Create a program that processes a directory of files:")
print("  - Skip files that can't be read (permission errors)")
print("  - Handle corrupted files gracefully")
print("  - Continue processing after errors")
print("  - Generate error report summary")
print("  - Retry failed operations with exponential backoff")

print("\nExercise 3: API Client with Error Handling")
print("Create an API client that handles:")
print("  - Network timeouts and retries")
print("  - HTTP error codes (404, 500, etc.)")
print("  - Rate limiting with exponential backoff")
print("  - Invalid JSON responses")
print("  - Connection pool exhaustion")

print("\nExercise 4: Data Validation Framework")
print("Create a validation framework that:")
print("  - Validates data types and ranges")
print("  - Provides detailed error messages")
print("  - Supports custom validation rules")
print("  - Collects all errors before failing")
print("  - Can be configured to fail fast or collect all errors")

# ============================================================================
# 10. COMMON GOTCHAS
# ============================================================================
print("\n10. COMMON GOTCHAS")
print("-" * 40)

print("1. Catching too broad exceptions")
print("   ❌ try:")
print("          # some code")
print("      except:")
print("          pass  # Hides all errors!")
print("   ✅ try:")
print("          # some code")
print("      except SpecificError:")
print("          # handle specific error")

print("\n2. Empty except blocks")
print("   ❌ try:")
print("          risky_operation()")
print("      except:")
print("          pass  # Silent failure!")
print("   ✅ try:")
print("          risky_operation()")
print("      except ExpectedError as e:")
print("          log_error(e)")
print("          handle_gracefully()")

print("\n3. Not cleaning up resources in finally")
print("   ❌ file = open('data.txt')")
print("      try:")
print("          process(file)")
print("      except:")
print("          handle_error()")
print("      # File might not be closed!")
print("   ✅ file = open('data.txt')")
print("      try:")
print("          process(file)")
print("      except:")
print("          handle_error()")
print("      finally:")
print("          file.close()")

print("\n4. Using exceptions for normal flow control")
print("   ❌ try:")
print("          value = dict[key]")
print("      except KeyError:")
print("          value = default  # Inefficient!")
print("   ✅ value = dict.get(key, default)")

print("\n5. Not preserving original traceback")
print("   ❌ try:")
print("          risky()")
print("      except Exception as e:")
print("          raise RuntimeError('Failed')  # Loses original trace!")
print("   ✅ try:")
print("          risky()")
print("      except Exception as e:")
print("          raise RuntimeError('Failed') from e")

# ============================================================================
# 11. BEST PRACTICES
# ============================================================================
print("\n11. BEST PRACTICES")
print("-" * 40)

print("1. Be specific with exception types")
print("   ✅ except ValueError:")
print("   ✅ except (FileNotFoundError, PermissionError):")
print("   ❌ except:  # Too broad!")

print("\n2. Use finally for cleanup")
print("   ✅ try:")
print("          resource = acquire()")
print("          use(resource)")
print("      finally:")
print("          release(resource)")

print("\n3. Provide helpful error messages")
print("   ❌ raise ValueError('Invalid input')")
print("   ✅ raise ValueError(f'Expected number, got {type(input).__name__}: {input}')")

print("\n4. Don't use exceptions for normal flow")
print("   ❌ Use try/except to check if key exists")
print("   ✅ Use 'key in dict' or dict.get()")

print("\n5. Log exceptions before handling")
print("   ✅ import logging")
print("      try:")
print("          risky_operation()")
print("      except Exception as e:")
print("          logging.error(f'Operation failed: {e}', exc_info=True)")
print("          handle_gracefully()")

print("\n6. Create custom exceptions for your domain")
print("   ✅ class PaymentFailedError(Exception):")
print("          pass")
print("   ✅ class InsufficientInventoryError(Exception):")
print("          pass")

print("\n7. Use context managers for resource management")
print("   ✅ with open('file.txt') as f:")
print("          content = f.read()")
print("   ✅ with DatabaseConnection() as db:")
print("          db.query('SELECT ...')")

# ============================================================================
# 12. REAL-WORLD EXAMPLE: DATA PIPELINE WITH ERROR HANDLING
# ============================================================================
print("\n12. REAL-WORLD EXAMPLE: DATA PIPELINE WITH ERROR HANDLING")
print("-" * 40)

import json
import csv
from datetime import datetime
import traceback

class DataPipelineError(Exception):
    """Base exception for data pipeline errors."""
    pass

class DataValidationError(DataPipelineError):
    """Raised when data fails validation."""
    pass

class DataTransformationError(DataPipelineError):
    """Raised when data transformation fails."""
    pass

class DataPipeline:
    """A robust data pipeline with comprehensive error handling."""
    
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.errors = []
        self.processed_count = 0
        self.error_count = 0
    
    def log_error(self, stage, error, data=None):
        """Log an error with context."""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'data': str(data)[:100] if data else None,
            'traceback': traceback.format_exc()
        }
        self.errors.append(error_info)
        self.error_count += 1
        print(f"[ERROR] {stage}: {type(error).__name__}: {error}")
    
    def validate_record(self, record):
        """Validate a data record."""
        required_fields = ['id', 'name', 'amount']
        for field in required_fields:
            if field not in record:
                raise DataValidationError(f"Missing required field: {field}")
        
        if not isinstance(record['id'], (int, str)):
            raise DataValidationError(f"Invalid id type: {type(record['id'])}")
        
        try:
            amount = float(record['amount'])
            if amount < 0:
                raise DataValidationError(f"Negative amount: {amount}")
        except ValueError:
            raise DataValidationError(f"Invalid amount: {record['amount']}")
        
        return True
    
    def transform_record(self, record):
        """Transform a data record."""
        try:
            transformed = {
                'record_id': str(record['id']),
                'customer_name': record['name'].strip().title(),
                'transaction_amount': float(record['amount']),
                'processed_at': datetime.now().isoformat(),
                'amount_category': 'HIGH' if float(record['amount']) > 1000 else 'LOW'
            }
            
            # Simulate a transformation error 10% of the time
            import random
            if random.random() < 0.1:
                raise DataTransformationError("Random transformation failure (simulated)")
                
            return transformed
        except Exception as e:
            raise DataTransformationError(f"Transformation failed: {e}")
    
    def process_record(self, record):
        """Process a single record with error handling."""
        try:
            # Step 1: Validate
            self.validate_record(record)
            
            # Step 2: Transform
            transformed = self.transform_record(record)
            
            # Step 3: Return success
            self.processed_count += 1
            return transformed
            
        except (DataValidationError, DataTransformationError) as e:
            self.log_error('process_record', e, record)
            return None
    
    def run(self):
        """Run the entire pipeline."""
        print(f"Starting data pipeline: {self.input_file} -> {self.output_file}")
        
        successful_records = []
        
        try:
            # Read input file
            with open(self.input_file, 'r') as f:
                reader = csv.DictReader(f)
                records = list(reader)
            
            print(f"Loaded {len(records)} records from {self.input_file}")
            
            # Process each record
            for i, record in enumerate(records, 1):
                if i % 10 == 0:
                    print(f"  Processing record {i}/{len(records)}...")
                
                result = self.process_record(record)
                if result:
                    successful_records.append(result)
            
            # Write output file
            if successful_records:
                with open(self.output_file, 'w') as f:
                    writer = csv.DictWriter(f, fieldnames=successful_records[0].keys())
                    writer.writeheader()
                    writer.writerows(successful_records)
            
            # Generate report
            self.generate_report()
            
            print(f"\nPipeline completed:")
            print(f"  Processed: {self.processed_count} records")
            print(f"  Failed: {self.error_count} records")
            print(f"  Success rate: {self.processed_count/(self.processed_count + self.error_count)*100:.1f}%")
            
            if self.error_count > 0:
                print(f"  Error details saved to pipeline_errors.json")
            
            return True
            
        except FileNotFoundError:
            print(f"Error: Input file '{self.input_file}' not found")
            return False
        except Exception as e:
            self.log_error('pipeline_run', e)
            print(f"Fatal pipeline error: {e}")
            return False
    
    def generate_report(self):
        """Generate error report."""
        if self.errors:
            with open('pipeline_errors.json', 'w') as f:
                json.dump(self.errors, f, indent=2)

# Create sample data for demonstration
print("Creating sample data for pipeline demonstration...")
sample_data = [
    {'id': 1, 'name': 'Alice Smith', 'amount': '1500.50'},
    {'id': 2, 'name': 'Bob Johnson', 'amount': '750.25'},
    {'id': 3, 'name': 'Charlie Brown', 'amount': '-100'},  # Invalid: negative amount
    {'id': 'four', 'name': 'Diana Prince', 'amount': '1200'},  # Valid: string id
    {'id': 5, 'name': 'Eve Davis', 'amount': 'not_a_number'},  # Invalid: non-numeric amount
    {'id': 6, 'name': 'Frank Wilson', 'amount': '800.75'},
    {'id': 7, 'name': 'Grace Lee', 'amount': '2000'},  # Will trigger random transformation error
]

with open('input_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'amount'])
    writer.writeheader()
    writer.writerows(sample_data)

print("Running data pipeline with error handling...")
pipeline = DataPipeline('input_data.csv', 'output_data.csv')
success = pipeline.run()

if success and pipeline.processed_count > 0:
    print("\nSample of processed data:")
    with open('output_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < 3:  # Show first 3 rows
                print(f"  {row}")
            else:
                break

# Clean up
import os
for file in ['input_data.csv', 'output_data.csv', 'pipeline_errors.json']:
    if os.path.exists(file):
        os.remove(file)

print("\nDemonstration complete!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Takeaways:
1. Use try/except blocks to handle runtime errors gracefully
2. Be specific about which exceptions you catch
3. Use finally for cleanup operations (closing files, connections)
4. Raise exceptions with informative error messages
5. Create custom exceptions for your application domain
6. Use else clause for code that should run only if no exception occurred
7. Don't use exceptions for normal flow control
8. Log exceptions before handling them
9. Use context managers for resource management
10. Consider error recovery strategies (retry, fallback, circuit breaker)

Error Handling Strategies:
- Fail fast: Detect errors early and fail immediately
- Graceful degradation: Continue with reduced functionality
- Retry with backoff: For transient errors (network, temporary failures)
- Circuit breaker: Stop trying after repeated failures
- Bulkhead: Isolate failures to prevent cascading

Next Steps:
- Practice with the exercises above
- Move to Tutorial 07: Modules and Imports
- Study Python's built-in exception hierarchy
- Explore logging module for production error logging
- Learn about testing with pytest and exception testing
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL 06")
print("=" * 60)