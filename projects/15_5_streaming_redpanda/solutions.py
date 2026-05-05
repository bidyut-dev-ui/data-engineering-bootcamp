#!/usr/bin/env python3
"""
Solutions for Streaming with Redpanda Practice Exercises
"""

import json
from kafka import KafkaProducer, KafkaConsumer

def solution_producer():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    for i in range(100):
        data = {"event_id": i, "metric": "cpu_usage", "value": 50 + i}
        producer.send('telemetry', data)
    
    producer.flush()
    print("Sent 100 messages to 'telemetry' topic.")

def solution_consumer():
    consumer = KafkaConsumer(
        'telemetry',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='monitor_group'
    )
    
    print("Monitoring 'telemetry' topic...")
    count = 0
    total_value = 0
    
    for message in consumer:
        val = message.value['value']
        total_value += val
        count += 1
        if count % 10 == 0:
            print(f"Processed {count} messages. Avg value: {total_value/count:.2f}")
        if count >= 100:
            break

if __name__ == "__main__":
    # Note: Requires Redpanda running via docker-compose
    try:
        solution_producer()
        solution_consumer()
    except Exception as e:
        print(f"Error: {e}. Check if Redpanda is running.")
