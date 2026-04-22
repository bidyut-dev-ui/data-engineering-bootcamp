#!/usr/bin/env python3
"""
Week 19.5: Django for Data Applications - Practice Exercises
================================================================

This file contains practice exercises for Django fundamentals with a focus on
data applications and 8GB RAM optimization. These exercises are designed to
help you master Django concepts for data engineering roles.

IMPORTANT: These are practice exercises only. Solutions are deferred to focus
on educational framework completion first (interview questions and gotchas).

Learning Objectives:
1. Django project setup and configuration for data applications
2. Django models for structured data storage
3. Django REST Framework for data APIs
4. Database integration and optimization
5. Memory-constrained deployment strategies
6. Data visualization with Django templates
7. Authentication and authorization for data APIs
8. Production deployment with Docker

Exercises are progressive in difficulty:
- Beginner (1-3): Basic Django setup and models
- Intermediate (4-6): APIs, authentication, and optimization
- Advanced (7-10): Production deployment, monitoring, and scaling
"""

import os
import sys
from pathlib import Path

# Exercise 1: Django Project Setup with 8GB RAM Optimization
"""
Create a Django project named 'data_dashboard' with the following optimizations:
1. Use SQLite for development (lightweight) and PostgreSQL for production simulation
2. Configure settings to use file-based caching instead of Redis/Memcached
3. Set up environment variables for database configuration
4. Implement development/production settings separation
5. Configure static files for local serving (no CDN required)

Requirements:
- Create a virtual environment with requirements.txt
- Generate a manage.py file
- Create a docker-compose.yml for PostgreSQL
- Implement settings.py with environment-based configuration
- Test the development server runs with `--nothreading` flag

Expected Output:
- Django project structure with data_dashboard/ and manage.py
- Working development server on localhost:8000
- Environment variables for DATABASE_URL, DEBUG, SECRET_KEY
"""

# Exercise 2: Django Models for Data Engineering
"""
Design Django models for a data engineering application that tracks:
1. Data sources (name, type, connection_string, last_updated)
2. ETL jobs (name, source, destination, status, started_at, completed_at)
3. Data quality metrics (job_id, records_processed, errors_count, validation_score)
4. Performance metrics (job_id, execution_time, memory_usage, cpu_usage)

Requirements:
- Create appropriate relationships between models (ForeignKey, OneToOne, ManyToMany)
- Implement model methods for common operations (e.g., calculate_success_rate)
- Add custom managers for filtering by status or date ranges
- Implement __str__ methods for admin interface
- Create database migrations

Expected Output:
- models.py file with 4 models and their relationships
- Database migrations that can be applied
- Admin interface registration for all models
"""

# Exercise 3: Django REST Framework API for Data Operations
"""
Create REST APIs using Django REST Framework for the data engineering models:
1. CRUD endpoints for DataSource model
2. List and detail endpoints for ETLJob with filtering by status and date
3. POST endpoint to trigger a new ETL job
4. GET endpoint to retrieve data quality metrics for a specific job
5. Analytics endpoint that returns summary statistics (total jobs, success rate, avg execution time)

Requirements:
- Use ModelViewSet for DataSource
- Use GenericAPIView for custom endpoints
- Implement proper serializers with validation
- Add pagination for list endpoints
- Include authentication (TokenAuthentication) and permissions (IsAuthenticated)
- Write API documentation using DRF's built-in documentation

Expected Output:
- API endpoints accessible at /api/v1/
- Token-based authentication working
- Filtering and pagination functional
- API documentation at /api/v1/docs/
"""

# Exercise 4: Database Integration and Optimization for 8GB RAM
"""
Optimize database operations for memory-constrained environments:
1. Implement connection pooling for PostgreSQL
2. Create database indexes for frequently queried fields
3. Implement query optimization using select_related and prefetch_related
4. Add database-level constraints (unique, check constraints)
5. Implement bulk operations for data ingestion
6. Create database views for complex queries

Requirements:
- Analyze query performance using Django's connection.queries
- Implement database connection pooling with django-db-connection-pool
- Create migration for indexes and constraints
- Write optimized queries that minimize memory usage
- Implement chunked processing for large datasets

Expected Output:
- Optimized database queries with execution time < 100ms
- Connection pooling configuration
- Database indexes migration
- Bulk import function that processes 10k records with < 500MB memory
"""

# Exercise 5: Data Visualization with Django Templates
"""
Create a data visualization dashboard using Django templates:
1. Dashboard showing ETL job status (pie chart using Chart.js)
2. Time series chart of job execution times over the last 7 days
3. Data quality metrics table with color-coded status
4. Real-time updates using Django Channels or polling
5. Export functionality (CSV, JSON) for all charts

Requirements:
- Use Bootstrap 5 for responsive design
- Implement Chart.js for client-side charts
- Create template inheritance with base.html
- Add AJAX endpoints for chart data
- Implement server-side pagination for large datasets
- Add filtering by date range and job type

Expected Output:
- Dashboard accessible at /dashboard/
- Interactive charts with tooltips
- Real-time updates (every 30 seconds)
- Export functionality working
- Responsive design on mobile devices
"""

