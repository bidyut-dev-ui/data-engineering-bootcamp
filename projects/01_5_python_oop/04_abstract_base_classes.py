"""
04_abstract_base_classes.py
Focus: Enforcing data contracts using the 'abc' module.
"""

from abc import ABC, abstractmethod

class BaseDataSink(ABC):
    """
    Abstract Base Class (ABC)
    Acts as a 'Template' or 'Interface'. 
    You cannot instantiate this class directly.
    """
    
    @abstractmethod
    def save(self, data: dict):
        """Every child MUST implement this method, or they won't run."""
        pass

    @abstractmethod
    def get_status(self):
        pass

class PostgresSink(BaseDataSink):
    """A concrete implementation of the BaseDataSink."""
    def save(self, data: dict):
        print(f"Saving to Postgres: {data}")

    def get_status(self):
        return "Connected to Postgres"

class S3Sink(BaseDataSink):
    """Another concrete implementation."""
    def save(self, data: dict):
        print(f"Uploading to S3 bucket: {data}")

    def get_status(self):
        return "S3 Bucket Accessible"

# --- Execution ---
if __name__ == "__main__":
    # This would RAISE AN ERROR:
    # try:
    #     base = BaseDataSink()
    # except TypeError as e:
    #     print(f"Error: {e}")

    sinks = [PostgresSink(), S3Sink()]

    for sink in sinks:
        print(f"Current Sink: {sink.get_status()}")
        sink.save({"id": 1, "value": "test_data"})

    # Key Takeaway for DE:
    # Use ABCs to define "Standards" for your team. 
    # If a new engineer needs to add a 'SnowflakeSink', they must follow your save/status interface.
    # This makes your main pipeline code generic and robust.
