import pandas as pd

def step_1_loading():
    print("\n=== Step 1: Loading Data ===")
    # Reading CSV
    # index_col=0 means we use the first column (order_id) as the index
    df = pd.read_csv('sales_data.csv') 
    print(f"Loaded CSV with shape: {df.shape}")
    print("First 5 rows:")
    print(df.head())
    return df

def step_2_inspection(df):
    print("\n=== Step 2: Inspection ===")
    print("Info (Data Types and Missing Values):")
    print(df.info())
    
    print("\nDescriptive Statistics:")
    print(df.describe())
    
    print("\nCheck for Missing Values:")
    print(df.isnull().sum())

def step_3_cleaning(df):
    print("\n=== Step 3: Cleaning ===")
    
    # 1. Handling Missing Values
    # We will drop rows where 'product' is missing
    initial_count = len(df)
    df_clean = df.dropna(subset=['product'])
    print(f"Dropped {initial_count - len(df_clean)} rows with missing products.")
    
    # 2. Fixing Inconsistent Data (Region casing)
    # Convert all regions to Title Case (e.g., 'north' -> 'North')
    print("Unique regions before fix:", df_clean['region'].unique())
    df_clean.loc[:, 'region'] = df_clean['region'].str.title()
    print("Unique regions after fix:", df_clean['region'].unique())
    
    # 3. Handling Invalid Data (Negative Quantity)
    # We assume negative quantity is a data entry error and convert to positive
    invalid_qty_count = (df_clean['quantity'] < 0).sum()
    print(f"Found {invalid_qty_count} rows with negative quantity.")
    df_clean.loc[:, 'quantity'] = df_clean['quantity'].abs()
    
    return df_clean

def step_4_transformation(df):
    print("\n=== Step 4: Transformation ===")
    # Create a new column 'total_sales'
    df['total_sales'] = df['quantity'] * df['unit_price']
    print("Added 'total_sales' column.")
    print(df[['product', 'quantity', 'unit_price', 'total_sales']].head())
    return df

def main():
    # Ensure data exists
    try:
        df = step_1_loading()
    except FileNotFoundError:
        print("Error: 'sales_data.csv' not found. Run generate_data.py first!")
        return

    step_2_inspection(df)
    df = step_3_cleaning(df)
    df = step_4_transformation(df)
    
    # Save cleaned data
    df.to_parquet('sales_clean.parquet')
    print("\nSaved cleaned data to 'sales_clean.parquet'")

if __name__ == "__main__":
    main()