# Exercise 6: Authentication and Authorization for Data APIs
"""
Implement comprehensive authentication and authorization:
1. User registration and login with email/password
2. Token-based authentication for API endpoints
3. Role-based permissions (admin, data_engineer, viewer)
4. API rate limiting (100 requests/hour for anonymous, 1000/hour for authenticated)
5. Audit logging for all data modifications
6. Two-factor authentication for admin users

Requirements:
- Use Django's built-in authentication system
- Extend User model with custom profile (role, department)
- Implement permission classes for different roles
- Create middleware for audit logging
- Use django-rest-framework-simplejwt for JWT tokens
- Implement django-ratelimit for API rate limiting

Expected Output:
- User registration and login endpoints
- JWT token issuance and validation
- Role-based access control working
- Audit logs in database
- Rate limiting returning 429 status when exceeded
"""

# Exercise 7: Production Deployment with Docker
"""
Containerize the Django application for production deployment:
1. Create Dockerfile with multi-stage build
2. Configure docker-compose.yml with PostgreSQL, Redis (optional), and Django
3. Implement health checks for all services
4. Configure production settings (DEBUG=False, proper ALLOWED_HOSTS)
5. Set up logging to stdout for Docker logs
6. Implement database backup and restore procedures

Requirements:
- Docker image size < 500MB
- Use Python 3.9 slim image as base
- Implement entrypoint.sh for database migrations
- Configure environment variables for production
- Set up volume for static files
- Create .dockerignore to exclude unnecessary files

Expected Output:
- Docker container running on localhost:8000
- All services healthy in docker-compose
- Static files served via Nginx or WhiteNoise
- Database migrations applied on container start
- Logs accessible via docker-compose logs
"""

# Exercise 8: Performance Monitoring and Optimization
"""
Implement performance monitoring for the Django application:
1. Add Django Debug Toolbar for development
2. Implement custom middleware for request timing
3. Create performance metrics endpoint (/api/v1/metrics/)
4. Set up database query monitoring
5. Implement caching strategy for frequently accessed data
6. Add memory usage monitoring with psutil

Requirements:
- Request response time < 200ms for API endpoints
- Database query count < 10 per page load
- Implement caching with django-redis or file-based cache
- Create performance dashboard showing key metrics
- Set up alerts for performance degradation
- Implement database connection health checks

Expected Output:
- Performance metrics endpoint returning JSON data
- Django Debug Toolbar working in development
- Cached responses for static data
- Memory usage monitoring with thresholds
- Performance dashboard at /admin/performance/
"""

# Exercise 9: Data Pipeline Integration
"""
Integrate Django with external data pipelines:
1. Create Celery tasks for asynchronous ETL jobs
2. Implement message queue with Redis or RabbitMQ
3. Create API endpoint to trigger data pipeline execution
4. Implement webhook endpoints for pipeline status updates
5. Add retry logic with exponential backoff for failed jobs
6. Create dashboard showing pipeline execution status

Requirements:
- Celery worker processing tasks asynchronously
- Message queue configured and working
- Webhook authentication and validation
- Task status tracking in database
- Email notifications for failed jobs
- Pipeline dependency management

Expected Output:
- Asynchronous task execution working
- Message queue processing tasks
- Webhook endpoint accepting POST requests
- Pipeline status dashboard
- Email notifications for failures
"""

# Exercise 10: Security Hardening for Data Applications
"""
Implement security best practices for Django data applications:
1. SQL injection prevention (use Django ORM properly)
2. Cross-Site Scripting (XSS) protection
3. Cross-Site Request Forgery (CSRF) protection
4. Secure headers (CSP, HSTS, X-Frame-Options)
5. Input validation and sanitization
6. Secure file upload handling
7. API security (rate limiting, authentication, encryption)

Requirements:
- All security headers properly configured
- Input validation for all API endpoints
- Secure file upload with virus scanning (ClamAV)
- API rate limiting and throttling
- Regular security dependency updates
- Security audit logging

Expected Output:
- Security headers present in HTTP responses
- Input validation rejecting malicious payloads
- Secure file upload with size and type restrictions
- API security working (authentication required)
- Security audit logs in database
"""

# Main function to run exercises (placeholder - solutions deferred)
def main():
    """Main function to demonstrate exercise structure."""
    print("Django for Data Applications - Practice Exercises")
    print("=" * 60)
    print("This file contains 10 practice exercises for mastering Django")
    print("for data engineering applications with 8GB RAM optimization.")
    print("\nExercises cover:")
    print("1. Django project setup with 8GB RAM optimization")
    print("2. Django models for data engineering")
    print("3. Django REST Framework API for data operations")
    print("4. Database integration and optimization")
    print("5. Data visualization with Django templates")
    print("6. Authentication and authorization for data APIs")
    print("7. Production deployment with Docker")
    print("8. Performance monitoring and optimization")
    print("9. Data pipeline integration")
    print("10. Security hardening for data applications")
    print("\nNote: Solutions are deferred to focus on educational framework completion.")
    print("Complete these exercises to practice your Django skills for data applications.")

if __name__ == "__main__":
    main()