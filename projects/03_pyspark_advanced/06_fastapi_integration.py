#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 6: FastAPI Integration for PySpark Jobs

This tutorial demonstrates how to integrate PySpark with FastAPI to create
REST API endpoints for PySpark jobs, enabling async job submission,
status tracking, and DataFrame operations as API endpoints.

Key Concepts:
- FastAPI REST API development
- Async PySpark job submission
- Job status tracking and monitoring
- DataFrame operations as API endpoints
- Integration with existing FastAPI projects

Optimized for 8GB RAM with efficient job queuing.
"""

import time
import uuid
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, count

# Initialize FastAPI app
app = FastAPI(
    title="PySpark Job API",
    description="REST API for submitting and monitoring PySpark jobs",
    version="1.0.0"
)

# Job tracking storage (in production, use Redis or database)
job_store: Dict[str, Dict] = {}

# Thread pool for running PySpark jobs
executor = ThreadPoolExecutor(max_workers=2)

# Pydantic models for request/response
class JobRequest(BaseModel):
    """Request model for submitting a PySpark job"""
    job_type: str = Field(..., description="Type of job: 'aggregation', 'filter', 'join', 'ml'")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Job parameters")
    dataset_path: Optional[str] = Field(None, description="Path to dataset (optional)")
    timeout_seconds: int = Field(300, description="Job timeout in seconds")

class JobResponse(BaseModel):
    """Response model for job submission"""
    job_id: str
    status: str
    submitted_at: datetime
    message: str

class JobStatus(BaseModel):
    """Job status response model"""
    job_id: str
    status: str
    submitted_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    progress: float
    result: Optional[Dict[str, Any]]
    error: Optional[str]

class DataFrameOperation(BaseModel):
    """Request model for DataFrame operations"""
    operation: str = Field(..., description="Operation: 'filter', 'select', 'groupby', 'agg'")
    columns: List[str] = Field(default_factory=list)
    filters: Optional[Dict[str, Any]] = None
    aggregation: Optional[Dict[str, List[str]]] = None

def create_spark_session_for_api():
    """Create a SparkSession optimized for API usage on 8GB RAM"""
    return SparkSession.builder \
        .appName("PySpark-API") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def generate_sample_data(spark):
    """Generate sample data for API demonstrations"""
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
    
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("salary", DoubleType(), True),
        StructField("years_experience", IntegerType(), True),
        StructField("location", StringType(), True)
    ])
    
    data = [
        (1, "Alice", "Engineering", 85000.0, 5, "New York"),
        (2, "Bob", "Marketing", 72000.0, 3, "San Francisco"),
        (3, "Charlie", "Engineering", 95000.0, 7, "New York"),
        (4, "Diana", "Sales", 68000.0, 2, "Chicago"),
        (5, "Eve", "Engineering", 110000.0, 10, "San Francisco"),
        (6, "Frank", "Marketing", 75000.0, 4, "Chicago"),
        (7, "Grace", "Sales", 82000.0, 6, "New York"),
        (8, "Henry", "Engineering", 90000.0, 8, "Chicago"),
        (9, "Ivy", "Marketing", 78000.0, 5, "San Francisco"),
        (10, "Jack", "Sales", 65000.0, 1, "New York")
    ]
    
    return spark.createDataFrame(data, schema)

def run_aggregation_job(job_id: str, parameters: Dict):
    """Run an aggregation PySpark job"""
    try:
        job_store[job_id]["status"] = "running"
        job_store[job_id]["started_at"] = datetime.now()
        job_store[job_id]["progress"] = 0.1
        
        # Initialize Spark
        spark = create_spark_session_for_api()
        job_store[job_id]["progress"] = 0.3
        
        # Generate or load data
        df = generate_sample_data(spark)
        job_store[job_id]["progress"] = 0.5
        
        # Perform aggregation based on parameters
        group_col = parameters.get("group_by", "department")
        agg_col = parameters.get("aggregate_column", "salary")
        
        result_df = df.groupBy(group_col).agg(
            spark_sum(agg_col).alias(f"total_{agg_col}"),
            avg(agg_col).alias(f"avg_{agg_col}"),
            count("*").alias("employee_count")
        )
        
        job_store[job_id]["progress"] = 0.8
        
        # Collect results
        results = []
        for row in result_df.collect():
            results.append(row.asDict())
        
        job_store[job_id]["result"] = {
            "aggregation_results": results,
            "row_count": df.count(),
            "columns": df.columns
        }
        
        job_store[job_id]["status"] = "completed"
        job_store[job_id]["progress"] = 1.0
        job_store[job_id]["completed_at"] = datetime.now()
        
        spark.stop()
        
    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)
        job_store[job_id]["completed_at"] = datetime.now()

def run_filter_job(job_id: str, parameters: Dict):
    """Run a filtering PySpark job"""
    try:
        job_store[job_id]["status"] = "running"
        job_store[job_id]["started_at"] = datetime.now()
        job_store[job_id]["progress"] = 0.1
        
        spark = create_spark_session_for_api()
        job_store[job_id]["progress"] = 0.3
        
        df = generate_sample_data(spark)
        job_store[job_id]["progress"] = 0.5
        
        # Apply filters
        filtered_df = df
        if "filters" in parameters:
            for column, value in parameters["filters"].items():
                if isinstance(value, list):
                    filtered_df = filtered_df.filter(col(column).isin(value))
                else:
                    filtered_df = filtered_df.filter(col(column) == value)
        
        job_store[job_id]["progress"] = 0.8
        
        # Collect results
        results = []
        for row in filtered_df.limit(100).collect():
            results.append(row.asDict())
        
        job_store[job_id]["result"] = {
            "filtered_results": results,
            "total_rows": filtered_df.count(),
            "original_rows": df.count()
        }
        
        job_store[job_id]["status"] = "completed"
        job_store[job_id]["progress"] = 1.0
        job_store[job_id]["completed_at"] = datetime.now()
        
        spark.stop()
        
    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)
        job_store[job_id]["completed_at"] = datetime.now()

def run_dataframe_operation(df, operation: DataFrameOperation):
    """Execute a DataFrame operation"""
    result_df = df
    
    if operation.operation == "filter" and operation.filters:
        for column, value in operation.filters.items():
            if isinstance(value, list):
                result_df = result_df.filter(col(column).isin(value))
            else:
                result_df = result_df.filter(col(column) == value)
    
    elif operation.operation == "select" and operation.columns:
        result_df = result_df.select(*operation.columns)
    
    elif operation.operation == "groupby" and operation.aggregation:
        agg_exprs = []
        for agg_func, cols in operation.aggregation.items():
            for col_name in cols:
                if agg_func == "sum":
                    agg_exprs.append(spark_sum(col_name).alias(f"{agg_func}_{col_name}"))
                elif agg_func == "avg":
                    agg_exprs.append(avg(col_name).alias(f"{agg_func}_{col_name}"))
                elif agg_func == "count":
                    agg_exprs.append(count(col_name).alias(f"{agg_func}_{col_name}"))
        
        if operation.columns:  # Group by columns
            result_df = result_df.groupBy(*operation.columns).agg(*agg_exprs)
    
    return result_df

# FastAPI endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PySpark Job API",
        "version": "1.0.0",
        "endpoints": {
            "submit_job": "POST /jobs/submit",
            "job_status": "GET /jobs/{job_id}",
            "list_jobs": "GET /jobs",
            "dataframe_operations": "POST /dataframe/operate"
        }
    }

@app.post("/jobs/submit", response_model=JobResponse)
async def submit_job(job_request: JobRequest, background_tasks: BackgroundTasks):
    """Submit a new PySpark job"""
    job_id = str(uuid.uuid4())
    
    # Store job metadata
    job_store[job_id] = {
        "job_id": job_id,
        "job_type": job_request.job_type,
        "parameters": job_request.parameters,
        "status": "submitted",
        "submitted_at": datetime.now(),
        "started_at": None,
        "completed_at": None,
        "progress": 0.0,
        "result": None,
        "error": None
    }
    
    # Schedule job execution based on type
    if job_request.job_type == "aggregation":
        background_tasks.add_task(run_aggregation_job, job_id, job_request.parameters)
    elif job_request.job_type == "filter":
        background_tasks.add_task(run_filter_job, job_id, job_request.parameters)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported job type: {job_request.job_type}")
    
    return JobResponse(
        job_id=job_id,
        status="submitted",
        submitted_at=job_store[job_id]["submitted_at"],
        message=f"Job {job_id} submitted successfully"
    )

@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get the status of a PySpark job"""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job = job_store[job_id]
    return JobStatus(**job)

