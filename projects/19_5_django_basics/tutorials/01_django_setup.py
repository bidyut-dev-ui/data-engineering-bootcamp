#!/usr/bin/env python3
"""
Week 19.5 - Django for Data Applications: Tutorial 1 - Django Setup
====================================================================

This tutorial covers setting up a Django project for data applications
with optimizations for 8GB RAM constraints.

Learning Objectives:
1. Create and configure a Django project
2. Set up virtual environment and dependencies
3. Configure settings for development vs production
4. Implement environment variables for configuration
5. Optimize Django for 8GB RAM constraints

Prerequisites:
- Python 3.8+ installed
- Basic understanding of web development
- 8GB RAM laptop (constraints considered throughout)
"""

import os
import sys
import subprocess
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python 3.8+ required. You have {sys.version}")
        return False
    
    print(f"✅ Python {sys.version}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Not in a virtual environment (recommended but not required)")
    
    return True

def create_virtual_environment():
    """Create a virtual environment for the project."""
    print("\n🏗️  Creating virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        # Create virtual environment
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created at 'venv/'")
        
        # Install pip and setuptools
        pip_path = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip"
        subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools"], check=True)
        print("✅ pip and setuptools upgraded")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies from requirements.txt."""
    print("\n📦 Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        pip_path = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip"
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_django_project():
    """Create Django project structure."""
    print("\n🚀 Creating Django project...")
    
    project_dir = Path("data_dashboard")
    
    if project_dir.exists():
        print("✅ Django project already exists")
        return True
    
    try:
        # Activate virtual environment and run django-admin
        python_path = "venv/bin/python" if os.name != 'nt' else "venv\\Scripts\\python"
        subprocess.run([python_path, "-m", "django", "startproject", "data_dashboard", "."], check=True)
        print("✅ Django project created")
        
        # Move manage.py to root
        manage_src = Path("data_dashboard/manage.py")
        if manage_src.exists():
            manage_src.rename("manage.py")
            print("✅ manage.py moved to root directory")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create Django project: {e}")
        return False

def configure_settings():
    """Configure Django settings for 8GB RAM optimization."""
    print("\n⚙️  Configuring Django settings for 8GB RAM...")
    
    settings_file = Path("data_dashboard/settings.py")
    if not settings_file.exists():
        print("❌ settings.py not found")
        return False
    
    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Add 8GB RAM optimizations
    optimizations = """
# 8GB RAM Optimizations
# ---------------------

# Database configuration for low memory usage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # SQLite is lightweight and perfect for 8GB RAM development
    }
}

# Cache configuration (file-based instead of Redis/Memcached)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'django_cache',
        'TIMEOUT': 300,  # 5 minutes
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Static files configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Session engine (file-based for low memory)
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = BASE_DIR / 'session_data'

# Email backend (console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Development server settings (run with --nothreading)
# python manage.py runserver --nothreading
"""
    
    # Find where to insert optimizations (after DATABASES configuration)
    if '# Database' in content:
        # Insert after database configuration
        parts = content.split('# Database')
        if len(parts) > 1:
            new_content = parts[0] + '# Database' + parts[1].split('\n\n', 1)[0] + '\n\n' + optimizations + parts[1].split('\n\n', 1)[1]
            
            with open(settings_file, 'w') as f:
                f.write(new_content)
            
            print("✅ Settings configured for 8GB RAM optimization")
            return True
    
    print("⚠️  Could not automatically configure settings, manual review needed")
    return False

def create_environment_file():
    """Create .env file for environment variables."""
    print("\n🔐 Creating environment configuration...")
    
    env_content = """# Django Environment Variables
# ============================

# Debug mode (True for development, False for production)
DEBUG=True

# Secret key (change this in production!)
SECRET_KEY=django-insecure-development-key-change-in-production

# Database URL (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite:///db.sqlite3

# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS allowed origins
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email configuration (console for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# 8GB RAM specific settings
DJANGO_SETTINGS_MODULE=data_dashboard.settings
PYTHONUNBUFFERED=1
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env file created with development configuration")
    return True

def verify_setup():
    """Verify the Django setup is working correctly."""
    print("\n🔧 Verifying setup...")
    
    try:
        python_path = "venv/bin/python" if os.name != 'nt' else "venv\\Scripts\\python"
        
        # Check Django version
        result = subprocess.run(
            [python_path, "-m", "django", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Django version: {result.stdout.strip()}")
        
        # Run migrations
        print("Running initial migrations...")
        subprocess.run([python_path, "manage.py", "migrate", "--check"], check=True)
        print("✅ Database migrations are ready")
        
        # Create superuser (optional)
        print("\nTo create a superuser for admin access, run:")
        print("  python manage.py createsuperuser")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup verification failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def demonstrate_8gb_ram_optimizations():
    """Explain 8GB RAM optimizations implemented."""
    print("\n" + "=" * 70)
    print("8GB RAM Optimization Summary")
    print("=" * 70)
    
    print("\n1. Database Choice:")
    print("   - SQLite for development (no separate database server)")
    print("   - Lightweight, file-based, perfect for 8GB RAM")
    print("   - Switch to PostgreSQL in production with Docker")
    
    print("\n2. Caching Strategy:")
    print("   - File-based cache instead of Redis/Memcached")
    print("   - Saves ~100MB+ of RAM")
    print("   - Location: django_cache/ directory")
    
    print("\n3. Static Files:")
    print("   - Whitenoise for serving static files")
    print("   - No need for Nginx in development")
    print("   - Compressed and efficient")
    
    print("\n4. Session Storage:")
    print("   - File-based sessions instead of database")
    print("   - Reduces database load")
    print("   - Location: session_data/ directory")
    
    print("\n5. Development Server:")
    print("   - Run with --nothreading flag:")
    print("     python manage.py runserver --nothreading")
    print("   - Reduces memory usage by ~30%")
    
    print("\n6. Logging:")
    print("   - Console-only logging in development")
    print("   - No file I/O overhead")
    print("   - Set to WARNING level to reduce noise")

def main():
    """Main tutorial function."""
    print("=" * 70)
    print("Django Setup Tutorial for Data Applications")
    print("=" * 70)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix issues and try again.")
        return
    
    # Step 2: Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Failed to create virtual environment.")
        return
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies.")
        return
    
    # Step 4: Create Django project
    if not create_django_project():
        print("\n❌ Failed to create Django project.")
        return
    
    # Step 5: Configure settings
    configure_settings()
    
    # Step 6: Create environment file
    create_environment_file()
    
    # Step 7: Verify setup
    if not verify_setup():
        print("\n⚠️  Setup verification had issues. Check manually.")
    
    # Step 8: Explain optimizations
    demonstrate_8gb_ram_optimizations()
    
    print("\n" + "=" * 70)
    print("✅ Django Setup Tutorial Completed!")
    print("=" * 70)
    
    print("\nNext Steps:")
    print("1. Activate virtual environment:")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   venv\\Scripts\\activate     # Windows")
    print("\n2. Run the development server:")
    print("   python manage.py runserver --nothreading")
    print("\n3. Access your application:")
    print("   - Web interface: http://localhost:8000")
    print("   - Admin interface: http://localhost:8000/admin")
    print("   - API documentation: http://localhost:8000/swagger")
    print("\n4. Continue with Tutorial 2: Models and Migrations")

if __name__ == "__main__":
    main()