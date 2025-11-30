from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from .database import get_db, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Data Warehouse API",
    description="REST API for querying the Data Warehouse built in Week 8",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    database: str

class SalesSummary(BaseModel):
    total_sales: float
    total_transactions: int
    average_order_value: float

class RegionSales(BaseModel):
    region: str
    total_sales: float
    transaction_count: int

class ProductSales(BaseModel):
    product_name: str
    category: str
    total_sales: float
    units_sold: int

class TopCustomer(BaseModel):
    customer_name: str
    region: str
    total_spent: float
    order_count: int

# Routes
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Data Warehouse API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Check API and database health"""
    try:
        db.execute(text("SELECT 1"))
        return HealthResponse(status="healthy", database="connected")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")

@app.get("/api/sales/summary", response_model=SalesSummary, tags=["Sales"])
def get_sales_summary(db: Session = Depends(get_db)):
    """Get overall sales summary"""
    try:
        query = text("""
            SELECT 
                COALESCE(SUM(total_amount), 0) as total_sales,
                COUNT(*) as total_transactions,
                COALESCE(AVG(total_amount), 0) as average_order_value
            FROM fact_sales
        """)
        result = db.execute(query).fetchone()
        
        return SalesSummary(
            total_sales=float(result[0]),
            total_transactions=int(result[1]),
            average_order_value=float(result[2])
        )
    except Exception as e:
        logger.error(f"Error fetching sales summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sales/by-region", response_model=List[RegionSales], tags=["Sales"])
def get_sales_by_region(db: Session = Depends(get_db)):
    """Get sales breakdown by region"""
    try:
        query = text("""
            SELECT 
                dc.region,
                SUM(fs.total_amount) as total_sales,
                COUNT(*) as transaction_count
            FROM fact_sales fs
            JOIN dim_customer dc ON fs.customer_key = dc.customer_key
            GROUP BY dc.region
            ORDER BY total_sales DESC
        """)
        results = db.execute(query).fetchall()
        
        return [
            RegionSales(
                region=row[0],
                total_sales=float(row[1]),
                transaction_count=int(row[2])
            )
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching sales by region: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sales/by-product", response_model=List[ProductSales], tags=["Sales"])
def get_sales_by_product(db: Session = Depends(get_db)):
    """Get sales breakdown by product"""
    try:
        query = text("""
            SELECT 
                dp.name as product_name,
                dp.category,
                SUM(fs.total_amount) as total_sales,
                SUM(fs.quantity) as units_sold
            FROM fact_sales fs
            JOIN dim_product dp ON fs.product_key = dp.product_key
            GROUP BY dp.name, dp.category
            ORDER BY total_sales DESC
        """)
        results = db.execute(query).fetchall()
        
        return [
            ProductSales(
                product_name=row[0],
                category=row[1],
                total_sales=float(row[2]),
                units_sold=int(row[3])
            )
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching sales by product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/top", response_model=List[TopCustomer], tags=["Customers"])
def get_top_customers(limit: int = 10, db: Session = Depends(get_db)):
    """Get top customers by total spend"""
    try:
        query = text("""
            SELECT 
                dc.name as customer_name,
                dc.region,
                SUM(fs.total_amount) as total_spent,
                COUNT(*) as order_count
            FROM fact_sales fs
            JOIN dim_customer dc ON fs.customer_key = dc.customer_key
            GROUP BY dc.name, dc.region
            ORDER BY total_spent DESC
            LIMIT :limit
        """)
        results = db.execute(query, {"limit": limit}).fetchall()
        
        return [
            TopCustomer(
                customer_name=row[0],
                region=row[1],
                total_spent=float(row[2]),
                order_count=int(row[3])
            )
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching top customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/info", tags=["Metadata"])
def get_api_info(db: Session = Depends(get_db)):
    """Get API metadata and statistics"""
    try:
        # Get table counts
        fact_count = db.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()
        customer_count = db.execute(text("SELECT COUNT(*) FROM dim_customer")).scalar()
        product_count = db.execute(text("SELECT COUNT(*) FROM dim_product")).scalar()
        
        return {
            "version": "1.0.0",
            "warehouse_stats": {
                "total_sales_records": fact_count,
                "total_customers": customer_count,
                "total_products": product_count
            }
        }
    except Exception as e:
        logger.error(f"Error fetching API info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

