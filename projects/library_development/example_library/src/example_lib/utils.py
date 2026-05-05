"""
Utility functions for the example library.

This module demonstrates:
1. Common utility patterns
2. String manipulation
3. Data transformation
4. File and path handling
5. Safe parsing and validation
"""

import re
import json
import hashlib
import uuid
import time
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timedelta
import inspect


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1
    
    return f"{size_bytes:.2f} {units[unit_index]}"


def human_readable_time(seconds: float) -> str:
    """
    Format time duration in human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Human-readable time string (e.g., "2h 30m 15s")
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)


def generate_id(prefix: str = "", length: int = 8) -> str:
    """
    Generate a unique identifier.
    
    Args:
        prefix: Optional prefix for the ID
        length: Length of the random part
        
    Returns:
        Unique identifier string
    """
    random_part = uuid.uuid4().hex[:length]
    if prefix:
        return f"{prefix}_{random_part}"
    return random_part


def slugify(text: str, separator: str = "_", max_length: int = 50) -> str:
    """
    Convert text to a URL-friendly slug.
    
    Args:
        text: Text to convert
        separator: Word separator
        max_length: Maximum length of the slug
        
    Returns:
        Slugified string
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace non-alphanumeric characters with separator
    text = re.sub(r'[^a-z0-9]+', separator, text)
    
    # Remove leading/trailing separators
    text = text.strip(separator)
    
    # Truncate to max length
    if len(text) > max_length:
        # Try to truncate at a separator
        truncated = text[:max_length]
        last_separator = truncated.rfind(separator)
        if last_separator > 0:
            text = truncated[:last_separator]
        else:
            text = truncated
    
    return text


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_dict(nested_dict: Dict[str, Any], separator: str = ".", prefix: str = "") -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        nested_dict: Dictionary to flatten
        separator: Separator for nested keys
        prefix: Prefix for keys (used internally for recursion)
        
    Returns:
        Flattened dictionary
    """
    flattened = {}
    
    for key, value in nested_dict.items():
        full_key = f"{prefix}{separator}{key}" if prefix else key
        
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, separator, full_key))
        elif isinstance(value, list):
            # Handle lists by converting to indexed keys
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened.update(flatten_dict(item, separator, f"{full_key}[{i}]"))
                else:
                    flattened[f"{full_key}[{i}]"] = item
        else:
            flattened[full_key] = value
    
    return flattened


def safe_parse_json(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string, returning default on error.
    
    Args:
        json_string: JSON string to parse
        default: Value to return on parsing error
        
    Returns:
        Parsed JSON object or default
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_parse_yaml(yaml_string: str, default: Any = None) -> Any:
    """
    Safely parse YAML string, returning default on error.
    
    Args:
        yaml_string: YAML string to parse
        default: Value to return on parsing error
        
    Returns:
        Parsed YAML object or default
    """
    try:
        import yaml
        return yaml.safe_load(yaml_string)
    except (yaml.YAMLError, ImportError, TypeError):
        return default


def get_file_hash(file_path: Union[str, Path], algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use
        
    Returns:
        Hexadecimal hash string
    """
    file_path = Path(file_path)
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Normalize a path, expanding user and resolving.
    
    Args:
        path: Path to normalize
        
    Returns:
        Normalized Path object
    """
    path = Path(path).expanduser().resolve()
    return path


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
    """
    directory = normalize_path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def timeit(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function that prints execution time
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper


def memoize(func: Callable) -> Callable:
    """
    Simple memoization decorator.
    
    Args:
        func: Function to memoize
        
    Returns:
        Memoized function
    """
    cache = {}
    
    def wrapper(*args, **kwargs):
        # Create a cache key from args and kwargs
        key = (args, frozenset(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL format is valid
    """
    pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[-\w.%?=&]*)?$'
    return bool(re.match(pattern, url))


def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including ellipsis
        ellipsis: Ellipsis string to append
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= len(ellipsis):
        return ellipsis[:max_length]
    
    return text[:max_length - len(ellipsis)] + ellipsis


def get_function_signature(func: Callable) -> str:
    """
    Get function signature as string.
    
    Args:
        func: Function to inspect
        
    Returns:
        Function signature string
    """
    try:
        sig = inspect.signature(func)
        return str(sig)
    except (ValueError, TypeError):
        return "()"


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def filter_dict(dictionary: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Filter dictionary to include only specified keys.
    
    Args:
        dictionary: Dictionary to filter
        keys: Keys to include
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in dictionary.items() if k in keys}


def exclude_dict(dictionary: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Filter dictionary to exclude specified keys.
    
    Args:
        dictionary: Dictionary to filter
        keys: Keys to exclude
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in dictionary.items() if k not in keys}


def to_bool(value: Any) -> bool:
    """
    Convert value to boolean.
    
    Args:
        value: Value to convert
        
    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value_lower = value.lower()
        if value_lower in ('true', 'yes', '1', 'on', 't'):
            return True
        if value_lower in ('false', 'no', '0', 'off', 'f'):
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    
    raise ValueError(f"Cannot convert {value} to boolean")


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object as string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Parse datetime string.
    
    Args:
        datetime_str: Datetime string
        format_str: Format string
        
    Returns:
        Datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(datetime_str, format_str)
    except (ValueError, TypeError):
        return None