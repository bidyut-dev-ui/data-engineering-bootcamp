# Week 27: Security & Authentication

**Goal**: Learn to secure APIs with JWT authentication, implement role-based access control (RBAC), and manage secrets properly.

## Scenario
Your data platform is going to production. You need to secure all API endpoints, implement different access levels for different teams, and ensure sensitive data is protected.

## Concepts Covered
1. **JWT (JSON Web Tokens)**: Stateless authentication
2. **RBAC (Role-Based Access Control)**: Permission management
3. **Password Hashing**: Secure credential storage (bcrypt)
4. **API Keys**: Alternative authentication method
5. **Secrets Management**: Environment variables, .env files
6. **OAuth2 Flow**: Industry-standard authentication
7. **Security Best Practices**: HTTPS, CORS, rate limiting

## Structure
- `app/main.py`: FastAPI with JWT authentication
- `app/auth.py`: Authentication utilities (optional enhancement)
- `requirements.txt`: Dependencies (PyJWT)
- `test_api.sh`: Automated testing script
- `.env.example`: Environment variables template

## Instructions

### 1. Setup
```bash
cd projects/19_secure_api
source ../../venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the API
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs`

### 3. Test Authentication Flow

#### Manual Testing (Swagger UI)

**Step 1: Try public endpoint**
- GET `/data/public` - Should work without auth

**Step 2: Try protected endpoint without auth**
- GET `/data/protected` - Should return 401 Unauthorized

**Step 3: Login**
- POST `/login`
- Body: `{"username": "admin", "password": "admin123"}`
- Copy the `access_token` from response

**Step 4: Use the token**
- Click "Authorize" button in Swagger UI
- Enter: `Bearer <your-token>`
- Now try `/data/protected` - Should work!

#### Automated Testing
```bash
./test_api.sh
```

**Expected Output**:
- Public endpoint works
- Admin can access all endpoints
- Analyst can access analyst endpoints but not admin endpoints
- Requests without tokens are rejected

### 4. Understanding JWT

**Token Structure**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTYzMjQ4MDAwMH0.signature
```

Three parts (separated by `.`):
1. **Header**: Algorithm and token type
2. **Payload**: User data (username, role, expiration)
3. **Signature**: Verification hash

**Decode your token**: Visit https://jwt.io and paste your token

### 5. Test Different Roles

**Users available**:
- `admin` / `admin123` - Full access
- `analyst` / `analyst123` - Analyst access
- `viewer` / `viewer123` - Read-only access

**Try**:
1. Login as `analyst`
2. Try to access `/admin/users` - Should fail (403 Forbidden)
3. Access `/data/analyst` - Should succeed

## Security Concepts Explained

### **JWT vs Session-Based Auth**

**Session-Based** (Traditional):
- Server stores session data
- Client gets session ID cookie
- Server looks up session on each request
- ❌ Doesn't scale well (need shared session store)

**JWT** (Modern):
- Server doesn't store anything
- Client stores token
- Token contains all needed info
- ✅ Scales horizontally
- ✅ Works across microservices

### **Role-Based Access Control (RBAC)**

```python
# Three levels of access:
viewer  → Can only read public data
analyst → Can read analytics data
admin   → Can do everything
```

### **Token Expiration**

Tokens expire after 30 minutes (configurable). Why?
- Limits damage if token is stolen
- Forces re-authentication
- Can revoke access by not issuing new tokens

## Homework / Challenge

### Challenge 1: Add Password Hashing
Currently passwords are stored in plain text. Fix this:
```bash
pip install passlib bcrypt
```

Create `app/auth.py`:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

Update `main.py` to use hashed passwords.

### Challenge 2: Add API Key Authentication
Some clients prefer API keys over JWT. Implement:
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in valid_api_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

### Challenge 3: Add Refresh Tokens
Implement refresh token flow:
1. Login returns both `access_token` (short-lived) and `refresh_token` (long-lived)
2. When access token expires, use refresh token to get new access token
3. Refresh tokens can be revoked

### Challenge 4: Add Rate Limiting
Prevent brute-force attacks:
```bash
pip install slowapi
```

Limit login attempts to 5 per minute per IP.

## Production Considerations

### **1. Secrets Management**
Never hardcode `SECRET_KEY`!

**Development**:
```bash
# .env file
SECRET_KEY=your-secret-key-here
```

**Production**:
- Use environment variables
- Or: AWS Secrets Manager, HashiCorp Vault
- Rotate keys regularly

### **2. HTTPS Only**
JWT tokens should NEVER be sent over HTTP.
```python
# In production
app.add_middleware(
    HTTPSRedirectMiddleware
)
```

### **3. Token Storage (Client-Side)**
- ✅ Store in memory (most secure, lost on refresh)
- ✅ HttpOnly cookies (good for web apps)
- ❌ localStorage (vulnerable to XSS)

### **4. CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*" in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Expected Learning Outcomes
- ✅ Implement JWT authentication in FastAPI
- ✅ Understand RBAC and permission models
- ✅ Secure API endpoints properly
- ✅ Manage secrets safely
- ✅ Know production security best practices
- ✅ Explain authentication vs authorization

## Interview Questions

**Q: What's the difference between authentication and authorization?**
A: Authentication verifies WHO you are (login). Authorization verifies WHAT you can do (permissions).

**Q: Why use JWT instead of sessions?**
A: JWT is stateless, scales better, works across microservices, no server-side storage needed.

**Q: How do you handle token expiration?**
A: Short-lived access tokens (30 min) + long-lived refresh tokens. Client refreshes automatically.

**Q: Where should you store JWT on the client?**
A: Best: HttpOnly cookies or memory. Avoid localStorage (XSS risk).
