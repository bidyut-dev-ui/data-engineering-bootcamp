#!/usr/bin/env python3
"""
Hadoop Basics Practice Exercises

Practice exercises for Hadoop ecosystem fundamentals optimized for 8GB RAM environments.
Covers Hadoop setup in Docker, HDFS operations, MapReduce, Hive, and Spark integration.

Note: These exercises assume Docker is available for Hadoop cluster setup.
"""

import sys
import os
import subprocess
import time
from typing import Dict, List, Tuple, Any, Optional

# ============================================================================
# Exercise 1: Hadoop Docker Setup for 8GB RAM
# ============================================================================

def exercise_1_hadoop_setup() -> Dict[str, Any]:
    """
    Exercise 1: Set Up Hadoop Cluster in Docker with Memory Constraints
    
    Tasks:
    1. Verify Docker is available and running
    2. Configure docker-compose.yml for 8GB RAM constraints
    3. Start single-node Hadoop cluster with optimized memory settings
    4. Verify cluster components are running (HDFS, YARN)
    5. Check resource usage to ensure within 8GB limits
    
    Returns:
        Dict: Setup results including cluster status and resource usage
    """
    print("\n=== Exercise 1: Hadoop Docker Setup for 8GB RAM ===")
    print("Setting up Hadoop cluster with memory constraints...")
    
    # TODO: Implement Hadoop Docker setup
    # 1. Check Docker availability
    # 2. Configure memory limits in docker-compose.yml
    # 3. Start Hadoop cluster using docker-compose
    # 4. Verify HDFS and YARN are operational
    # 5. Return cluster status and resource metrics
    
    print("   [TODO: Implement Hadoop Docker setup]")
    return {
        "docker_available": False,
        "cluster_running": False,
        "hdfs_available": False,
        "yarn_available": False,
        "memory_usage_mb": 0
    }

# ============================================================================
# Exercise 2: HDFS Operations
# ============================================================================

def exercise_2_hdfs_operations() -> Dict[str, Any]:
    """
    Exercise 2: HDFS File Operations and Management
    
    Tasks:
    1. Connect to HDFS using Python (hdfs3 or subprocess)
    2. Create directories and set permissions
    3. Upload local files to HDFS
    4. List, read, and delete files in HDFS
    5. Monitor HDFS storage usage and block distribution
    
    Returns:
        Dict: HDFS operation results including file counts and storage metrics
    """
    print("\n=== Exercise 2: HDFS Operations ===")
    print("Performing HDFS file operations...")
    
    # TODO: Implement HDFS operations
    # 1. Connect to HDFS (localhost:9000)
    # 2. Create directory structure
    # 3. Upload sample data files
    # 4. Perform file operations (list, read, delete)
    # 5. Return operation results and metrics
    
    print("   [TODO: Implement HDFS operations]")
    return {
        "directories_created": [],
        "files_uploaded": 0,
        "total_size_mb": 0,
        "hdfs_used_percentage": 0.0
    }

# ============================================================================
# Exercise 3: MapReduce with Python (MRJob)
# ============================================================================

def exercise_3_mapreduce_wordcount() -> Dict[str, Any]:
    """
    Exercise 3: MapReduce Word Count Implementation
    
    Tasks:
    1. Implement word count MapReduce job using MRJob
    2. Configure job for 8GB RAM (memory limits, reducers)
    3. Run job on sample text data in HDFS
    4. Monitor job progress and resource usage
    5. Analyze results and compare performance
    
    Returns:
        Dict: MapReduce job results including word counts and performance metrics
    """
    print("\n=== Exercise 3: MapReduce Word Count ===")
    print("Running MapReduce word count job...")
    
    # TODO: Implement MapReduce word count
    # 1. Create MRJob word count class
    # 2. Configure for Hadoop with memory constraints
    # 3. Upload input data to HDFS
    # 4. Run job and collect results
    # 5. Return word counts and job metrics
    
    print("   [TODO: Implement MapReduce word count]")
    return {
        "total_words": 0,
        "unique_words": 0,
        "job_duration_seconds": 0,
        "memory_used_mb": 0,
        "top_10_words": []
    }

# ============================================================================
# Exercise 4: Hive Data Processing
# ============================================================================

