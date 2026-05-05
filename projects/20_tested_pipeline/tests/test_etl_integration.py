import pytest
import pandas as pd
from test_data_processing import clean_sales_data, calculate_total_revenue

def test_full_etl_pipeline(tmp_path):
    """
    Problem Statement:
    You need to test the end-to-end flow: Load -> Clean -> Transform.
    
    Solution:
    1. Create a raw CSV file.
    2. Run the cleaning logic.
    3. Run the aggregation logic.
    4. Assert the final output matches expectations.
    """
    # 1. Setup raw data
    raw_file = tmp_path / "raw_orders.csv"
    raw_df = pd.DataFrame({
        'order_id': [1, 2, 2, 3], # 2 is duplicate
        'customer_id': [101, 102, 102, 103],
        'amount': [100.0, 200.0, 200.0, -50.0], # -50 should be removed
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-02', '2024-01-03']
    })
    raw_df.to_csv(raw_file, index=False)
    
    # 2. Act
    cleaned_df = clean_sales_data(pd.read_csv(raw_file))
    total_rev = calculate_total_revenue(cleaned_df)
    
    # 3. Assert
    # Duplicate '2' removed, Negative '-50' removed. Remaining: 1 (100) and 2 (200)
    assert len(cleaned_df) == 2
    assert total_rev == 300.0
    print("Integration test PASSED")

if __name__ == "__main__":
    pytest.main([__file__])
