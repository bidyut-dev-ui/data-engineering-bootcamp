import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sales_data(num_rows=1000):
    print(f"Generating {num_rows} rows of sample data...")
    
    # Products
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'HDMI Cable', 'Webcam']
    prices = {'Laptop': 1200, 'Mouse': 25, 'Keyboard': 45, 'Monitor': 300, 'HDMI Cable': 15, 'Webcam': 80}
    
    # Regions
    regions = ['North', 'South', 'East', 'West']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_rows):
        prod = random.choice(products)
        region = random.choice(regions)
        qty = random.randint(1, 10)
        price = prices[prod]
        
        # Introduce some messiness (Data Cleaning targets)
        if random.random() < 0.05:
            region = region.lower() # Inconsistent casing
        if random.random() < 0.02:
            qty = -1 * qty # Invalid negative quantity
        if random.random() < 0.02:
            prod = None # Missing value
            
        date = start_date + timedelta(days=random.randint(0, 365))
        
        data.append({
            'order_id': 1000 + i,
            'date': date.strftime('%Y-%m-%d'),
            'product': prod,
            'region': region,
            'quantity': qty,
            'unit_price': price
        })
        
    df = pd.DataFrame(data)
    
    # Save as CSV
    df.to_csv('sales_data.csv', index=False)
    print("Created 'sales_data.csv'")
    
    # Save a subset as JSON
    df.head(50).to_json('sales_subset.json', orient='records')
    print("Created 'sales_subset.json'")

if __name__ == "__main__":
    generate_sales_data()
