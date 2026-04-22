#!/usr/bin/env python3
"""
Practice Exercises for Data Janitor Project

This module contains exercises for building a CLI tool to clean messy server logs,
flatten nested JSON structures, and optimize data storage.

IMPORTANT: Do NOT provide solutions in this file. The exercises should contain
TODO placeholders where learners will implement their own solutions.
"""

import json
from typing import Dict, Any, List, Optional
import pandas as pd
from pathlib import Path
import argparse
import sys


def exercise_1_basic_log_parsing() -> Dict[str, Any]:
    """
    Exercise 1: Basic Log Parsing
    
    Create a function that reads a JSONL file line by line, parses each line as JSON,
    and returns a list of dictionaries. Handle malformed JSON gracefully.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Read a JSONL file containing server logs, parse each line as JSON,
        and return a list of dictionaries. Handle lines that are not valid JSON
        by logging a warning and skipping them.
        
        Requirements:
        1. Use a generator to read the file line by line (memory-efficient)
        2. Parse each line with json.loads()
        3. Skip lines that cause JSONDecodeError, log a warning
        4. Return list of valid log entries
        
        Example input line: {"timestamp": "2023-01-01T12:00:00", "action": "login", "metadata": {"ip": "192.168.1.1"}}
        """,
        "hint": "Use try-except around json.loads() to handle malformed JSON",
        "function_name": "parse_jsonl_file",
        "parameters": ["file_path: str"],
        "returns": "List[Dict[str, Any]]"
    }


def exercise_2_flatten_nested_structures() -> Dict[str, Any]:
    """
    Exercise 2: Flatten Nested JSON Structures
    
    Create a function that flattens nested dictionaries in log entries.
    For example, flatten metadata.ip and metadata.user_agent to top-level columns.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Flatten nested JSON structures in log entries to create a flat DataFrame.
        
        Given a log entry like:
        {
            "timestamp": "2023-01-01T12:00:00",
            "action": "login",
            "metadata": {
                "ip": "192.168.1.1",
                "user_agent": "Mozilla/5.0"
            }
        }
        
        Transform it to:
        {
            "timestamp": "2023-01-01T12:00:00",
            "action": "login",
            "ip": "192.168.1.1",
            "user_agent": "Mozilla/5.0"
        }
        
        Requirements:
        1. Handle arbitrary nesting depth (but assume reasonable depth for logs)
        2. Prefix nested keys with parent key (e.g., "metadata_ip") or flatten directly
        3. Handle cases where nested dict might be missing
        """,
        "hint": "Use recursion or pandas.json_normalize() for flattening",
        "function_name": "flatten_log_entry",
        "parameters": ["log_entry: Dict[str, Any]"],
        "returns": "Dict[str, Any]"
    }


def exercise_3_data_quality_checks() -> Dict[str, Any]:
    """
    Exercise 3: Data Quality Checks
    
    Implement data quality checks for log data:
    - Drop rows with missing timestamps
    - Standardize action names (lowercase)
    - Validate IP addresses format
    - Remove bot traffic based on user_agent
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Implement comprehensive data quality checks for server logs.
        
        Requirements:
        1. Drop rows where timestamp is missing or cannot be parsed
        2. Convert all action values to lowercase
        3. Validate IP addresses (basic format validation)
        4. Filter out bot traffic (user_agent contains "Bot", "bot", "crawler", "spider")
        5. Remove duplicate log entries based on timestamp + ip + action
        
        The function should return cleaned DataFrame and a report of actions taken.
        """,
        "hint": "Use pandas operations for efficient filtering and transformation",
        "function_name": "clean_log_data",
        "parameters": ["df: pd.DataFrame"],
        "returns": "Tuple[pd.DataFrame, Dict[str, int]] (cleaned_df, stats)"
    }


def exercise_4_cli_argument_parsing() -> Dict[str, Any]:
    """
    Exercise 4: CLI Argument Parsing
    
    Create a command-line interface using argparse with the following options:
    --input-dir, --output-dir, --filter-bot, --verbose, --help
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Build a robust CLI interface for the data janitor tool using argparse.
        
        Required arguments:
        1. --input-dir: Directory containing raw JSONL files (required)
        2. --output-dir: Directory to save cleaned Parquet files (optional, default: ./processed)
        3. --filter-bot: Flag to enable bot filtering (optional)
        4. --verbose: Flag to enable verbose logging (optional)
        5. --help: Show help message
        
        The CLI should:
        - Validate that input directory exists
        - Create output directory if it doesn't exist
        - Parse arguments and return a configuration object
        """,
        "hint": "Use argparse.ArgumentParser with appropriate argument types and defaults",
        "function_name": "parse_cli_arguments",
        "parameters": ["args: Optional[List[str]] = None"],
        "returns": "argparse.Namespace"
    }


def exercise_5_parquet_optimization() -> Dict[str, Any]:
    """
    Exercise 5: Parquet File Optimization
    
    Optimize Parquet file writing with proper schema, compression, and partitioning.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Write cleaned log data to Parquet format with optimizations.
        
        Requirements:
        1. Use appropriate compression (snappy or gzip)
        2. Specify schema/dtypes for columns to reduce file size
        3. Consider partitioning by date if timestamp column exists
        4. Add metadata to the Parquet file (version, processing timestamp)
        5. Implement incremental append if output file already exists
        
        The function should handle large datasets efficiently.
        """,
        "hint": "Use pandas.to_parquet() with compression and partition_cols parameters",
        "function_name": "write_to_parquet",
        "parameters": ["df: pd.DataFrame", "output_path: str", "partition_by_date: bool = True"],
        "returns": "str (path to written file)"
    }


