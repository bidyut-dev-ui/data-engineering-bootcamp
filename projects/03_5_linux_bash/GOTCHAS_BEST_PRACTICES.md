# Linux & Bash Gotchas and Best Practices for Data Engineers

## Overview
This document covers common pitfalls, optimization techniques, and best practices for using Linux and Bash in data engineering workflows, with special attention to 8GB RAM constraints.

## Table of Contents
1. [Text Processing Gotchas](#text-processing-gotchas)
2. [File Permission Pitfalls](#file-permission-pitfalls)
3. [Bash Scripting Anti-Patterns](#bash-scripting-anti-patterns)
4. [Process Management Issues](#process-management-issues)
5. [Disk Operations Problems](#disk-operations-problems)
6. [Memory Optimization (8GB RAM Focus)](#memory-optimization-8gb-ram-focus)
7. [Security Best Practices](#security-best-practices)
8. [Performance Optimization](#performance-optimization)
9. [Debugging Techniques](#debugging-techniques)
10. [Production Readiness Checklist](#production-readiness-checklist)

---

## Text Processing Gotchas

### 1. **Grep with Large Files**
**Gotcha**: Using `grep` on multi-GB files without options can cause memory issues.
```bash
# ❌ Bad: Loads entire file into memory
grep "error" huge.log

# ✅ Good: Use --line-buffered for streaming
grep --line-buffered "error" huge.log

# ✅ Better: Use pv for progress monitoring
pv huge.log | grep "error" > errors.txt
```

**Best Practice**: For files >1GB, use:
- `grep --line-buffered` for real-time processing
- `split` to process in chunks
- `pv` (pipe viewer) to monitor progress

### 2. **Awk Memory Consumption**
**Gotcha**: Awk stores entire arrays in memory.
```bash
# ❌ Bad: Counting unique values in huge file
awk '{count[$1]++} END {for (i in count) print i, count[i]}' huge.csv

# ✅ Good: Use sort/uniq for large datasets
cut -d, -f1 huge.csv | sort | uniq -c | sort -nr
```

**Optimization**: 
- Use `mawk` instead of `gawk` for better memory efficiency
- Process files in chunks with `split -l 1000000`
- Use `LC_ALL=C` for faster sorting: `LC_ALL=C sort file`

### 3. **Sed In-Place Editing**
**Gotcha**: `sed -i` creates temporary files that can fill disk.
```bash
# ❌ Bad: On large files, creates temp file of same size
sed -i 's/old/new/g' 10GB_file.txt

# ✅ Good: Process in chunks
split -l 1000000 10GB_file.txt chunk_
for f in chunk_*; do
  sed 's/old/new/g' "$f" > "${f}_processed"
  rm "$f"
done
cat chunk_*_processed > result.txt
```

### 4. **Sort Memory Limits**
**Gotcha**: `sort` uses memory based on file size.
```bash
# ❌ Bad: Sorting huge file with default memory
sort huge_file.csv > sorted.csv

# ✅ Good: Specify memory limits
sort --buffer-size=1G --parallel=2 huge_file.csv > sorted.csv

# ✅ Better: Use external sort for very large files
sort --buffer-size=500M --temporary-directory=/tmp/sort_tmp huge_file.csv
```

**8GB RAM Tip**: Set `--buffer-size=2G` max to leave room for other processes.

---

## File Permission Pitfalls

### 1. **Umask Misunderstanding**
**Gotcha**: Default permissions may expose sensitive data.
```bash
# ❌ Bad: Creating files without considering umask
touch config.yaml  # Might be 644 (world-readable)

# ✅ Good: Set secure umask
umask 0077  # Results in 600 for files, 700 for directories
touch config.yaml
```

**Best Practice**: Add to `~/.bashrc`:
```bash
# Secure default for data engineering
umask 0077  # Owner only
```

### 2. **Setuid/Setgid Dangers**
**Gotcha**: Incorrect use of special permissions.
```bash
# ❌ Dangerous: Making scripts setuid
chmod 4755 script.sh  # Security risk!

# ✅ Safe: Use sudo or proper group permissions
sudo ./script.sh
# OR
chgrp data_team script.sh
chmod 2750 script.sh  # setgid, group executable
```

### 3. **ACL Overcomplication**
**Gotcha**: Using ACLs when simple permissions suffice.
```bash
# ❌ Overcomplicated
setfacl -m u:alice:rwx file.txt
setfacl -m g:data_team:rx file.txt

# ✅ Simpler (if possible)
chgrp data_team file.txt
chmod 750 file.txt
```

**Rule**: Use ACLs only when standard Unix permissions are insufficient.

---

## Bash Scripting Anti-Patterns

### 1. **Missing Error Handling**
**Gotcha**: Scripts fail silently.
```bash
#!/bin/bash
# ❌ Bad: No error checking
cd /nonexistent
rm -rf *.tmp  # Dangerous if cd failed!

# ✅ Good: Fail fast
set -euo pipefail
cd /nonexistent || { echo "Directory not found"; exit 1; }
rm -rf *.tmp
```

**Essential Settings**:
```bash
#!/bin/bash
set -e          # Exit on error
set -u          # Error on undefined variables
set -o pipefail # Catch pipeline failures
```

### 2. **Unquoted Variables**
**Gotcha**: Spaces and special characters cause issues.
```bash
# ❌ Bad
file=$1
rm $file  # Fails if $file contains spaces

# ✅ Good
file="$1"
rm "$file"
```

**Rule**: Always quote variables: `"$var"`, `"${array[@]}"`

### 3. **Subshell Overuse**
**Gotcha**: Creating unnecessary subshells wastes resources.
```bash
# ❌ Inefficient
count=$(cat file.txt | wc -l)

# ✅ Efficient
count=$(wc -l < file.txt)
```

**Optimization**: 
- Use process substitution: `diff <(sort file1) <(sort file2)`
- Avoid pipes when direct redirection works

### 4. **Global Variable Pollution**
**Gotcha**: Variables leak between functions.
```bash
# ❌ Bad
process_data() {
  result="..."  # Global by default
}

# ✅ Good
process_data() {
  local result="..."  # Local scope
}
```

**Best Practice**: Use `local` for all function variables.

---

## Process Management Issues

### 1. **Zombie Processes**
**Gotcha**: Child processes not reaped.
```bash
# ❌ Bad: No signal handling
./long_running.sh &

# ✅ Good: Trap signals
trap 'kill $(jobs -p)' EXIT
./long_running.sh &
wait  # Reap child processes
```

### 2. **Resource Leaks**
**Gotcha**: File descriptors not closed.
```bash
# ❌ Bad
exec 3< input.txt
# ... use fd 3 ...
# Forgot: exec 3<&-

# ✅ Good: Use automatic cleanup
{
  exec 3< input.txt
  # ... use fd 3 ...
}  # fd 3 automatically closed
```

### 3. **Signal Propagation**
**Gotcha**: Background processes don't receive signals.
```bash
# ❌ Bad
./server.sh &
# Ctrl+C kills parent but not child

# ✅ Good: Use job control
set -m  # Enable job control
./server.sh &
fg  # Bring to foreground to receive signals
```

---

## Disk Operations Problems

### 1. **Full Disk During Operations**
**Gotcha**: Operations fail mid-way.
```bash
# ❌ Risky
tar -czf backup.tar.gz /data  # Might fill disk

# ✅ Safe: Check disk space first
required=$(du -s /data | cut -f1)
available=$(df /backup | tail -1 | awk '{print $4}')
if (( required * 110 / 100 > available )); then
  echo "Insufficient disk space"
  exit 1
fi
```

### 2. **Inefficient File Copying**
**Gotcha**: `cp` vs `rsync` misuse.
```bash
# ❌ For large directories
cp -r /source /dest  # No resume, no verification

# ✅ Better
rsync -av --progress /source/ /dest/
# Resume with: rsync -av --partial /source/ /dest/
```

### 3. **Inode Exhaustion**
**Gotcha**: Many small files fill inodes before disk.
```bash
# Monitor inode usage
df -i  # Check inode usage
# Clean up small files
find /tmp -type f -name "*.tmp" -mtime +7 -delete
```

---

## Memory Optimization (8GB RAM Focus)

### 1. **Command Memory Footprint**
**Tool-Specific Optimizations**:

| Tool | Default Issue | 8GB RAM Fix |
|------|--------------|-------------|
| `grep` | Buffers entire pattern space | Use `--line-buffered`, `-m` limit |
| `sort` | Tries to use all memory | `--buffer-size=2G --parallel=2` |
| `awk` | Array memory bloat | Use `mawk`, process in chunks |
| `find` | Large result sets | Use `-print0 | xargs -0` |
| `tar` | Memory during compression | Use `--use-compress-program=pigz` |

### 2. **Swap Configuration**
**Gotcha**: Poor swap settings cause thrashing.
```bash
# ✅ Optimal for 8GB RAM
sudo sysctl vm.swappiness=10        # Reduce swapping tendency
sudo sysctl vm.vfs_cache_pressure=50 # Keep dentry/inode cache
```

### 3. **OOM Killer Prevention**
**Best Practice**: Set process limits.
```bash
# In scripts
ulimit -v 2000000  # 2GB virtual memory limit
ulimit -m 1500000  # 1.5GB resident set limit
```

### 4. **Monitoring Memory Usage**
**Essential Commands**:
```bash
# Real-time monitoring
htop --sort-key=PERCENT_MEM  # Sort by memory usage

# Process-specific
ps aux --sort=-%mem | head -10  # Top memory users

# Detailed analysis
pmap -x $(pidof process)  # Memory map of process
```

---

## Security Best Practices

### 1. **Credential Management**
**Never Do**:
```bash
# ❌ NEVER hardcode credentials
password="secret123"
api_key="abc123def456"

# ❌ DON'T store in world-readable files
chmod 644 .env  # Bad!
```

**Best Practices**:
```bash
# ✅ Use environment variables
export DB_PASSWORD=$(cat /run/secrets/db_password)

# ✅ Secure file permissions
chmod 600 .env.production
chown root:root .env.production

# ✅ Use keyrings or secret managers
# AWS Secrets Manager, HashiCorp Vault, etc.
```

### 2. **Input Validation**
**Gotcha**: Trusting user input in scripts.
```bash
# ❌ Dangerous
read -p "Enter filename: " file
rm "$file"  # Could be "../../etc/passwd"

# ✅ Safe: Validate input
read -p "Enter filename: " file
if [[ ! "$file" =~ ^[a-zA-Z0-9_.-]+$ ]]; then
  echo "Invalid filename"
  exit 1
fi
```

### 3. **Secure Temporary Files**
**Gotcha**: Predictable temp file names.
```bash
# ❌ Predictable
tempfile="/tmp/script_$$.tmp"

# ✅ Secure
tempfile=$(mktemp /tmp/script_XXXXXXXXXX)
trap 'rm -f "$tempfile"' EXIT  # Cleanup on exit
```

---

## Performance Optimization

### 1. **Command Chaining Efficiency**
**Inefficient**:
```bash
cat file.txt | grep "error" | sort | uniq -c
```

**Efficient**:
```bash
# Single pass when possible
awk '/error/ {count[$0]++} END {for (line in count) print count[line], line}' file.txt

# Use built-in sorting
grep "error" file.txt | sort -u
```

### 2. **Parallel Processing**
**For Multi-core Systems**:
```bash
# Process files in parallel
find . -name "*.log" -print0 | xargs -0 -P 4 -I {} sh -c 'process_log "{}"'

# GNU Parallel (more powerful)
parallel -j 4 process_log ::: *.log
```

### 3. **I/O Optimization**
**Reduce Disk I/O**:
```bash
# ❌ Multiple reads
grep "A" file.txt > a.txt
grep "B" file.txt > b.txt

# ✅ Single read
awk '/A/ {print > "a.txt"} /B/ {print > "b.txt"}' file.txt
```

---

## Debugging Techniques

### 1. **Verbose Script Execution**
```bash
#!/bin/bash
set -x  # Print commands as executed
set -v  # Print shell input lines

# Or run script with
bash -x script.sh
```

### 2. **Tracing System Calls**
```bash
# Trace file operations
strace -e trace=file script.sh

# Trace network calls
strace -e trace=network script.sh
```

### 3. **Memory Debugging**
```bash
# Check for memory leaks
valgrind --leak-check=full ./script.sh

# Monitor memory usage
/usr/bin/time -v ./script.sh  # Detailed resource usage
```

### 4. **Performance Profiling**
```bash
# Time each command
time (command1; command2; command3)

# Profile CPU usage
perf stat ./script.sh
```

---

## Production Readiness Checklist

### Script Quality
- [ ] `set -euo pipefail` at top
- [ ] All variables quoted: `"$var"`
- [ ] Functions use `local` variables
- [ ] Error messages go to stderr: `echo "Error" >&2`
- [ ] Exit codes meaningful (0=success, non-zero=failure)
- [ ] Input validation for all arguments
- [ ] Safe temporary file creation with `mktemp`
- [ ] Cleanup traps: `trap 'cleanup' EXIT`

### Security
- [ ] No hardcoded credentials
- [ ] File permissions appropriate (600 for secrets)
- [ ] No world-writable directories
- [ ] Input sanitization for user-provided data
- [ ] Use of secure random: `/dev/urandom`
- [ ] No `eval` or indirect execution of user input

### Performance
- [ ] Memory limits set: `ulimit -v`
- [ ] Large file processing in chunks
- [ ] Efficient command chaining (minimize pipes)
- [ ] Parallel processing where applicable
- [ ] Disk I/O minimized

### Monitoring
- [ ] Logging to syslog or structured logs
- [ ] Progress indicators for long operations
- [ ] Resource usage logging (CPU, memory, disk)
- [ ] Alerting on failures
- [ ] Metrics export for Prometheus/Graphite

### Documentation
- [ ] Usage: `./script.sh --help`
- [ ] README with examples
- [ ] Dependencies listed
- [ ] Environment variables documented
- [ ] Exit codes documented

### Deployment
- [ ] Versioned in Git
- [ ] CI/CD pipeline
- [ ] Testing suite
- [ ] Rollback procedure
- [ ] Configuration externalized

---

## Common Pitfalls Summary

### 1. **The `rm -rf /` Disaster**
**Never** use variables with `rm -rf` without validation:
```bash
# ❌ CATASTROPHIC
dir="$1"
rm -rf "/$dir"  # If $1 is empty, becomes rm -rf /

# ✅ Safe
[[ -n "$dir" ]] && rm -rf "/$dir"
```

### 2. **Bash Arithmetic Gotchas**
```bash
# ❌ Wrong: string comparison
if [ $count > 10 ]; then ...

# ✅ Correct: arithmetic comparison
if (( count > 10 )); then ...
if [ $count -gt 10 ]; then ...
```

### 3. **Pathname Expansion Surprises**
```bash
# ❌ Fails if no .txt files
for file in *.txt; do
  echo "Processing $file"
done

# ✅ Safe
shopt -s nullglob
for file in *.txt; do
  echo "Processing $file"
done
```

### 4. **Date/Time Parsing Issues**
```bash
# ❌ Platform-dependent
date -d "yesterday"

# ✅ Portable
date -d "1 day ago"
date --date="1 day ago"
```

---

## Quick Reference

### Essential Options
```bash
# Safety first
set -euo pipefail

# Secure defaults
umask 0077

# Memory limits
ulimit -v 2000000  # 2GB virtual memory

# Efficient sorting
export LC_ALL=C
```

### Performance Commands
```bash
# Monitor memory
htop --sort-key=PERCENT_MEM

# Find large files
find / -type f -size +100M -exec ls -lh {} \;

# Check disk I/O
iotop

# Monitor network
nethogs
```

### Debugging Commands
```bash
# Trace execution
bash -x script.sh

# Check syntax
bash -n script.sh

# Profile time
time ./script.sh

# Memory debug
valgrind --tool=memcheck ./script.sh
```

---

## Final Recommendations

1. **Test with Large Data**: Always test scripts with representative data sizes.
2. **Monitor Resource Usage**: Use `htop`, `iotop`, `nethogs` during development.
3. **Implement Graceful Degradation**: Scripts should handle resource constraints gracefully.
4. **Use Version Control**: All scripts should be in Git with meaningful commits.
5. **Document Assumptions**: Clearly document hardware requirements and limitations.
6. **Plan for Failure**: Implement retry logic, checkpointing, and recovery procedures.
7. **Security First**: Assume the script will run in a production environment with sensitive data.

Remember: On 8GB RAM systems, every megabyte counts. Optimize for memory first, then CPU, then I/O.

---

*Last Updated: April 2026*  
*Focus: Data Engineering, 8GB RAM Optimization, Production Readiness*