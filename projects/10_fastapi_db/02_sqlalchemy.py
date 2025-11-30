from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sqlalchemy.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class ItemCreate(BaseModel):
    name: str
    price: float

class Item(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True  # Allows ORM model conversion

# FastAPI app
app = FastAPI(title="FastAPI with SQLAlchemy")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: ItemCreate, db: Session = None):
    """Create a new item using SQLAlchemy ORM"""
    if db is None:
        db = next(get_db())
    
    db_item = ItemDB(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = None):
    """Get all items with pagination"""
    if db is None:
        db = next(get_db())
    
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = None):
    """Get a specific item by ID"""
    if db is None:
        db = next(get_db())
    
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = None):
    """Delete an item"""
    if db is None:
        db = next(get_db())
    
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

@app.get("/")
def root():
    return {"message": "FastAPI with SQLAlchemy ORM", "docs": "/docs"}
