# Week 19.5: Django for Data Applications

## 🎯 Learning Objectives

By the end of this week, you will be able to:

1. **Set up a Django project** with data engineering best practices
2. **Design Django models** for structured data storage
3. **Build REST APIs** with Django REST Framework for data access
4. **Integrate Django with databases** (PostgreSQL, SQLite) and data pipelines
5. **Create data visualization dashboards** using Django templates
6. **Implement authentication and authorization** for data APIs
7. **Deploy a data application** with Docker and production settings
8. **Optimize Django for 8GB RAM** constraints

## 🖥️ Hardware Constraints & Configuration

This project is designed to run on **8GB RAM laptops with zero GPU**. Key optimizations:

- **Database**: SQLite for development (lightweight), PostgreSQL for production simulation
- **Memory**: Django development server with `--nothreading` to reduce memory usage
- **Caching**: Use file-based cache instead of Redis/Memcached
- **Static files**: Serve locally during development, no CDN required
- **Concurrency**: Limit to 2 worker processes in production simulation

## 📁 Project Structure

```
19_5_django_basics/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Docker setup for PostgreSQL
├── manage.py                          # Django management script
├── data_dashboard/                    # Main Django project
│   ├── __init__.py
│   ├── settings.py                    # Project settings (dev/prod)
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
├── api/                               # Django app for REST API
│   ├── __init__.py
│   ├── admin.py                       # Admin interface
│   ├── apps.py
│   ├── models.py                      # Data models
│   ├── serializers.py                 # DRF serializers
│   ├── views.py                       # API views
│   ├── urls.py                        # App URLs
│   └── tests.py
├── dashboard/                         # Django app for web interface
│   ├── __init__.py
│   ├── views.py                       # Template views
│   ├── urls.py                        # Dashboard URLs
│   ├── templates/                     # HTML templates
│   │   └── dashboard/
│   │       ├── index.html
│   │       ├── charts.html
│   │       └── data_table.html
│   └── static/                        # CSS/JS assets
│       └── dashboard/
├── data_loader/                       # Data ingestion and ETL
│   ├── __init__.py
│   ├── management/
│   │   └── commands/
│   │       └── load_sample_data.py    # Custom management command
│   └── utils.py                       # Data processing utilities
├── tutorials/                         # Step-by-step tutorials
│   ├── 01_django_setup.py            # Project setup and configuration
│   ├── 02_models_and_migrations.py   # Database models
│   ├── 03_rest_api.py                # Building REST APIs
│   ├── 04_data_visualization.py      # Charts and dashboards
│   ├── 05_integration.py             # Integrating with data pipelines
│   └── 06_deployment.py              # Docker and production
├── sample_data/                       # Sample datasets
│   ├── sales_data.csv
│   ├── user_activity.json
│   └── sensor_readings.parquet
├── GOTCHAS_BEST_PRACTICES.md          # Common pitfalls and solutions
└── INTERVIEW_QUESTIONS.md             # Django interview preparation
```

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
cd data-engineering-bootcamp/projects/19_5_django_basics
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Database
```bash
# Using SQLite (default, no setup needed)
python manage.py migrate

# OR using PostgreSQL with Docker
docker-compose up -d postgres
python manage.py migrate
```

### 4. Load Sample Data
```bash
python manage.py load_sample_data
```

### 5. Run Development Server
```bash
python manage.py runserver --nothreading
```

### 6. Access the Application
- **Web Dashboard**: http://localhost:8000/
- **REST API**: http://localhost:8000/api/
- **Admin Interface**: http://localhost:8000/admin/ (create superuser first)

## 📚 Tutorials

### Tutorial 1: Django Setup for Data Applications
Learn to configure Django with data engineering best practices, including settings for development vs production, environment variables, and project structure.

### Tutorial 2: Models and Migrations for Structured Data
Design Django models for various data types (time-series, relational, document), create migrations, and optimize database queries for large datasets.

### Tutorial 3: Building REST APIs with Django REST Framework
Create RESTful APIs for data access, implement filtering, pagination, and serialization for efficient data transfer.

### Tutorial 4: Data Visualization with Django Templates
Build interactive dashboards with charts (using Chart.js), data tables, and real-time updates without heavy JavaScript frameworks.

### Tutorial 5: Integrating Django with Data Pipelines
Connect Django to external data sources (APIs, databases, files), schedule data updates with Celery (or Django-Q for lightweight alternative), and handle data validation.

### Tutorial 6: Deployment and Production Considerations
Containerize with Docker, configure production settings (security, performance), and deploy to Heroku/Render (free tiers).

## 🎯 Real-World Application

This project teaches you to build **data applications** - web applications that:
- **Expose data** through APIs for other services
- **Visualize data** for business intelligence
- **Ingest and process data** from various sources
- **Provide data management interfaces** for non-technical users

**Example use cases**:
- Internal dashboard for monitoring data pipeline metrics
- Customer-facing portal for data exports/reports
- Data annotation tool for ML training data
- API gateway for data science models

## 📈 Expected Outcomes

After completing this project, you will have:

1. **A fully functional data dashboard** with:
   - REST API for programmatic data access
   - Web interface with charts and tables
   - Admin interface for data management
   - Sample datasets loaded and queryable

2. **Understanding of Django architecture** for data applications:
   - Model-View-Template (MVT) pattern
   - Django REST Framework for APIs
   - Database optimization techniques
   - Deployment strategies

3. **Practical skills** to:
   - Design data models in Django
   - Build and document REST APIs
   - Create data visualization interfaces
   - Integrate with existing data infrastructure

## 🚨 Important Notes for 8GB RAM

1. **Database Choice**: Use SQLite for development to minimize memory usage
2. **Concurrency**: Run Django with `--nothreading` flag during development
3. **Caching**: Implement Django's built-in cache framework with file backend
4. **Static Files**: Use `whitenoise` for serving static files without Nginx
5. **Background Tasks**: Use Django-Q instead of Celery for lighter memory footprint
6. **Monitoring**: Use Django Debug Toolbar only when needed

## 🔗 Integration with Other Projects

This Django project integrates with several other bootcamp projects:

- **FastAPI projects (Weeks 9-10)**: Compare Django REST Framework vs FastAPI
- **Database projects (Weeks 4-7)**: Use PostgreSQL/MySQL instead of SQLite
- **ML projects (Weeks 13-16)**: Expose ML models through Django APIs
- **Capstone project (Week 17)**: Use Django as the frontend for your data platform

## 📚 Further Learning

1. **Official Documentation**:
   - [Django Documentation](https://docs.djangoproject.com/)
   - [Django REST Framework](https://www.django-rest-framework.org/)
   - [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

2. **Books**:
   - "Two Scoops of Django" by Daniel and Audrey Feldroy
   - "Django for APIs" by William S. Vincent

3. **Courses**:
   - [Django for Everybody (Coursera)](https://www.coursera.org/specializations/django)
   - [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

4. **Community**:
   - [Django Forum](https://forum.djangoproject.com/)
   - [Django Subreddit](https://www.reddit.com/r/django/)

---

**Ready to start?** Begin with `tutorials/01_django_setup.py` to set up your development environment!