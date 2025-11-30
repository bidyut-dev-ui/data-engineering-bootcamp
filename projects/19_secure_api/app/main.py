from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Secure API with JWT")
security = HTTPBearer()

# User database (in production, use real database)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # In production: hash with bcrypt
        "role": "admin"
    },
    "analyst": {
        "username": "analyst",
        "password": "analyst123",
        "role": "analyst"
    },
    "viewer": {
        "username": "viewer",
        "password": "viewer123",
        "role": "viewer"
    }
}

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role: str

# JWT Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Dependencies
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    
    username = payload.get("sub")
    role = payload.get("role")
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return User(username=username, role=role)

def require_role(required_role: str):
    """Dependency to check user role"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}"
            )
        return current_user
    return role_checker

# Routes
@app.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    """Login endpoint - returns JWT token"""
    user = fake_users_db.get(login_data.username)
    
    if not user or user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Secure API with JWT Authentication"}

@app.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@app.get("/data/public")
def get_public_data():
    """Public endpoint - no authentication required"""
    return {"data": "This is public data", "access": "public"}

@app.get("/data/protected")
def get_protected_data(current_user: User = Depends(get_current_user)):
    """Protected endpoint - requires authentication"""
    return {
        "data": "This is protected data",
        "access": "authenticated",
        "user": current_user.username
    }

@app.get("/data/analyst")
def get_analyst_data(current_user: User = Depends(require_role("analyst"))):
    """Analyst-only endpoint"""
    return {
        "data": "Sensitive analytics data",
        "access": "analyst",
        "user": current_user.username
    }

@app.get("/admin/users")
def get_all_users(current_user: User = Depends(require_role("admin"))):
    """Admin-only endpoint"""
    return {
        "users": list(fake_users_db.keys()),
        "access": "admin",
        "admin": current_user.username
    }

@app.post("/admin/users")
def create_user(
    username: str,
    password: str,
    role: str,
    current_user: User = Depends(require_role("admin"))
):
    """Admin-only: Create new user"""
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    fake_users_db[username] = {
        "username": username,
        "password": password,  # In production: hash this!
        "role": role
    }
    
    return {"message": f"User {username} created successfully"}
