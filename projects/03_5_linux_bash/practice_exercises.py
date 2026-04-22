#!/usr/bin/env python3
"""
Linux & Bash Practice Exercises for Data Engineers

This file contains practical exercises to master Linux command line skills
essential for data engineering workflows, Docker management, and server administration.
Focus on 8GB RAM optimization and production-ready practices.
"""

import subprocess
import os
import sys
from pathlib import Path

def exercise_1_text_processing():
    """
    Exercise 1: Text Processing with grep, awk, and sed
    
    Scenario: You have a large log file (access.log) and need to extract specific information.
    
    Tasks:
    1. Count the total number of lines in the log file
    2. Find all lines containing "ERROR" (case-insensitive)
    3. Extract the 3rd column (HTTP status codes) and count occurrences of each code
    4. Replace all occurrences of "192.168.1.1" with "REDACTED_IP"
    5. Find the top 5 most frequent IP addresses
    
    Learning Objectives:
    - Master grep with regex patterns
    - Use awk for column extraction and aggregation
    - Apply sed for in-place text replacement
    - Combine commands with pipes for complex data extraction
    """
    print("Exercise 1: Text Processing with grep, awk, and sed")
    print("=" * 60)
    print("\nCreate a log analysis script that:")
    print("1. Uses 'wc -l' to count total lines")
    print("2. Uses 'grep -i error' to find error lines")
    print("3. Uses 'awk' to extract and count status codes")
    print("4. Uses 'sed' to redact sensitive IP addresses")
    print("5. Uses 'sort', 'uniq', and 'head' to find top IPs")
    print("\nExpected commands to learn:")
    print("  grep -i 'error' access.log")
    print("  awk '{print $9}' access.log | sort | uniq -c")
    print("  sed 's/192\\.168\\.1\\.1/REDACTED_IP/g' access.log")
    print("  awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -5")
    print("\nMemory Optimization Tip:")
    print("- Use 'grep -c' instead of 'grep | wc -l' for counting")
    print("- Process files in chunks with 'split' for large files")
    print("- Use 'awk' for multiple operations in single pass")

def exercise_2_file_permissions():
    """
    Exercise 2: File Permissions and Security
    
    Scenario: You need to secure sensitive configuration files and scripts
    in a multi-user environment.
    
    Tasks:
    1. Set read-only permissions for configuration files
    2. Make scripts executable only by owner
    3. Create a directory with specific permissions for a team
    4. Verify permissions using ls -l and stat
    5. Understand octal vs symbolic permission notation
    
    Learning Objectives:
    - Master chmod with both octal and symbolic notation
    - Understand user/group/other permission concepts
    - Apply appropriate permissions for different file types
    - Use umask to set default permissions
    """
    print("\nExercise 2: File Permissions and Security")
    print("=" * 60)
    print("\nCreate a permission management script that:")
    print("1. Sets config files to 644 (rw-r--r--)")
    print("2. Sets scripts to 755 (rwxr-xr-x)")
    print("3. Sets secret files to 600 (rw-------)")
    print("4. Creates shared directories with 2770 (setgid)")
    print("\nExpected commands to learn:")
    print("  chmod 644 config.yaml")
    print("  chmod u+x script.sh")
    print("  chmod 600 secrets.env")
    print("  chmod 2770 shared_data/")
    print("  ls -l --time-style=full-iso")
    print("  stat -c '%A %a %U %G %n' filename")
    print("\nSecurity Best Practices:")
    print("- Never use 777 permissions in production")
    print("- Use groups for team collaboration instead of world permissions")
    print("- Regularly audit file permissions with find /path -type f -perm /o=rwx")

