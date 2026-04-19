# Setup & Refresher: Gotchas and Best Practices

## 🚨 Common Gotchas for Environment Setup

### 1. **Virtual Environment Activation Issues**
**❌ DON'T:**
```bash
# Wrong: Forgetting to activate virtual environment
python3 -m venv venv
python script.py  # Uses system Python, not virtual environment
```

**✅ DO:**
```bash
# Correct: Always activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
python script.py          # Now uses virtual environment Python
```

**Why:** Virtual environments isolate dependencies. Without activation, you use system Python which may have different versions or packages.

### 2. **Python Version Mismatch**
**❌ DON'T:**
```bash
# Wrong: Assuming 'python' refers to Python 3
python --version  # Might be Python 2.7 on some systems
```

**✅ DO:**
```bash
# Correct: Explicitly use python3
python3 --version
python3 -m venv venv
```

**Why:** Some systems have both Python 2 and Python 3 installed. Data engineering requires Python 3.10+.

### 3. **Docker Not Running in WSL2**
**❌ DON'T:**
```bash
# Wrong: Docker not properly configured for WSL2
docker ps  # Error: Cannot connect to Docker daemon
```

**✅ DO:**
```bash
# Correct: Ensure Docker Desktop is running and exposed to WSL2
# 1. Start Docker Desktop on Windows
# 2. In WSL2, check Docker is accessible
docker --version
docker run hello-world
```

**Why:** Docker Desktop must be running on Windows and configured to expose daemon to WSL2.

### 4. **Insufficient Disk Space for Data Processing**
**❌ DON'T:**
```bash
# Wrong: Not checking disk space before large operations
python process_large_dataset.py  # Fails halfway due to disk full
```

**✅ DO:**
```bash
# Correct: Check disk space first
df -h  # Check available space
# Ensure at least 5GB free for data engineering tasks
```

**Why:** Data engineering involves large datasets. Running out of disk space mid-process corrupts data.

### 5. **Memory Issues on 8GB RAM Laptops**
**❌ DON'T:**
```python
# Wrong: Loading entire dataset into memory
import pandas as pd
df = pd.read_csv("10gb_file.csv")  # Crashes on 8GB RAM
```

**✅ DO:**
```python
# Correct: Use chunking or memory-efficient techniques
import pandas as pd
chunk_size = 10000
for chunk in pd.read_csv("10gb_file.csv", chunksize=chunk_size):
    process_chunk(chunk)
```

**Why:** 8GB RAM is limited for large datasets. Use streaming/chunking approaches.

## 🏆 Best Practices for Data Engineering Setup

### 1. **Systematic Environment Verification**
```python
# Create a comprehensive check script
import sys
import shutil
import subprocess

def check_environment():
    """Verify all required tools and versions"""
    checks = {
        "Python 3.10+": sys.version_info >= (3, 10),
        "Git": shutil.which("git") is not None,
        "Docker": shutil.which("docker") is not None,
        "Virtual Environment": "VIRTUAL_ENV" in os.environ,
    }
    return checks
```

### 2. **Automated Setup Script**
```bash
#!/bin/bash
# setup.sh - Automated environment setup
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. **Memory Optimization for 8GB RAM**
```bash
# Set environment variables for memory optimization
export PYTHONMALLOC=malloc  # Use system malloc instead of pymalloc
export MALLOC_ARENA_MAX=2   # Reduce memory fragmentation
export OMP_NUM_THREADS=2    # Limit parallel threads
```

### 4. **Docker Memory Limits**
```yaml
# docker-compose.yml - Set memory limits
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    deploy:
      resources:
        limits:
          memory: 2G  # Limit container memory
```

### 5. **Version Pinning for Reproducibility**
```txt
# requirements.txt - Pin versions
pandas==2.1.0
numpy==1.24.0
sqlalchemy==2.0.0
docker==6.1.0
```

## 🔧 Troubleshooting Common Issues

### Issue 1: "Command not found" for python3
**Solution:**
```bash
# Install Python 3.10+ if missing
sudo apt update
sudo apt install python3.10 python3.10-venv
```

### Issue 2: Docker permission denied
**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Issue 3: Virtual environment not working
**Solution:**
```bash
# Recreate virtual environment
deactivate  # If active
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Issue 4: Port conflicts (e.g., port 5432 already in use)
**Solution:**
```bash
# Find process using port
sudo lsof -i :5432
# Kill process or use different port
```

### Issue 5: Out of memory errors
**Solution:**
```bash
# Check memory usage
free -h
# Kill unnecessary processes
# Use swap if available
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📊 Performance Optimization Checklist

### For 8GB RAM Systems:
- [ ] Use `pandas.read_csv(chunksize=10000)` for large files
- [ ] Set `dtype` parameter to reduce memory usage
- [ ] Use `category` dtype for string columns with few unique values
- [ ] Enable `low_memory=False` only when necessary
- [ ] Use `del` to delete unused variables
- [ ] Call `gc.collect()` after large operations

### Docker Configuration:
- [ ] Set memory limits in docker-compose.yml
- [ ] Use `.dockerignore` to exclude unnecessary files
- [ ] Use multi-stage builds to reduce image size
- [ ] Set appropriate CPU limits

### Python Environment:
- [ ] Use virtual environments for each project
- [ ] Pin package versions in requirements.txt
- [ ] Regularly update security patches
- [ ] Use `pip-tools` for dependency management

## 🎯 Quick Reference Commands

### Environment Check:
```bash
# Check Python version
python3 --version

# Check available tools
which git docker python3

# Check disk space
df -h .

# Check memory
free -h
```

### Virtual Environment:
```bash
# Create
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

### Docker:
```bash
# Check Docker is running
docker ps

# Run test container
docker run hello-world

# Clean up unused containers/images
docker system prune -a
```

## 🚀 Next Steps After Setup

1. **Verify Setup**: Run `python check_env.py` to confirm everything works
2. **Test Memory Limits**: Process a sample dataset to ensure no memory issues
3. **Backup Configuration**: Save your environment setup for future reference
4. **Document Issues**: Keep notes of any problems and solutions for future troubleshooting

Remember: A properly configured environment saves hours of debugging later. Take the time to set it up correctly!