"""
Practice Exercises for FastAPI Database Integration

This module contains hands-on exercises to master connecting FastAPI with databases,
performing CRUD operations, using SQLAlchemy ORM, handling database errors,
and implementing production-ready patterns.

Exercises range from basic SQLite integration to advanced connection pooling
and async database operations.
"""

# Exercise 1: Basic SQLite CRUD with FastAPI
"""
Create a FastAPI application that connects to an SQLite database and implements
CRUD operations for a 'books' table with the following schema:
- id: INTEGER PRIMARY KEY
- title: TEXT NOT NULL
- author: TEXT NOT NULL
- published_year: INTEGER

Implement the following endpoints:
1. POST /books/ - Create a new book
2. GET /books/ - List all books
3. GET /books/{book_id} - Get a specific book by ID
4. PUT /books/{book_id} - Update a book
5. DELETE /books/{book_id} - Delete a book

Requirements:
- Use raw SQLite3 connections (no ORM)
- Implement proper error handling for missing books (404)
- Use parameterized queries to prevent SQL injection
- Include database initialization function
"""

# Exercise 2: SQLAlchemy ORM Integration
"""
Refactor Exercise 1 to use SQLAlchemy ORM instead of raw SQLite.

Create SQLAlchemy models for the 'books' table and implement the same CRUD endpoints
using SQLAlchemy's session management.

Additional requirements:
- Use SQLAlchemy declarative base for model definition
- Implement proper session lifecycle (context managers)
- Add validation using Pydantic models for request/response
- Include database migration awareness (Alembic setup not required)
"""

# Exercise 3: Connection Pooling with Databases
"""
Implement connection pooling for a PostgreSQL database (simulated with SQLite for practice).

Create a connection pool that:
1. Limits maximum connections to 10
2. Reuses connections instead of creating new ones for each request
3. Properly handles connection timeouts
4. Implements connection health checks

Modify your FastAPI application to use this connection pool for all database operations.

Bonus: Implement connection pooling using a library like `asyncpg` or `psycopg2.pool`.
"""

# Exercise 4: Database Error Handling and Transactions
"""
Enhance your FastAPI application with comprehensive error handling and transaction management.

Implement:
1. Database constraint violation handling (unique, foreign key, not null)
2. Automatic rollback on exceptions
3. Retry logic for transient database errors
4. Custom HTTPException mapping for different database errors
5. Transaction isolation levels awareness

Create test scenarios that trigger:
- Duplicate key errors
- Foreign key constraint violations
- Database connection failures
- Deadlock situations
"""

# Exercise 5: Async Database Operations
"""
Convert your FastAPI application to use async database operations.

Requirements:
1. Use async SQLAlchemy with `asyncpg` or `aiosqlite`
2. Implement async endpoints with proper await patterns
3. Handle concurrent database operations safely
4. Benchmark performance improvements (optional)

Implement endpoints that:
- Perform multiple concurrent database queries
- Use async transaction management
- Handle async connection pooling
"""

# Exercise 6: Database Migration Integration
"""
Integrate database migrations into your FastAPI application using Alembic.

Create:
1. Alembic configuration and migration environment
2. Initial migration for the 'books' table
3. A second migration that adds a new column 'genre' to the 'books' table
4. Automatic migration application on application startup (for development)
5. Rollback capability for failed migrations

Bonus: Implement migration version checking in health check endpoint.
"""

# Exercise 7: Multi-Tenant Database Architecture
"""
Implement a multi-tenant database architecture where each tenant has a separate database.

Design:
1. Tenant identification via API key or subdomain
2. Dynamic database connection switching based on tenant
3. Shared connection pool per tenant
4. Tenant isolation guarantees

Create endpoints that:
- Create a new tenant with a dedicated database
- Switch database connections based on tenant context
- Perform operations scoped to the tenant's database
"""

# Exercise 8: Database Performance Optimization
"""
Optimize your FastAPI database application for performance.

Implement:
1. Query optimization with proper indexing
2. N+1 query problem detection and solution
3. Database query caching with Redis (simulate with in-memory cache)
4. Pagination for large result sets
5. Lazy loading vs eager loading strategies

Create performance benchmarks and compare:
- Raw SQL vs ORM performance
- Connection pooling impact
- Caching effectiveness
"""

# Helper functions and templates (if needed)
def get_db_connection():
    """Template for database connection (to be implemented in exercises)"""
    pass

class BookModel:
    """Template for Book model (to be implemented in exercises)"""
    pass

if __name__ == "__main__":
    print("FastAPI Database Practice Exercises")
    print("Complete each exercise by implementing the described functionality.")
    print("Test your implementations using the FastAPI development server.")
    print("\nExercise Summary:")
    print("1. Basic SQLite CRUD")
    print("2. SQLAlchemy ORM Integration")
    print("3. Connection Pooling")
    print("4. Error Handling & Transactions")
    print("5. Async Database Operations")
    print("6. Database Migrations")
    print("7. Multi-Tenant Architecture")
    print("8. Performance Optimization")