"""
01_classes_and_objects.py
Focus: Encapsulation and managing state in a data pipeline.
"""

class DataProcessor:
    """
    A simple class to encapsulate a data processing task.
    Instead of passing a filename through 10 functions, we store it as state.
    """
    
    def __init__(self, source_name: str):
        # Instance Variable: Unique to each instance of the class
        self.source_name = source_name
        self.processed_count = 0
        self.is_active = True
        print(f"Initializing Processor for: {self.source_name}")

    def process_record(self, record: dict):
        """Instance Method: Can access and modify the instance's state."""
        if not self.is_active:
            print("Processor is inactive.")
            return

        # Simulate processing logic
        print(f"Processing record from {self.source_name}: {record}")
        self.processed_count += 1

    def get_summary(self):
        """Returns the current state of this specific processor."""
        return {
            "source": self.source_name,
            "records_processed": self.processed_count,
            "status": "Active" if self.is_active else "Inactive"
        }

# --- Execution ---
if __name__ == "__main__":
    # Create two different instances (Objects)
    # They share the same logic (Class) but have different state (Data)
    user_processor = DataProcessor("users_table")
    order_processor = DataProcessor("orders_csv")

    user_processor.process_record({"id": 1, "name": "Alice"})
    user_processor.process_record({"id": 2, "name": "Bob"})
    
    order_processor.process_record({"id": 101, "amount": 50.0})

    print("\n--- Summary Report ---")
    print(user_processor.get_summary())
    print(order_processor.get_summary())

    # Key Takeaway for DE:
    # Classes help you avoid "Global Variable Hell" in complex pipelines.
    # Each 'DataProcessor' maintains its own count and status.
