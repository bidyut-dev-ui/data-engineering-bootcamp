import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

def generate_customer_activity(num_days=30, customers_per_day=100):
    """Generate simulated customer activity data"""
    
    activities = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    customer_ids = list(range(1, 1001))  # 1000 customers
    
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        
        # Random subset of customers active each day
        active_customers = random.sample(customer_ids, customers_per_day)
        
        for customer_id in active_customers:
            # Generate activity
            activity = {
                'customer_id': customer_id,
                'date': date.strftime('%Y-%m-%d'),
                'page_views': random.randint(1, 50),
                'time_on_site': random.randint(60, 3600),  # seconds
                'items_viewed': random.randint(0, 20),
                'items_added_to_cart': random.randint(0, 5),
                'purchase_made': random.choice([0, 1]) if random.random() < 0.3 else 0,
                'purchase_amount': round(random.uniform(10, 500), 2) if random.random() < 0.3 else 0,
                'support_tickets': random.randint(0, 2) if random.random() < 0.1 else 0
            }
            activities.append(activity)
    
    return pd.DataFrame(activities)

def save_as_api_response(df, output_dir='data/raw'):
    """Save data as if it came from an API"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Group by date and save as separate files
    for date, group in df.groupby('date'):
        filename = f"{output_dir}/activity_{date}.json"
        group.to_json(filename, orient='records', indent=2)
        print(f"Created {filename}")

if __name__ == "__main__":
    print("Generating customer activity data...\n")
    df = generate_customer_activity(num_days=30)
    
    print(f"Generated {len(df)} activity records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nSample data:")
    print(df.head())
    
    save_as_api_response(df)
    print("\n✓ Data generation complete!")
