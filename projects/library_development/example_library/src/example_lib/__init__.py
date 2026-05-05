"""
Example Library - A comprehensive Python library demonstrating modern packaging and development practices.

This library provides example implementations of common patterns and utilities
for educational purposes in the Data Engineering Bootcamp.
"""

__version__ = "0.1.0"
__author__ = "Data Engineering Bootcamp"
__email__ = "bootcamp@example.com"

# Core exports
from .core import (
    DataProcessor,
    ConfigManager,
    Cache,
    retry,
    timeout,
    validate_input,
    transform_data,
    batch_process,
)

# Utility exports
from .utils import (
    format_size,
    human_readable_time,
    generate_id,
    slugify,
    chunk_list,
    flatten_dict,
    safe_parse_json,
    safe_parse_yaml,
)

# Exception exports
from .exceptions import (
    ExampleLibError,
    ConfigurationError,
    ValidationError,
    ProcessingError,
    TimeoutError,
    RetryExhaustedError,
)

# Plugin system exports
from .plugins import (
    Plugin,
    PluginManager,
    register_plugin,
    get_plugin,
    list_plugins,
)

# CLI exports (if available)
try:
    from .cli import main
except ImportError:
    # CLI might not be available if click isn't installed
    pass

# Pytest plugin exports (if available)
try:
    from .pytest_plugin import pytest_configure, pytest_addoption
except ImportError:
    # Pytest plugin might not be available
    pass

__all__ = [
    # Core
    "DataProcessor",
    "ConfigManager",
    "Cache",
    "retry",
    "timeout",
    "validate_input",
    "transform_data",
    "batch_process",
    
    # Utils
    "format_size",
    "human_readable_time",
    "generate_id",
    "slugify",
    "chunk_list",
    "flatten_dict",
    "safe_parse_json",
    "safe_parse_yaml",
    
    # Exceptions
    "ExampleLibError",
    "ConfigurationError",
    "ValidationError",
    "ProcessingError",
    "TimeoutError",
    "RetryExhaustedError",
    
    # Plugins
    "Plugin",
    "PluginManager",
    "register_plugin",
    "get_plugin",
    "list_plugins",
    
    # Version
    "__version__",
    "__author__",
    "__email__",
]