# Week 28: Testing & Data Quality

**Goal**: Learn to write comprehensive tests for data pipelines, implement data quality checks, and measure code coverage.

## Scenario
Your team is deploying data pipelines to production. You need to ensure code quality through automated testing and implement data quality checks to catch issues before they reach users.

## Concepts Covered
1. **Unit Testing**: Testing individual functions with pytest
2. **Integration Testing**: Testing component interactions
3. **Data Quality**: Great Expectations framework
4. **Test Coverage**: Measuring how much code is tested
5. **Test-Driven Development (TDD)**: Writing tests first
6. **Fixtures**: Reusable test data
7. **Mocking**: Simulating external dependencies

## Structure
- `tests/test_data_processing.py`: Pytest unit tests
- `tests/test_data_quality.py`: Great Expectations checks
- `requirements.txt`: Testing dependencies
- `pytest.ini`: Pytest configuration
- `.coveragerc`: Coverage configuration

## Instructions

### 1. Setup
```bash
cd projects/20_tested_pipeline
source ../../venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Unit Tests
```bash
pytest tests/test_data_processing.py -v
```

**Expected Output**:
```
test_data_processing.py::TestSalesData::test_load_data PASSED
test_data_processing.py::TestSalesData::test_clean_sales_data_removes_duplicates PASSED
test_data_processing.py::TestSalesData::test_clean_sales_data_removes_negative_amounts PASSED
test_data_processing.py::TestSalesData::test_calculate_total_revenue PASSED
test_data_processing.py::TestSalesData::test_get_top_customers PASSED
test_data_processing.py::TestSalesData::test_validate_data_quality_detects_issues PASSED

====== 6 passed in 0.15s ======
```

### 3. Run with Coverage
```bash
pytest tests/test_data_processing.py --cov=. --cov-report=html
```

Open `htmlcov/index.html` to see detailed coverage report.

**Target**: Aim for >80% code coverage

### 4. Run Data Quality Checks
```bash
python tests/test_data_quality.py
```

**Expected Output**:
```
Setting up data quality expectations...

✓ Columns must exist in correct order
✓ Critical columns cannot be null
✓ Order IDs must be unique
✓ Amount must be between 0 and 1,000,000
✓ Status must be valid value
✓ Date must be in YYYY-MM-DD format

==================================================
Validating sample data...
==================================================

Total expectations: 6
Successful: 6
Failed: 0
Success rate: 100.0%
```

## Testing Concepts Explained

### **Unit Tests vs Integration Tests**

**Unit Test**: Tests a single function in isolation
```python
def test_calculate_total_revenue():
    df = pd.DataFrame({'amount': [100, 200, 300]})
    assert calculate_total_revenue(df) == 600
```

**Integration Test**: Tests multiple components together
```python
def test_full_pipeline():
    raw_data = load_data('input.csv')
    cleaned = clean_data(raw_data)
    result = process_data(cleaned)
    assert result is not None
```

### **Fixtures**: Reusable Test Data

```python
@pytest.fixture
def sample_data():
    """Create test data once, use in multiple tests"""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30]
    })

def test_sum(sample_data):
    assert sample_data['value'].sum() == 60

def test_count(sample_data):
    assert len(sample_data) == 3
```

### **Test Coverage**

Coverage measures which lines of code are executed during tests.

**Good coverage** (>80%):
- All critical paths tested
- Edge cases covered
- Error handling verified

**Bad coverage** (<50%):
- Many code paths untested
- Higher risk of bugs
- Less confidence in changes

### **Great Expectations**

Framework for data quality checks. Think of it as "unit tests for data".

**Common Expectations**:
- `expect_column_values_to_not_be_null()`
- `expect_column_values_to_be_unique()`
- `expect_column_values_to_be_between()`
- `expect_column_values_to_be_in_set()`

## Homework / Challenge

### Challenge 1: Add More Tests
Extend `test_data_processing.py`:
1. Test for handling empty DataFrames
2. Test for handling invalid date formats
3. Test for handling very large numbers
4. Achieve 90%+ coverage

### Challenge 2: Integration Test for ETL
Create `tests/test_etl_integration.py`:
```python
def test_full_etl_pipeline():
    # 1. Extract
    raw_data = extract_from_source()
    
    # 2. Transform
    cleaned_data = transform(raw_data)
    
    # 3. Load
    load_to_warehouse(cleaned_data)
    
    # 4. Verify
    result = query_warehouse("SELECT COUNT(*) FROM sales")
    assert result > 0
```

### Challenge 3: Parameterized Tests
Test multiple scenarios with one test:
```python
@pytest.mark.parametrize("input,expected", [
    (100, 100),
    (200, 200),
    (-50, 0),  # Negative should become 0
])
def test_clean_amount(input, expected):
    result = clean_amount(input)
    assert result == expected
```

### Challenge 4: Data Quality Suite
Create a complete Great Expectations suite:
1. Save expectations to JSON
2. Load and apply to new data
3. Generate HTML report
4. Integrate with Airflow DAG

## Best Practices

### **1. Test Naming Convention**
```python
# Good
def test_calculate_revenue_with_valid_data():
    pass

def test_calculate_revenue_with_empty_dataframe():
    pass

# Bad
def test1():
    pass
```

### **2. Arrange-Act-Assert Pattern**
```python
def test_example():
    # Arrange: Set up test data
    df = pd.DataFrame({'amount': [100, 200]})
    
    # Act: Execute the function
    result = calculate_total(df)
    
    # Assert: Verify the result
    assert result == 300
```

### **3. Test One Thing**
```python
# Good: Tests one specific behavior
def test_removes_duplicates():
    df = pd.DataFrame({'id': [1, 1, 2]})
    result = remove_duplicates(df)
    assert len(result) == 2

# Bad: Tests multiple things
def test_everything():
    df = load_data()
    df = clean_data(df)
    df = transform_data(df)
    assert len(df) > 0  # What exactly are we testing?
```

### **4. Use Fixtures for Setup**
```python
@pytest.fixture
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()  # Cleanup

def test_query(database_connection):
    result = database_connection.execute("SELECT 1")
    assert result is not None
```

## Production Integration

### **1. Run Tests in CI/CD**
```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    pytest tests/ --cov=. --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### **2. Pre-commit Hooks**
```bash
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest
      language: system
      pass_filenames: false
```

### **3. Data Quality in Airflow**
```python
from airflow.operators.python import PythonOperator

def validate_data(**context):
    df = load_data()
    ge_df = ge.from_pandas(df)
    results = ge_df.validate()
    
    if not results.success:
        raise ValueError("Data quality check failed!")

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data
)
```

## Expected Learning Outcomes
- ✅ Write effective unit tests with pytest
- ✅ Implement data quality checks with Great Expectations
- ✅ Measure and improve code coverage
- ✅ Understand TDD principles
- ✅ Integrate testing into CI/CD pipelines
- ✅ Debug failing tests efficiently

## Interview Questions

**Q: What's the difference between unit and integration tests?**
A: Unit tests test individual functions in isolation. Integration tests test how multiple components work together.

**Q: What is test coverage and what's a good target?**
A: Coverage measures % of code executed during tests. Target: 80%+ for critical code, 60%+ overall.

**Q: How do you test data quality in production?**
A: Use frameworks like Great Expectations to define expectations, run checks in pipelines, alert on failures.

**Q: What is TDD?**
A: Test-Driven Development: Write tests first, then write code to make tests pass. Ensures testable, well-designed code.
