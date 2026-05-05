"""
Core functionality for the example library.

This module demonstrates:
1. Class design with proper typing and documentation
2. Decorator patterns for common functionality
3. Context manager implementation
4. Error handling and validation
5. Configuration management
"""

import time
import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps
from contextlib import contextmanager
import threading
from pathlib import Path

from .exceptions import (
    ExampleLibError,
    ConfigurationError,
    ValidationError,
    ProcessingError,
    TimeoutError,
    RetryExhaustedError,
)

# Type variables for generic functions
T = TypeVar('T')
R = TypeVar('R')

# Configure logging
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    A generic data processor that demonstrates class design patterns.
    
    Features:
    - Configurable processing pipeline
    - Validation hooks
    - Error handling with retries
    - Progress tracking
    - Batch processing
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data processor.
        
        Args:
            config: Configuration dictionary with processing options
        """
        self.config = config or {}
        self._validation_hooks: List[Callable] = []
        self._processing_hooks: List[Callable] = []
        self._error_hooks: List[Callable] = []
        self._stats = {
            'processed': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None,
        }
    
    def add_validation_hook(self, hook: Callable) -> None:
        """Add a validation hook to be called before processing."""
        self._validation_hooks.append(hook)
    
    def add_processing_hook(self, hook: Callable) -> None:
        """Add a processing hook to be called during processing."""
        self._processing_hooks.append(hook)
    
    def add_error_hook(self, hook: Callable) -> None:
        """Add an error hook to be called when errors occur."""
        self._error_hooks.append(hook)
    
    def validate(self, data: Any) -> bool:
        """
        Validate data using all registered validation hooks.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes, False otherwise
            
        Raises:
            ValidationError: If validation fails and error hooks are configured
        """
        for hook in self._validation_hooks:
            try:
                if not hook(data):
                    if self._error_hooks:
                        raise ValidationError(f"Validation failed: {hook.__name__}")
                    return False
            except Exception as e:
                logger.warning(f"Validation hook {hook.__name__} raised exception: {e}")
                if self._error_hooks:
                    raise ValidationError(f"Validation hook error: {e}")
                return False
        return True
    
    def process(self, data: Any) -> Any:
        """
        Process data with error handling and hooks.
        
        Args:
            data: Data to process
            
        Returns:
            Processed data
            
        Raises:
            ProcessingError: If processing fails
        """
        self._stats['start_time'] = time.time()
        
        try:
            # Validate data
            if not self.validate(data):
                raise ValidationError("Data validation failed")
            
            # Apply processing hooks
            result = data
            for hook in self._processing_hooks:
                result = hook(result)
            
            # Update stats
            self._stats['processed'] += 1
            
            return result
            
        except Exception as e:
            self._stats['errors'] += 1
            logger.error(f"Processing error: {e}")
            
            # Call error hooks
            for hook in self._error_hooks:
                try:
                    hook(e, data)
                except Exception as hook_error:
                    logger.error(f"Error hook failed: {hook_error}")
            
            raise ProcessingError(f"Failed to process data: {e}") from e
        
        finally:
            self._stats['end_time'] = time.time()
    
    def batch_process(self, data_list: List[Any]) -> List[Any]:
        """
        Process a batch of data items.
        
        Args:
            data_list: List of data items to process
            
        Returns:
            List of processed items
        """
        results = []
        for i, data in enumerate(data_list):
            try:
                result = self.process(data)
                results.append(result)
            except ProcessingError as e:
                logger.warning(f"Failed to process item {i}: {e}")
                # Optionally add None or continue based on config
                if self.config.get('skip_errors', False):
                    continue
                else:
                    raise
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        stats = self._stats.copy()
        if stats['start_time'] and stats['end_time']:
            stats['duration'] = stats['end_time'] - stats['start_time']
            if stats['processed'] > 0:
                stats['avg_time_per_item'] = stats['duration'] / stats['processed']
        return stats


class ConfigManager:
    """
    Configuration manager with file watching and validation.
    
    Features:
    - Multiple configuration sources (file, environment, defaults)
    - Type validation and conversion
    - File watching for automatic reload
    - Hierarchical configuration with overrides
    """
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (JSON or YAML)
        """
        self.config_file = Path(config_file) if config_file else None
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = {}
        self._validators: Dict[str, Callable] = {}
        self._watcher_thread: Optional[threading.Thread] = None
        self._stop_watching = threading.Event()
        
        # Load initial configuration
        self.reload()
    
    def set_default(self, key: str, value: Any) -> None:
        """Set a default value for a configuration key."""
        self._defaults[key] = value
    
    def set_validator(self, key: str, validator: Callable) -> None:
        """Set a validator function for a configuration key."""
        self._validators[key] = validator
    
    def reload(self) -> None:
        """Reload configuration from all sources."""
        config = {}
        
        # 1. Load defaults
        config.update(self._defaults)
        
        # 2. Load from file if exists
        if self.config_file and self.config_file.exists():
            try:
                file_content = self.config_file.read_text()
                if self.config_file.suffix.lower() == '.json':
                    file_config = json.loads(file_content)
                elif self.config_file.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    file_config = yaml.safe_load(file_content)
                else:
                    raise ConfigurationError(f"Unsupported config file format: {self.config_file.suffix}")
                
                config.update(file_config)
            except Exception as e:
                raise ConfigurationError(f"Failed to load config file: {e}") from e
        
        # 3. Load from environment variables
        import os
        for key in self._defaults.keys():
            env_key = key.upper().replace('.', '_')
            if env_key in os.environ:
                # Try to parse the value based on default type
                default_value = self._defaults[key]
                env_value = os.environ[env_key]
                
                if isinstance(default_value, bool):
                    # Handle boolean values
                    config[key] = env_value.lower() in ('true', '1', 'yes', 'on')
                elif isinstance(default_value, int):
                    config[key] = int(env_value)
                elif isinstance(default_value, float):
                    config[key] = float(env_value)
                elif isinstance(default_value, list):
                    # Parse comma-separated lists
                    config[key] = [item.strip() for item in env_value.split(',')]
                else:
                    config[key] = env_value
        
        # 4. Validate configuration
        self._validate_config(config)
        
        # 5. Update internal config
        self._config = config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration using registered validators."""
        for key, validator in self._validators.items():
            if key in config:
                try:
                    if not validator(config[key]):
                        raise ValidationError(f"Validation failed for key: {key}")
                except Exception as e:
                    raise ValidationError(f"Validator error for key {key}: {e}") from e
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        # Support dot notation for nested keys
        if '.' in key:
            parts = key.split('.')
            value = self._config
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value
        else:
            return self._config.get(key, default)
    
    def start_watching(self, interval: int = 5) -> None:
        """
        Start watching configuration file for changes.
        
        Args:
            interval: Check interval in seconds
        """
        if not self.config_file:
            raise ConfigurationError("No config file specified for watching")
        
        def watch_loop():
            last_mtime = self.config_file.stat().st_mtime if self.config_file.exists() else 0
            
            while not self._stop_watching.is_set():
                time.sleep(interval)
                
                if self.config_file.exists():
                    current_mtime = self.config_file.stat().st_mtime
                    if current_mtime > last_mtime:
                        logger.info(f"Config file changed, reloading...")
                        try:
                            self.reload()
                            last_mtime = current_mtime
                        except Exception as e:
                            logger.error(f"Failed to reload config: {e}")
        
        self._watcher_thread = threading.Thread(target=watch_loop, daemon=True)
        self._watcher_thread.start()
    
    def stop_watching(self) -> None:
        """Stop watching configuration file."""
        self._stop_watching.set()
        if self._watcher_thread:
            self._watcher_thread.join(timeout=2.0)


class Cache(Generic[T]):
    """
    A simple caching implementation with TTL and size limits.
    
    Features:
    - Time-based expiration (TTL)
    - Size-based eviction (LRU)
    - Thread-safe operations
    - Statistics tracking
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0,
        }
    
    def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            # Evict if needed
            if len(self._cache) >= self.max_size:
                self._evict_oldest()
            
            expiration = time.time() + (ttl or self.default_ttl)
            self._cache[key] = {
                'value': value,
                'expiration': expiration,
                'access_time': time.time(),
            }
            self._stats['size'] = len(self._cache)
    
    def get(self, key: str, default: Any = None) -> Optional[T]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            default: Default value if key not found or expired
            
        Returns:
            Cached value or default
        """
        with self._lock:
            if key not in self._cache:
                self._stats['misses'] += 1
                return default
            
            item = self._cache[key]
            
            # Check expiration
            if time.time() > item['expiration']:
                del self._cache[key]
                self._stats['misses'] += 1
                self._stats['size'] = len(self._cache)
                return default
            
            # Update access time for LRU
            item['access_time'] = time.time()
            self._stats['hits'] += 1
            return item['value']
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats['size'] = len(self._cache)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all items from cache."""
        with self._lock:
            self._cache.clear()
            self._stats['size'] = 0
    
    def _evict_oldest(self) -> None:
        """Evict the least recently used item."""
        if not self._cache:
            return
        
        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['access_time'])
        del self._cache[oldest_key]
        self._stats['evictions'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = self._stats.copy()
        if stats['hits'] + stats['misses'] > 0:
            stats['hit_rate'] = stats['hits'] / (stats['hits'] + stats['misses'])
        return stats


# Decorator functions

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple = (Exception,)):
    """
    Retry decorator for handling transient failures.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        break
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise RetryExhaustedError(
                f"Function {func.__name__} failed after {max_attempts} attempts"
            ) from last_exception
        
        return wrapper
    return decorator


def timeout(seconds: float):
    """
    Timeout decorator for limiting function execution time.
    
    Args:
        seconds: Maximum execution time in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            exception = None
            
            def target():
                nonlocal result, exception
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    exception = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout=seconds)
            
            if thread.is_alive():
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
            
            if exception:
                raise exception
            
            return result
        
        return wrapper
    return decorator


# Utility functions

def validate_input(data: Any, validator: Callable, error_message: str = "Validation failed") -> Any:
    """
    Validate input data using a validator function.
    
    Args:
        data: Data to validate
        validator: Function that returns True if data is valid
        error_message: Error message if validation fails
        
    Returns:
        Validated data
        
    Raises:
        ValidationError: If validation fails
    """
    if not validator(data):
        raise ValidationError(error_message)
    return data


def transform_data(data: Any, transformer: Callable) -> Any:
    """
    Transform data using a transformer function.
    
    Args:
        data: Data to transform
        transformer: Function to transform data
        
    Returns:
        Transformed data
    """
    return transformer(data)


def batch_process(items: List[Any], processor: Callable, batch_size: int = 100) -> List[Any]:
    """
    Process items in batches.
    
    Args:
        items: List of items to process
        processor: Function to process each batch
        batch_size: Number of items per batch
        
    Returns:
        List of processed items
    """
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_result = processor(batch)
        results.extend(batch_result)
    return results