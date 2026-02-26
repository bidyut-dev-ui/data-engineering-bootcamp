import pandas as pd
import great_expectations as gx

# 1. Initialize a Data Context
context = gx.get_context()

def run_data_quality_checks(csv_file: str):
    """
    Simulates a production data ingestion quality check.
    If data breaks, trust breaks!
    """
    print(f"--- Running Reliability Checks on {csv_file} ---")
    
    # 2. Connect to data source
    try:
        df = pd.read_csv(csv_file)
        validator = context.sources.pandas_default.read_dataframe(df)
        print(f"Data Loaded Successfully: {len(df)} rows found.")
    except Exception as e:
        print(f"CRITICAL INCIDENT: Could not load data. Alerts triggering! Error: {e}")
        return

    # 3. Define Expectations (SLOs for your data correctness)
    
    # Expectation 1: The 'transaction_id' must never be null and must be unique
    validator.expect_column_values_to_not_be_null("transaction_id")
    validator.expect_column_values_to_be_unique("transaction_id")

    # Expectation 2: The 'amount' should always be greater than 0
    validator.expect_column_values_to_be_between(
        "amount", min_value=0.01, max_value=None
    )

    # Expectation 3: The 'type' must be in our approved list
    validator.expect_column_values_to_be_in_set(
        "type", ["BUY", "SELL", "DIVIDEND"]
    )

    # 4. Save and Run the Expectations
    validator.save_expectation_suite(discard_failed_expectations=False)
    checkpoint_result = validator.head()

    print("\n--- Reliability Report ---")
    if checkpoint_result.success:
        print("✅ Data Quality Passed. Proceeding to Data Warehouse insert.")
    else:
        print("❌ DATA QUALITY FAILED! Halting Pipeline! Triggering PagerDuty/Slack Alerts.")
        # In a real application, you parse checkpoint_result for specific failure reasons
        print("See detailed metrics for incident response.")

if __name__ == "__main__":
    # Create a mock good file
    pd.DataFrame({
        "transaction_id": ["T1", "T2", "T3"],
        "amount": [100.5, 20.0, 5000.0],
        "type": ["BUY", "SELL", "BUY"]
    }).to_csv("good_data.csv", index=False)

    # Create a mock BAD file (negative amount, bad type, missing ID)
    pd.DataFrame({
        "transaction_id": ["T4", "T5", "T5"], # Duplicate ID
        "amount": [-50.0, 20.0, 5000.0],      # Negative amount
        "type": ["BUY", "UNKNOWN", "BUY"]     # Bad categorical data
    }).to_csv("bad_data.csv", index=False)

    print("Running on GOOD data...")
    run_data_quality_checks("good_data.csv")
    
    print("\n--------------------------\n")

    print("Running on INCIDENT/BAD data...")
    run_data_quality_checks("bad_data.csv")
