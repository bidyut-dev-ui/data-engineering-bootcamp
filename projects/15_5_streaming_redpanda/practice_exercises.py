#!/usr/bin/env python3
"""
Streaming with Redpanda Practice Exercises

This file contains 10 practice exercises covering:
1. Event-driven vs batch processing concepts
2. Redpanda/Kafka architecture
3. Producer implementation
4. Consumer implementation
5. Real-time aggregation
6. Fault tolerance and exactly-once semantics
7. Scaling consumers with consumer groups
8. Monitoring streaming pipelines
9. Memory-efficient streaming on 8GB RAM
10. End-to-end streaming pipeline design

Each exercise focuses on practical implementation with 8GB RAM constraints.
"""

import json
import time
import random
import uuid
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Exercise 1: Event-Driven Architecture Fundamentals
def exercise_1_event_driven_concepts() -> Dict[str, Any]:
    """
    Understand event-driven vs batch processing architectures.
    
    Requirements:
    1. Compare event-driven and batch processing characteristics
    2. Identify use cases for each approach
    3. Explain the role of message brokers (Redpanda/Kafka)
    4. Describe the components of a streaming pipeline
    5. Discuss trade-offs for 8GB RAM environments
    
    Focus on understanding when to use streaming vs batch.
    """
    print("=== Exercise 1: Event-Driven Architecture Fundamentals ===")
    print("Compare event-driven and batch processing approaches.")
    
    # TODO: Research and document key differences
    # 1. Latency requirements
    # 2. Data volume characteristics
    # 3. Processing patterns
    # 4. Resource requirements
    # 5. Use case examples
    
    return {
        "description": "Compare event-driven and batch processing architectures",
        "expected_output_keys": ["comparison_table", "use_cases", "trade_offs", "ram_considerations"],
        "memory_constraint": "Streaming requires constant memory for buffering, batch needs memory for entire dataset",
        "hint": "Consider factors like data velocity, processing latency, and state management"
    }

# Exercise 2: Redpanda/Kafka Architecture
def exercise_2_streaming_architecture() -> Dict[str, Any]:
    """
    Understand Redpanda/Kafka architecture and components.
    
    Requirements:
    1. Explain topics, partitions, and replication
    2. Describe producer and consumer roles
    3. Understand consumer groups and offset management
    4. Explain the role of brokers and ZooKeeper (if applicable)
    5. Compare Redpanda vs Apache Kafka for 8GB RAM
    
    Focus on architecture decisions for resource-constrained environments.
    """
    print("=== Exercise 2: Streaming Architecture ===")
    print("Understand Redpanda/Kafka components and their roles.")
    
    # TODO: Research and document architecture
    # 1. Topic partitioning strategies
    # 2. Replication for fault tolerance
    # 3. Consumer group coordination
    # 4. Memory optimization techniques
    
    return {
        "description": "Understand Redpanda/Kafka architecture and components",
        "expected_output_keys": ["architecture_diagram", "component_descriptions", "partitioning_strategies", "memory_optimizations"],
        "memory_constraint": "Redpanda is more memory-efficient than Kafka, suitable for 8GB RAM",
        "hint": "Focus on how partitioning affects parallelism and memory usage"
    }

# Exercise 3: Producer Implementation
def exercise_3_producer_implementation() -> Dict[str, Any]:
    """
    Implement a Redpanda/Kafka producer with fault tolerance.
    
    Requirements:
    1. Create a producer that sends financial tick data
    2. Implement retry logic for failed sends
    3. Add message batching for efficiency
    4. Include message key for proper partitioning
    5. Monitor memory usage during high-volume production
    
    Optimize for 8GB RAM environment.
    """
    print("=== Exercise 3: Producer Implementation ===")
    print("Implement a fault-tolerant Redpanda producer.")
    
    # TODO: Implement producer with these features
    # 1. Connection pooling and reuse
    # 2. Async sending with callbacks
    # 3. Batch accumulation with size/time limits
    # 4. Error handling and retries
    # 5. Memory monitoring
    
    return {
        "description": "Implement a fault-tolerant Redpanda producer",
        "expected_output_keys": ["producer_code", "retry_mechanism", "batching_strategy", "memory_monitoring", "performance_metrics"],
        "memory_constraint": "Limit batch size to control memory usage, monitor producer buffer",
        "hint": "Use kafka-python's KafkaProducer with batch_size and linger_ms parameters"
    }

# Exercise 4: Consumer Implementation
def exercise_4_consumer_implementation() -> Dict[str, Any]:
    """
    Implement a Redpanda/Kafka consumer with proper offset management.
    
    Requirements:
    1. Create a consumer that processes financial ticks
    2. Implement manual offset commit for exactly-once semantics
    3. Handle consumer rebalancing gracefully
    4. Add dead letter queue for failed messages
    5. Monitor and control memory usage during consumption
    
    Design for 8GB RAM constraints.
    """
    print("=== Exercise 4: Consumer Implementation ===")
    print("Implement a robust Redpanda consumer with offset management.")
    
    # TODO: Implement consumer with these features
    # 1. Consumer group configuration
    # 2. Manual offset commit
    # 3. Error handling and DLQ
    # 4. Rebalance listeners
    # 5. Memory-efficient processing
    
    return {
        "description": "Implement a robust Redpanda consumer with offset management",
        "expected_output_keys": ["consumer_code", "offset_management", "error_handling", "rebalance_handling", "memory_usage"],
        "memory_constraint": "Process messages in small batches, avoid accumulating large in-memory state",
        "hint": "Use auto_offset_reset='earliest' for development, manual commits for production"
    }

