#!/bin/bash

# Create a directory for logs if it doesn't exist
mkdir -p logs

echo "Generating log files..."

# Generate access.log
# Format: IP - [Date] "Method Path Protocol" Status Size
for i in {1..100}; do
    IP="192.168.1.$((RANDOM % 255))"
    STATUS_CODES=("200" "200" "200" "404" "500" "301")
    STATUS=${STATUS_CODES[$((RANDOM % ${#STATUS_CODES[@]}))]}
    PATHS=("/home" "/about" "/contact" "/products" "/api/data")
    PATH=${PATHS[$((RANDOM % ${#PATHS[@]}))]}
    
    echo "$IP - [$(date)] \"GET $PATH HTTP/1.1\" $STATUS $((RANDOM % 1000))" >> logs/access.log
done

# Generate error.log with some "sensitive" data
for i in {1..20}; do
    echo "[ERROR] Connection failed at $(date)" >> logs/error.log
    echo "[CRITICAL] DB password exposed: secret123" >> logs/error.log
done

echo "✅ Logs generated in ./logs/"
echo "   - logs/access.log (100 lines)"
echo "   - logs/error.log (40 lines)"
