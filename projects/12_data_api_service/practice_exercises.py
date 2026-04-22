#!/usr/bin/env python3
"""
Practice Exercises for Data API Service Project

This module contains exercises focused on building production-ready REST APIs
with FastAPI, database integration, Dockerization, and deployment patterns.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import sqlite3
from contextlib import contextmanager
import subprocess
import sys
import os


def exercise_1_basic_fastapi_setup() -> Dict[str, Any]:
    """
    Exercise 1: Basic FastAPI Setup
    
    Create a minimal FastAPI application with health check endpoint.
    Focus on proper project structure, dependency injection, and error handling.
    
    Requirements:
    1. Create a FastAPI app with title "Data API Service"
    2. Add a GET /health endpoint that returns {"status": "healthy", "timestamp": current_iso_time}
    3. Add proper CORS middleware configuration
    4. Include comprehensive OpenAPI documentation
    5. Add request logging middleware
    
    Memory Considerations (8GB RAM):
    - Use connection pooling for database connections
    - Implement response caching for frequently accessed endpoints
    - Monitor memory usage with psutil
    """
    return {
        "description": "Create a basic FastAPI application with health check endpoint",
        "learning_objectives": [
            "FastAPI project structure and configuration",
            "Dependency injection patterns",
            "CORS middleware setup",
            "OpenAPI documentation generation",
            "Memory-efficient API design"
        ],
        "requirements": [
            "FastAPI app with proper metadata",
            "Health check endpoint with timestamp",
            "CORS middleware configuration",
            "Request logging middleware",
            "Memory monitoring integration"
        ],
        "difficulty": "Beginner",
        "estimated_time": "30 minutes",
        "prerequisites": ["Python basics", "HTTP/REST concepts"]
    }


def exercise_2_database_connection_pooling() -> Dict[str, Any]:
    """
    Exercise 2: Database Connection Pooling
    
    Implement efficient database connection management for PostgreSQL data warehouse.
    Focus on connection pooling, connection lifecycle, and error recovery.
    
    Requirements:
    1. Create a database connection module with SQLAlchemy
    2. Implement connection pooling with configurable pool size
    3. Add connection health checks and automatic reconnection
    4. Create dependency injection for database sessions
    5. Implement connection leak detection and monitoring
    
    Memory Considerations (8GB RAM):
    - Limit connection pool size based on available memory
    - Implement connection timeout to prevent resource exhaustion
    - Use connection recycling to prevent memory fragmentation
    - Monitor connection pool metrics
    """
    return {
        "description": "Implement database connection pooling for PostgreSQL",
        "learning_objectives": [
            "SQLAlchemy connection pooling configuration",
            "Database session lifecycle management",
            "Connection health monitoring",
            "Dependency injection patterns",
            "Memory-efficient connection management"
        ],
        "requirements": [
            "SQLAlchemy engine with connection pooling",
            "Configurable pool size and timeout",
            "Connection health check endpoint",
            "Session dependency injection",
            "Connection leak detection"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "45 minutes",
        "prerequisites": ["SQLAlchemy basics", "PostgreSQL familiarity"]
    }


def exercise_3_analytical_endpoints_design() -> Dict[str, Any]:
    """
    Exercise 3: Analytical Endpoints Design
    
    Design and implement RESTful analytical endpoints for data warehouse queries.
    Focus on query optimization, pagination, and response serialization.
    
    Requirements:
    1. Create sales summary endpoint with aggregation queries
    2. Implement regional sales breakdown with filtering capabilities
    3. Add top customers endpoint with pagination
    4. Create product performance analytics with time-based filtering
    5. Implement query parameter validation and sanitization
    
    Memory Considerations (8GB RAM):
    - Use server-side pagination to limit result set size
    - Implement query result streaming for large datasets
    - Add response compression for bandwidth optimization
    - Cache frequently accessed analytical results
    """
    return {
        "description": "Design analytical endpoints for data warehouse queries",
        "learning_objectives": [
            "RESTful API design for analytics",
            "SQL aggregation and window functions",
            "Query parameter validation",
            "Response pagination strategies",
            "Memory-efficient data serialization"
        ],
        "requirements": [
            "Sales summary aggregation endpoint",
            "Regional sales breakdown with filtering",
            "Top customers with pagination",
            "Product performance analytics",
            "Query parameter validation"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "60 minutes",
        "prerequisites": ["SQL aggregation", "FastAPI routing"]
    }


def exercise_4_error_handling_and_logging() -> Dict[str, Any]:
    """
    Exercise 4: Error Handling and Logging
    
    Implement comprehensive error handling and logging for production API.
    Focus on structured logging, error classification, and monitoring integration.
    
    Requirements:
    1. Create custom exception hierarchy for API errors
    2. Implement global exception handlers with proper HTTP status codes
    3. Add structured logging with correlation IDs
    4. Create health check endpoint with dependency status
    5. Implement request/response logging middleware
    
    Memory Considerations (8GB RAM):
    - Implement log rotation to prevent disk space exhaustion
    - Use asynchronous logging to reduce I/O blocking
    - Limit log verbosity based on environment
    - Implement log aggregation for distributed tracing
    """
    return {
        "description": "Implement error handling and logging for production API",
        "learning_objectives": [
            "Custom exception hierarchy design",
            "Global exception handling in FastAPI",
            "Structured logging implementation",
            "Health check with dependency monitoring",
            "Request/response logging middleware"
        ],
        "requirements": [
            "Custom exception classes with HTTP status codes",
            "Global exception handlers",
            "Structured logging with correlation IDs",
            "Health check with dependency status",
            "Request/response logging middleware"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "45 minutes",
        "prerequisites": ["Python exception handling", "Logging concepts"]
    }


def exercise_5_dockerization_multi_stage_build() -> Dict[str, Any]:
    """
    Exercise 5: Dockerization with Multi-Stage Build
    
    Create production-ready Docker image with multi-stage build optimization.
    Focus on image size reduction, security hardening, and environment configuration.
    
    Requirements:
    1. Create multi-stage Dockerfile with build and runtime stages
    2. Implement non-root user for security
    3. Add health check configuration
    4. Create environment variable configuration
    5. Implement resource limits and memory constraints
    
    Memory Considerations (8GB RAM):
    - Set container memory limits based on host constraints
    - Implement OOM killer configuration
    - Use Alpine-based images for smaller footprint
    - Configure swap usage for memory-intensive operations
    """
    return {
        "description": "Create production Docker image with multi-stage build",
        "learning_objectives": [
            "Docker multi-stage build optimization",
            "Container security hardening",
            "Health check configuration",
            "Environment variable management",
            "Resource limit configuration"
        ],
        "requirements": [
            "Multi-stage Dockerfile",
            "Non-root user configuration",
            "Health check endpoint integration",
            "Environment variable validation",
            "Resource limit configuration"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "60 minutes",
        "prerequisites": ["Docker basics", "Container concepts"]
    }


def exercise_6_docker_compose_orchestration() -> Dict[str, Any]:
    """
    Exercise 6: Docker Compose Orchestration
    
    Orchestrate multi-service application with Docker Compose.
    Focus on service dependencies, network configuration, and volume management.
    
    Requirements:
    1. Create docker-compose.yml with API and database services
    2. Implement service dependency management
    3. Add network configuration for service communication
    4. Create volume configuration for data persistence
    5. Implement environment variable inheritance
    
    Memory Considerations (8GB RAM):
    - Configure service resource limits in docker-compose
    - Implement service restart policies for resilience
    - Use named volumes for better performance
    - Configure swap usage for memory-intensive services
    """
    return {
        "description": "Orchestrate multi-service application with Docker Compose",
        "learning_objectives": [
            "Docker Compose service orchestration",
            "Service dependency management",
            "Network configuration",
            "Volume management",
            "Environment variable inheritance"
        ],
        "requirements": [
            "docker-compose.yml with multiple services",
            "Service dependency configuration",
            "Network setup for inter-service communication",
            "Volume configuration for data persistence",
            "Environment variable management"
        ],
        "difficulty": "Intermediate",
        "estimated_time": "45 minutes",
        "prerequisites": ["Docker Compose basics", "Multi-service architecture"]
    }


def exercise_7_api_authentication_and_authorization() -> Dict[str, Any]:
    """
    Exercise 7: API Authentication and Authorization
    
    Implement API key authentication and role-based authorization.
    Focus on security best practices, token validation, and audit logging.
    
    Requirements:
    1. Implement API key authentication middleware
    2. Create role-based authorization system
    3. Add rate limiting to prevent abuse
    4. Implement audit logging for security events
    5. Create token rotation and revocation mechanism
    
    Memory Considerations (8GB RAM):
    - Use in-memory cache for active API keys
    - Implement token blacklisting with TTL
    - Monitor authentication service memory usage
    - Use efficient data structures for rate limiting
    """
    return {
        "description": "Implement API authentication and authorization",
        "learning_objectives": [
            "API key authentication implementation",
            "Role-based authorization design",
            "Rate limiting strategies",
            "Audit logging for security",
            "Token management lifecycle"
        ],
        "requirements": [
            "API key authentication middleware",
            "Role-based authorization system",
            "Rate limiting implementation",
            "Audit logging for security events",
            "Token rotation mechanism"
        ],
        "difficulty": "Advanced",
        "estimated_time": "75 minutes",
        "prerequisites": ["Authentication concepts", "Security best practices"]
    }


def exercise_8_response_caching_and_optimization() -> Dict[str, Any]:
    """
    Exercise 8: Response Caching and Optimization
    
    Implement response caching strategies for API performance optimization.
    Focus on cache invalidation, conditional requests, and cache hierarchy.
    
    Requirements:
    1. Implement in-memory response caching
    2. Add Redis integration for distributed caching
    3. Create cache invalidation strategies
    4. Implement conditional requests (ETag, Last-Modified)
    5. Add cache control headers
    
    Memory Considerations (8GB RAM):
    - Implement cache size limits based on available memory
    - Use LRU cache eviction policy
    - Monitor cache hit ratio and memory usage
    - Implement cache warming for critical endpoints
    """
    return {
        "description": "Implement response caching for API performance",
        "learning_objectives": [
            "In-memory caching strategies",
            "Redis integration for distributed caching",
            "Cache invalidation patterns",
            "Conditional request implementation",
            "Cache control header configuration"
        ],
        "requirements": [
            "In-memory response caching",
            "Redis integration for distributed cache",
            "Cache invalidation strategies",
            "Conditional request support",
            "Cache control headers"
        ],
        "difficulty": "Advanced",
        "estimated_time": "60 minutes",
        "prerequisites": ["Caching concepts", "Redis basics"]
    }


def exercise_9_monitoring_and_metrics() -> Dict[str, Any]:
    """
    Exercise 9: Monitoring and Metrics
    
    Implement comprehensive monitoring and metrics collection for API.
    Focus on performance metrics, business metrics, and alerting.
    
    Requirements:
    1. Add Prometheus metrics endpoint
    2. Implement custom business metrics
    3. Create health check with dependency status
    4. Add request tracing with OpenTelemetry
    5. Implement alerting rules for critical metrics
    
    Memory Considerations (8GB RAM):
    - Limit metrics cardinality to prevent memory bloat
    - Implement metrics aggregation to reduce storage
    - Use sampling for high-volume tracing
    - Monitor metrics collector memory usage
    """
    return {
        "description": "Implement monitoring and metrics collection",
        "learning_objectives": [
            "Prometheus metrics integration",
            "Custom business metrics design",
            "Health check with dependency monitoring",
            "Request tracing implementation",
            "Alerting rule configuration"
        ],
        "requirements": [
            "Prometheus metrics endpoint",
            "Custom business metrics",
            "Health check with dependency status",
            "Request tracing with OpenTelemetry",
            "Alerting rules for critical metrics"
        ],
        "difficulty": "Advanced",
        "estimated_time": "75 minutes",
        "prerequisites": ["Monitoring concepts", "Metrics collection"]
    }


def exercise_10_production_deployment_patterns() -> Dict[str, Any]:
    """
    Exercise 10: Production Deployment Patterns
    
    Design and implement production deployment strategies for API service.
    Focus on zero-downtime deployment, rollback strategies, and configuration management.
    
    Requirements:
    1. Implement blue-green deployment strategy
    2. Create configuration management with environment separation
    3. Add database migration automation
    4. Implement canary release pattern
    5. Create rollback procedures and automation
    
    Memory Considerations (8GB RAM):
    - Implement deployment memory budgeting
    - Use resource quotas for deployment environments
    - Monitor deployment impact on system resources
    - Implement gradual traffic shifting for memory-intensive deployments
    """
    return {
        "description": "Design production deployment strategies",
        "learning_objectives": [
            "Blue-green deployment implementation",
            "Configuration management patterns",
            "Database migration automation",
            "Canary release strategy",
            "Rollback procedure design"
        ],
        "requirements": [
            "Blue-green deployment strategy",
            "Configuration management system",
            "Database migration automation",
            "Canary release implementation",
            "Rollback procedures"
        ],
        "difficulty": "Advanced",
        "estimated_time": "90 minutes",
        "prerequisites": ["Deployment concepts", "CI/CD basics"]
    }


def main():
    """Main function to demonstrate exercise structure"""
    exercises = [
        exercise_1_basic_fastapi_setup,
        exercise_2_database_connection_pooling,
        exercise_3_analytical_endpoints_design,
        exercise_4_error_handling_and_logging,
        exercise_5_dockerization_multi_stage_build,
        exercise_6_docker_compose_orchestration,
        exercise_7_api_authentication_and_authorization,
        exercise_8_response_caching_and_optimization,
        exercise_9_monitoring_and_metrics,
        exercise_10_production_deployment_patterns,
    ]
    
    print("Data API Service Practice Exercises")
    print("=" * 50)
    
    for i, exercise_func in enumerate(exercises, 1):
        exercise = exercise_func()
        print(f"\nExercise {i}: {exercise['description']}")
        print(f"Difficulty: {exercise['difficulty']}")
        print(f"Estimated Time: {exercise['estimated_time']}")
        print(f"Learning Objectives:")
        for obj in exercise['learning_objectives']:
            print(f"  - {obj}")
    
    print("\n" + "=" * 50)
    print("Total Exercises: 10")
    print("Focus Areas: FastAPI, Database Integration, Docker, Deployment, Monitoring")
    print("Memory Considerations: Optimized for 8GB RAM environments")


if __name__ == "__main__":
    main()