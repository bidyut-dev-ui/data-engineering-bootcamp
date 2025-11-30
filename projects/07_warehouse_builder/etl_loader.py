import pandas as pd
from sqlalchemy import create_engine, text
import time

# Connect to Postgres (Port 5434)
DB_URL = "postgresql://user:password@localhost:5434/warehouse_db"

def wait_for_db(engine):
    print("Waiting for DB...")
    for _ in range(10):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except:
            time.sleep(2)
    raise Exception("DB not ready")

def load_schema(engine):
    print("Creating Schema...")
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()

def etl_process(engine):
    print("Starting ETL...")
    
    # 1. Extract
    print("Extracting CSVs...")
    df_prods = pd.read_csv('data/products.csv')
    df_custs = pd.read_csv('data/customers.csv')
    df_sales = pd.read_csv('data/sales.csv')
    
    with engine.connect() as conn:
        # 2. Load Dimensions (SCD Type 1 - Overwrite/Append)
        # In a real scenario, we would check for existing records.
        # Here we just truncate and reload for simplicity or append.
        
        print("Loading Dim_Product...")
        # Map CSV columns to DB columns
        dim_prod_data = df_prods.rename(columns={
            'id': 'original_id', 
            'cat': 'category', 
            'price': 'current_price'
        })
        dim_prod_data.to_sql('dim_product', conn, if_exists='append', index=False)
        
        print("Loading Dim_Customer...")
        dim_cust_data = df_custs.rename(columns={'id': 'original_id'})
        dim_cust_data[['original_id', 'name', 'region']].to_sql('dim_customer', conn, if_exists='append', index=False)
        
        print("Loading Dim_Date...")
        # Generate date dimension from sales dates
        unique_dates = pd.to_datetime(df_sales['date'].unique())
        dim_date_data = pd.DataFrame({
            'date_key': unique_dates.strftime('%Y%m%d').astype(int),
            'full_date': unique_dates,
            'year': unique_dates.year,
            'month': unique_dates.month,
            'day_name': unique_dates.day_name()
        })
        dim_date_data.to_sql('dim_date', conn, if_exists='append', index=False)
        
        # 3. Load Fact Table
        print("Loading Fact_Sales...")
        
        # We need to look up the surrogate keys (product_key, customer_key) from the DB
        # Read back the dimensions to get the generated keys
        db_prods = pd.read_sql("SELECT product_key, original_id FROM dim_product", conn)
        db_custs = pd.read_sql("SELECT customer_key, original_id FROM dim_customer", conn)
        
        # Merge Sales with Dimensions
        fact_df = df_sales.merge(db_prods, left_on='prod_id', right_on='original_id')
        fact_df = fact_df.merge(db_custs, left_on='cust_id', right_on='original_id')
        
        # Calculate Date Key
        fact_df['date_key'] = pd.to_datetime(fact_df['date']).dt.strftime('%Y%m%d').astype(int)
        
        # Calculate Total Amount (We need price from products)
        # Note: In a real warehouse, we might fetch historical price. Here we use current price from CSV.
        fact_df = fact_df.merge(df_prods[['id', 'price']], left_on='prod_id', right_on='id')
        fact_df['total_amount'] = fact_df['qty'] * fact_df['price']
        
        # Select final columns
        final_fact = fact_df[[
            'txn_id', 'customer_key', 'product_key', 'date_key', 'qty', 'total_amount'
        ]]
        
        final_fact.to_sql('fact_sales', conn, if_exists='append', index=False)
        print(f"Loaded {len(final_fact)} rows into Fact_Sales.")

def main():
    engine = create_engine(DB_URL)
    wait_for_db(engine)
    load_schema(engine)
    etl_process(engine)
    print("Warehouse Build Complete!")

if __name__ == "__main__":
    main()
