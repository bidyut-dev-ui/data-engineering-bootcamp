#!/usr/bin/env python3
"""
Advanced Python: Decorators and Descriptors

This tutorial covers Python's metaprogramming features:
- Function decorators with and without arguments
- Class decorators
- Property descriptors and data descriptors
- Custom descriptor patterns for validation and data management

Key Concepts:
- Decorator syntax and implementation
- Descriptor protocol (__get__, __set__, __delete__)
- Property vs descriptor vs attribute
- Metaprogramming patterns
"""

import time
import functools
import logging
from typing import Any, Callable, Optional, TypeVar, cast
from datetime import datetime
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


# ============================================================================
# PART 1: FUNCTION DECORATORS
# ============================================================================

def simple_decorator(func: F) -> F:
    """
    A simple decorator that logs function calls.
    
    This is a decorator without arguments that wraps the function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned {result}")
        return result
    return cast(F, wrapper)


def timer_decorator(func: F) -> F:
    """Decorator that measures execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        logger.info(f"{func.__name__} took {elapsed:.4f} seconds")
        
        return result
    return cast(F, wrapper)


def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator factory that creates a retry decorator.
    
    This is a decorator WITH arguments, so it returns a decorator function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(f"Attempt {attempt}/{max_attempts} for {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt} failed: {e}")
                    
                    if attempt < max_attempts:
                        logger.info(f"Waiting {delay} seconds before retry...")
                        time.sleep(delay)
            
            # All attempts failed
            raise Exception(f"Function {func.__name__} failed after {max_attempts} attempts") from last_exception
        
        return cast(F, wrapper)
    return decorator


class CacheDecorator:
    """
    A class-based decorator for caching function results.
    
    Demonstrates that decorators can be implemented as classes
    with __call__ method.
    """
    
    def __init__(self, func: F):
        self.func = func
        self.cache: dict = {}
        functools.update_wrapper(self, func)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Create a cache key from arguments
        cache_key = (args, tuple(sorted(kwargs.items())))
        
        if cache_key in self.cache:
            logger.info(f"Cache hit for {self.func.__name__}{args}")
            return self.cache[cache_key]
        
        logger.info(f"Cache miss for {self.func.__name__}{args}")
        result = self.func(*args, **kwargs)
        self.cache[cache_key] = result
        
        return result
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        logger.info(f"Cache cleared for {self.func.__name__}")


# Example functions to decorate
@simple_decorator
def greet(name: str) -> str:
    """A simple greeting function."""
    return f"Hello, {name}!"


@timer_decorator
def calculate_sum(n: int) -> int:
    """Calculate sum of numbers from 1 to n."""
    return sum(range(1, n + 1))


@retry_decorator(max_attempts=2, delay=0.5)
def unreliable_operation(should_fail: bool = False) -> str:
    """An operation that might fail."""
    if should_fail and time.time() % 2 < 1:
        raise ValueError("Random failure!")
    return "Operation succeeded"


@CacheDecorator
def expensive_computation(x: int, y: int) -> int:
    """Simulate an expensive computation."""
    time.sleep(0.5)  # Simulate computation time
    return x * y + x + y


async def run_decorator_examples() -> None:
    """Demonstrate function decorators."""
    print("\n" + "="*60)
    print("PART 1: FUNCTION DECORATORS")
    print("="*60)
    
    print("\n1. Simple decorator (logging):")
    print(f"   Result: {greet('Alice')}")
    
    print("\n2. Timer decorator:")
    result = calculate_sum(1000000)
    print(f"   Sum of first 1,000,000 numbers: {result}")
    
    print("\n3. Retry decorator:")
    try:
        result = unreliable_operation(should_fail=True)
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Failed after retries: {e}")
    
    print("\n4. Cache decorator (class-based):")
    print("   First call (cache miss):")
    result1 = expensive_computation(5, 10)
    print(f"   Result: {result1}")
    
    print("   Second call (cache hit):")
    result2 = expensive_computation(5, 10)
    print(f"   Result: {result2}")
    
    print("   Different arguments (cache miss):")
    result3 = expensive_computation(3, 7)
    print(f"   Result: {result3}")


# ============================================================================
# PART 2: CLASS DECORATORS
# ============================================================================

def add_methods(**methods: Callable) -> Callable:
    """
    Class decorator that adds methods to a class.
    
    This demonstrates how decorators can modify classes.
    """
    def decorator(cls: type) -> type:
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls
    return decorator


def singleton(cls: type) -> type:
    """
    Class decorator that makes a class a singleton.
    
    Only one instance of the class will ever be created.
    """
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


def validate_attributes(*required_attrs: str) -> Callable:
    """
    Class decorator that validates required attributes.
    
    Checks that decorated classes have all required attributes.
    """
    def decorator(cls: type) -> type:
        original_init = cls.__init__
        
        @functools.wraps(original_init)
        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            original_init(self, *args, **kwargs)
            
            missing = [attr for attr in required_attrs if not hasattr(self, attr)]
            if missing:
                raise AttributeError(
                    f"{cls.__name__} missing required attributes: {missing}"
                )
        
        cls.__init__ = new_init
        return cls
    
    return decorator


