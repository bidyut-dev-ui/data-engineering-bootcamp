"""
Custom exceptions for the example library.

This module demonstrates:
1. Creating a hierarchy of custom exceptions
2. Adding context and metadata to exceptions
3. Proper exception chaining
4. Documentation and usage patterns
"""


class ExampleLibError(Exception):
    """
    Base exception for all library errors.
    
    This should be caught by users of the library to handle
    any library-specific errors.
    """
    
    def __init__(self, message: str, context: dict = None):
        """
        Initialize the exception.
        
        Args:
            message: Error message
            context: Additional context about the error
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        """String representation with context if available."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} [{context_str}]"
        return self.message


class ConfigurationError(ExampleLibError):
    """
    Raised when there's a configuration error.
    
    This could be due to:
    - Missing required configuration
    - Invalid configuration values
    - Configuration file parsing errors
    """
    pass


class ValidationError(ExampleLibError):
    """
    Raised when data validation fails.
    
    This could be due to:
    - Invalid input data
    - Missing required fields
    - Type mismatches
    - Constraint violations
    """
    
    def __init__(self, message: str, field: str = None, value: Any = None, **kwargs):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Value that caused the failure
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if field is not None:
            context['field'] = field
        if value is not None:
            context['value'] = value
        
        super().__init__(message, context)
        self.field = field
        self.value = value


class ProcessingError(ExampleLibError):
    """
    Raised when data processing fails.
    
    This could be due to:
    - Processing logic errors
    - External service failures
    - Resource constraints
    - Timeouts during processing
    """
    
    def __init__(self, message: str, step: str = None, input_data: Any = None, **kwargs):
        """
        Initialize processing error.
        
        Args:
            message: Error message
            step: Processing step that failed
            input_data: Input data that caused the failure
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if step is not None:
            context['step'] = step
        if input_data is not None:
            context['input_data_type'] = type(input_data).__name__
        
        super().__init__(message, context)
        self.step = step
        self.input_data = input_data


class TimeoutError(ExampleLibError):
    """
    Raised when an operation times out.
    
    Note: This doesn't conflict with built-in TimeoutError
    because it's a subclass of ExampleLibError.
    """
    
    def __init__(self, message: str, timeout_seconds: float = None, **kwargs):
        """
        Initialize timeout error.
        
        Args:
            message: Error message
            timeout_seconds: Timeout duration in seconds
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if timeout_seconds is not None:
            context['timeout_seconds'] = timeout_seconds
        
        super().__init__(message, context)
        self.timeout_seconds = timeout_seconds


class RetryExhaustedError(ExampleLibError):
    """
    Raised when all retry attempts have been exhausted.
    """
    
    def __init__(self, message: str, max_attempts: int = None, last_exception: Exception = None, **kwargs):
        """
        Initialize retry exhausted error.
        
        Args:
            message: Error message
            max_attempts: Maximum number of retry attempts
            last_exception: The last exception that occurred
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if max_attempts is not None:
            context['max_attempts'] = max_attempts
        if last_exception is not None:
            context['last_exception'] = str(last_exception)
            context['last_exception_type'] = type(last_exception).__name__
        
        super().__init__(message, context)
        self.max_attempts = max_attempts
        self.last_exception = last_exception


class PluginError(ExampleLibError):
    """
    Raised when there's an error with plugins.
    
    This could be due to:
    - Plugin loading failures
    - Plugin compatibility issues
    - Plugin execution errors
    """
    
    def __init__(self, message: str, plugin_name: str = None, plugin_type: str = None, **kwargs):
        """
        Initialize plugin error.
        
        Args:
            message: Error message
            plugin_name: Name of the plugin that failed
            plugin_type: Type of plugin
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if plugin_name is not None:
            context['plugin_name'] = plugin_name
        if plugin_type is not None:
            context['plugin_type'] = plugin_type
        
        super().__init__(message, context)
        self.plugin_name = plugin_name
        self.plugin_type = plugin_type


class DependencyError(ExampleLibError):
    """
    Raised when there's a dependency-related error.
    
    This could be due to:
    - Missing required dependencies
    - Version incompatibilities
    - Import errors
    """
    
    def __init__(self, message: str, dependency: str = None, required_version: str = None, **kwargs):
        """
        Initialize dependency error.
        
        Args:
            message: Error message
            dependency: Name of the missing dependency
            required_version: Required version
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if dependency is not None:
            context['dependency'] = dependency
        if required_version is not None:
            context['required_version'] = required_version
        
        super().__init__(message, context)
        self.dependency = dependency
        self.required_version = required_version


class SerializationError(ExampleLibError):
    """
    Raised when serialization or deserialization fails.
    
    This could be due to:
    - Invalid JSON/YAML
    - Unserializable objects
    - Encoding issues
    """
    
    def __init__(self, message: str, data_type: str = None, format: str = None, **kwargs):
        """
        Initialize serialization error.
        
        Args:
            message: Error message
            data_type: Type of data being serialized
            format: Serialization format (json, yaml, etc.)
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if data_type is not None:
            context['data_type'] = data_type
        if format is not None:
            context['format'] = format
        
        super().__init__(message, context)
        self.data_type = data_type
        self.format = format


class ResourceError(ExampleLibError):
    """
    Raised when there's a resource-related error.
    
    This could be due to:
    - Insufficient memory/disk space
    - File system errors
    - Network connectivity issues
    """
    
    def __init__(self, message: str, resource_type: str = None, resource_path: str = None, **kwargs):
        """
        Initialize resource error.
        
        Args:
            message: Error message
            resource_type: Type of resource (file, memory, network, etc.)
            resource_path: Path to the resource
            **kwargs: Additional context
        """
        context = kwargs.copy()
        if resource_type is not None:
            context['resource_type'] = resource_type
        if resource_path is not None:
            context['resource_path'] = resource_path
        
        super().__init__(message, context)
        self.resource_type = resource_type
        self.resource_path = resource_path


# Helper functions for working with exceptions

def wrap_exception(exception: Exception, wrapper_class: type, message: str = None) -> ExampleLibError:
    """
    Wrap an existing exception in a library exception.
    
    Args:
        exception: Exception to wrap
        wrapper_class: Library exception class to wrap with
        message: Optional custom message
        
    Returns:
        Wrapped exception
    """
    if message is None:
        message = str(exception)
    
    # Create the wrapped exception
    wrapped = wrapper_class(message)
    
    # Preserve the original traceback
    wrapped.__cause__ = exception
    
    return wrapped


def is_library_error(exception: Exception) -> bool:
    """
    Check if an exception is a library error.
    
    Args:
        exception: Exception to check
        
    Returns:
        True if exception is a library error
    """
    return isinstance(exception, ExampleLibError)


def get_error_context(exception: Exception) -> dict:
    """
    Extract context from a library error.
    
    Args:
        exception: Exception to extract context from
        
    Returns:
        Context dictionary or empty dict
    """
    if isinstance(exception, ExampleLibError):
        return exception.context or {}
    return {}


def format_exception_chain(exception: Exception) -> str:
    """
    Format an exception chain for logging.
    
    Args:
        exception: Exception to format
        
    Returns:
        Formatted exception chain string
    """
    parts = []
    current = exception
    
    while current is not None:
        parts.append(f"{type(current).__name__}: {current}")
        current = current.__cause__
    
    return " -> ".join(parts)