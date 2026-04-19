"""
Practice Exercises for Databases & Docker Project

This file contains hands-on exercises to reinforce database concepts with Docker
and SQLAlchemy for data engineering.
These exercises are designed for 8GB RAM laptops with no GPU.
"""

import sys
import time
import subprocess
import os
from typing import List, Dict, Any, Optional

def exercise_1_docker_compose_basics():
    """
    Exercise 1: Docker Compose Basics
    
    Task: Understand and manipulate Docker Compose configurations.
    
    Requirements:
    1. Examine the provided docker-compose.yml file and explain each section.
    2. Write a function that checks if Docker Compose is installed and running.
    3. Create a Python function that starts the database container using docker-compose.
    4. Write a function that waits for the database to be ready (health check).
    
    Memory Constraint: Ensure Docker commands don't consume excessive memory.
    """
    # TODO: Implement this function
    pass

def exercise_2_database_connection_pooling():
    """
    Exercise 2: Database Connection Pooling
    
    Task: Implement efficient database connections with connection pooling.
    
    Requirements:
    1. Create a connection pool using SQLAlchemy's engine with pool settings.
    2. Implement a context manager for database connections that automatically
       returns connections to the pool.
    3. Write a function that executes multiple queries using the same connection
       to demonstrate connection reuse.
    4. Handle connection errors and implement retry logic.
    
    Memory Constraint: Limit connection pool size to prevent memory exhaustion.
    """
    # TODO: Implement this function
    pass

def exercise_3_sqlalchemy_orm_modeling():
    """
    Exercise 3: SQLAlchemy ORM Modeling
    
    Task: Create and use SQLAlchemy ORM models for data engineering.
    
    Requirements:
    1. Define ORM models for a typical e-commerce schema:
       - Customer (id, name, email, created_at)
       - Product (id, name, price, category)
       - Order (id, customer_id, order_date, total_amount)
       - OrderItem (id, order_id, product_id, quantity, price)
    
    2. Implement relationships between models (one-to-many, many-to-one).
    3. Create a function that inserts sample data using the ORM.
    4. Write queries using SQLAlchemy's query API (filter, join, aggregate).
    
    Memory Constraint: Use batch inserts for large data to avoid memory issues.
    """
    # TODO: Implement this function
    pass

def exercise_4_database_migrations():
    """
    Exercise 4: Database Migrations
    
    Task: Implement schema evolution using Alembic migrations.
    
    Requirements:
    1. Create an initial migration for the e-commerce schema from Exercise 3.
    2. Write a migration that adds a new column 'discount_percentage' to Product table.
    3. Implement a backward migration (downgrade) that removes the column.
    4. Write a data migration that populates the new column with default values.
    
    Memory Constraint: Process data in chunks during data migrations.
    """
    # TODO: Implement this function
    pass

def exercise_5_transaction_management():
    """
    Exercise 5: Transaction Management
    
    Task: Master ACID properties and transaction handling.
    
    Requirements:
    1. Implement a function that transfers funds between two accounts atomically.
    2. Create a nested transaction scenario with savepoints.
    3. Handle transaction isolation levels (read committed, repeatable read).
    4. Implement optimistic concurrency control using version numbers.
    
    Memory Constraint: Keep transaction duration short to avoid locking issues.
    """
    # TODO: Implement this function
    pass

def exercise_6_bulk_data_operations():
    """
    Exercise 6: Bulk Data Operations
    
    Task: Efficiently handle large-scale data operations.
    
    Requirements:
    1. Implement bulk insert of 10,000 records using SQLAlchemy's bulk operations.
    2. Create a function that updates records in batches of 1000.
    3. Implement UPSERT (INSERT ON CONFLICT UPDATE) operations.
    4. Write a function that exports query results to CSV in chunks.
    
    Memory Constraint: Process data in batches to stay within 8GB RAM limit.
    """
    # TODO: Implement this function
    pass

def exercise_7_database_backup_restore():
    """
    Exercise 7: Database Backup and Restore
    
    Task: Implement database backup strategies using Docker and Python.
    
    Requirements:
    1. Create a function that uses `pg_dump` to backup the database.
    2. Implement a restore function using `pg_restore`.
    3. Write a Python script that automates daily backups with retention policy.
    4. Create a function that verifies backup integrity.
    
    Memory Constraint: Stream backup data to avoid loading entire database in memory.
    """
    # TODO: Implement this function
    pass

def exercise_8_monitoring_and_performance():
    """
    Exercise 8: Monitoring and Performance
    
    Task: Monitor database performance and optimize queries.
    
    Requirements:
    1. Implement query logging that captures slow queries (> 100ms).
    2. Create a function that explains query execution plans.
    3. Write index creation logic for common query patterns.
    4. Implement connection pool monitoring (active/idle connections).
    
    Memory Constraint: Monitor memory usage of database connections.
    """
    # TODO: Implement this function
    pass

def exercise_9_multi_database_integration():
    """
    Exercise 9: Multi-Database Integration
    
    Task: Work with multiple database systems (PostgreSQL, SQLite).
    
    Requirements:
    1. Create a Docker Compose file with both PostgreSQL and SQLite services.
    2. Implement a data synchronization function between the two databases.
    3. Write a query that joins data from both databases (using SQLAlchemy).
    4. Handle database-specific SQL differences (date functions, string operations).
    
    Memory Constraint: Transfer data between databases in chunks.
    """
    # TODO: Implement this function
    pass

def exercise_10_production_readiness():
    """
    Exercise 10: Production Readiness
    
    Task: Prepare database setup for production deployment.
    
    Requirements:
    1. Implement environment-based configuration (dev, test, prod).
    2. Create a health check endpoint for database connectivity.
    3. Write a function that validates database schema on application startup.
    4. Implement connection failure handling with circuit breaker pattern.
    
    Memory Constraint: Ensure connection pooling settings are appropriate for 8GB RAM.
    """
    # TODO: Implement this function
    pass

def main():
    """
    Main function to run all exercises.
    """
    print("Databases & Docker Practice Exercises")
    print("=" * 50)
    
    exercises = [
        ("Docker Compose Basics", exercise_1_docker_compose_basics),
        ("Connection Pooling", exercise_2_database_connection_pooling),
        ("SQLAlchemy ORM Modeling", exercise_3_sqlalchemy_orm_modeling),
        ("Database Migrations", exercise_4_database_migrations),
        ("Transaction Management", exercise_5_transaction_management),
        ("Bulk Data Operations", exercise_6_bulk_data_operations),
        ("Backup & Restore", exercise_7_database_backup_restore),
        ("Monitoring & Performance", exercise_8_monitoring_and_performance),
        ("Multi-Database Integration", exercise_9_multi_database_integration),
        ("Production Readiness", exercise_10_production_readiness),
    ]
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * 30)
        try:
            func()
            print(f"  Exercise function called successfully")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("All exercises completed (stubs implemented)")

if __name__ == "__main__":
    main()