from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(
    title="CI/CD Demo API",
    version=os.getenv("APP_VERSION", "1.0.0")
)

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

@app.get("/")
def read_root():
    return {"message": "CI/CD Demo API"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.get("/data")
def get_data():
    return {
        "data": [1, 2, 3, 4, 5],
        "count": 5
    }
