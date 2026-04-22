# Django for Data Applications: Gotchas & Best Practices

## Overview
This document covers common pitfalls, optimization techniques, and best practices for using Django in data engineering applications, with special focus on 8GB RAM constraints.

## 🚨 Critical Gotchas

### 1. **Memory Management in Django**
**Gotcha**: Django's ORM can load entire querysets into memory, causing OOM errors on 8GB RAM.
**Solution**:
- Use `.iterator()` for large querysets
- Implement chunked processing with `Paginator`
- Set `QuerySet.iterator(chunk_size=1000)` for large datasets
- Avoid `list(queryset)` on large results

```python
# BAD: Loads all records into memory
all_users = list(User.objects.all())

# GOOD: Processes in chunks
for user in User.objects.all().iterator(chunk_size=1000):
    process_user(user)
```

### 2. **Database Connection Pooling**
**Gotcha**: Django creates new database connections for each request, causing connection exhaustion.
**Solution**:
- Use `django-db-connection-pool` for PostgreSQL
- Configure `CONN_MAX_AGE` appropriately (300 seconds for development)
- Monitor connection count with `django-db-connections`

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django_db_connection_pool.backends.postgresql',
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 20,
            'RECYCLE': 3600,
        }
    }
}
```

### 3. **N+1 Query Problem**
**Gotcha**: Accessing related objects in loops causes multiple database queries.
**Solution**:
- Use `select_related()` for ForeignKey and OneToOne relationships
- Use `prefetch_related()` for ManyToMany and reverse ForeignKey relationships
- Implement `django-debug-toolbar` to identify N+1 issues

```python
# BAD: N+1 queries
for job in ETLJob.objects.all():
    print(job.source.name)  # New query for each job

# GOOD: Single query with joins
for job in ETLJob.objects.select_related('source').all():
    print(job.source.name)  # No additional queries
```

### 4. **Migration Lock Issues**
**Gotcha**: Concurrent migration execution can cause database locks in production.
**Solution**:
- Use `--plan` to preview migrations before applying
- Implement zero-downtime migrations with `django-pg-zero-downtime-migrations`
- Schedule migrations during maintenance windows
- Test migrations on staging first

```bash
# Preview migrations
python manage.py migrate --plan

# Apply with zero downtime
python manage.py migrate --zero-downtime
```

### 5. **Static Files in Production**
**Gotcha**: Django's development server serves static files slowly; production requires separate serving.
**Solution**:
- Use `whitenoise` for simple static file serving
- Configure `STATICFILES_STORAGE` for CDN in production
- Run `collectstatic` during deployment
- Set proper cache headers for static assets

```python
# settings.py
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Before CommonMiddleware
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🏆 Best Practices

### 1. **Project Structure for Data Applications**
```bash
data_dashboard/
├── api/                          # REST API app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── dashboard/                    # Web interface app
│   ├── templates/
│   ├── static/
│   └── views.py
├── data_pipeline/               # ETL and data processing
│   ├── tasks.py                 # Celery tasks
│   ├── processors.py            # Data processors
│   └── validators.py            # Data validation
├── monitoring/                  # Monitoring and metrics
│   ├── metrics.py
│   └── alerts.py
└── utils/                       # Shared utilities
    ├── database.py
    ├── caching.py
    └── security.py
```

### 2. **Environment-Based Configuration**
```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment detection
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

# Load environment-specific settings
if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .development import *
```

### 3. **Database Optimization for 8GB RAM**
```python
# settings/database.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'data_dashboard'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 300,  # Connection reuse
        'OPTIONS': {
            'connect_timeout': 10,
            'application_name': 'data_dashboard',
        }
    }
}

# Query optimization
DJANGO_QUERY_DEBUG = os.getenv('DJANGO_QUERY_DEBUG', 'False') == 'True'
if DJANGO_QUERY_DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
```

### 4. **Caching Strategy**
```python
# Multi-level caching for 8GB RAM
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,  # Remove 1/3 of entries when max reached
        }
    },
    'file_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 86400,  # 24 hours for static data
    }
}

# Cache usage patterns
from django.core.cache import cache

# Cache expensive queries
def get_data_summary():
    cache_key = 'data_summary_v1'
    result = cache.get(cache_key)
    if result is None:
        result = expensive_calculation()
        cache.set(cache_key, result, timeout=3600)  # 1 hour
    return result
```

### 5. **API Design for Data Applications**
```python
# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum

class DataSourceViewSet(ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Custom endpoint for data source statistics"""
        stats = {
            'total_sources': self.queryset.count(),
            'by_type': dict(self.queryset.values_list('type').annotate(count=Count('id'))),
            'avg_update_frequency': self.queryset.aggregate(
                avg=Avg('update_frequency_hours')
            )['avg'],
        }
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test connection to data source"""
        source = self.get_object()
        is_connected = source.test_connection()
        return Response({'connected': is_connected})
```

### 6. **Authentication and Security**
```python
# JWT Authentication with refresh tokens
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',
        'anon': '100/hour',
    }
}

# Secure headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
```

