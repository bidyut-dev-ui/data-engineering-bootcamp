"""
Pytest plugin for the example library.

This module demonstrates:
1. Creating pytest plugins
2. Adding custom command-line options
3. Implementing custom fixtures
4. Adding custom markers
5. Integrating with test discovery
"""

import pytest
import tempfile
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Generator

from .core import DataProcessor, ConfigManager, Cache
from .exceptions import ExampleLibError


def pytest_addoption(parser):
    """
    Add command-line options for the example library plugin.
    
    This function is called by pytest to add custom command-line options.
    """
    group = parser.getgroup("example-lib", "Example Library testing options")
    
    group.addoption(
        "--example-lib-config",
        action="store",
        default=None,
        help="Path to example library configuration file"
    )
    
    group.addoption(
        "--example-lib-cache-size",
        action="store",
        type=int,
        default=100,
        help="Cache size for example library tests"
    )
    
    group.addoption(
        "--example-lib-debug",
        action="store_true",
        default=False,
        help="Enable debug mode for example library tests"
    )


def pytest_configure(config):
    """
    Configure pytest with example library plugin.
    
    This function is called by pytest to configure the plugin.
    """
    # Add custom markers
    config.addinivalue_line(
        "markers",
        "example_lib: mark test as using example library features"
    )
    
    config.addinivalue_line(
        "markers",
        "example_lib_slow: mark test as slow (requires special handling)"
    )
    
    config.addinivalue_line(
        "markers",
        "example_lib_integration: mark test as integration test"
    )
    
    # Store plugin configuration
    config.example_lib_config = {
        'config_file': config.getoption("--example-lib-config"),
        'cache_size': config.getoption("--example-lib-cache-size"),
        'debug': config.getoption("--example-lib-debug"),
    }
    
    if config.example_lib_config['debug']:
        print(f"Example Library Plugin configured: {config.example_lib_config}")


@pytest.fixture(scope="session")
def example_lib_config(pytestconfig) -> Dict[str, Any]:
    """
    Provide example library configuration.
    
    This fixture provides the plugin configuration to tests.
    """
    return pytestconfig.example_lib_config


@pytest.fixture
def temp_config_file() -> Generator[Path, None, None]:
    """
    Create a temporary configuration file for testing.
    
    This fixture creates a temporary JSON configuration file
    and cleans it up after the test.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config = {
            'test': {
                'enabled': True,
                'timeout': 30,
                'retries': 3,
            },
            'logging': {
                'level': 'INFO',
                'format': 'json',
            }
        }
        json.dump(config, f, indent=2)
        temp_file = Path(f.name)
    
    yield temp_file
    
    # Cleanup
    if temp_file.exists():
        temp_file.unlink()


@pytest.fixture
def config_manager(temp_config_file: Path) -> ConfigManager:
    """
    Provide a ConfigManager instance for testing.
    
    This fixture creates a ConfigManager with a temporary
    configuration file.
    """
    return ConfigManager(temp_config_file)


@pytest.fixture
def data_processor() -> DataProcessor:
    """
    Provide a DataProcessor instance for testing.
    
    This fixture creates a DataProcessor with default configuration.
    """
    return DataProcessor()


@pytest.fixture
def cache(example_lib_config: Dict[str, Any]) -> Cache:
    """
    Provide a Cache instance for testing.
    
    This fixture creates a Cache with configurable size.
    """
    cache_size = example_lib_config.get('cache_size', 100)
    return Cache(max_size=cache_size)


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Provide sample data for testing.
    
    This fixture provides a dictionary of sample data that
    can be used in tests.
    """
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25},
            {'id': 3, 'name': 'Charlie', 'age': 35},
        ],
        'products': [
            {'id': 101, 'name': 'Laptop', 'price': 999.99},
            {'id': 102, 'name': 'Mouse', 'price': 29.99},
            {'id': 103, 'name': 'Keyboard', 'price': 79.99},
        ],
        'metadata': {
            'timestamp': '2024-01-01T12:00:00Z',
            'version': '1.0.0',
            'source': 'test',
        }
    }


@pytest.fixture
def sample_yaml_data() -> str:
    """
    Provide sample YAML data for testing.
    
    This fixture provides a YAML string that can be used
    for parsing tests.
    """
    return """
database:
  host: localhost
  port: 5432
  name: test_db
  credentials:
    username: admin
    password: secret

logging:
  level: DEBUG
  handlers:
    - console
    - file

features:
  enabled:
    - caching
    - validation
    - monitoring
  disabled:
    - analytics
"""