# Example classes to decorate
@add_methods(
    say_hello=lambda self: f"Hello from {self.name}",
    get_age=lambda self: datetime.now().year - self.birth_year
)
class Person:
    """A simple person class that will get methods added by decorator."""
    
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year
    
    def __repr__(self) -> str:
        return f"Person(name={self.name}, birth_year={self.birth_year})"


@singleton
class DatabaseConnection:
    """A singleton database connection class."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
        logger.info(f"Creating database connection to {connection_string}")
    
    def connect(self) -> None:
        self.connected = True
        logger.info("Database connected")
    
    def disconnect(self) -> None:
        self.connected = False
        logger.info("Database disconnected")


@validate_attributes("name", "email", "age")
class User:
    """A user class that requires specific attributes."""
    
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age
    
    def __repr__(self) -> str:
        return f"User(name={self.name}, email={self.email}, age={self.age})"


async def run_class_decorator_examples() -> None:
    """Demonstrate class decorators."""
    print("\n" + "="*60)
    print("PART 2: CLASS DECORATORS")
    print("="*60)
    
    print("\n1. Add methods decorator:")
    person = Person("Alice", 1990)
    print(f"   Created: {person}")
    print(f"   say_hello: {person.say_hello()}")
    print(f"   get_age: {person.get_age()}")
    
    print("\n2. Singleton decorator:")
    db1 = DatabaseConnection("postgresql://localhost/mydb")
    db1.connect()
    
    db2 = DatabaseConnection("postgresql://localhost/mydb")
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   db2 connected: {db2.connected}")
    
    print("\n3. Validate attributes decorator:")
    try:
        user = User("Bob", "bob@example.com", 30)
        print(f"   Created valid user: {user}")
        
        # This would fail
        # invalid_user = User("Charlie", 25)  # Missing email
    except Exception as e:
        print(f"   Error: {e}")


# ============================================================================
# PART 3: DESCRIPTORS
# ============================================================================

class ValidatedAttribute:
    """
    A descriptor that validates attribute values.
    
    Descriptors implement __get__, __set__, and/or __delete__ methods.
    They control access to attributes on classes.
    """
    
    def __init__(self, validator: Callable[[Any], bool], default: Any = None):
        self.validator = validator
        self.default = default
        self.data = {}
    
    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        
        # Return the value for this object, or default if not set
        return self.data.get(id(obj), self.default)
    
    def __set__(self, obj: Any, value: Any) -> None:
        if not self.validator(value):
            raise ValueError(f"Invalid value: {value}")
        
        # Store value keyed by object id
        self.data[id(obj)] = value
    
    def __delete__(self, obj: Any) -> None:
        # Remove the value for this object
        self.data.pop(id(obj), None)


class PositiveNumber(ValidatedAttribute):
    """Descriptor for positive numbers."""
    
    def __init__(self, default: float = 0.0):
        super().__init__(lambda x: isinstance(x, (int, float)) and x >= 0, default)


class BoundedString(ValidatedAttribute):
    """Descriptor for strings with length bounds."""
    
    def __init__(self, min_len: int = 0, max_len: int = 100, default: str = ""):
        validator = lambda s: isinstance(s, str) and min_len <= len(s) <= max_len
        super().__init__(validator, default)


class TypedAttribute:
    """
    A descriptor that enforces type checking.
    
    This is a data descriptor (has __set__) that controls attribute access.
    """
    
    def __init__(self, expected_type: type):
        self.expected_type = expected_type
        self.data = {}
    
    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        return self.data.get(id(obj))
    
    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, got {type(value).__name__}"
            )
        self.data[id(obj)] = value
    
    def __delete__(self, obj: Any) -> None:
        self.data.pop(id(obj), None)


class LazyProperty:
    """
    A descriptor for lazy evaluation of properties.
    
    Computes value once and caches it.
    """
    
    def __init__(self, func: Callable[[Any], Any]):
        self.func = func
        self.cache = {}
    
    def __get__(self, obj: Any, objtype: type = None) -> Any:
        if obj is None:
            return self
        
        obj_id = id(obj)
        if obj_id not in self.cache:
            self.cache[obj_id] = self.func(obj)
        
        return self.cache[obj_id]


# Example class using descriptors
class Product:
    """A product class using descriptors for validation."""
    
    # Using custom descriptors
    name = BoundedString(min_len=1, max_len=50)
    price = PositiveNumber(default=0.0)
    quantity = PositiveNumber(default=0)
    
    # Using typed descriptor
    category = TypedAttribute(str)
    
    def __init__(self, name: str, price: float, quantity: int, category: str):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
    
    @LazyProperty
    def total_value(self) -> float:
        """Lazy property: computed once and cached."""
        logger.info("Computing total value...")
        return self.price * self.quantity
    
    def __repr__(self) -> str:
        return f"Product(name={self.name}, price=${self.price:.2f}, quantity={self.quantity})"


async def run_descriptor_examples() -> None:
    """Demonstrate descriptor usage."""
    print("\n" + "="*60)
    print("PART 3: DESCRIPTORS")
    print("="*60)
    
    print("\n1. Creating product with validated attributes:")
    try:
        product = Product("Laptop", 999.99, 10, "Electronics")
        print(f"   Created: {product}")
        print(f"   Total value: ${product.total_value:.2f}")
        print(f"   Total value (cached): ${product.total_value:.2f}")
        
        print("\n2. Testing validation:")
        try:
            product.price = -100  # Should fail
        except ValueError as e:
            print(f"   Price validation failed: {e}")
        
        try:
            product.name = ""  # Should fail (too short)
        except ValueError as e:
            print(f"   Name validation failed: {e}")
        
        try:
            product.category = 123  # Should fail (wrong type)
        except TypeError as e:
            print(f"   Type validation failed: {e}")
        
        print("\n3. Testing successful updates:")
        product.price = 899.99
        product.quantity = 15
        print(f"   Updated: {product}")
        print(f"   New total value: ${product.total_value:.2f}")
        
    except Exception as e:
        print(f"   Error: {e}")


# ============================================================================
# PART 4: PROPERTY DESCRIPTORS
# ============================================================================

class Temperature:
    """
    Class demonstrating property descriptors for computed attributes.
    
    Properties are a special type of descriptor built into Python.
    """
    
    def __init__(self, celsius: float):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set temperature in Celsius."""
        if value < -273.15:  # Absolute zero
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit (computed property)."""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature via Fahrenheit value."""
        self._celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self) -> float:
        """Get temperature in Kelvin (computed property)."""
        return self._celsius + 273.15
    
    @kelvin.setter 
    def kelvin(self, value: float) -> None:
        """Set temperature via Kelvin value."""
        if value < 0:
            raise ValueError("Temperature cannot be below 0 Kelvin")
        self._celsius = value - 273.15