@app.get("/jobs")
async def list_jobs(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, description="Maximum number of jobs to return")
):
    """List all PySpark jobs with optional filtering"""
    jobs = list(job_store.values())
    
    if status:
        jobs = [job for job in jobs if job["status"] == status]
    
    jobs.sort(key=lambda x: x["submitted_at"], reverse=True)
    
    return {
        "total_jobs": len(jobs),
        "jobs": jobs[:limit]
    }

@app.post("/dataframe/operate")
async def operate_dataframe(operation: DataFrameOperation):
    """Execute DataFrame operations directly"""
    try:
        spark = create_spark_session_for_api()
        df = generate_sample_data(spark)
        
        result_df = run_dataframe_operation(df, operation)
        
        # Collect sample results
        results = []
        for row in result_df.limit(50).collect():
            results.append(row.asDict())
        
        spark.stop()
        
        return {
            "operation": operation.operation,
            "result_count": result_df.count(),
            "sample_results": results,
            "schema": result_df.schema.json()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "active_jobs": sum(1 for job in job_store.values() if job["status"] in ["submitted", "running"]),
        "total_jobs": len(job_store)
    }

@app.get("/spark/info")
async def spark_info():
    """Get Spark configuration information"""
    try:
        spark = create_spark_session_for_api()
        conf = spark.sparkContext.getConf().getAll()
        spark.stop()
        
        return {
            "spark_config": dict(conf),
            "memory_config": {
                "driver_memory": "2g",
                "executor_memory": "1g",
                "total_cores": 2
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Main function to run the FastAPI server"""
    import uvicorn
    
    print("=" * 80)
    print("PYSPARK FASTAPI INTEGRATION SERVER")
    print("=" * 80)
    print("This server provides REST API endpoints for PySpark jobs.")
    print("Endpoints:")
    print("  - POST /jobs/submit    : Submit a new PySpark job")
    print("  - GET  /jobs/{job_id}  : Check job status")
    print("  - GET  /jobs           : List all jobs")
    print("  - POST /dataframe/operate: Execute DataFrame operations")
    print("  - GET  /health         : Health check")
    print("  - GET  /spark/info     : Spark configuration")
    print("\nStarting server on http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()