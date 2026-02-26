#!/bin/bash
set -e

echo "Waiting for Redpanda to start..."
sleep 15

# Create a topic named 'financial_ticks' with 3 partitions and a replication factor of 1
docker exec -it redpanda-1 rpk topic create financial_ticks -p 3 -r 1

echo "Topics in Redpanda:"
docker exec -it redpanda-1 rpk topic list

echo "Redpanda setup complete! UI is available at localhost:8080"