# Exercise 5: Real-Time Aggregation
def exercise_5_real_time_aggregation() -> Dict[str, Any]:
    """
    Implement real-time aggregation with windowing.
    
    Requirements:
    1. Create sliding window aggregations (1-minute, 5-minute windows)
    2. Implement tumbling windows for fixed-time aggregations
    3. Handle late-arriving data
    4. Manage aggregation state efficiently
    5. Optimize for memory usage on 8GB RAM
    
    Focus on state management and memory efficiency.
    """
    print("=== Exercise 5: Real-Time Aggregation ===")
    print("Implement windowed aggregations for streaming data.")
    
    # TODO: Implement windowed aggregation
    # 1. Time-based windowing
    # 2. State management (in-memory vs external store)
    # 3. Late data handling
    # 4. Memory-efficient data structures
    
    return {
        "description": "Implement real-time aggregation with windowing",
        "expected_output_keys": ["aggregation_logic", "windowing_implementation", "state_management", "late_data_handling", "performance_metrics"],
        "memory_constraint": "Use bounded data structures, evict old windows, consider external state stores",
        "hint": "Consider using Redis for external state if memory becomes constrained"
    }

# Exercise 6: Fault Tolerance and Exactly-Once Semantics
def exercise_6_fault_tolerance() -> Dict[str, Any]:
    """
    Implement fault tolerance and exactly-once processing.
    
    Requirements:
    1. Design idempotent consumer processing
    2. Implement producer idempotence
    3. Handle consumer failures and restarts
    4. Design for partition reassignment
    5. Test recovery scenarios
    
    Ensure reliability within 8GB RAM constraints.
    """
    print("=== Exercise 6: Fault Tolerance ===")
    print("Implement exactly-once semantics and fault tolerance.")
    
    # TODO: Implement fault tolerance mechanisms
    # 1. Idempotent operations
    # 2. Transactional producers
    # 3. Consumer checkpointing
    # 4. Failure recovery procedures
    
    return {
        "description": "Implement fault tolerance and exactly-once semantics",
        "expected_output_keys": ["idempotence_implementation", "transaction_management", "checkpoint_strategy", "recovery_procedures", "test_scenarios"],
        "memory_constraint": "Checkpoint frequently but not too frequently to avoid I/O overhead",
        "hint": "Use Kafka's transactional API or implement idempotent consumers with deduplication"
    }

# Exercise 7: Scaling with Consumer Groups
def exercise_7_scaling_consumers() -> Dict[str, Any]:
    """
    Design and implement scalable consumer groups.
    
    Requirements:
    1. Configure consumer groups for horizontal scaling
    2. Implement partition assignment strategies
    3. Handle consumer group rebalancing
    4. Monitor consumer lag
    5. Optimize for 8GB RAM per consumer instance
    
    Focus on scaling within resource constraints.
    """
    print("=== Exercise 7: Scaling with Consumer Groups ===")
    print("Design scalable consumer groups for parallel processing.")
    
    # TODO: Implement scalable consumer group
    # 1. Consumer group configuration
    # 2. Partition assignment monitoring
    # 3. Lag monitoring and alerting
    # 4. Dynamic scaling logic
    
    return {
        "description": "Design and implement scalable consumer groups",
        "expected_output_keys": ["consumer_group_design", "partition_assignment", "lag_monitoring", "scaling_strategy", "performance_metrics"],
        "memory_constraint": "Each consumer instance should stay under 2GB RAM for 4-instance deployment on 8GB",
        "hint": "Use Kafka's built-in consumer group coordination, monitor with Burrow or similar tools"
    }

# Exercise 8: Streaming Pipeline Monitoring
def exercise_8_streaming_monitoring() -> Dict[str, Any]:
    """
    Implement comprehensive monitoring for streaming pipelines.
    
    Requirements:
    1. Monitor producer throughput and latency
    2. Track consumer lag and processing rates
    3. Implement health checks for Redpanda brokers
    4. Set up alerts for abnormal conditions
    5. Design dashboards for pipeline visibility
    
    Keep monitoring lightweight for 8GB RAM environment.
    """
    print("=== Exercise 8: Streaming Pipeline Monitoring ===")
    print("Implement monitoring and observability for streaming pipelines.")
    
    # TODO: Implement monitoring system
    # 1. Metrics collection (throughput, latency, lag)
    # 2. Health check endpoints
    # 3. Alerting rules
    # 4. Dashboard design
    
    return {
        "description": "Implement comprehensive monitoring for streaming pipelines",
        "expected_output_keys": ["monitoring_architecture", "metrics_collection", "alerting_rules", "dashboard_design", "health_checks"],
        "memory_constraint": "Use lightweight metrics collection, avoid storing extensive history in memory",
        "hint": "Consider Prometheus for metrics, Grafana for dashboards, keep scrape intervals reasonable"
    }

