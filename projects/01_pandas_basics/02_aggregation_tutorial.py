import pandas as pd

def main():
    print("=== Aggregation & Grouping Tutorial ===")
    
    try:
        # Load the cleaned data from the previous step
        df = pd.read_parquet('sales_clean.parquet')
    except FileNotFoundError:
        print("Error: 'sales_clean.parquet' not found. Run 01_basics_tutorial.py first!")
        return

    # 1. Simple GroupBy
    # Total sales by Region
    print("\n--- Total Sales by Region ---")
    region_sales = df.groupby('region')['total_sales'].sum()
    print(region_sales)
    
    # 2. Multiple Aggregations
    # Total quantity and Average price by Product
    print("\n--- Product Stats (Total Qty, Avg Price) ---")
    product_stats = df.groupby('product').agg({
        'quantity': 'sum',
        'unit_price': 'mean',
        'total_sales': 'sum'
    })
    # Sort by total sales descending
    print(product_stats.sort_values('total_sales', ascending=False))
    
    # 3. Time-based Aggregation
    # Convert date column to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract month
    df['month'] = df['date'].dt.to_period('M')
    
    print("\n--- Monthly Sales Trend ---")
    monthly_sales = df.groupby('month')['total_sales'].sum()
    print(monthly_sales)

if __name__ == "__main__":
    main()
