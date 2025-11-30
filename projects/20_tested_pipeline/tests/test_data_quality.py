import great_expectations as ge
import pandas as pd
from datetime import datetime

def create_expectation_suite():
    """Create Great Expectations suite for sales data"""
    
    # Load sample data
    df = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': [101, 102, 103],
        'amount': [100.0, 200.0, 150.0],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'status': ['completed', 'completed', 'pending']
    })
    
    # Convert to Great Expectations DataFrame
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    print("Setting up data quality expectations...\n")
    
    # 1. Column existence
    ge_df.expect_table_columns_to_match_ordered_list([
        'order_id', 'customer_id', 'amount', 'order_date', 'status'
    ])
    print("✓ Columns must exist in correct order")
    
    # 2. No nulls in critical columns
    for col in ['order_id', 'customer_id', 'amount']:
        ge_df.expect_column_values_to_not_be_null(col)
    print("✓ Critical columns cannot be null")
    
    # 3. Unique order IDs
    ge_df.expect_column_values_to_be_unique('order_id')
    print("✓ Order IDs must be unique")
    
    # 4. Amount must be positive
    ge_df.expect_column_values_to_be_between('amount', min_value=0, max_value=1000000)
    print("✓ Amount must be between 0 and 1,000,000")
    
    # 5. Status must be valid
    ge_df.expect_column_values_to_be_in_set('status', ['pending', 'completed', 'cancelled'])
    print("✓ Status must be valid value")
    
    # 6. Date format
    ge_df.expect_column_values_to_match_strftime_format('order_date', '%Y-%m-%d')
    print("✓ Date must be in YYYY-MM-DD format")
    
    # Get validation results
    print("\n" + "="*50)
    print("Validating sample data...")
    print("="*50 + "\n")
    
    results = ge_df.validate()
    
    print(f"Total expectations: {results.statistics['evaluated_expectations']}")
    print(f"Successful: {results.statistics['successful_expectations']}")
    print(f"Failed: {results.statistics['unsuccessful_expectations']}")
    print(f"Success rate: {results.statistics['success_percent']:.1f}%")
    
    return ge_df

def validate_new_data(filepath):
    """Validate new data file against expectations"""
    print(f"\nValidating file: {filepath}")
    
    # Load data
    df = pd.read_csv(filepath)
    ge_df = ge.from_pandas(df)
    
    # Apply expectations
    ge_df.expect_column_values_to_not_be_null('order_id')
    ge_df.expect_column_values_to_not_be_null('customer_id')
    ge_df.expect_column_values_to_not_be_null('amount')
    ge_df.expect_column_values_to_be_unique('order_id')
    ge_df.expect_column_values_to_be_between('amount', min_value=0, max_value=1000000)
    
    # Validate
    results = ge_df.validate()
    
    if results.success:
        print("✅ Data quality check PASSED")
    else:
        print("❌ Data quality check FAILED")
        print("\nFailed expectations:")
        for result in results.results:
            if not result.success:
                print(f"  - {result.expectation_config.expectation_type}")
    
    return results.success

if __name__ == "__main__":
    # Create and test expectations
    create_expectation_suite()
    
    # Example: Test with sample file
    # validate_new_data('sample_sales.csv')
