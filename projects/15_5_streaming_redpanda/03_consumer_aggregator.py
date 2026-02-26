import json
from collections import defaultdict
from kafka import KafkaConsumer

# Connect to Redpanda on the external port mapped in docker-compose
consumer = KafkaConsumer(
    'financial_ticks',
    bootstrap_servers=['localhost:19092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='volume-aggregator-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Starting real-time volume aggregator...")
print("Listening for events on 'financial_ticks' topic...")

# Dictionary to hold our rolling aggregation: { 'AAPL': total_volume, 'MSFT': total_volume }
volume_aggregation = defaultdict(int)
messages_processed = 0

try:
    for message in consumer:
        tick = message.value
        symbol = tick['symbol']
        volume = tick['volume']
        
        # Aggregate the volume
        volume_aggregation[symbol] += volume
        messages_processed += 1
        
        # Print an update every 5 messages to simulate a windowed output
        if messages_processed % 5 == 0:
            print("\n--- Real-Time Total Volume by Symbol ---")
            for sym, vol in sorted(volume_aggregation.items()):
                print(f"{sym}: {vol:,} shares")
            print("----------------------------------------")

except KeyboardInterrupt:
    print("\nStopping volume aggregator...")
    consumer.close()
