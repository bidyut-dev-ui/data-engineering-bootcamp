# Week 3.5: Linux & Bash for Data Engineers

**Goal**: Master the command line skills needed for Airflow, Docker, and server management.

## Scenario
You are managing a Linux server that hosts your data pipelines. You need to generate logs, analyze them for errors, and secure sensitive configuration files.

## Concepts Covered
1. **Text Processing**: `grep` (find), `awk` (extract columns), `sed` (replace), `sort`, `uniq`.
2. **File Permissions**: `chmod` (change mode), `ls -l` (list details).
3. **IO Redirection**: `>` (write), `>>` (append), `|` (pipe).
4. **Bash Scripting**: Variables, loops, conditionals.

## Instructions

### 1. Setup
```bash
cd projects/03_5_linux_bash
```

### 2. Generate Data
Run the generator script to create fake server logs.
```bash
bash generate_logs.sh
```
*Check the `logs/` directory to see the created files.*

### 3. Analyze Logs
Run the analysis pipeline. This uses `awk` and `grep` to extract insights.
```bash
bash analyze_logs.sh
```

**Expected Output**:
```
=== LOG ANALYSIS REPORT ===
1. Total Requests: 100
2. 404 Errors: 12
3. 500 Errors: 8
4. Top 5 IP Addresses:
   ...
```

### 4. Manage Permissions
Learn how to secure files.
```bash
bash manage_permissions.sh
```
*Observe how the file permissions change in the output (e.g., `-rw-r--r--` to `-rw-------`).*

## Deep Dive: The Commands

### **Grep (Global Regular Expression Print)**
Finds lines matching a pattern.
```bash
grep "404" logs/access.log
```

### **Awk (Aho, Weinberger, and Kernighan)**
Extracts columns from text.
```bash
# Print the 1st column (IP address)
awk '{print $1}' logs/access.log
```

### **Piping (|)**
Passes the output of one command to the next.
```bash
# Get IPs -> Sort them -> Count unique -> Sort by count
awk '{print $1}' logs/access.log | sort | uniq -c | sort -nr
```

### **Chmod (Change Mode)**
- `chmod +x script.sh`: Make executable.
- `chmod 600 file`: Read/Write for owner, nothing for others.
- `chmod 755 file`: Read/Write/Execute for owner, Read/Execute for others.

## Interview Questions

**Q: How do you find all files containing the word "error" in a directory?**
A: `grep -r "error" /path/to/directory`

**Q: What does `chmod 777` do and why is it bad?**
A: It gives Read, Write, and Execute permissions to EVERYONE (Owner, Group, Others). It is a huge security risk.

**Q: How do you view the last 50 lines of a huge log file?**
A: `tail -n 50 large_file.log` (or `tail -f` to follow it live).

**Q: How do you check which processes are consuming the most CPU?**
A: Use `top` or `htop`.

## Homework / Challenge
1. Modify `analyze_logs.sh` to count requests by **Protocol** (HTTP/1.1 vs others).
2. Create a script that archives the logs: moves `*.log` to a `backup/` folder and zips them (`tar -czf`).
