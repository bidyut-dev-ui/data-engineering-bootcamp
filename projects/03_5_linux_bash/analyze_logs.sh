#!/bin/bash

LOG_FILE="logs/access.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Error: $LOG_FILE not found. Run generate_logs.sh first."
    exit 1
fi

echo "=== LOG ANALYSIS REPORT ==="
echo

# 1. Count total requests
TOTAL=$(wc -l < "$LOG_FILE")
echo "1. Total Requests: $TOTAL"

# 2. Count 404 Errors (using grep)
ERRORS_404=$(grep " 404 " "$LOG_FILE" | wc -l)
echo "2. 404 Errors: $ERRORS_404"

# 3. Count 500 Errors
ERRORS_500=$(grep " 500 " "$LOG_FILE" | wc -l)
echo "3. 500 Errors: $ERRORS_500"

# 4. Top 5 IP Addresses (using awk, sort, uniq)
echo "4. Top 5 IP Addresses:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 5

# 5. Most Requested Paths
echo "5. Most Requested Paths:"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 5

echo
echo "=== END REPORT ==="
