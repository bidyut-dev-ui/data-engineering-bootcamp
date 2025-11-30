#!/bin/bash

# This script demonstrates permission handling
# In a real scenario, you might use this to secure keys or logs

echo "=== PERMISSION MANAGER ==="

# 1. Create a "sensitive" file
echo "SUPER_SECRET_API_KEY=12345" > secret_config.env
echo "Created secret_config.env"

# Check current permissions
ls -l secret_config.env

# 2. Lock it down (Read/Write for owner ONLY)
echo -e "\nLocking down file (chmod 600)..."
chmod 600 secret_config.env
ls -l secret_config.env

# 3. Make a script executable
echo -e "\nMaking analyze_logs.sh executable (chmod +x)..."
chmod +x analyze_logs.sh
ls -l analyze_logs.sh

echo -e "\n✅ Permissions updated."
