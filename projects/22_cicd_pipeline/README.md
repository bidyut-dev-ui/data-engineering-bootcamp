# Week 30: CI/CD & Deployment Automation

**Goal**: Learn to automate testing, building, and deployment of data applications using GitHub Actions and Docker.

## Scenario
Your team is deploying code multiple times per day. Manual testing and deployment is error-prone and slow. You need to automate the entire pipeline from code commit to production deployment.

## Concepts Covered
1. **Continuous Integration (CI)**: Automated testing on every commit
2. **Continuous Deployment (CD)**: Automated deployment to production
3. **GitHub Actions**: CI/CD platform
4. **Docker Registry**: Storing and versioning images
5. **Automated Testing**: Running tests in CI pipeline
6. **Code Quality**: Linting, formatting, coverage
7. **Deployment Strategies**: Blue-green, canary, rolling

## Structure
- `.github/workflows/ci-cd.yml`: GitHub Actions workflow
- `app/main.py`: Simple FastAPI application
- `tests/test_main.py`: Automated tests
- `Dockerfile`: Container image definition
- `requirements.txt`: Python dependencies

## Instructions

### 1. Understanding the CI/CD Pipeline

**Pipeline Stages**:
```
Code Push → Test → Lint → Build → Deploy
```

**What Happens**:
1. **Test**: Run pytest, check coverage
2. **Lint**: Check code style (flake8, black, isort)
3. **Build**: Create Docker image, push to registry
4. **Deploy**: Deploy to production (if main branch)

### 2. Local Testing

Before pushing to GitHub, test locally:

```bash
cd projects/22_cicd_pipeline

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=app --cov-report=term

# Run linting
pip install flake8 black isort
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
```

**Expected Output**:
```
tests/test_main.py::test_read_root PASSED
tests/test_main.py::test_health_check PASSED
tests/test_main.py::test_get_data PASSED

====== 3 passed in 0.25s ======

Coverage: 95%
```

### 3. Build Docker Image Locally

```bash
# Build
docker build -t data-api:local .

# Run
docker run -p 8000:8000 data-api:local

# Test
curl http://localhost:8000/health
```

### 4. GitHub Actions Setup

**Step 1: Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

**Step 2: Add Secrets**
Go to GitHub repo → Settings → Secrets and variables → Actions

Add:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub token

**Step 3: Watch the Pipeline**
- Go to Actions tab
- See the workflow running
- Check each job (test, lint, build, deploy)

### 5. Understanding the Workflow

**Trigger**:
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

**Jobs Run in Parallel**:
- `test`: Runs pytest
- `lint`: Checks code quality

**Jobs Run Sequentially**:
- `build`: Runs after test + lint pass
- `deploy`: Runs after build (only on main branch)

### 6. Making Changes

**Workflow**:
```bash
# 1. Create feature branch
git checkout -b feature/add-endpoint

# 2. Make changes
# Edit app/main.py

# 3. Add tests
# Edit tests/test_main.py

# 4. Test locally
pytest tests/ -v

# 5. Commit and push
git add .
git commit -m "Add new endpoint"
git push origin feature/add-endpoint

# 6. Create Pull Request
# GitHub will automatically run CI

# 7. Merge when tests pass
```

## CI/CD Best Practices

### **1. Test Pyramid**
```
        /\
       /E2E\      (Few) - Slow, expensive
      /------\
     /  API  \    (Some) - Medium speed
    /--------\
   /   Unit   \   (Many) - Fast, cheap
  /------------\
```

### **2. Fail Fast**
```yaml
# Run fastest tests first
jobs:
  lint:        # 30 seconds
  unit-test:   # 1 minute
  integration: # 5 minutes
  e2e:         # 15 minutes
```

### **3. Branch Protection**
Enable on GitHub:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date

### **4. Semantic Versioning**
```
v1.2.3
│ │ │
│ │ └─ Patch (bug fixes)
│ └─── Minor (new features, backwards compatible)
└───── Major (breaking changes)
```

### **5. Environment Variables**
```yaml
# Different configs per environment
env:
  ENVIRONMENT: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Homework / Challenge

### Challenge 1: Add Pre-commit Hooks
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
```

Install: `pip install pre-commit && pre-commit install`

### Challenge 2: Add Deployment Environments
Modify workflow to deploy to:
- `develop` branch → Staging environment
- `main` branch → Production environment

### Challenge 3: Add Slack Notifications
```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Build failed: ${{ github.repository }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Challenge 4: Database Migrations
Add step to run migrations before deployment:
```yaml
- name: Run migrations
  run: |
    python manage.py migrate
```

## Deployment Strategies

### **1. Blue-Green Deployment**
```
Blue (current)  → Green (new)
     ↓                ↓
  Traffic      Switch traffic
```

**Pros**: Instant rollback  
**Cons**: 2x resources

### **2. Canary Deployment**
```
90% → Old version
10% → New version (canary)

If OK:
100% → New version
```

**Pros**: Low risk  
**Cons**: Complex routing

### **3. Rolling Deployment**
```
Server 1: Update → Test → OK
Server 2: Update → Test → OK
Server 3: Update → Test → OK
```

**Pros**: No downtime  
**Cons**: Mixed versions running

## Expected Learning Outcomes
- ✅ Set up GitHub Actions CI/CD pipeline
- ✅ Automate testing and deployment
- ✅ Build and push Docker images
- ✅ Understand deployment strategies
- ✅ Implement code quality checks
- ✅ Use environment-specific configurations

## Interview Questions

**Q: What's the difference between CI and CD?**
A: CI (Continuous Integration) = automated testing on every commit. CD (Continuous Deployment) = automated deployment to production.

**Q: What should be in a CI pipeline?**
A: Linting, unit tests, integration tests, security scanning, build, push to registry.

**Q: How do you handle secrets in CI/CD?**
A: Use platform secrets (GitHub Secrets, AWS Secrets Manager), never commit to code, rotate regularly.

**Q: What's a good deployment strategy for zero downtime?**
A: Blue-green or rolling deployment. Both allow switching without downtime.

## Production Checklist

Before deploying to production:
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] Security scan completed
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Monitoring/alerts configured
- [ ] Load testing completed
- [ ] Stakeholders notified

## Cleanup
```bash
# Stop local containers
docker stop $(docker ps -q)

# Remove images
docker rmi data-api:local
```

---

**Congratulations!** You've completed Month 7 - Production Engineering & Team Leadership. You now have the skills to:
- Secure APIs with JWT
- Write comprehensive tests
- Monitor production systems
- Automate deployments

These are the skills that differentiate senior engineers and team leads from individual contributors.
