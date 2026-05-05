"""
pydantic_v2_tutorial.py
Focus: Advanced Pydantic V2 patterns for Data Engineering.
"""

from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from typing import Optional

# 1. Pydantic Settings: Managing Pipeline Configuration
class PipelineConfig(BaseSettings):
    # Automatically reads from environment variables (e.g. DB_URL)
    db_url: str = Field("postgresql://localhost:5432/db", alias="DB_URL")
    batch_size: int = 100
    debug: bool = False
    
    model_config = SettingsConfigDict(env_prefix="DE_")

# 2. Advanced Validation: Data Cleaning at the source
class RawUserRecord(BaseModel):
    user_id: int
    raw_name: str = Field(..., min_length=1)
    email: str
    age: int
    
    # Field Validator: Cleaning specific fields
    @field_validator('raw_name')
    @classmethod
    def clean_name(cls, v: str) -> str:
        return v.strip().title()

    # Model Validator: Cross-field validation logic
    @model_validator(mode='after')
    def check_age_and_id(self) -> 'RawUserRecord':
        if self.age < 18 and self.user_id < 1000:
            raise ValueError("Test user IDs must be > 1000 for minors.")
        return self

    # Computed Field: Derived data for the pipeline
    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18

# --- Execution ---
if __name__ == "__main__":
    print("--- 1. Configuration Management ---")
    config = PipelineConfig()
    print(f"Connecting to: {config.db_url}")

    print("\n--- 2. Data Validation & Cleaning ---")
    try:
        user = RawUserRecord(
            user_id=500, 
            raw_name="  alice smith  ", 
            email="alice@example.com", 
            age=25
        )
        print(f"Cleaned Name: {user.raw_name}")
        print(f"Is Adult? {user.is_adult}")
        
        # This should fail validation
        invalid_user = RawUserRecord(user_id=1, raw_name="Bob", email="b@b.com", age=15)
    except ValueError as e:
        print(f"Validation Error Caught: {e}")

    # Key Takeaway for DE:
    # Use Pydantic to ensure your data is clean BEFORE it hits the database.
    # Use Pydantic Settings to manage your secrets and pipeline flags.
