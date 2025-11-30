import pandas as pd
import pytest
from datetime import datetime

def load_sales_data(filepath):
    """Load sales data from CSV"""
    return pd.read_csv(filepath)

def clean_sales_data(df):
    """Clean sales data"""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove rows with missing critical fields
    df = df.dropna(subset=['order_id', 'customer_id', 'amount'])
    
    # Ensure amount is positive
    df = df[df['amount'] > 0]
    
    # Convert date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    return df

def calculate_total_revenue(df):
    """Calculate total revenue"""
    return df['amount'].sum()

def get_top_customers(df, n=10):
    """Get top N customers by total spend"""
    return df.groupby('customer_id')['amount'].sum().nlargest(n)

def validate_data_quality(df):
    """Validate data quality rules"""
    issues = []
    
    # Check for nulls in critical columns
    critical_cols = ['order_id', 'customer_id', 'amount', 'order_date']
    for col in critical_cols:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            issues.append(f"{col} has {null_count} null values")
    
    # Check for negative amounts
    negative_count = (df['amount'] < 0).sum()
    if negative_count > 0:
        issues.append(f"Found {negative_count} negative amounts")
    
    # Check for future dates
    future_dates = (df['order_date'] > datetime.now()).sum()
    if future_dates > 0:
        issues.append(f"Found {future_dates} future dates")
    
    return issues

# Tests
class TestSalesData:
    """Test suite for sales data processing"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        return pd.DataFrame({
            'order_id': [1, 2, 3, 3, 4],  # 3 is duplicate
            'customer_id': [101, 102, 103, 103, 104],
            'amount': [100.0, 200.0, 150.0, 150.0, -50.0],  # -50 is invalid
            'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-03', '2024-01-04']
        })
    
    def test_load_data(self, tmp_path):
        """Test data loading"""
        # Create temporary CSV
        test_file = tmp_path / "test_sales.csv"
        df = pd.DataFrame({
            'order_id': [1, 2],
            'customer_id': [101, 102],
            'amount': [100.0, 200.0],
            'order_date': ['2024-01-01', '2024-01-02']
        })
        df.to_csv(test_file, index=False)
        
        # Test loading
        loaded_df = load_sales_data(test_file)
        assert len(loaded_df) == 2
        assert 'order_id' in loaded_df.columns
    
    def test_clean_sales_data_removes_duplicates(self, sample_data):
        """Test that duplicates are removed"""
        cleaned = clean_sales_data(sample_data)
        assert len(cleaned) < len(sample_data)
        assert cleaned['order_id'].duplicated().sum() == 0
    
    def test_clean_sales_data_removes_negative_amounts(self, sample_data):
        """Test that negative amounts are removed"""
        cleaned = clean_sales_data(sample_data)
        assert (cleaned['amount'] > 0).all()
    
    def test_calculate_total_revenue(self):
        """Test revenue calculation"""
        df = pd.DataFrame({
            'order_id': [1, 2, 3],
            'customer_id': [101, 102, 103],
            'amount': [100.0, 200.0, 150.0],
            'order_date': ['2024-01-01', '2024-01-02', '2024-01-03']
        })
        total = calculate_total_revenue(df)
        assert total == 450.0
    
    def test_get_top_customers(self):
        """Test top customers calculation"""
        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4],
            'customer_id': [101, 101, 102, 103],
            'amount': [100.0, 200.0, 150.0, 50.0],
            'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']
        })
        top = get_top_customers(df, n=2)
        assert len(top) == 2
        assert top.iloc[0] == 300.0  # Customer 101
    
    def test_validate_data_quality_detects_issues(self, sample_data):
        """Test data quality validation"""
        issues = validate_data_quality(sample_data)
        assert len(issues) > 0  # Should detect negative amount
        assert any('negative' in issue.lower() for issue in issues)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
