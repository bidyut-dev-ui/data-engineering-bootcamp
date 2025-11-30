from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Advanced FastAPI Patterns")

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Product name")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: Optional[str] = Field(None, max_length=200)
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    """Response model - can be different from request"""
    name: str
    price: float
    price_with_tax: float

@app.get("/")
def read_root():
    return {"message": "Advanced FastAPI Tutorial"}

@app.get("/items/")
def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
    search: Optional[str] = Query(None, min_length=3, description="Search term")
):
    """
    List items with pagination and optional search.
    
    - **skip**: Offset for pagination
    - **limit**: Maximum number of results
    - **search**: Filter by name (optional)
    """
    return {
        "skip": skip,
        "limit": limit,
        "search": search,
        "message": "In a real app, this would query a database"
    }

@app.post("/items/", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    """
    Create a new item with validation.
    
    Returns the item with calculated tax.
    """
    price_with_tax = item.price + (item.price * (item.tax or 0))
    return ItemResponse(
        name=item.name,
        price=item.price,
        price_with_tax=price_with_tax
    )

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}
