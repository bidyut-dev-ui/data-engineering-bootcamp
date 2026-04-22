#!/usr/bin/env python3
"""
Practice Exercises for FastAPI Basics Project

This file contains hands-on exercises to reinforce FastAPI concepts for building
RESTful APIs with automatic validation and documentation.
These exercises are designed for 8GB RAM laptops with no GPU.
"""

import sys
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

# FastAPI imports would be in solutions, but not needed in practice file
# from fastapi import FastAPI, HTTPException, Query, Path, Body
# from pydantic import BaseModel, Field

def exercise_1_basic_fastapi_app():
    """
    Exercise 1: Basic FastAPI Application Setup
    
    Task: Create a simple FastAPI application with basic endpoints.
    
    Requirements:
    1. Create a FastAPI app instance with appropriate metadata (title, description, version).
    2. Implement a root endpoint ("/") that returns a welcome message.
    3. Implement a health check endpoint ("/health") that returns {"status": "healthy"}.
    4. Implement a GET endpoint ("/info") that returns application metadata.
    
    Memory Constraint: Keep the application lightweight, avoid loading large datasets.
    """
    # TODO: Implement this function (solution would create actual FastAPI app)
    pass


def exercise_2_path_and_query_parameters():
    """
    Exercise 2: Path and Query Parameters
    
    Task: Implement endpoints with path parameters and query parameters.
    
    Requirements:
    1. Create a GET endpoint "/items/{item_id}" that returns item details based on path parameter.
    2. Add optional query parameters to "/items" endpoint: skip (int, default=0), limit (int, default=10).
    3. Implement validation for path parameter (item_id must be positive integer).
    4. Create a GET endpoint "/search" with query parameters: q (str), category (Optional[str]), min_price (Optional[float]).
    
    Memory Constraint: Use efficient data structures for in-memory storage.
    """
    # TODO: Implement this function
    pass


def exercise_3_request_models_validation():
    """
    Exercise 3: Request Models and Validation with Pydantic
    
    Task: Create Pydantic models for request validation.
    
    Requirements:
    1. Define a Pydantic model "Item" with fields: id (int), name (str, min_length=1, max_length=100), 
       price (float, gt=0), category (str), tags (List[str], default=[]).
    2. Create a POST endpoint "/items" that accepts an Item in request body and returns the created item.
    3. Add validation for duplicate item IDs (simulate with in-memory storage).
    4. Create a PUT endpoint "/items/{item_id}" that updates an existing item.
    
    Memory Constraint: Limit in-memory storage to 1000 items maximum.
    """
    # TODO: Implement this function
    pass


def exercise_4_response_models_serialization():
    """
    Exercise 4: Response Models and Serialization
    
    Task: Implement response models with different serialization strategies.
    
    Requirements:
    1. Create a response model "UserResponse" that excludes password field from User model.
    2. Implement a GET endpoint "/users/{user_id}" that returns user data without sensitive fields.
    3. Create an endpoint "/users" that returns paginated user list with metadata (total, page, limit).
    4. Implement response_model_exclude_none to exclude None values from responses.
    
    Memory Constraint: Use generators for large dataset simulations to stay within 8GB RAM.
    """
    # TODO: Implement this function
    pass


def exercise_5_error_handling_custom_exceptions():
    """
    Exercise 5: Error Handling and Custom Exceptions
    
    Task: Implement comprehensive error handling in FastAPI.
    
    Requirements:
    1. Create custom HTTPException handlers for 404 (Not Found) and 422 (Validation Error).
    2. Implement a global exception handler for unexpected errors (500).
    3. Create a middleware that logs all requests and responses.
    4. Add rate limiting to prevent abuse (simulate with simple counter).
    
    Memory Constraint: Log files should rotate to prevent disk space issues.
    """
    # TODO: Implement this function
    pass


def exercise_6_dependency_injection():
    """
    Exercise 6: Dependency Injection
    
    Task: Use FastAPI's dependency injection system for reusable components.
    
    Requirements:
    1. Create a dependency that extracts and validates API key from headers.
    2. Implement a dependency for database connection pooling (simulate with mock).
    3. Create a dependency that paginates results (skip, limit).
    4. Use dependencies in multiple endpoints to demonstrate code reuse.
    
    Memory Constraint: Connection pool size should be limited for 8GB RAM.
    """
    # TODO: Implement this function
    pass


def exercise_7_automatic_documentation_customization():
    """
    Exercise 7: Automatic Documentation and Customization
    
    Task: Customize and extend FastAPI's automatic documentation.
    
    Requirements:
    1. Add custom tags to organize endpoints in Swagger UI.
    2. Implement custom response descriptions and examples.
    3. Add OpenAPI schema extensions for API metadata.
    4. Create a custom docs endpoint with additional information.
    
    Memory Constraint: Documentation generation shouldn't load large datasets.
    """
    # TODO: Implement this function
    pass


def exercise_8_performance_optimization():
    """
    Exercise 8: Performance Optimization for 8GB RAM
    
    Task: Optimize FastAPI application for memory-constrained environments.
    
    Requirements:
    1. Implement response compression (gzip) for large responses.
    2. Use async/await for I/O bound operations (simulate with sleep).
    3. Implement caching for frequently accessed endpoints (in-memory LRU cache).
    4. Add memory monitoring middleware to track application memory usage.
    
    Memory Constraint: All optimizations must respect 8GB RAM limit.
    """
    # TODO: Implement this function
    pass


def main():
    """
    Run all FastAPI practice exercises in sequence.
    This is a demonstration function - actual solutions would be in solutions.py.
    """
    exercises = [
        ("Basic FastAPI App Setup", exercise_1_basic_fastapi_app),
        ("Path and Query Parameters", exercise_2_path_and_query_parameters),
        ("Request Models and Validation", exercise_3_request_models_validation),
        ("Response Models and Serialization", exercise_4_response_models_serialization),
        ("Error Handling and Custom Exceptions", exercise_5_error_handling_custom_exceptions),
        ("Dependency Injection", exercise_6_dependency_injection),
        ("Automatic Documentation Customization", exercise_7_automatic_documentation_customization),
        ("Performance Optimization", exercise_8_performance_optimization),
    ]
    
    print("FastAPI Practice Exercises")
    print("=" * 50)
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * 30)
        try:
            # In practice file, we just show the docstring
            docstring = func.__doc__
            if docstring:
                # Extract just the task description
                lines = docstring.strip().split('\n')
                task_line = None
                for line in lines:
                    if line.strip().startswith('Task:'):
                        task_line = line.strip()
                        break
                if task_line:
                    print(f"  {task_line}")
                else:
                    print("  (See function docstring for details)")
            else:
                print("  No documentation available")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("Note: These are practice exercises. Implementations are in solutions.py")
    print("Each exercise focuses on specific FastAPI concepts for data engineering.")


if __name__ == "__main__":
    main()