# Exercise 9: Memory-Efficient Streaming on 8GB RAM
def exercise_9_memory_efficient_streaming() -> Dict[str, Any]:
    """
    Optimize streaming pipelines for 8GB RAM constraints.
    
    Requirements:
    1. Design memory-efficient data structures for state
    2. Implement backpressure mechanisms
    3. Optimize serialization/deserialization
    4. Configure appropriate buffer sizes
    5. Implement graceful degradation under memory pressure
    
    Focus on practical optimizations for limited memory.
    """
    print("=== Exercise 9: Memory-Efficient Streaming ===")
    print("Optimize streaming pipelines for 8GB RAM constraints.")
    
    # TODO: Implement memory optimizations
    # 1. Efficient data structures
    # 2. Backpressure implementation
    # 3. Serialization optimization
    # 4. Memory monitoring and adjustment
    
    return {
        "description": "Optimize streaming pipelines for 8GB RAM constraints",
        "expected_output_keys": ["optimization_strategies", "memory_monitoring", "backpressure_implementation", "performance_comparison", "configuration_recommendations"],
        "memory_constraint": "Target <6GB peak usage to allow for OS and other processes",
        "hint": "Use protobuf or Avro for efficient serialization, implement streaming algorithms that don't require full dataset in memory"
    }

# Exercise 10: End-to-End Streaming Pipeline
def exercise_10_end_to_end_pipeline() -> Dict[str, Any]:
    """
    Design and implement a complete streaming pipeline.
    
    Requirements:
    1. Integrate producer, consumer, and aggregation components
    2. Implement error handling and recovery end-to-end
    3. Add monitoring and observability throughout
    4. Design for scalability and fault tolerance
    5. Optimize for 8GB RAM deployment
    
    Create a production-ready streaming pipeline.
    """
    print("=== Exercise 10: End-to-End Streaming Pipeline ===")
    print("Design and implement a complete streaming pipeline.")
    
    # TODO: Implement end-to-end pipeline
    # 1. Component integration
    # 2. End-to-end error handling
    # 3. Comprehensive monitoring
    # 4. Deployment configuration
    # 5. Performance testing
    
    return {
        "description": "Design and implement a complete streaming pipeline",
        "expected_output_keys": ["pipeline_architecture", "component_integration", "error_handling", "monitoring_setup", "deployment_config", "performance_results"],
        "memory_constraint": "Complete pipeline must operate within 8GB RAM including Redpanda, producers, and consumers",
        "hint": "Use Docker Compose for local testing, implement circuit breakers and bulkheads for fault isolation"
    }

def main():
    """Run all exercises and print summaries."""
    print("Streaming with Redpanda Practice Exercises")
    print("=" * 60)
    print("This module contains 10 exercises covering:")
    print("1. Event-driven vs batch processing concepts")
    print("2. Redpanda/Kafka architecture")
    print("3. Producer implementation")
    print("4. Consumer implementation")
    print("5. Real-time aggregation")
    print("6. Fault tolerance and exactly-once semantics")
    print("7. Scaling consumers with consumer groups")
    print("8. Monitoring streaming pipelines")
    print("9. Memory-efficient streaming on 8GB RAM")
    print("10. End-to-end streaming pipeline design")
    print("\nEach exercise is designed with 8GB RAM constraints.")
    print("Implement the TODO sections in each function.")
    
    # Exercise summaries
    exercises = [
        exercise_1_event_driven_concepts,
        exercise_2_streaming_architecture,
        exercise_3_producer_implementation,
        exercise_4_consumer_implementation,
        exercise_5_real_time_aggregation,
        exercise_6_fault_tolerance,
        exercise_7_scaling_consumers,
        exercise_8_streaming_monitoring,
        exercise_9_memory_efficient_streaming,
        exercise_10_end_to_end_pipeline
    ]
    
    print("\n" + "=" * 60)
    print("Exercise Summaries:")
    for i, exercise_func in enumerate(exercises, 1):
        result = exercise_func()
        print(f"\n{i}. {result['description']}")
        print(f"   Expected outputs: {', '.join(result['expected_output_keys'])}")
        print(f"   Memory constraint: {result['memory_constraint']}")
    
    print("\n" + "=" * 60)
    print("Implementation Notes:")
    print("- All exercises should be implemented with 8GB RAM constraints")
    print("- Redpanda is more memory-efficient than Kafka for resource-constrained environments")
    print("- Implement proper error handling and fault tolerance")
    print("- Monitor memory usage throughout streaming operations")
    print("- Test with both small and large data volumes")
    print("- Consider using async/await for non-blocking I/O where appropriate")
    
    return {"status": "exercises_defined", "count": len(exercises)}

if __name__ == "__main__":
    main()