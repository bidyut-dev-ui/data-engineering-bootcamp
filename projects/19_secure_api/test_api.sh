#!/bin/bash

# Test script for JWT authentication

BASE_URL="http://localhost:8000"

echo "=== Testing Secure API ==="
echo

# 1. Test public endpoint (no auth)
echo "1. Testing public endpoint (no authentication)..."
curl -s $BASE_URL/data/public | jq
echo

# 2. Login as admin
echo "2. Logging in as admin..."
ADMIN_TOKEN=$(curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

echo "Admin token: ${ADMIN_TOKEN:0:20}..."
echo

# 3. Get current user info
echo "3. Getting current user info..."
curl -s $BASE_URL/me \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo

# 4. Access protected data
echo "4. Accessing protected data..."
curl -s $BASE_URL/data/protected \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo

# 5. Access admin endpoint
echo "5. Accessing admin endpoint..."
curl -s $BASE_URL/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq
echo

# 6. Login as analyst
echo "6. Logging in as analyst..."
ANALYST_TOKEN=$(curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst","password":"analyst123"}' | jq -r '.access_token')
echo

# 7. Try to access admin endpoint as analyst (should fail)
echo "7. Trying to access admin endpoint as analyst (should fail)..."
curl -s $BASE_URL/admin/users \
  -H "Authorization: Bearer $ANALYST_TOKEN" | jq
echo

# 8. Access analyst endpoint as analyst (should succeed)
echo "8. Accessing analyst endpoint as analyst..."
curl -s $BASE_URL/data/analyst \
  -H "Authorization: Bearer $ANALYST_TOKEN" | jq
echo

# 9. Try without token (should fail)
echo "9. Trying to access protected endpoint without token (should fail)..."
curl -s $BASE_URL/data/protected | jq
echo

echo "=== Tests Complete ==="
