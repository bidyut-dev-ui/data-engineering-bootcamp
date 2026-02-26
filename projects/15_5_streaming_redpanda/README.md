# Week 15.5: Event-Driven & Streaming Pipelines

**Tag:** `#role-datacompany-senior`, `#skill-streaming`

## Overview
Financial and Trading Platforms require real-time processing capabilities. In this module, we introduce **Redpanda**, a C++ lightweight alternative to Apache Kafka, to handle streaming events within our strict memory constraints.

## Learning Objectives
- Event-driven vs Batch processing
- Topics, Producers, and Consumers
- Real-time stock ticker ingestion
- Basic windowed aggregations

## System Requirements
- Redpanda Docker container (`redpandadata/redpanda`)
- `kafka-python` or `confluent-kafka` Python packages

## Project Instructions
Build a real-time producer that mimics a high-frequency financial ticker. Use a consumer to calculate rolling 1-minute volume aggregations.

### 1. Start Redpanda
First, ensure Docker is running, then spin up the Redpanda container:
```bash
docker compose up -d
```
Redpanda comes with a built-in UI you can access at `http://localhost:8080`.

### 2. Setup Dependencies & Topics
Install the required Python packages and run the setup script to create your `financial_ticks` topic.
```bash
pip install -r requirements.txt
chmod +x 01_setup_topics.sh
./01_setup_topics.sh
```

### 3. Start the Real-Time Producer
In a terminal, start simulating high-frequency trading data:
```bash
python 02_producer.py
```
Leave this running so it continues to pump data into Redpanda.

### 4. Start the Consumer Aggregator
Open a **second terminal tab**, navigate to this exact folder, and start the aggregator. It will connect to the stream and calculate real-time volume:
```bash
python 03_consumer_aggregator.py
```

### 5. Verify the Results
Watch the second terminal output update dynamically with aggregated ticker volumes! Or, open `http://localhost:8080` in your browser to watch the data flow through the topics visually.

### 6. Teardown
```bash
docker compose down
```
