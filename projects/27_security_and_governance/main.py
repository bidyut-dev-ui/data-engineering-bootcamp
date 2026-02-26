import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# In a real app, you would load this module
from importlib import import_module
pii_middleware = import_module("01_pii_middleware")
PIIMaskingMiddleware = pii_middleware.PIIMaskingMiddleware

class Settings(BaseSettings):
    """
    Pydantic Settings classes automatically read from Environment Variables.
    This is a critical security practice: Never hardcode secrets!
    """
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ENVIRONMENT: str = "dev"
    
    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(title="Data Company Secure API")

# Add our custom security middleware to intercept all requests
app.add_middleware(PIIMaskingMiddleware)

@app.get("/health")
def health_check():
    # Demonstrating env variable usage
    return {"status": "ok", "env": settings.ENVIRONMENT}

@app.get("/user/lookup")
def lookup_user(ssn: str = None, email: str = None):
    # This route simulates receiving sensitive data.
    # Because of PIIMaskingMiddleware, if the 'ssn' or 'email' parameter 
    # appears in the URL, our logs will redact it!
    return {"message": "User query executed securely."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