@pytest.fixture
def sample_json_data() -> str:
    """
    Provide sample JSON data for testing.
    
    This fixture provides a JSON string that can be used
    for parsing tests.
    """
    return json.dumps({
        "project": {
            "name": "Example Library",
            "version": "1.0.0",
            "authors": ["Alice", "Bob"],
            "dependencies": {
                "required": ["click>=8.0.0", "pyyaml>=6.0"],
                "optional": ["pytest>=7.0.0", "black>=22.0.0"]
            }
        },
        "settings": {
            "debug": False,
            "timeout": 30,
            "retries": 3
        }
    }, indent=2)


# Custom assertions for example library

class ExampleLibAssertions:
    """
    Custom assertion helpers for example library tests.
    
    This class provides assertion methods that can be used
    in tests to validate example library behavior.
    """
    
    @staticmethod
    def assert_valid_config(config: Dict[str, Any], required_keys: list = None):
        """
        Assert that a configuration dictionary is valid.
        
        Args:
            config: Configuration dictionary to validate
            required_keys: List of required keys (optional)
        """
        assert isinstance(config, dict), "Config must be a dictionary"
        assert len(config) > 0, "Config must not be empty"
        
        if required_keys:
            for key in required_keys:
                assert key in config, f"Config missing required key: {key}"
    
    @staticmethod
    def assert_data_processed(processor: DataProcessor, data: Any):
        """
        Assert that data can be processed successfully.
        
        Args:
            processor: DataProcessor instance
            data: Data to process
        """
        try:
            result = processor.process(data)
            assert result is not None, "Processing should return a result"
            return result
        except ExampleLibError as e:
            pytest.fail(f"Data processing failed: {e}")
    
    @staticmethod
    def assert_cache_behavior(cache: Cache, key: str, value: Any, ttl: int = 60):
        """
        Assert cache set/get behavior.
        
        Args:
            cache: Cache instance
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        # Set value
        cache.set(key, value, ttl)
        
        # Get value (should exist)
        cached_value = cache.get(key)
        assert cached_value == value, f"Cache get returned wrong value: {cached_value}"
        
        # Get non-existent key
        non_existent = cache.get("non_existent_key")
        assert non_existent is None, "Non-existent key should return None"
        
        # Delete key
        deleted = cache.delete(key)
        assert deleted, "Delete should return True for existing key"
        
        # Verify deleted
        deleted_value = cache.get(key)
        assert deleted_value is None, "Deleted key should return None"


@pytest.fixture
def example_lib_assert():
    """
    Provide ExampleLibAssertions instance for testing.
    
    This fixture provides an instance of ExampleLibAssertions
    that can be used in tests.
    """
    return ExampleLibAssertions()


# Custom hooks for test lifecycle

def pytest_collection_modifyitems(config, items):
    """
    Modify collected test items based on example library configuration.
    
    This hook can be used to skip or modify tests based on
    plugin configuration.
    """
    debug_mode = config.example_lib_config.get('debug', False)
    
    for item in items:
        # Skip slow tests unless in debug mode
        if "example_lib_slow" in item.keywords and not debug_mode:
            item.add_marker(pytest.mark.skip(reason="Slow test skipped in non-debug mode"))
        
        # Add custom attribute for tracking
        item.example_lib_tested = False


def pytest_runtest_setup(item):
    """
    Setup hook for each test.
    
    This hook is called before each test runs.
    """
    if "example_lib" in item.keywords:
        # Example library specific setup
        print(f"Running example library test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """
    Teardown hook for each test.
    
    This hook is called after each test runs.
    """
    if "example_lib" in item.keywords:
        # Example library specific teardown
        print(f"Completed example library test: {item.name}")


# Custom reporting

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Add custom summary to terminal output.
    
    This hook adds example library specific information
    to the test summary.
    """
    example_lib_tests = []
    for item in terminalreporter.stats.get('passed', []):
        if "example_lib" in item.keywords:
            example_lib_tests.append(item)
    
    for item in terminalreporter.stats.get('failed', []):
        if "example_lib" in item.keywords:
            example_lib_tests.append(item)
    
    if example_lib_tests:
        terminalreporter.write_sep("=", "Example Library Test Summary")
        terminalreporter.write_line(f"Total example library tests: {len(example_lib_tests)}")
        
        passed = sum(1 for item in example_lib_tests if item in terminalreporter.stats.get('passed', []))
        failed = sum(1 for item in example_lib_tests if item in terminalreporter.stats.get('failed', []))
        
        terminalreporter.write_line(f"Passed: {passed}, Failed: {failed}")
        
        if config.example_lib_config.get('debug', False):
            terminalreporter.write_line("Debug mode: Enabled")


# Plugin metadata (for pytest discovery)
__version__ = "1.0.0"
__author__ = "Example Library Team"
__description__ = "Pytest plugin for Example Library testing"