### 7. **Monitoring and Logging**
```python
# Structured logging for data applications
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/data_dashboard.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'data_pipeline': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### 8. **Performance Optimization Checklist**
- [ ] **Database**: Indexes on frequently queried fields
- [ ] **Queries**: Use `select_related` and `prefetch_related`
- [ ] **Caching**: Implement multi-level caching strategy
- [ ] **Static files**: Use CDN or whitenoise with compression
- [ ] **Middleware**: Remove unused middleware in production
- [ ] **Templates**: Use template fragment caching
- [ ] **API**: Implement pagination and filtering
- [ ] **Monitoring**: Set up performance metrics and alerts

### 9. **Deployment Checklist for 8GB RAM**
- [ ] **Memory limits**: Set container memory limits in docker-compose
- [ ] **Worker processes**: Limit Gunicorn workers (2-4 for 8GB RAM)
- [ ] **Database**: Use connection pooling with appropriate pool size
- [ ] **Caching**: Use file-based or Redis caching (if available)
- [ ] **Static files**: Pre-compress and CDN for production
- [ ] **Logging**: Rotate logs to prevent disk space issues
- [ ] **Monitoring**: Set up memory usage alerts
- [ ] **Backups**: Regular database backups with retention policy

### 10. **Testing Strategy**
```python
# tests/test_performance.py
import time
from django.test import TestCase
from django.db import connection

class PerformanceTests(TestCase):
    def test_query_performance(self):
        """Ensure queries execute within acceptable time limits"""
        start_time = time.time()
        
        # Execute complex query
        results = DataSource.objects.filter(
            is_active=True
        ).select_related('owner').prefetch_related('jobs')
        
        list(results)  # Force evaluation
        
        execution_time = time.time() - start_time
        self.assertLess(execution_time, 1.0)  # Should complete in < 1 second
        
        # Check query count
        self.assertLess(len(connection.queries), 10)
```

## 🔧 Troubleshooting Common Issues

### 1. **High Memory Usage**
**Symptoms**: Application crashes with OOM errors, slow response times
**Diagnosis**:
```bash
# Monitor memory usage
docker stats
ps aux | grep python
free -h

# Profile Django memory
import tracemalloc
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

**Solutions**:
- Reduce Gunicorn worker count
- Implement query optimization
- Use chunked processing for large datasets
- Add memory limits to Docker containers

### 2. **Database Performance Issues**
**Symptoms**: Slow API responses, high database CPU usage
**Diagnosis**:
```sql
-- Check slow queries
EXPLAIN ANALYZE SELECT * FROM api_datasource WHERE is_active = true;

-- Check index usage
SELECT * FROM pg_stat_user_indexes;
```

**Solutions**:
- Add missing indexes
- Optimize query patterns
- Implement database connection pooling
- Use read replicas for heavy read workloads

### 3. **API Rate Limiting Issues**
**Symptoms**: 429 errors, inconsistent API performance
**Diagnosis**:
```python
# Check rate limit headers
import requests
response = requests.get('http://localhost:8000/api/v1/sources/')
print(response.headers.get('X-RateLimit-Limit'))
print(response.headers.get('X-RateLimit-Remaining'))
```

**Solutions**:
- Adjust throttle rates based on usage patterns
- Implement caching for expensive endpoints
- Use API keys with different rate limits
- Monitor and alert on rate limit breaches

## 📈 Performance Benchmarks (8GB RAM)

| Operation | Target Performance | Optimization Tips |
|-----------|-------------------|-------------------|
| API Response Time | < 200ms | Use caching, optimize queries |
| Database Query | < 100ms | Add indexes, use connection pooling |
| Large Data Export | < 30s for 10k records | Use streaming responses, chunked processing |
| Memory Usage | < 2GB per container | Limit worker processes, optimize data structures |
| Concurrent Users | 50-100 users | Implement caching, use CDN for static files |

## 🚀 Production Readiness Checklist

### Before Deployment
- [ ] All tests passing (unit, integration, performance)
- [ ] Security scan completed (no critical vulnerabilities)
- [ ] Performance benchmarks meet targets
- [ ] Database migrations tested and backed up
- [ ] Environment variables configured
- [ ] Monitoring and alerting set up
- [ ] Disaster recovery plan documented

### After Deployment
- [ ] Application health checks passing
- [ ] Performance metrics within expected ranges
- [ ] Error rate < 1%
- [ ] Database connections stable
- [ ] Cache hit rate > 80%
- [ ] User authentication working
- [ ] Data pipelines executing successfully

## 🔗 Additional Resources

1. **Django Documentation**: https://docs.djangoproject.com/
2. **Django REST Framework**: https://www.django-rest-framework.org/
3. **Django Deployment Checklist**: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
4. **PostgreSQL Optimization**: https://www.postgresql.org/docs/current/performance-tips.html
5. **8GB RAM Optimization Guide**: https://github.com/django/django/wiki/8GB-RAM-Optimization

---

*Last Updated: 2026-04-22*  
*For issues or suggestions, refer to the project README or create an issue in the repository.*