class Circle:
    """Class demonstrating property descriptors with validation."""
    
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def diameter(self) -> float:
        return 2 * self._radius
    
    @diameter.setter
    def diameter(self, value: float) -> None:
        self.radius = value / 2
    
    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2
    
    @area.setter
    def area(self, value: float) -> None:
        import math
        if value <= 0:
            raise ValueError("Area must be positive")
        self.radius = (value / math.pi) ** 0.5
    
    @property
    def circumference(self) -> float:
        import math
        return 2 * math.pi * self._radius
    
    @circumference.setter
    def circumference(self, value: float) -> None:
        import math
        if value <= 0:
            raise ValueError("Circumference must be positive")
        self.radius = value / (2 * math.pi)


async def run_property_examples() -> None:
    """Demonstrate property descriptors."""
    print("\n" + "="*60)
    print("PART 4: PROPERTY DESCRIPTORS")
    print("="*60)
    
    print("\n1. Temperature class with property descriptors:")
    temp = Temperature(25.0)
    print(f"   Initial: {temp.celsius}°C")
    print(f"   Fahrenheit: {temp.fahrenheit}°F")
    print(f"   Kelvin: {temp.kelvin}K")
    
    temp.fahrenheit = 77.0
    print(f"   After setting to 77°F: {temp.celsius:.1f}°C")
    
    temp.kelvin = 300.0
    print(f"   After setting to 300K: {temp.celsius:.1f}°C")
    
    print("\n2. Circle class with computed properties:")
    circle = Circle(5.0)
    print(f"   Radius: {circle.radius}")
    print(f"   Diameter: {circle.diameter}")
    print(f"   Area: {circle.area:.2f}")
    print(f"   Circumference: {circle.circumference:.2f}")
    
    circle.diameter = 20.0
    print(f"   After setting diameter to 20: radius={circle.radius}")
    
    circle.area = 100.0
    print(f"   After setting area to 100: radius={circle.radius:.2f}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main() -> None:
    """Run all decorator and descriptor examples."""
    print("="*60)
    print("ADVANCED PYTHON: DECORATORS AND DESCRIPTORS TUTORIAL")
    print("="*60)
    
    try:
        await run_decorator_examples()
        await run_class_decorator_examples()
        await run_descriptor_examples()
        await run_property_examples()
        
        print("\n" + "="*60)
        print("TUTORIAL COMPLETE!")
        print("="*60)
        print("\nKey Concepts Covered:")
        print("1. Function Decorators - Modify function behavior")
        print("2. Class Decorators - Modify class definition")
        print("3. Descriptors - Control attribute access (__get__, __set__)")
        print("4. Property Descriptors - Built-in descriptor for computed attributes")
        print("\nUse Cases:")
        print("- Validation and type checking")
        print("- Caching and memoization")
        print("- Logging and timing")
        print("- Access control and security")
        print("- API design and abstraction")
        
    except Exception as e:
        logger.error(f"Error in tutorial: {e}")
        raise


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())