def exercise_3_bash_scripting():
    """
    Exercise 3: Bash Scripting Fundamentals
    
    Scenario: Create robust bash scripts for automation tasks.
    
    Tasks:
    1. Write a script that accepts command-line arguments
    2. Implement error handling with exit codes
    3. Use variables, arrays, and loops
    4. Create functions for reusable code
    5. Parse command output and make decisions
    
    Learning Objectives:
    - Write production-ready bash scripts
    - Handle errors and edge cases
    - Use bash built-in features effectively
    - Follow shell scripting best practices
    """
    print("\nExercise 3: Bash Scripting Fundamentals")
    print("=" * 60)
    print("\nCreate a robust bash script that:")
    print("1. Accepts input file and output directory as arguments")
    print("2. Validates file existence and permissions")
    print("3. Processes data in batches to avoid memory issues")
    print("4. Logs progress and errors to a file")
    print("5. Returns appropriate exit codes (0=success, 1=error)")
    print("\nScript structure to implement:")
    print("  #!/bin/bash")
    print("  set -euo pipefail  # Fail on errors, undefined vars, pipe fails")
    print("  LOG_FILE=\"processing.log\"")
    print("  function log_message() {")
    print("    echo \"$(date): $1\" | tee -a \"$LOG_FILE\"")
    print("  }")
    print("  # Argument parsing")
    print("  if [ $# -ne 2 ]; then")
    print("    echo \"Usage: $0 <input_file> <output_dir>\"")
    print("    exit 1")
    print("  fi")
    print("\nMemory Optimization:")
    print("- Process files line by line instead of loading entire file")
    print("- Use 'while read' loops for large files")
    print("- Clean up temporary files immediately")

def exercise_4_process_management():
    """
    Exercise 4: Process Management and Monitoring
    
    Scenario: Monitor and manage long-running data processing jobs.
    
    Tasks:
    1. List running processes and filter by name/CPU/memory
    2. Kill unresponsive processes gracefully
    3. Run processes in background and manage jobs
    4. Monitor resource usage (CPU, memory, disk I/O)
    5. Set up process limits with ulimit
    
    Learning Objectives:
    - Use ps, top, htop, and pgrep effectively
    - Manage background jobs with jobs, fg, bg
    - Understand signals (SIGTERM, SIGKILL, SIGINT)
    - Monitor system resources for bottleneck detection
    """
    print("\nExercise 4: Process Management and Monitoring")
    print("=" * 60)
    print("\nCreate a process monitoring script that:")
    print("1. Lists top 10 memory-consuming processes")
    print("2. Kills processes older than 24 hours")
    print("3. Monitors disk space and sends alerts")
    print("4. Restarts failed services automatically")
    print("\nExpected commands to learn:")
    print("  ps aux --sort=-%mem | head -11")
    print("  find /proc -maxdepth 1 -type d -name '[0-9]*' -mmin +1440")
    print("  df -h --output=source,pcent,target | grep -v 'Use%'")
    print("  nohup ./long_running_process.sh &")
    print("\n8GB RAM Optimization:")
    print("- Set memory limits with 'ulimit -v'")
    print("- Use 'nice' and 'ionice' for process priority")
    print("- Monitor swap usage with 'free -h'")

def exercise_5_disk_operations():
    """
    Exercise 5: Disk Operations and Storage Management
    
    Scenario: Manage large datasets on disk with limited storage.
    
    Tasks:
    1. Find and delete old temporary files
    2. Archive and compress log files
    3. Monitor disk usage and identify large files
    4. Create and manage symbolic links
    5. Work with tar, gzip, and zip archives
    
    Learning Objectives:
    - Efficient disk space management
    - File compression and archiving techniques
    - Symbolic vs hard links
    - Disk I/O performance optimization
    """
    print("\nExercise 5: Disk Operations and Storage Management")
    print("=" * 60)
    print("\nCreate a disk management script that:")
    print("1. Finds files older than 30 days and archives them")
    print("2. Compresses logs with optimal compression level")
    print("3. Identifies the 10 largest files/directories")
    print("4. Cleans up temporary directories safely")
    print("\nExpected commands to learn:")
    print("  find /path -type f -mtime +30 -exec tar -czf {}.tar.gz {} \\;")
    print("  du -ah /path | sort -rh | head -10")
    print("  gzip --best large_file.log")
    print("  ln -s /actual/path /link/path")
    print("\nStorage Optimization:")
    print("- Use 'tar czf' for better compression than zip")
    print("- Consider using 'pigz' for parallel compression")
    print("- Implement log rotation with logrotate")

