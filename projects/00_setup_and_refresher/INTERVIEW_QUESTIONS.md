# Setup & Refresher Interview Questions

## 📋 Table of Contents
1. [Environment Setup Fundamentals](#environment-setup-fundamentals)
2. [Virtual Environments & Dependency Management](#virtual-environments--dependency-management)
3. [Docker & Containerization](#docker--containerization)
4. [Memory & Performance Optimization](#memory--performance-optimization)
5. [Troubleshooting & Debugging](#troubleshooting--debugging)
6. [Best Practices & Security](#best-practices--security)
7. [Scenario-Based Questions](#scenario-based-questions)

---

## Environment Setup Fundamentals

### 1. **Why is proper environment setup critical for data engineering projects?**
**Answer:** Proper environment setup ensures:
- **Reproducibility**: Same code works across different machines/environments
- **Isolation**: Prevents dependency conflicts between projects
- **Consistency**: All team members use identical tool versions
- **Performance**: Optimized settings for data processing tasks
- **Debugging**: Easier to identify environment-specific issues

**Follow-up:** What are the minimum requirements for a data engineering environment?

### 2. **Explain the difference between system Python and virtual environment Python**
**Answer:**
- **System Python**: Installed globally on the OS, used by system tools
- **Virtual Environment Python**: Isolated copy with its own site-packages
- **Key differences**:
  - Virtual environments have separate package installations
  - System Python should not be modified (risk of breaking OS tools)
  - Virtual environments allow different Python versions per project
  - Virtual environments are disposable and recreatable

### 3. **How would you verify if a development environment is ready for data engineering?**
**Answer:** Create a checklist script that verifies:
```python
# Check Python version (3.10+)
import sys
assert sys.version_info >= (3, 10)

# Check essential tools
import shutil
assert shutil.which("git") is not None
assert shutil.which("docker") is not None

# Check disk space (min 5GB free)
import shutil
total, used, free = shutil.disk_usage("/")
assert free > 5 * 1024**3  # 5GB in bytes

# Check memory (min 8GB RAM)
import psutil
assert psutil.virtual_memory().total >= 8 * 1024**3  # 8GB
```

### 4. **What are the common pitfalls when setting up Python on different operating systems?**
**Answer:**
- **Windows**: Path issues, line endings (CRLF vs LF), permission problems
- **Linux/Mac**: Python 2 vs Python 3 confusion, package manager conflicts
- **WSL2**: Docker integration, filesystem performance, Windows firewall issues
- **All**: Environment variables, PATH configuration, Unicode/encoding issues

---

## Virtual Environments & Dependency Management

### 5. **Compare `venv`, `virtualenv`, `conda`, and `pipenv` for Python environment management**
**Answer:**
| Tool | Pros | Cons | Best For |
|------|------|------|----------|
| **venv** | Built-in, simple, lightweight | No dependency resolution | Basic projects, Python 3.3+ |
| **virtualenv** | Works with Python 2, more features | External dependency | Legacy projects |
| **conda** | Cross-language, binary packages | Large, slower, different ecosystem | Data science, ML projects |
| **pipenv** | Dependency resolution, lock files | Slower, less adoption | Application development |

### 6. **How does `requirements.txt` differ from `Pipfile`?**
**Answer:**
- **requirements.txt**: Simple text file listing packages with optional version constraints
- **Pipfile**: TOML format with separate sections for packages and dev-packages, includes source URLs
- **Key difference**: Pipfile supports dependency resolution and generates Pipfile.lock for reproducible builds

### 7. **Explain dependency pinning and why it's important**
**Answer:** Dependency pinning means specifying exact package versions:
```txt
# Good: Pinned versions
pandas==2.1.0
numpy==1.24.0

# Bad: Floating versions (can break)
pandas>=2.0.0
numpy
```
**Importance:**
- Prevents breaking changes from updates
- Ensures reproducible builds
- Makes debugging easier (known working versions)
- Required for production deployments

### 8. **How would you handle conflicting dependencies in a project?**
**Answer:**
1. **Identify conflict**: `pip check` or dependency tree analysis
2. **Isolate**: Use virtual environments for each conflicting component
3. **Version negotiation**: Find compatible versions that satisfy all requirements
4. **Dependency resolution tools**: Use `pip-tools`, `poetry`, or `conda`
5. **Refactor**: Consider if architecture changes can eliminate conflict
6. **Document**: Clearly document the conflict and chosen solution

---

## Docker & Containerization

### 9. **Why use Docker for data engineering environments?**
**Answer:** Docker provides:
- **Consistency**: Same environment everywhere (dev, test, prod)
- **Isolation**: No "works on my machine" problems
- **Portability**: Easy to share and deploy
- **Resource control**: Limit CPU/memory usage
- **Versioning**: Docker images are versioned artifacts
- **Scalability**: Easy to scale with orchestration tools

### 10. **What's the difference between a Docker image and a container?**
**Answer:**
- **Image**: Read-only template with application code and dependencies (like a class)
- **Container**: Running instance of an image (like an object)
- **Analogy**: Image = recipe, Container = cooked meal

### 11. **How would you optimize a Docker image for data engineering?**
**Answer:**
```dockerfile
# Multi-stage build to reduce size
FROM python:3.10-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Set memory limits
ENV PYTHONMALLOC=malloc
ENV MALLOC_ARENA_MAX=2

# Non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser app/ /app
WORKDIR /app
```

### 12. **Explain Docker volumes and when to use them in data engineering**
**Answer:** Docker volumes persist data outside containers:
- **Use cases**:
  - Database data (PostgreSQL, MySQL)
  - Shared datasets between containers
  - Log files that need to survive container restarts
  - Configuration files that might need updates
- **Types**: Named volumes (managed by Docker), bind mounts (host paths), tmpfs (memory)

---

## Memory & Performance Optimization

### 13. **How would you optimize Python for 8GB RAM systems?**
**Answer:**
```python
# Environment variables
import os
os.environ['PYTHONMALLOC'] = 'malloc'  # Use system malloc
os.environ['MALLOC_ARENA_MAX'] = '2'   # Reduce memory fragmentation
os.environ['OMP_NUM_THREADS'] = '2'    # Limit parallel threads

# Pandas optimizations
import pandas as pd
df = pd.read_csv('large.csv', 
                 dtype={'category_col': 'category'},  # Reduce memory
                 usecols=['needed_cols'],            # Load only needed columns
                 chunksize=10000)                    # Process in chunks
```

### 14. **What are memory-mapped files and when should they be used?**
**Answer:** Memory-mapped files use virtual memory to access files:
- **How it works**: File appears as memory array, OS handles paging
- **Benefits**: Efficient for large files, shared memory between processes
- **Use cases**: Large datasets that don't fit in RAM, shared read-only data
- **Python**: `mmap` module, `numpy.memmap`, `pandas.read_csv(..., memory_map=True)`

### 15. **Explain garbage collection in Python and how to optimize it**
**Answer:**
- **Reference counting**: Primary mechanism, automatic
- **Generational GC**: For cyclic references, runs periodically
- **Optimization techniques**:
  ```python
  import gc
  
  # Manual control
  gc.disable()  # For performance-critical sections
  gc.enable()
  
  # Force collection
  gc.collect()
  
  # Tune thresholds
  gc.set_threshold(700, 10, 10)
  
  # Delete large objects explicitly
  del large_dataframe
  gc.collect()
  ```

### 16. **How would you monitor memory usage in a Python data pipeline?**
**Answer:**
```python
import psutil
import resource
import tracemalloc

def monitor_memory():
    # System memory
    process = psutil.Process()
    memory_info = process.memory_info()
    
    # Python memory tracking
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    
    # Your code here
    
    snapshot2 = tracemalloc.take_snapshot()
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    # Resource limits
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    
    return {
        'rss_mb': memory_info.rss / 1024**2,
        'vms_mb': memory_info.vms / 1024**2,
        'memory_leaks': top_stats[:10],
        'memory_limit_mb': soft / 1024**2 if soft != -1 else 'unlimited'
    }
```

---

## Troubleshooting & Debugging

### 17. **A team member says "it works on my machine" but fails in production. How do you debug?**
**Answer:** Systematic approach:
1. **Environment comparison**: Document all differences (OS, Python version, packages, environment variables)
2. **Reproduce locally**: Use Docker to match production environment
3. **Check logs**: Application logs, system logs, Docker logs
4. **Resource differences**: Memory, CPU, disk space, network
5. **Data differences**: Test with same input data
6. **Permissions**: File permissions, database permissions
7. **Network**: Firewall, proxies, DNS

### 18. **How would you debug a "Killed" process (often OOM killer)?**
**Answer:**
1. **Check system logs**: `dmesg | grep -i kill` or `journalctl -k`
2. **Monitor memory**: Use `top`, `htop`, or `ps aux --sort=-%mem`
3. **Reproduce with limits**: `ulimit -v $((8 * 1024 * 1024))` (8GB virtual memory)
4. **Use memory profiler**: `memory_profiler`, `filprofiler`, `py-spy`
5. **Add swap**: Temporary solution while fixing memory leak
6. **Implement chunking**: Process data in smaller batches

### 19. **What would you do if `pip install` fails with compilation errors?**
**Answer:**
1. **Install build tools**: `apt-get install build-essential python3-dev`
2. **Use wheels**: `pip install --only-binary :all: package-name`
3. **Alternative package**: Look for pre-compiled version or conda package
4. **Docker approach**: Use pre-built Docker image with packages installed
5. **Version downgrade**: Try older version that might have wheels
6. **Build from source**: As last resort, with proper dependencies

### 20. **How do you handle port conflicts when starting services?**
**Answer:**
```bash
# Find process using port
sudo lsof -i :5432
sudo netstat -tulpn | grep :5432
ss -tulpn | grep :5432

# Solutions:
# 1. Stop conflicting service
sudo systemctl stop postgresql

# 2. Change port in your service
docker run -p 5433:5432 postgres

# 3. Kill process (if safe)
sudo kill -9 <PID>

# 4. Use different port entirely
```

---

## Best Practices & Security

### 21. **What security considerations are important for data engineering environments?**
**Answer:**
- **Secrets management**: Never commit passwords/API keys to git
- **Network security**: Firewall rules, VPN for database access
- **Principle of least privilege**: Minimal permissions for services
- **Regular updates**: Security patches for OS and packages
- **Audit logging**: Track who accessed what data
- **Data encryption**: At rest and in transit
- **Access controls**: RBAC for data and tools

### 22. **How would you set up a development environment for a team?**
**Answer:**
1. **Documentation**: Clear setup instructions in README.md
2. **Automation**: `setup.sh` script or `Makefile` for common tasks
3. **Containerization**: Docker Compose for all services
4. **Version control**: `.gitignore` for environment-specific files
5. **Code quality**: Pre-commit hooks, linters, formatters
6. **Testing**: Unit tests that run in CI/CD
7. **Monitoring**: Basic health checks for services

### 23. **What's your approach to keeping development environments in sync?**
**Answer:**
- **Infrastructure as Code**: Dockerfiles, docker-compose.yml, Terraform
- **Version pinning**: Exact versions in requirements.txt/Pipfile.lock
- **Regular updates**: Scheduled dependency updates (Dependabot, Renovate)
- **Automated testing**: CI/CD pipeline tests all environment changes
- **Documentation drift**: Regular review of setup instructions
- **Developer onboarding**: Standardized checklist for new team members

### 24. **How do you balance reproducibility with development speed?**
**Answer:**
- **Development**: Fast iterations with hot reload, debug tools
- **Testing/Staging**: Match production as closely as possible
- **Production**: Fully reproducible, versioned, audited
- **Tools**: Use same Docker base image across environments
- **Configuration**: Environment variables for differences
- **Local overrides**: Allow developers to override settings locally

---

## Scenario-Based Questions

### 25. **You need to set up a new data engineering project for a team of 5. What's your plan?**
**Answer:**
1. **Infrastructure**: Docker Compose with PostgreSQL, Redis, Airflow
2. **Development**: VS Code dev containers or local virtual environments
3. **Version control**: Git with branching strategy, PR reviews
4. **CI/CD**: GitHub Actions for testing and deployment
5. **Documentation**: README.md, architecture diagrams, runbooks
6. **Monitoring**: Basic logging, error tracking, performance metrics
7. **Onboarding**: Setup script, example data, tutorial

### 26. **A critical data pipeline is failing due to memory issues. How do you triage?**
**Answer:**
1. **Immediate**: Add swap space, restart with memory limits
2. **Diagnose**: Memory profiler to identify leak/chunk to optimize
3. **Optimize**: Implement chunking, use more efficient data structures
4. **Scale**: Consider if hardware upgrade is needed
5. **Prevent**: Add memory monitoring and alerts
6. **Document**: Root cause analysis and prevention plan

### 27. **You're inheriting a project with undocumented environment setup. How do you proceed?**
**Answer:**
1. **Reverse engineer**: `pip freeze`, `docker history`, configuration files
2. **Document**: Create setup instructions as you discover requirements
3. **Automate**: Create setup script from discovered requirements
4. **Containerize**: Dockerize to capture environment exactly
5. **Test**: Verify setup works from scratch
6. **Improve**: Add missing best practices (security, monitoring, etc.)

### 28. **How would you migrate a project from Conda to Docker?**
**Answer:**
1. **Analyze**: Document all Conda packages and versions
2. **Dockerize**: Create Dockerfile with equivalent apt/pip installs
3. **Test**: Verify all functionality works in Docker
4. **Optimize**: Multi-stage builds, reduce image size
5. **Document**: Update setup instructions for Docker
6. **Transition**: Parallel run, then switch team to Docker
7. **Cleanup**: Remove Conda files from project

---

## 🎯 Quick Assessment Questions

### For Junior Candidates:
1. What command creates a Python virtual environment?
2. How do you check if Docker is running?
3. What does `requirements.txt` contain?
4. How would you install a Python package?

### For Mid-Level Candidates:
1. How do you handle conflicting Python package versions?
2. What are the benefits of Docker for data engineering?
3. How would you debug a memory leak in Python?
4. What's the difference between `COPY` and `ADD` in Dockerfile?

### For Senior Candidates:
1. Design a multi-environment setup (dev, staging, prod)
2. How would you implement secrets management?
3. Design a disaster recovery plan for development environment
4. How do you ensure environment parity across team members?

---

## 📚 Resources for Further Learning

1. **Python Virtual Environments**: [Python venv documentation](https://docs.python.org/3/library/venv.html)
2. **Docker Best Practices**: [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
3. **Memory Optimization**: [Python memory management](https://realpython.com/python-memory-management/)
4. **Security**: [OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
5. **Performance**: [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)