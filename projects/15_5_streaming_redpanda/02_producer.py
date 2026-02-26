import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer

# Connect to Redpanda on the external port mapped in docker-compose
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'financial_ticks'
SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "VTI", "SPY"]
TYPES = ["BUY", "SELL"]

def generate_tick():
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "symbol": random.choice(SYMBOLS),
        "type": random.choice(TYPES),
        "price": round(random.uniform(50.0, 500.0), 2),
        "volume": random.randint(10, 1000)
    }

print(f"Starting simulated financial tick stream to topic '{TOPIC_NAME}'...")
print("Press Ctrl+C to stop.")

try:
    while True:
        tick = generate_tick()
        # Publish the message
        producer.send(TOPIC_NAME, value=tick)
        print(f"Published: {tick['symbol']} {tick['type']} {tick['volume']} shares @ ${tick['price']}")
        
        # Flush to ensure it's sent
        producer.flush()
        
        # Wait a random fraction of a second to simulate real-time ticks
        time.sleep(random.uniform(0.1, 1.0))

except KeyboardInterrupt:
    print("\nStopping data generation...")
    producer.close()