def exercise_6_network_utilities():
    """
    Exercise 6: Network Utilities for Data Engineering
    
    Scenario: Troubleshoot network issues in data pipelines.
    
    Tasks:
    1. Test connectivity to databases and APIs
    2. Download files with curl and wget
    3. Monitor network traffic
    4. Parse network configuration
    5. Use SSH for remote server management
    
    Learning Objectives:
    - Network troubleshooting fundamentals
    - Secure file transfer methods
    - Remote command execution
    - Network performance monitoring
    """
    print("\nExercise 6: Network Utilities for Data Engineering")
    print("=" * 60)
    print("\nCreate a network diagnostics script that:")
    print("1. Tests connectivity to multiple endpoints")
    print("2. Measures latency and packet loss")
    print("3. Downloads files with resume capability")
    print("4. Checks open ports on localhost")
    print("\nExpected commands to learn:")
    print("  curl -I https://api.example.com")
    print("  wget --continue http://example.com/large_file.csv")
    print("  netstat -tulpn | grep LISTEN")
    print("  ssh user@host 'command'")
    print("\nNetwork Optimization:")
    print("- Use 'curl --parallel' for concurrent downloads")
    print("- Implement timeout and retry logic")
    print("- Monitor bandwidth with 'iftop' or 'nethogs'")

def exercise_7_environment_variables():
    """
    Exercise 7: Environment Variables and Configuration
    
    Scenario: Manage application configuration across different environments.
    
    Tasks:
    1. Set and export environment variables
    2. Source configuration files
    3. Use environment-specific settings
    4. Secure sensitive credentials
    5. Validate configuration before execution
    
    Learning Objectives:
    - Environment variable management
    - Configuration file best practices
    - Secret management techniques
    - Environment validation
    """
    print("\nExercise 7: Environment Variables and Configuration")
    print("=" * 60)
    print("\nCreate a configuration management script that:")
    print("1. Sources environment-specific config files")
    print("2. Validates required variables are set")
    print("3. Exports variables with proper scoping")
    print("4. Handles default values for optional variables")
    print("\nExpected commands/patterns:")
    print("  export DATABASE_URL=\"postgresql://user:pass@host/db\"")
    print("  source .env.production")
    print("  : \"${API_KEY:?Error: API_KEY is required}\"")
    print("  CONFIG_FILE=\"${CONFIG_FILE:-config/default.yaml}\"")
    print("\nSecurity Considerations:")
    print("- Never hardcode credentials in scripts")
    print("- Use .env files with proper permissions (600)")
    print("- Consider using secret management tools for production")

def exercise_8_automation_with_cron():
    """
    Exercise 8: Automation with Cron and Systemd
    
    Scenario: Schedule regular data pipeline jobs.
    
    Tasks:
    1. Create cron jobs for periodic tasks
    2. Monitor cron job execution
    3. Create systemd services for long-running processes
    4. Set up logging and alerting for scheduled jobs
    5. Handle job dependencies and error recovery
    
    Learning Objectives:
    - Cron syntax and scheduling
    - Systemd service management
    - Job monitoring and alerting
    - Dependency management in automation
    """
    print("\nExercise 8: Automation with Cron and Systemd")
    print("=" * 60)
    print("\nCreate an automation setup that:")
    print("1. Runs a data pipeline every hour")
    print("2. Sends email alerts on failure")
    print("3. Logs output with timestamps")
    print("4. Prevents overlapping executions")
    print("\nCron examples to implement:")
    print("  # Run every hour at minute 0")
    print("  0 * * * * /path/to/script.sh >> /var/log/pipeline.log 2>&1")
    print("  # Run daily at 2 AM")
    print("  0 2 * * * /path/to/daily_job.sh")
    print("\nSystemd service example:")
    print("  [Unit]")
    print("  Description=Data Pipeline Service")
    print("  After=network.target")
    print("  ")
    print("  [Service]")
    print("  Type=simple")
    print("  ExecStart=/path/to/pipeline.sh")
    print("  Restart=on-failure")
    print("  MemoryLimit=2G")