def exercise_4_hive_processing() -> Dict[str, Any]:
    """
    Exercise 4: Data Processing with Apache Hive
    
    Tasks:
    1. Connect to Hive server using PyHive or subprocess
    2. Create external tables pointing to HDFS data
    3. Run SQL queries for data analysis
    4. Optimize queries for 8GB RAM (partitioning, bucketing)
    5. Compare Hive performance with direct MapReduce
    
    Returns:
        Dict: Hive processing results including query results and performance
    """
    print("\n=== Exercise 4: Hive Data Processing ===")
    print("Processing data with Apache Hive...")
    
    # TODO: Implement Hive data processing
    # 1. Connect to Hive server
    # 2. Create tables from HDFS data
    # 3. Run analytical queries
    # 4. Implement partitioning for performance
    # 5. Return query results and metrics
    
    print("   [TODO: Implement Hive data processing]")
    return {
        "tables_created": [],
        "queries_executed": 0,
        "total_rows_processed": 0,
        "query_performance": {}
    }

# ============================================================================
# Exercise 5: Hadoop-Spark Integration
# ============================================================================

def exercise_5_hadoop_spark_integration() -> Dict[str, Any]:
    """
    Exercise 5: Integrating Spark with Hadoop Ecosystem
    
    Tasks:
    1. Configure PySpark to read from/write to HDFS
    2. Process HDFS data using Spark DataFrames
    3. Compare Spark performance with MapReduce and Hive
    4. Implement memory optimization for 8GB RAM
    5. Build end-to-end pipeline from HDFS to Spark to output
    
    Returns:
        Dict: Integration results including performance comparison and pipeline metrics
    """
    print("\n=== Exercise 5: Hadoop-Spark Integration ===")
    print("Integrating Spark with Hadoop ecosystem...")
    
    # TODO: Implement Hadoop-Spark integration
    # 1. Configure SparkSession for HDFS access
    # 2. Read data from HDFS into Spark DataFrame
    # 3. Process data with Spark transformations
    # 4. Write results back to HDFS
    # 5. Compare performance with other Hadoop components
    
    print("   [TODO: Implement Hadoop-Spark integration]")
    return {
        "spark_hdfs_integration": False,
        "data_read_from_hdfs": 0,
        "processing_time_seconds": 0,
        "performance_comparison": {}
    }

# ============================================================================
# Main Function to Run All Exercises
# ============================================================================

def main():
    """Run all Hadoop practice exercises in sequence."""
    print("=" * 70)
    print("HADOOP BASICS PRACTICE EXERCISES")
    print("Optimized for 8GB RAM Environments")
    print("=" * 70)
    
    # Check if Docker is available (required for Hadoop setup)
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Docker is available")
        else:
            print("⚠ Docker may not be running")
    except FileNotFoundError:
        print("✗ Docker not found. Some exercises require Docker for Hadoop cluster.")
        print("  Install Docker Desktop or Docker Engine first.")
    
    try:
        # Exercise 1: Hadoop Setup
        print("\n" + "=" * 40)
        print("Starting Exercise 1: Hadoop Docker Setup")
        print("=" * 40)
        setup_results = exercise_1_hadoop_setup()
        print(f"   Setup results: {setup_results}")
        
        # Exercise 2: HDFS Operations
        print("\n" + "=" * 40)
        print("Starting Exercise 2: HDFS Operations")
        print("=" * 40)
        hdfs_results = exercise_2_hdfs_operations()
        print(f"   HDFS results: {hdfs_results}")
        
        # Exercise 3: MapReduce
        print("\n" + "=" * 40)
        print("Starting Exercise 3: MapReduce Word Count")
        print("=" * 40)
        mapreduce_results = exercise_3_mapreduce_wordcount()
        print(f"   MapReduce results: {mapreduce_results}")
        
        # Exercise 4: Hive Processing
        print("\n" + "=" * 40)
        print("Starting Exercise 4: Hive Data Processing")
        print("=" * 40)
        hive_results = exercise_4_hive_processing()
        print(f"   Hive results: {hive_results}")
        
        # Exercise 5: Hadoop-Spark Integration
        print("\n" + "=" * 40)
        print("Starting Exercise 5: Hadoop-Spark Integration")
        print("=" * 40)
        integration_results = exercise_5_hadoop_spark_integration()
        print(f"   Integration results: {integration_results}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("EXERCISES COMPLETED")
        print("=" * 70)
        print("All Hadoop practice exercises have been executed.")
        print("Implement the TODO sections to complete each exercise.")
        print("\nNext steps:")
        print("1. Complete Exercise 1-5 implementations")
        print("2. Create solutions in solutions.py")
        print("3. Test with actual Hadoop Docker cluster")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error running exercises: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)