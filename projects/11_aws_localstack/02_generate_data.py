import csv
import random
import uuid
from datetime import datetime, timedelta

def generate_financial_data(filename="raw_transactions.csv", num_records=1000):
    users = [f"USR_{i:04d}" for i in range(1, 101)]
    symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "VTI", "SPY"]
    types = ["BUY", "SELL", "DIVIDEND"]

    print(f"Generating {num_records} transaction records to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["transaction_id", "user_id", "timestamp", "symbol", "type", "amount", "price"])
        
        for _ in range(num_records):
            timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 24))
            writer.writerow([
                str(uuid.uuid4()),
                random.choice(users),
                timestamp.isoformat(),
                random.choice(symbols),
                random.choice(types),
                round(random.uniform(1.0, 50.0), 2),
                round(random.uniform(50.0, 500.0), 2)
            ])
    
    print("Done!")

if __name__ == "__main__":
    generate_financial_data()
