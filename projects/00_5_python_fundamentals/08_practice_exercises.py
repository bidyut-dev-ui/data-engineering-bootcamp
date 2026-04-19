"""
Tutorial 08: Practice Exercises - Applying Python Fundamentals

Learning Objectives:
- Apply all Python concepts from tutorials 1-7 in practical scenarios
- Solve real-world data engineering problems using Python
- Practice debugging and code optimization
- Build confidence through hands-on exercises

This tutorial contains 10 comprehensive exercises that combine multiple
Python concepts. Each exercise has a problem description, hints, and
a solution section (to be completed by the learner).
"""

import os
import json
import csv
import math
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional, Any

# ============================================================================
# EXERCISE 1: Data Cleaning and Validation
# ============================================================================
"""
Problem: You have a list of employee records with potential issues:
- Missing or empty values
- Invalid salary ranges
- Duplicate IDs
- Invalid date formats

Write a function to clean and validate the data.
"""

def exercise_1_data_cleaning():
    """Clean and validate employee data."""
    employees = [
        {"id": 101, "name": "Alice", "salary": "50000", "join_date": "2023-01-15"},
        {"id": 102, "name": "", "salary": "invalid", "join_date": "2023-02-30"},  # Invalid
        {"id": 103, "name": "Bob", "salary": "75000", "join_date": "2023-03-10"},
        {"id": 101, "name": "Alice Duplicate", "salary": "50000", "join_date": "2023-01-15"},  # Duplicate ID
        {"id": 104, "name": "Charlie", "salary": "-10000", "join_date": "2023-04-01"},  # Negative salary
        {"id": 105, "name": "Diana", "salary": "60000", "join_date": "15-04-2023"},  # Wrong date format
        {"id": 106, "name": "Eve", "salary": "120000", "join_date": "2023-05-20"},
    ]
    
    # TODO: Implement data cleaning
    # 1. Remove duplicates (keep first occurrence)
    # 2. Validate salary: must be positive integer between 30000 and 200000
    # 3. Validate join_date: must be in YYYY-MM-DD format and a valid date
    # 4. Remove records with empty names
    # 5. Return cleaned list and statistics
    
    cleaned = []
    stats = {
        "total_processed": 0,
        "duplicates_removed": 0,
        "invalid_salary": 0,
        "invalid_date": 0,
        "empty_name": 0,
        "final_count": 0
    }
    
    # Your implementation here
    seen_ids = set()
    
    for emp in employees:
        stats["total_processed"] += 1
        
        # Check for duplicate ID
        if emp["id"] in seen_ids:
            stats["duplicates_removed"] += 1
            continue
        
        # Check for empty name
        if not emp["name"] or emp["name"].strip() == "":
            stats["empty_name"] += 1
            continue
        
        # Validate salary
        try:
            salary = int(emp["salary"])
            if salary < 30000 or salary > 200000:
                stats["invalid_salary"] += 1
                continue
        except ValueError:
            stats["invalid_salary"] += 1
            continue
        
        # Validate date
        try:
            datetime.strptime(emp["join_date"], "%Y-%m-%d")
        except ValueError:
            stats["invalid_date"] += 1
            continue
        
        # All checks passed
        seen_ids.add(emp["id"])
        # Convert salary to integer
        emp["salary"] = salary
        cleaned.append(emp)
    
    stats["final_count"] = len(cleaned)
    return cleaned, stats

# ============================================================================
# EXERCISE 2: File Processing Pipeline
# ============================================================================
"""
Problem: Process a CSV file of sales data to:
1. Read the CSV file
2. Calculate total sales per product
3. Find the best-selling product
4. Write results to a JSON file
5. Generate a summary report
"""

