# Linux & Bash Interview Questions for Data Engineers

## Overview
This document contains interview questions for Linux command line and Bash scripting skills essential for data engineering roles. Questions cover text processing, system administration, scripting, and optimization for resource-constrained environments (8GB RAM).

## Table of Contents
1. [Beginner Questions](#beginner-questions)
2. [Intermediate Questions](#intermediate-questions)
3. [Advanced Questions](#advanced-questions)
4. [System Administration](#system-administration)
5. [Performance & Optimization](#performance--optimization)
6. [Security & Permissions](#security--permissions)
7. [Scenario-Based Questions](#scenario-based-questions)
8. [Practical Exercises](#practical-exercises)
9. [Evaluation Rubric](#evaluation-rubric)

---

## Beginner Questions

### 1. Core Linux Commands
**Q1.1:** What is the difference between `grep`, `awk`, and `sed`? When would you use each?
**Q1.2:** How do you view the first 10 and last 10 lines of a file?
**Q1.3:** Explain the difference between `>` and `>>` operators.
**Q1.4:** How do you find all files modified in the last 7 days?
**Q1.5:** What does `chmod 755` mean? Break down the octal notation.

### 2. File Operations
**Q2.1:** How do you copy a directory recursively while preserving permissions?
**Q2.2:** What's the difference between `cp` and `rsync`?
**Q2.3:** How do you find and delete files older than 30 days?
**Q2.4:** Explain the difference between hard links and symbolic links.
**Q2.5:** How do you check disk usage by directory?

### 3. Process Management
**Q3.1:** How do you list all processes and sort by memory usage?
**Q3.2:** What's the difference between `kill` and `kill -9`?
**Q3.3:** How do you run a process in the background and bring it to foreground?
**Q3.4:** What does `nohup` do and when would you use it?
**Q3.5:** How do you check which process is using a specific port?

### 4. Basic Bash Scripting
**Q4.1:** How do you pass arguments to a bash script and access them?
**Q4.2:** What's the difference between `$@` and `$*`?
**Q4.3:** How do you check if a file exists in bash?
**Q4.4:** Write a simple bash script that takes a filename as input and counts lines, words, and characters.
**Q4.5:** How do you make a bash script executable?

---

## Intermediate Questions

### 5. Text Processing
**Q5.1:** Given a CSV file, how would you extract the 3rd column?
**Q5.2:** How do you remove duplicate lines from a file while preserving order?
**Q5.3:** Write a command to find all lines containing "ERROR" but not "WARNING".
**Q5.4:** How would you replace all occurrences of "foo" with "bar" in all `.txt` files recursively?
**Q5.5:** How do you count the frequency of each word in a text file?

### 6. Shell Scripting
**Q6.1:** What does `set -euo pipefail` do and why is it important?
**Q6.2:** How do you handle errors in bash scripts?
**Q6.3:** What's the difference between `[ ]` and `[[ ]]` in bash?
**Q6.4:** How do you parse command-line options in bash (short and long options)?
**Q6.5:** Write a script that processes files in parallel with a limit of 4 concurrent processes.

### 7. System Monitoring
**Q7.1:** How do you monitor CPU, memory, and disk I/O in real-time?
**Q7.2:** What commands would you use to identify a memory leak?
**Q7.3:** How do you check system load average and what do the three numbers mean?
**Q7.4:** How would you monitor network connections and bandwidth usage?
**Q7.5:** What's the difference between `free -m` and `vmstat`?

### 8. Environment & Configuration
**Q8.1:** What's the difference between `.bashrc`, `.bash_profile`, and `.profile`?
**Q8.2:** How do you set environment variables for a script without affecting the parent shell?
**Q8.3:** What does `source` command do vs executing a script?
**Q8.4:** How do you make an alias permanent?
**Q8.5:** Explain the `PATH` environment variable and how it's used.

---

## Advanced Questions

### 9. Performance Optimization
**Q9.1:** How would you optimize a bash script that processes 100GB of log files on a system with 8GB RAM?
**Q9.2:** What are the memory implications of using `sort` on large files? How would you handle it?
**Q9.3:** How do you prevent the OOM (Out Of Memory) killer from terminating important processes?
**Q9.4:** What's the most efficient way to concatenate thousands of small files into one large file?
**Q9.5:** How would you monitor and optimize swap usage?

### 10. Advanced Text Manipulation
**Q10.1:** Write an `awk` one-liner to calculate the sum of the 2nd column in a CSV.
**Q10.2:** How do you extract text between two patterns using `sed`?
**Q10.3:** Write a command to find the 10 most common IP addresses in an Apache log file.
**Q10.4:** How would you convert a TSV file to CSV while handling embedded commas?
**Q10.5:** Write a pipeline to find all unique users who logged in today from auth.log.

### 11. Process Control & Signals
**Q11.1:** How do you handle SIGTERM and SIGINT in a bash script?
**Q11.2:** What's the difference between job control and process groups?
**Q11.3:** How do you daemonize a process properly?
**Q11.4:** Write a script that restarts a process if it dies, but not more than 5 times in a minute.
**Q11.5:** How do you limit CPU and memory usage of a process?

### 12. Advanced Bash Features
**Q12.1:** What are bash arrays and how do you use them?
**Q12.2:** Explain process substitution (`<()` and `>()`).
**Q12.3:** How do you create and use named pipes (FIFOs)?
**Q12.4:** What are bash traps and how are they useful?
**Q12.5:** How do you implement timeouts in bash scripts?

---

## System Administration

### 13. User & Permission Management
**Q13.1:** How do you create a user with a specific home directory and shell?
**Q13.2:** What's the difference between `su` and `sudo`?
**Q13.3:** How do you set up passwordless SSH authentication?
**Q13.4:** Explain the difference between `umask 022` and `umask 027`.
**Q13.5:** How do you find all files with SUID/SGID bits set?

### 14. Disk & Filesystem
**Q14.1:** What's the difference between `ext4`, `xfs`, and `btrfs`?
**Q14.2:** How do you resize a partition without losing data?
**Q14.3:** What's the purpose of `/etc/fstab` and how do you edit it safely?
**Q14.4:** How do you check and repair filesystem errors?
**Q14.5:** What's the difference between `du` and `df`?

### 15. Networking
**Q15.1:** How do you check if a port is open on a remote server?
**Q15.2:** What's the difference between `netstat`, `ss`, and `lsof` for network monitoring?
**Q15.3:** How do you route traffic through a specific interface?
**Q15.4:** Explain the purpose of `iptables` vs `firewalld`.
**Q15.5:** How do you troubleshoot DNS resolution issues?

### 16. Package Management
**Q16.1:** What's the difference between `apt-get`, `yum`, and `dnf`?
**Q16.2:** How do you find which package provides a specific file?
**Q16.3:** How do you pin a package version to prevent updates?
**Q16.4:** What's the difference between installing from source vs package manager?
**Q16.5:** How do you create a local package repository?

---

## Performance & Optimization

### 17. Memory Management (8GB RAM Focus)
**Q17.1:** How would you configure swap space on an 8GB RAM system?
**Q17.2:** What kernel parameters would you tune for better memory management?
**Q17.3:** How do you identify memory leaks in long-running processes?
**Q17.4:** What's the difference between RSS, VSZ, and USS in memory usage?
**Q17.5:** How do you limit memory usage of a specific process?

### 18. I/O Optimization
**Q18.1:** How do you measure disk I/O performance?
**Q18.2:** What's the difference between synchronous and asynchronous I/O?
**Q18.3:** How do you optimize read/write operations for large sequential files?
**Q18.4:** What's the impact of filesystem block size on performance?
**Q18.5:** How do you use `ionice` to prioritize I/O operations?

### 19. CPU Optimization
**Q19.1:** How do you pin processes to specific CPU cores?
**Q19.2:** What's the difference between `nice` and `renice`?
**Q19.3:** How do you monitor CPU cache misses?
**Q19.4:** What are CPU affinity and how do you set it?
**Q19.5:** How do you identify CPU-bound vs I/O-bound processes?

### 20. Network Optimization
**Q20.1:** How do you tune TCP parameters for high-throughput data transfer?
**Q20.2:** What's the difference between `netcat` and `socat`?
**Q20.3:** How do you measure network latency and bandwidth?
**Q20.4:** What are MTU and MSS, and how do they affect performance?
**Q20.5:** How do you troubleshoot packet loss?

---

## Security & Permissions

### 21. File Security
**Q21.1:** What's the difference between `chmod`, `chown`, and `chgrp`?
**Q21.2:** How do you set up ACLs (Access Control Lists)?
**Q21.3:** What are sticky bits and when are they used?
**Q21.4:** How do you find world-writable files?
**Q21.5:** What's the security implication of SUID/SGID binaries?

### 22. System Security
**Q22.1:** How do you audit failed login attempts?
**Q22.2:** What's the purpose of SELinux/AppArmor?
**Q22.3:** How do you secure SSH server configuration?
**Q22.4:** What are the best practices for firewall configuration?
**Q22.5:** How do you monitor for rootkit infections?

### 23. Secure Scripting
**Q23.1:** How do you safely handle passwords in bash scripts?
**Q23.2:** What are the risks of using `eval` in bash?
**Q23.3:** How do you prevent shell injection attacks?
**Q23.4:** What's the secure way to create temporary files?
**Q23.5:** How do you validate and sanitize user input in scripts?

---

## Scenario-Based Questions

### 24. Log Analysis Scenarios
**Q24.1:** You have a 50GB Apache log file. How would you find the top 10 IP addresses making requests, while using less than 2GB of RAM?
**Q24.2:** A log file contains timestamps in mixed formats (some ISO, some epoch). How would you normalize them all to ISO format?
**Q24.3:** You need to extract all unique error messages from application logs, but the file is too large to load into memory. What's your approach?
**Q24.4:** How would you monitor a log file in real-time and send alerts when specific patterns appear?
**Q24.5:** You have daily log files for the past year. How would you generate a monthly summary report?

### 25. Data Processing Scenarios
**Q25.1:** You need to merge 1000 CSV files, each 100MB, into a single file. How would you do this efficiently?
**Q25.2:** A process is writing to a file, and you need to read from it simultaneously without blocking. How would you accomplish this?
**Q25.3:** You have a pipeline that processes data through 5 different bash scripts. How would you ensure proper error handling and restart from failure point?
**Q25.4:** How would you convert a 10GB JSON file to CSV using command-line tools?
**Q25.5:** You need to distribute processing of a large file across multiple machines. How would you split the work and combine results?

### 26. System Administration Scenarios
**Q26.1:** A server with 8GB RAM is experiencing high memory usage. How would you diagnose the issue?
**Q26.2:** You need to deploy a bash script to 100 servers. How would you ensure consistent execution and collect results?
**Q26.3:** A critical production script suddenly starts failing. How would you debug it without affecting the running system?
**Q26.4:** You need to migrate 1TB of data between servers with minimal downtime. What's your strategy?
**Q26.5:** How would you implement rolling log rotation for an application that writes 10GB of logs daily?

### 27. Optimization Scenarios
**Q27.1:** A bash script processing database dumps is taking 8 hours. How would you profile and optimize it?
**Q27.2:** You have a script that downloads files from 100 URLs sequentially. How would you parallelize it safely?
**Q27.3:** A cron job is causing high I/O wait during business hours. How would you reschedule or throttle it?
**Q27.4:** How would you implement a rate limiter in bash for API calls?
**Q27.5:** You need to process streaming data from a socket. How would you handle backpressure and buffer management?

---

## Practical Exercises

### Exercise 1: Log Analysis Pipeline
Create a bash script that:
1. Takes a directory of log files as input
2. Processes each file to extract error counts by hour
3. Generates a summary report in CSV format
4. Sends an alert if error rate exceeds threshold
5. Handles log rotation (processes .gz files)
6. Uses less than 1GB RAM regardless of log size

### Exercise 2: System Monitoring Dashboard
Create a set of scripts that:
1. Monitor CPU, memory, disk, and network usage
2. Store metrics in a time-series format
3. Generate HTML dashboard with charts
4. Send alerts when thresholds are breached
5. Support historical data analysis (last 30 days)
6. Run efficiently on 8GB RAM system

### Exercise 3: Data Processing Framework
Design a bash-based ETL framework that:
1. Processes CSV, JSON, and XML files
2. Validates data schema and quality
3. Handles malformed records gracefully
4. Supports incremental processing
5. Maintains audit logs
6. Can resume from failure point

### Exercise 4: Secure File Transfer System
Implement a secure file transfer system that:
1. Encrypts files before transfer
2. Verifies integrity with checksums
3. Supports resumable transfers
4. Logs all transfers for audit
5. Limits bandwidth usage during business hours
6. Integrates with existing authentication systems

### Exercise 5: Container Management Scripts
Create scripts to manage Docker containers that:
1. Monitor container resource usage
2. Restart failed containers automatically
3. Rotate container logs
4. Update containers with zero downtime
5. Backup container data
6. Generate resource usage reports

---

## Evaluation Rubric

### Technical Knowledge (40%)
- **Excellent (35-40 pts)**: Demonstrates deep understanding of Linux internals, bash advanced features, system administration, and performance optimization. Can explain trade-offs between different approaches.
- **Good (25-34 pts)**: Solid understanding of core commands, scripting, and system monitoring. Can solve complex problems but may need guidance on advanced topics.
- **Fair (15-24 pts)**: Basic command knowledge, can write simple scripts but struggles with optimization and advanced features.
- **Poor (0-14 pts)**: Limited Linux experience, cannot write functional scripts or troubleshoot basic issues.

### Problem-Solving Ability (30%)
- **Excellent (25-30 pts)**: Approaches problems systematically, considers multiple solutions, evaluates trade-offs, proposes innovative solutions for resource constraints.
- **Good (18-24 pts)**: Identifies key issues, proposes reasonable solutions, considers practical constraints like 8GB RAM limit.
- **Fair (10-17 pts)**: Struggles to identify root causes, proposes simplistic or impractical solutions.
- **Poor (0-9 pts)**: Cannot articulate problem-solving approach or propose viable solutions.

### Scripting & Automation (20%)
- **Excellent (17-20 pts)**: Writes robust, production-ready scripts with proper error handling, logging, and resource management. Follows best practices.
- **Good (12-16 pts)**: Functional scripts with some error handling. Minor issues with edge cases or resource optimization.
- **Fair (7-11 pts)**: Scripts work but have significant issues (poor error handling, inefficient code, security issues).
- **Poor (0-6 pts)**: Scripts do not work, major structural issues, ignores best practices.

### Security & Reliability (10%)
- **Excellent (9-10 pts)**: Implements secure practices, proper error handling, logging, and monitoring. Considers edge cases and failure scenarios.
- **Good (6-8 pts)**: Basic security and reliability considerations. Some gaps in comprehensive error handling.
- **Fair (3-5 pts)**: Minimal security considerations, poor error handling.
- **Poor (0-2 pts)**: Security vulnerabilities, no error handling.

### Total Score Interpretation
- **90-100 pts**: Expert level, ready for senior/architect roles
- **75-89 pts**: Strong intermediate, ready for production responsibilities
- **60-74 pts**: Competent, suitable for junior roles with supervision
- **40-59 pts**: Needs significant improvement and training
- **0-39 pts**: Not ready for Linux/Bash responsibilities

---

## Common Interview Patterns

### 1. **The "Explain in Detail" Question**
*Example: "Explain what happens when you type `ls -l` and press Enter"*
- Cover: shell parsing, PATH lookup, system calls, terminal output
- Mention: inode reading, permission checking, formatting output

### 2. **The "Optimize This" Question**
*Example: "This script is slow with large files. How would you optimize it?"*
- Identify bottlenecks: I/O, memory, CPU
- Suggest: streaming processing, parallelization, efficient commands
- Consider: trade-offs between simplicity and performance

### 3. **The "Debug This" Question**
*Example: "This script fails sometimes. What could be wrong?"*
- Check: error handling, race conditions, resource limits
- Test: edge cases, large inputs, permission issues
- Suggest: logging, monitoring, defensive programming

### 4. **The "Design a Solution" Question**
*Example: "Design a system to process daily log files from 100 servers"*
- Consider: scalability, reliability, monitoring
- Address: error handling, data consistency, performance
- Include: deployment, maintenance, troubleshooting

---

## Preparation Resources

### Recommended Reading
1. **Books**:
   - "The Linux Command Line" by William Shotts
   - "Bash Cookbook" by Carl Albing and JP Vossen
   - "Linux System Administration" by Tom Adelstein and Bill Lubanovic

2. **Online Resources**:
   - GNU Core Utilities documentation
   - Bash Reference Manual
   - Linux Documentation Project
   - Stack Overflow Bash tag

3. **Practice Platforms**:
   - OverTheWire Bandit (security-focused)
   - HackerRank Linux Shell challenges
   - Codewars Bash katas
   - Advent of Code (bash solutions)

### Key Concepts to Master
1. **Text Processing**: `grep`, `awk`, `sed`, `sort`, `uniq`, `cut`, `paste`
2. **File Operations**: `find`, `xargs`, `tar`, `rsync`, `dd`
3. **Process Management**: `ps`, `top`, `htop`, `kill`, `nohup`, `screen`, `tmux`
4. **Networking**: `netstat`, `ss`, `curl`, `wget`, `nc`, `ssh`, `scp`
5. **System Monitoring**: `vmstat`, `iostat`, `sar`, `dstat`, `iotop`
6. **Performance Tools**: `time`, `strace`, `ltrace`, `perf`, `valgrind`

### Practice Projects
1. **Log Analysis System**: Process Apache/nginx logs, generate reports, send alerts
2. **System Monitor**: Collect metrics, create dashboards, implement alerting
3. **Backup Script**: Incremental backups, encryption, verification, rotation
4. **Deployment Automation**: Scripted deployments with rollback capability
5. **Data Pipeline**: ETL process with validation, error handling, monitoring

---

## Interview Tips

### 1. **Think Aloud**
- Explain your thought process
- Ask clarifying questions
- Mention trade-offs and considerations

### 2. **Start Simple, Then Optimize**
- First make it work, then make it fast
- Mention naive solution, then optimized version
- Consider edge cases and error handling

### 3. **Know Your Tools**
- Mention alternative approaches
- Explain why you chose a specific tool
- Acknowledge limitations of your approach

### 4. **Consider Constraints**
- Always mention memory/CPU/disk constraints
- Discuss scalability implications
- Think about maintenance and monitoring

### 5. **Write Readable Code**
- Use meaningful variable names
- Add comments for complex logic
- Follow shell scripting best practices

### 6. **Test Your Solutions**
- Mention how you would test
- Consider edge cases
- Discuss error scenarios

---

## Final Advice

1. **Practice Daily**: Use Linux as your daily driver
2. **Read Manuals**: `man` pages are your best friend
3. **Learn by Doing**: Solve real problems, not just exercises
4. **Understand Internals**: Know how things work, not just how to use them
5. **Stay Updated**: Linux and tools evolve constantly
6. **Contribute**: Share scripts, answer questions, participate in communities

Remember: The best Linux engineers aren't just command memorizers—they're problem solvers who understand how the system works and can apply that knowledge creatively.

---

*Last Updated: April 2026*  
*Focus: Data Engineering, System Administration, 8GB RAM Optimization*