def exercise_9_performance_monitoring():
    """
    Exercise 9: Performance Monitoring and Optimization
    
    Scenario: Monitor system performance and optimize resource usage.
    
    Tasks:
    1. Monitor CPU, memory, disk, and network usage
    2. Identify resource bottlenecks
    3. Optimize command performance
    4. Profile script execution time
    5. Implement resource limits
    
    Learning Objectives:
    - System performance monitoring tools
    - Resource optimization techniques
    - Performance profiling and benchmarking
    - Capacity planning for data pipelines
    """
    print("\nExercise 9: Performance Monitoring and Optimization")
    print("=" * 60)
    print("\nCreate a performance monitoring script that:")
    print("1. Tracks system resource usage over time")
    print("2. Identifies memory leaks in processes")
    print("3. Optimizes disk I/O for large file operations")
    print("4. Profiles command execution time")
    print("\nMonitoring commands to use:")
    print("  vmstat 1 10  # Virtual memory statistics")
    print("  iostat -dx 1 # Disk I/O statistics")
    print("  time command # Measure execution time")
    print("  /usr/bin/time -v command # Detailed resource usage")
    print("\n8GB RAM Specific Optimization:")
    print("- Use 'free -h' to monitor memory usage")
    print("- Set 'vm.swappiness=10' to reduce swapping")
    print("- Use 'ionice' for disk-intensive operations")

def exercise_10_troubleshooting_and_debugging():
    """
    Exercise 10: Troubleshooting and Debugging
    
    Scenario: Debug failing scripts and system issues.
    
    Tasks:
    1. Enable debug mode in bash scripts
    2. Capture and analyze error logs
    3. Use strace for system call tracing
    4. Analyze core dumps and crash reports
    5. Create reproducible test cases
    
    Learning Objectives:
    - Systematic debugging approach
    - Log analysis techniques
    - System call tracing
    - Error reproduction and testing
    """
    print("\nExercise 10: Troubleshooting and Debugging")
    print("=" * 60)
    print("\nCreate a debugging framework that:")
    print("1. Enables verbose logging with debug levels")
    print("2. Captures stack traces on errors")
    print("3. Logs environment variables and system state")
    print("4. Creates minimal reproducible test cases")
    print("\nDebugging techniques to implement:")
    print("  set -x  # Print commands as they execute")
    print("  trap 'echo \"Error at line $LINENO\"; exit 1' ERR")
    print("  strace -f -o trace.log ./script.sh")
    print("  bash -n script.sh  # Syntax check")
    print("\nMemory Debugging:")
    print("- Use 'valgrind' for memory leak detection")
    print("- Monitor with 'pmap' for process memory mapping")
    print("- Check for memory fragmentation issues")

def main():
    """Main function to run all exercises"""
    print("Linux & Bash Practice Exercises for Data Engineers")
    print("=" * 60)
    print("\nThese exercises focus on essential Linux skills for data engineering,")
    print("with special attention to 8GB RAM optimization and production practices.")
    print("\nEach exercise includes:")
    print("1. Real-world scenario")
    print("2. Specific tasks to complete")
    print("3. Learning objectives")
    print("4. Example commands")
    print("5. Memory optimization tips")
    print("\n" + "=" * 60)
    
    exercises = [
        exercise_1_text_processing,
        exercise_2_file_permissions,
        exercise_3_bash_scripting,
        exercise_4_process_management,
        exercise_5_disk_operations,
        exercise_6_network_utilities,
        exercise_7_environment_variables,
        exercise_8_automation_with_cron,
        exercise_9_performance_monitoring,
        exercise_10_troubleshooting_and_debugging,
    ]
    
    for i, exercise in enumerate(exercises, 1):
        exercise()
        if i < len(exercises):
            print("\n" + "-" * 60 + "\n")
    
    print("\n" + "=" * 60)
    print("Additional Resources:")
    print("- GNU Core Utilities documentation")
    print("- Bash Reference Manual")
    print("- Linux Performance by Brendan Gregg")
    print("- The Art of Command Line (GitHub)")
    print("\nRemember: Always test commands in a safe environment first!")
    print("Use 'man command' to read the manual for any command.")

if __name__ == "__main__":
    main()