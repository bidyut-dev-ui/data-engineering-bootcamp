"""
02_methods_and_decorators.py
Focus: Understanding @classmethod and @staticmethod in pipeline design.
"""

class DatabaseClient:
    # Class Variable: Shared across all instances (e.g., a default timeout)
    DEFAULT_TIMEOUT = 30

    def __init__(self, connection_string: str, timeout: int = None):
        self.connection_string = connection_string
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.is_connected = False

    # 1. Instance Method: Needs access to 'self' (the object's state)
    def connect(self):
        print(f"Connecting to {self.connection_string} with timeout {self.timeout}s...")
        self.is_connected = True

    # 2. Class Method: Accesses the Class (cls), not the instance.
    # Often used as a 'Factory' to create instances in different ways.
    @classmethod
    def from_config(cls, config_dict: dict):
        """Creates a DatabaseClient directly from a configuration dictionary."""
        print("Creating client from config dictionary...")
        conn_str = f"{config_dict['host']}:{config_dict['port']}"
        return cls(connection_string=conn_str, timeout=config_dict.get('timeout'))

    # 3. Static Method: Just a function that lives inside the class namespace.
    # Doesn't need 'self' or 'cls'. Used for utility functions related to the class.
    @staticmethod
    def validate_connection_string(conn_str: str):
        """Check if the string looks valid before even trying to connect."""
        return ":" in conn_str and len(conn_str) > 5

# --- Execution ---
if __name__ == "__main__":
    # Standard initialization
    client1 = DatabaseClient("localhost:5432")
    
    # Factory initialization (Very common in Airflow/Production code)
    config = {"host": "prod-db", "port": 5432, "timeout": 60}
    client2 = DatabaseClient.from_config(config)

    # Static utility usage
    is_valid = DatabaseClient.validate_connection_string("localhost:5432")
    print(f"Is 'localhost:5432' valid? {is_valid}")

    client2.connect()

    # Key Takeaway for DE:
    # Use @classmethod for "alternative constructors" (e.g., from_json, from_env).
    # Use @staticmethod for logic that belongs to the class concept but doesn't touch data.
