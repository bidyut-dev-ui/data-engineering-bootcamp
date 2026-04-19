"""
Practice Exercises for Setup & Refresher Project

This file contains hands-on exercises to reinforce environment setup skills.
These exercises are designed for 8GB RAM laptops with no GPU.
"""

import sys
import platform
import shutil
import subprocess
import os

def exercise_1_check_python_version():
    """
    Exercise 1: Check Python Version and Environment
    
    Task: Write a function that checks if Python 3.10+ is installed
    and prints the version details.
    
    Requirements:
    - Use sys.version_info to check version
    - Print a friendly message indicating if version is sufficient
    - Return True if Python 3.10+, False otherwise
    """
    # TODO: Implement this function
    pass

def exercise_2_verify_tools_installed():
    """
    Exercise 2: Verify Required Tools
    
    Task: Check if essential tools (git, docker, python) are installed
    and available in PATH.
    
    Requirements:
    - Use shutil.which() to check tool availability
    - Return a dictionary with tool names as keys and boolean availability as values
    - Handle missing tools gracefully
    """
    # TODO: Implement this function
    pass

def exercise_3_create_virtual_environment():
    """
    Exercise 3: Virtual Environment Setup
    
    Task: Create a function that sets up a Python virtual environment.
    
    Requirements:
    - Check if virtual environment already exists
    - Use subprocess to create venv if needed
    - Return path to the created/verified virtual environment
    - Include error handling for permission issues
    """
    # TODO: Implement this function
    pass

def exercise_4_check_disk_space():
    """
    Exercise 4: Disk Space Check for Data Engineering
    
    Task: Check available disk space and warn if low.
    
    Requirements:
    - Use shutil.disk_usage() to check disk space
    - Warn if less than 5GB free (for data processing)
    - Return available space in GB
    """
    # TODO: Implement this function
    pass

def exercise_5_memory_check():
    """
    Exercise 5: Memory Availability Check
    
    Task: Check system memory for 8GB RAM optimization.
    
    Requirements:
    - Use psutil if available, or platform-specific commands
    - Check available RAM
    - Suggest optimal settings for data engineering tasks
    - Return memory info in GB
    """
    # TODO: Implement this function
    pass

def exercise_6_setup_optimization():
    """
    Exercise 6: Environment Optimization for 8GB RAM
    
    Task: Create optimization recommendations for memory-constrained setup.
    
    Requirements:
    - Check current Python memory settings
    - Suggest environment variables for memory optimization
    - Recommend Docker memory limits
    - Return a list of optimization suggestions
    """
    # TODO: Implement this function
    pass

def exercise_7_troubleshoot_common_issues():
    """
    Exercise 7: Troubleshooting Common Setup Issues
    
    Task: Simulate and fix common environment setup problems.
    
    Requirements:
    - Create a function that detects common issues:
      * Docker not running
      * Virtual environment not activated
      * Insufficient permissions
      * Port conflicts
    - Provide solutions for each detected issue
    """
    # TODO: Implement this function
    pass

def run_all_exercises():
    """Run all exercises and display results"""
    print("=== Setup & Refresher Practice Exercises ===\n")
    
    exercises = [
        ("1. Python Version Check", exercise_1_check_python_version),
        ("2. Tool Verification", exercise_2_verify_tools_installed),
        ("3. Virtual Environment Setup", exercise_3_create_virtual_environment),
        ("4. Disk Space Check", exercise_4_check_disk_space),
        ("5. Memory Check", exercise_5_memory_check),
        ("6. Environment Optimization", exercise_6_setup_optimization),
        ("7. Troubleshooting", exercise_7_troubleshoot_common_issues),
    ]
    
    for name, func in exercises:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = func()
            if result is not None:
                print(f"Result: {result}")
        except NotImplementedError:
            print("Exercise not implemented yet")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("This file contains practice exercises for environment setup.")
    print("Implement each function according to the docstring instructions.")
    print("\nTo test your implementations, run:")
    print("  python practice_exercises.py")
    print("\nOr implement the functions and call run_all_exercises()")