def exercise_6_memory_efficient_processing() -> Dict[str, Any]:
    """
    Exercise 6: Memory-Efficient Processing
    
    Process large log files using chunking to avoid memory issues on 8GB RAM.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Process large log files memory-efficiently using chunking.
        
        Requirements:
        1. Read and process JSONL files in chunks (e.g., 10,000 lines at a time)
        2. Clean each chunk independently
        3. Write chunks to Parquet incrementally
        4. Monitor memory usage and adjust chunk size dynamically
        5. Handle partial failures (save progress)
        
        The function should work with files larger than available RAM.
        """,
        "hint": "Use generators and pandas read_json with chunksize or lines=True",
        "function_name": "process_large_files",
        "parameters": ["input_dir: str", "output_path: str", "chunk_size: int = 10000"],
        "returns": "Dict[str, Any] (processing statistics)"
    }


def exercise_7_error_handling_and_logging() -> Dict[str, Any]:
    """
    Exercise 7: Error Handling and Logging
    
    Implement comprehensive error handling and logging for production readiness.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Make the data janitor tool production-ready with proper error handling.
        
        Requirements:
        1. Set up logging with different levels (INFO, WARNING, ERROR)
        2. Handle file I/O errors gracefully
        3. Implement retry logic for transient failures
        4. Create a summary report of processing results
        5. Send alerts for critical errors (simulate with logging)
        
        The tool should never crash silently.
        """,
        "hint": "Use Python's logging module and try-except blocks with specific exceptions",
        "function_name": "setup_logging_and_error_handling",
        "parameters": ["log_level: str = 'INFO'"],
        "returns": "logging.Logger"
    }


def exercise_8_performance_benchmarking() -> Dict[str, Any]:
    """
    Exercise 8: Performance Benchmarking
    
    Benchmark different approaches to find the most efficient processing method.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Benchmark different data processing approaches to optimize performance.
        
        Requirements:
        1. Compare pandas vs. polars vs. dask for log processing
        2. Measure memory usage, processing time, and CPU utilization
        3. Test different chunk sizes for memory-constrained environments
        4. Compare different Parquet compression algorithms
        5. Generate a performance report with recommendations
        
        Focus on 8GB RAM constraint.
        """,
        "hint": "Use time.time() for timing and psutil for memory monitoring",
        "function_name": "benchmark_processing_methods",
        "parameters": ["input_file: str", "methods: List[str] = ['pandas', 'polars', 'dask']"],
        "returns": "Dict[str, Dict[str, float]] (benchmark results)"
    }


def exercise_9_docker_containerization() -> Dict[str, Any]:
    """
    Exercise 9: Docker Containerization
    
    Create a Dockerfile to containerize the data janitor tool.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Containerize the data janitor tool for deployment.
        
        Requirements:
        1. Create a Dockerfile with Python 3.9+ base image
        2. Install dependencies from requirements.txt
        3. Copy the janitor tool and make it executable
        4. Set up entrypoint and default command
        5. Optimize Docker image size (multi-stage build if possible)
        6. Add health checks
        
        The container should run the janitor tool with mounted volumes for data.
        """,
        "hint": "Use alpine Python image for smaller size, copy only necessary files",
        "function_name": "create_dockerfile",
        "parameters": [],
        "returns": "str (Dockerfile content)"
    }


def exercise_10_end_to_end_pipeline() -> Dict[str, Any]:
    """
    Exercise 10: End-to-End Pipeline
    
    Build a complete ETL pipeline that processes logs on a schedule.
    
    Returns:
        Dict with 'description' and 'hint' for the exercise
    """
    return {
        "description": """
        Create an end-to-end pipeline that processes logs automatically.
        
        Requirements:
        1. Watch a directory for new JSONL files (using watchdog or inotify)
        2. Process new files as they arrive
        3. Maintain state of processed files (avoid reprocessing)
        4. Send notifications when processing completes or fails
        5. Generate daily summary reports
        
        Simulate a production data pipeline scenario.
        """,
        "hint": "Use threading or asyncio for file watching, maintain a SQLite state database",
        "function_name": "create_continuous_pipeline",
        "parameters": ["watch_dir: str", "processed_dir: str", "check_interval: int = 60"],
        "returns": "None (runs continuously)"
    }


def main():
    """Print all exercise descriptions."""
    exercises = [
        exercise_1_basic_log_parsing(),
        exercise_2_flatten_nested_structures(),
        exercise_3_data_quality_checks(),
        exercise_4_cli_argument_parsing(),
        exercise_5_parquet_optimization(),
        exercise_6_memory_efficient_processing(),
        exercise_7_error_handling_and_logging(),
        exercise_8_performance_benchmarking(),
        exercise_9_docker_containerization(),
        exercise_10_end_to_end_pipeline(),
    ]
    
    print("=" * 80)
    print("DATA JANITOR PRACTICE EXERCISES")
    print("=" * 80)
    print("\nThese exercises help you build a production-ready data cleaning tool.")
    print("Implement each function according to the specifications.\n")
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\n{'='*60}")
        print(f"EXERCISE {i}: {exercise['function_name']}")
        print(f"{'='*60}")
        print(f"Description: {exercise['description'].strip()}")
        print(f"\nFunction: {exercise['function_name']}({', '.join(exercise['parameters'])})")
        print(f"Returns: {exercise['returns']}")
        print(f"Hint: {exercise['hint']}")
        print(f"\nTODO: Implement the function above according to the requirements.")
        print(f"{'-'*60}")


if __name__ == "__main__":
    main()