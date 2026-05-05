"""
practice_exercises.py
Object-Oriented Python for Data Engineering
"""

# Exercise 1: The Configurable Pipeline
# -----------------------------------
# Create a class 'PipelineConfig' that stores 'batch_size', 'retries', and 'env'.
# Use a @classmethod 'production_config()' that returns a config with 
# batch_size=1000, retries=5, and env='prod'.

class PipelineConfig:
    def __init__(self, batch_size: int, retries: int, env: str):
        self.batch_size = batch_size
        self.retries = retries
        self.env = env

    @classmethod
    def production_config(cls):
        """Factory method for production environment."""
        return cls(batch_size=1000, retries=5, env='prod')


# Exercise 2: The Reusable Database Client (ABC Challenge)
# ------------------------------------------------------
# 1. Create an Abstract Base Class 'BaseClient'.
# 2. Define two @abstractmethods: 'execute_query(query)' and 'close_connection()'.
# 3. Implement a class 'MySQLClient' that inherits from BaseClient.
# 4. Implement a class 'SnowflakeClient' that inherits from BaseClient.
# 5. Write a function 'run_job(client)' that takes ANY BaseClient and runs a test query.

from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def execute_query(self, query: str):
        pass

    @abstractmethod
    def close_connection(self):
        pass

class MySQLClient(BaseClient):
    def execute_query(self, query: str):
        print(f"Executing MySQL query: {query}")
        return [{"row": 1}]

    def close_connection(self):
        print("Closing MySQL connection.")

class SnowflakeClient(BaseClient):
    def execute_query(self, query: str):
        print(f"Executing Snowflake query: {query}")
        return [{"row": 100}]

    def close_connection(self):
        print("Closing Snowflake connection.")

def run_job(client: BaseClient):
    """Polymorphic function that works with any client."""
    print(f"\n--- Running Job with {type(client).__name__} ---")
    data = client.execute_query("SELECT * FROM users")
    print(f"Result: {data}")
    client.close_connection()


# --- Test Your Implementation ---
if __name__ == "__main__":
    print("--- Exercise 1: Config ---")
    prod = PipelineConfig.production_config()
    print(f"Env: {prod.env}, Batch: {prod.batch_size}")

    print("\n--- Exercise 2: ABC & Polymorphism ---")
    mysql = MySQLClient()
    snowflake = SnowflakeClient()

    run_job(mysql)
    run_job(snowflake)