def exercise_2_file_processing(input_file: str, output_json: str, report_file: str):
    """Process sales data from CSV."""
    # Sample data structure (create this file if it doesn't exist)
    sample_data = [
        ["product", "date", "quantity", "price"],
        ["Laptop", "2024-01-15", "2", "999.99"],
        ["Mouse", "2024-01-15", "5", "29.99"],
        ["Laptop", "2024-01-16", "1", "999.99"],
        ["Keyboard", "2024-01-16", "3", "79.99"],
        ["Mouse", "2024-01-17", "10", "29.99"],
        ["Monitor", "2024-01-17", "1", "299.99"],
    ]
    
    # Create sample file if it doesn't exist
    if not os.path.exists(input_file):
        with open(input_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        print(f"Created sample data file: {input_file}")
    
    # TODO: Implement the processing pipeline
    # 1. Read the CSV file
    # 2. Calculate total revenue per product (quantity * price)
    # 3. Find product with highest total revenue
    # 4. Write results to JSON file
    # 5. Generate a text report with summary statistics
    
    product_sales = defaultdict(float)
    total_revenue = 0.0
    total_items = 0
    
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    product = row['product']
                    quantity = int(row['quantity'])
                    price = float(row['price'])
                    
                    revenue = quantity * price
                    product_sales[product] += revenue
                    total_revenue += revenue
                    total_items += quantity
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skipping invalid row: {row} - Error: {e}")
                    continue
        
        # Find best selling product
        best_product = None
        best_revenue = 0.0
        
        for product, revenue in product_sales.items():
            if revenue > best_revenue:
                best_revenue = revenue
                best_product = product
        
        # Prepare results for JSON
        results = {
            "product_sales": {k: round(v, 2) for k, v in product_sales.items()},
            "summary": {
                "total_revenue": round(total_revenue, 2),
                "total_items_sold": total_items,
                "best_selling_product": best_product,
                "best_product_revenue": round(best_revenue, 2),
                "average_price_per_item": round(total_revenue / total_items, 2) if total_items > 0 else 0
            },
            "processing_date": datetime.now().isoformat()
        }
        
        # Write to JSON file
        with open(output_json, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Generate text report
        with open(report_file, 'w') as f:
            f.write("=" * 50 + "\n")
            f.write("SALES REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Product Sales Breakdown:\n")
            f.write("-" * 30 + "\n")
            for product, revenue in sorted(product_sales.items(), key=lambda x: x[1], reverse=True):
                f.write(f"{product:15} ${revenue:10.2f}\n")
            
            f.write("\nSummary Statistics:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Revenue:      ${total_revenue:10.2f}\n")
            f.write(f"Total Items Sold:   {total_items:10}\n")
            f.write(f"Best Selling:       {best_product}\n")
            f.write(f"Best Product Rev:   ${best_revenue:10.2f}\n")
            f.write(f"Avg Price/Item:     ${total_revenue/total_items if total_items > 0 else 0:10.2f}\n")
        
        print(f"Processing complete. Results saved to {output_json} and {report_file}")
        return results
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# ============================================================================
# EXERCISE 3: Function Composition and Decorators
# ============================================================================
"""
Problem: Create a pipeline of data transformations using function composition
and decorators for logging and validation.
"""

def exercise_3_function_pipeline():
    """Implement a data transformation pipeline."""
    
    # Decorator for logging function execution
    def log_execution(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            print(f"[LOG] Starting {func.__name__} at {start_time}")
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"[LOG] Completed {func.__name__} in {duration:.3f} seconds")
            return result
        return wrapper
    
    # Decorator for validating input data
    def validate_data(func):
        def wrapper(data):
            if not isinstance(data, list):
                raise TypeError("Input must be a list")
            if len(data) == 0:
                raise ValueError("Input list cannot be empty")
            if not all(isinstance(x, (int, float)) for x in data):
                raise ValueError("All elements must be numbers")
            return func(data)
        return wrapper
    
    # TODO: Implement the transformation functions with decorators
    
    @log_execution
    @validate_data
    def calculate_statistics(data: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of numbers."""
        if not data:
            return {}
        
        n = len(data)
        total = sum(data)
        mean = total / n
        
        # Calculate variance
        variance = sum((x - mean) ** 2 for x in data) / n
        
        # Calculate standard deviation
        std_dev = math.sqrt(variance)
        
        # Find min and max
        min_val = min(data)
        max_val = max(data)
        
        # Calculate median
        sorted_data = sorted(data)
        mid = n // 2
        if n % 2 == 0:
            median = (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            median = sorted_data[mid]
        
        return {
            "count": n,
            "sum": total,
            "mean": mean,
            "median": median,
            "variance": variance,
            "std_dev": std_dev,
            "min": min_val,
            "max": max_val,
            "range": max_val - min_val
        }
    
    @log_execution
    @validate_data
    def normalize_data(data: List[float]) -> List[float]:
        """Normalize data to range [0, 1]."""
        if not data:
            return []
        
        min_val = min(data)
        max_val = max(data)
        
        # Avoid division by zero
        if max_val == min_val:
            return [0.5] * len(data)
        
        return [(x - min_val) / (max_val - min_val) for x in data]
    
    @log_execution
    @validate_data
    def detect_outliers(data: List[float], threshold: float = 2.0) -> List[Tuple[int, float]]:
        """Detect outliers using standard deviation method."""
        if len(data) < 2:
            return []
        
        stats = calculate_statistics(data)
        mean = stats["mean"]
        std_dev = stats["std_dev"]
        
        outliers = []
        for i, value in enumerate(data):
            z_score = abs((value - mean) / std_dev) if std_dev > 0 else 0
            if z_score > threshold:
                outliers.append((i, value, z_score))
        
        return outliers
    
    # Test the pipeline
    test_data = [10.5, 12.3, 11.8, 13.1, 10.9, 50.0, 11.2, 9.8]  # 50.0 is an outlier
    
    print("\n" + "="*60)
    print("EXERCISE 3: Function Pipeline Test")
    print("="*60)
    
    try:
        # Calculate statistics
        stats = calculate_statistics(test_data)
        print(f"\nStatistics: {stats}")
        
        # Normalize data
        normalized = normalize_data(test_data)
        print(f"\nNormalized data (first 5): {normalized[:5]}")
        
        # Detect outliers
        outliers = detect_outliers(test_data, threshold=2.0)
        print(f"\nOutliers detected: {len(outliers)}")
        for idx, value, z_score in outliers:
            print(f"  Index {idx}: value={value}, z-score={z_score:.2f}")
        
        # Test error handling
        print("\nTesting error handling...")
        try:
            calculate_statistics("not a list")
        except TypeError as e:
            print(f"  Expected TypeError caught: {e}")
        
        try:
            calculate_statistics([])
        except ValueError as e:
            print(f"  Expected ValueError caught: {e}")
        
        return stats, normalized, outliers
        
    except Exception as e:
        print(f"Error in pipeline: {e}")
        return None

# ============================================================================
# EXERCISE 4: Class Design for Data Structures
# ============================================================================
"""
Problem: Design classes to represent a simple e-commerce system with
products, customers, and orders.
"""

def exercise_4_class_design():
    """Implement e-commerce system classes."""
    
    class Product:
        def __init__(self, product_id: int, name: str, price: float, category: str, stock: int = 0):
            self.product_id = product_id
            self.name = name
            self.price = price
            self.category = category
            self.stock = stock
        
        def __str__(self):
            return f"{self.name} (${self.price:.2f}) - {self.stock} in stock"
        
        def __repr__(self):
            return f"Product(id={self.product_id}, name='{self.name}', price={self.price})"
        
        def apply_discount(self, percent: float) -> float:
            """Apply discount and return new price."""
            if percent < 0 or percent > 100:
                raise ValueError("Discount must be between 0 and 100")
            discount = self.price * (percent / 100)
            return self.price - discount
        
        def update_stock(self, quantity: int) -> bool:
            """Update stock level. Return True if successful."""
            new_stock = self.stock + quantity
            if new_stock < 0:
                return False
            self.stock = new_stock
            return True
    
    class Customer:
        def __init__(self, customer_id: int, name: str, email: str):
            self.customer_id = customer_id
            self.name = name
            self.email = email
            self.orders = []
            self.total_spent = 0.0
        
        def __str__(self):
            return f"{self.name} ({self.email}) - {len(self.orders)} orders"
        
        def add_order(self, order: 'Order'):
            """Add an order to customer's history."""
            self.orders.append(order)
            self.total_spent += order.total_amount
        
        def get_order_history(self) -> List[Dict]:
            """Return order history as list of dictionaries."""
            return [
                {
                    "order_id": order.order_id,
                    "date": order.order_date,
                    "total": order.total_amount,
                    "items": len(order.items)
                }
                for order in self.orders
            ]
    
    class OrderItem:
        def __init__(self, product: Product, quantity: int):
            self.product = product
            self.quantity = quantity
            self.subtotal = product.price * quantity
        
        def __str__(self):
            return f"{self.quantity}x {self.product.name}: ${self.subtotal:.2f}"
    
    class Order:
        order_counter = 1000  # Class variable for generating order IDs
        
        def __init__(self, customer: Customer):
            self.order_id = Order.order_counter
            Order.order_counter += 1
            self.customer = customer
            self.order_date = datetime.now()
            self.items = []
            self.total_amount = 0.0
            self.status = "pending"
        
        def add_item(self, product: Product, quantity: int) -> bool:
            """Add item to order if product is in stock."""
            if quantity <= 0:
                return False
            
            if product.stock < quantity:
                print(f"Insufficient stock for {product.name}. Available: {product.stock}")
                return False
            
            # Update product stock
            if not product.update_stock(-quantity):
                return False
            
            # Add to order
            item = OrderItem(product, quantity)
            self.items.append(item)
            self.total_amount += item.subtotal
            return True
        
        def remove_item(self, product_id: int) -> bool:
            """Remove item from order and restore stock."""
            for i, item in enumerate(self.items):
                if item.product.product_id == product_id:
                    # Restore stock
                    item.product.update_stock(item.quantity)
                    
                    # Update total
                    self.total_amount -= item.subtotal
                    
                    # Remove item
                    self.items.pop(i)
                    return True
            return False
        
        def complete_order(self):
            """Mark order as completed and add to customer history."""
            if self.status == "completed":
                return False
            
            if len(self.items) == 0:
                print("Cannot complete empty order")
                return False
            
            self.status = "completed"
            self.customer.add_order(self)
            return True
        
        def get_receipt(self) -> str:
            """Generate receipt as string."""
            receipt = []
            receipt.append("=" * 50)
            receipt.append(f"ORDER #{self.order_id}")
            receipt.append(f"Date: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}")
            receipt.append(f"Customer: {self.customer.name}")
            receipt.append("-" * 50)
            
            for item in self.items:
                receipt.append(f"{item.quantity:3d} x {item.product.name:20} ${item.subtotal:8.2f}")
            
            receipt.append("-" * 50)
            receipt.append(f"TOTAL: ${self.total_amount:33.2f}")
            receipt.append(f"Status: {self.status}")
            receipt.append("=" * 50)
            
            return "\n".join(receipt)
    
    # TODO: Test the e-commerce system
    print("\n" + "="*60)
    print("EXERCISE 4: E-commerce System Test")
    print("="*60)
    
    # Create products
    laptop = Product(1, "Laptop", 999.99, "Electronics", 10)
    mouse = Product(2, "Wireless Mouse", 29.99, "Electronics", 50)
    keyboard = Product(3, "Mechanical Keyboard", 79.99, "Electronics", 25)
    
    # Create customer
    alice = Customer(101, "Alice Smith", "alice@example.com")
    
    # Create order
    order1 = Order(alice)
    
    # Add items to order
    print("\nAdding items to order...")
    print(f"Add laptop: {order1.add_item(laptop, 2)}")
    print(f"Add mouse: {order1.add_item(mouse, 3)}")
    print(f"Add keyboard: {order1.add_item(keyboard, 1)}")
    
    # Try to add item with insufficient stock
    print(f"Add more laptops (should fail): {order1.add_item(laptop, 20)}")
    
    # Print receipt
    print("\nOrder Receipt:")
    print(order1.get_receipt())
    
    # Complete order
    print(f"\nComplete order: {order1.complete_order()}")
    
    # Check customer history
    print(f"\nCustomer order history: {alice.get_order_history()}")
    print(f"Total spent by customer: ${alice.total_spent:.2f}")
    
    # Check updated stock
    print(f"\nUpdated stock levels:")
    print(f"  Laptop: {laptop.stock}")
    print(f"  Mouse: {mouse.stock}")
    print(f"  Keyboard: {keyboard.stock}")
    
    return {
        "products": [laptop, mouse, keyboard],
        "customer": alice,
        "order": order1
    }

# ============================================================================
# EXERCISE 5: Error Handling and Recovery
# ============================================================================
"""
Problem: Implement robust error handling for a data ingestion system
that reads from multiple sources and handles various failure scenarios.
"""

def exercise_5_error_handling():
    """Implement robust error handling for data ingestion."""
    
    class DataIngestionError(Exception):
        """Custom exception for data ingestion failures."""
        pass
    
    class DataSource:
        def __init__(self, name: str, requires_auth: bool = False):
            self.name = name
            self.requires_auth = requires_auth
            self.connection_attempts = 0
            self.max_attempts = 3
        
        def connect(self) -> bool:
            """Simulate connection attempt."""
            self.connection_attempts += 1
            
            # Simulate random failures
            import random
            if random.random() < 0.3:  # 30% chance of failure
                raise ConnectionError(f"Failed to connect to {self.name}")
            
            print(f"Connected to {self.name}")
            return True
        
        def fetch_data(self) -> List[Dict]:
            """Simulate data fetching."""
            # Simulate random data
            import random
            data = []
            for i in range(random.randint(1, 5)):
                data.append({
                    "id": i + 1,
                    "value": random.randint(10, 100),
                    "timestamp": datetime.now().isoformat()
                })
            
            # Simulate occasional data corruption
            if random.random() < 0.2:  # 20% chance of corruption
                data[0]["value"] = "invalid"
            
            return data
    
    class DataIngestor:
        def __init__(self):
            self.sources = []
            self.ingested_data = []
            self.failed_sources = []
        
        def add_source(self, source: DataSource):
            self.sources.append(source)
        
        def ingest_from_source(self, source: DataSource) -> Optional[List[Dict]]:
            """Ingest data from a single source with retry logic."""
            attempts = 0
            
            while attempts < source.max_attempts:
                try:
                    # Connect to source
                    source.connect()
                    
                    # Fetch data
                    raw_data = source.fetch_data()
                    
                    # Validate and clean data
                    cleaned_data = []
                    for item in raw_data:
                        try:
                            # Validate data structure
                            if not isinstance(item, dict):
                                raise ValueError("Item must be a dictionary")
                            
                            # Validate required fields
                            if "id" not in item or "value" not in item:
                                raise ValueError("Missing required fields")
                            
                            # Convert value to integer
                            item["value"] = int(item["value"])
                            
                            # Add source information
                            item["source"] = source.name
                            item["ingestion_time"] = datetime.now().isoformat()
                            
                            cleaned_data.append(item)
                            
                        except (ValueError, TypeError) as e:
                            print(f"  Warning: Skipping invalid item: {item} - Error: {e}")
                            continue
                    
                    return cleaned_data
                    
                except ConnectionError as e:
                    attempts += 1
                    print(f"  Connection attempt {attempts} failed: {e}")
                    if attempts >= source.max_attempts:
                        raise DataIngestionError(f"Failed to connect to {source.name} after {attempts} attempts")
                    
                except Exception as e:
                    raise DataIngestionError(f"Error ingesting from {source.name}: {e}")
            
            return None
        
        def ingest_all(self) -> Dict[str, Any]:
            """Ingest data from all sources with comprehensive error handling."""
            total_sources = len(self.sources)
            successful = 0
            failed = 0
            
            print(f"\nStarting ingestion from {total_sources} sources...")
            
            for source in self.sources:
                print(f"\nProcessing {source.name}...")
                
                try:
                    data = self.ingest_from_source(source)
                    if data:
                        self.ingested_data.extend(data)
                        successful += 1
                        print(f"  Successfully ingested {len(data)} records")
                    else:
                        failed += 1
                        self.failed_sources.append(source.name)
                        print(f"  Failed to ingest from {source.name}")
                
                except DataIngestionError as e:
                    failed += 1
                    self.failed_sources.append(source.name)
                    print(f"  Ingestion failed: {e}")
                
                except Exception as e:
                    failed += 1
                    self.failed_sources.append(source.name)
                    print(f"  Unexpected error: {e}")
            
            # Generate summary
            summary = {
                "total_sources": total_sources,
                "successful": successful,
                "failed": failed,
                "total_records": len(self.ingested_data),
                "failed_sources": self.failed_sources,
                "success_rate": (successful / total_sources * 100) if total_sources > 0 else 0,
                "ingestion_time": datetime.now().isoformat()
            }
            
            # Save summary to file
            try:
                with open("ingestion_summary.json", "w") as f:
                    json.dump(summary, f, indent=2)
                print(f"\nSummary saved to ingestion_summary.json")
            except IOError as e:
                print(f"\nWarning: Could not save summary: {e}")
            
            return summary
    
    # TODO: Test the error handling system
    print("\n" + "="*60)
    print("EXERCISE 5: Error Handling System Test")
    print("="*60)
    
    # Create data sources
    source1 = DataSource("API_1", requires_auth=True)
    source2 = DataSource("Database_1")
    source3 = DataSource("File_System")
    
    # Create ingestor
    ingestor = DataIngestor()
    ingestor.add_source(source1)
    ingestor.add_source(source2)
    ingestor.add_source(source3)
    
    # Run ingestion
    summary = ingestor.ingest_all()
    
    print(f"\nIngestion Summary:")
    print(f"  Total sources: {summary['total_sources']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Total records: {summary['total_records']}")
    print(f"  Success rate: {summary['success_rate']:.1f}%")
    
    if summary['failed_sources']:
        print(f"  Failed sources: {', '.join(summary['failed_sources'])}")
    
    # Display sample of ingested data
    if ingestor.ingested_data:
        print(f"\nSample of ingested data (first 3 records):")
        for i, record in enumerate(ingestor.ingested_data[:3]):
            print(f"  Record {i+1}: {record}")
    
    return summary

# ============================================================================
# EXERCISE 6: Algorithm Implementation
# ============================================================================
"""
Problem: Implement common algorithms used in data engineering:
1. Search algorithms
2. Sorting algorithms
3. Data compression (simple run-length encoding)
4. Data validation algorithms
"""

def exercise_6_algorithms():
    """Implement common data engineering algorithms."""
    
    # 1. Binary Search
    def binary_search(arr: List[int], target: int) -> Optional[int]:
        """Return index of target in sorted array, or None if not found."""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    
    # 2. Quick Sort
    def quick_sort(arr: List[Any]) -> List[Any]:
        """Implement quick sort algorithm."""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)
    
    # 3. Run-Length Encoding
    def run_length_encode(data: str) -> List[Tuple[str, int]]:
        """Compress string using run-length encoding."""
        if not data:
            return []
        
        encoded = []
        count = 1
        current_char = data[0]
        
        for char in data[1:]:
            if char == current_char:
                count += 1
            else:
                encoded.append((current_char, count))
                current_char = char
                count = 1
        
        encoded.append((current_char, count))
        return encoded
    
    def run_length_decode(encoded: List[Tuple[str, int]]) -> str:
        """Decode run-length encoded data."""
        return ''.join(char * count for char, count in encoded)
    
    # 4. Data Validation: Luhn Algorithm (credit card validation)
    def luhn_checksum(card_number: str) -> bool:
        """Validate credit card number using Luhn algorithm."""
        # Remove non-digit characters
        digits = [int(d) for d in card_number if d.isdigit()]
        
        if len(digits) < 2:
            return False
        
        # Double every second digit from the right
        total = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        
        return total % 10 == 0
    
    # 5. Find duplicates in large dataset (using hash set)
    def find_duplicates(data: List[Any], max_memory: int = 1000) -> List[Any]:
        """Find duplicates while respecting memory constraints."""
        if len(data) <= max_memory:
            # Simple approach for small datasets
            seen = set()
            duplicates = set()
            
            for item in data:
                if item in seen:
                    duplicates.add(item)
                else:
                    seen.add(item)
            
            return list(duplicates)
        else:
            # Chunked approach for large datasets
            duplicates = set()
            seen_chunk = set()
            
            for i in range(0, len(data), max_memory):
                chunk = data[i:i + max_memory]
                seen_chunk.clear()
                
                for item in chunk:
                    if item in seen_chunk:
                        duplicates.add(item)
                    else:
                        seen_chunk.add(item)
            
            return list(duplicates)
    
    # TODO: Test all algorithms
    print("\n" + "="*60)
    print("EXERCISE 6: Algorithms Test")
    print("="*60)
    
    # Test binary search
    sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11
    result_idx = binary_search(sorted_arr, target)
    print(f"\nBinary Search:")
    print(f"  Array: {sorted_arr}")
    print(f"  Target: {target}")
    print(f"  Found at index: {result_idx}")
    print(f"  Value at index: {sorted_arr[result_idx] if result_idx is not None else 'Not found'}")
    
    # Test quick sort
    unsorted_arr = [64, 34, 25, 12, 22, 11, 90, 5, 77, 88]
    sorted_result = quick_sort(unsorted_arr)
    print(f"\nQuick Sort:")
    print(f"  Original: {unsorted_arr}")
    print(f"  Sorted: {sorted_result}")
    print(f"  Is sorted: {sorted_result == sorted(unsorted_arr)}")
    
    # Test run-length encoding
    test_string = "AAAABBBCCDAA"
    encoded = run_length_encode(test_string)
    decoded = run_length_decode(encoded)
    print(f"\nRun-Length Encoding:")
    print(f"  Original: '{test_string}'")
    print(f"  Encoded: {encoded}")
    print(f"  Decoded: '{decoded}'")
    print(f"  Compression ratio: {len(test_string)} chars -> {len(encoded)} tuples")
    print(f"  Is lossless: {decoded == test_string}")
    
    # Test Luhn algorithm
    test_cards = [
        "4532015112830366",  # Valid Visa
        "6011000990139424",  # Valid Discover
        "1234567812345678",  # Invalid
        "4111111111111111",  # Valid (test number)
    ]
    
    print(f"\nLuhn Algorithm (Credit Card Validation):")
    for card in test_cards:
        is_valid = luhn_checksum(card)
        print(f"  {card}: {'Valid' if is_valid else 'Invalid'}")
    
    # Test duplicate finding
    large_data = list(range(1000)) + [42, 42, 999, 500, 500, 500, 123]
    duplicates = find_duplicates(large_data, max_memory=100)
    print(f"\nDuplicate Finding:")
    print(f"  Dataset size: {len(large_data)}")
    print(f"  Memory limit: 100 items per chunk")
    print(f"  Duplicates found: {duplicates}")
    print(f"  Count: {len(duplicates)} duplicates")
    
    return {
        "binary_search": result_idx,
        "quick_sort": sorted_result,
        "rle_encoded": encoded,
        "rle_decoded": decoded,
        "card_validation": [(card, luhn_checksum(card)) for card in test_cards],
        "duplicates": duplicates
    }

# ============================================================================
# EXERCISE 7: Module Integration
# ============================================================================
"""
Problem: Create a complete module that integrates multiple Python concepts
to solve a real-world data engineering problem.
"""

def exercise_7_module_integration():
    """Create an integrated data processing module."""
    
    # Import our own module functions (simulated)
    from datetime import datetime, timedelta
    import json
    import csv