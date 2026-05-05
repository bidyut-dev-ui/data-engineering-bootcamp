# Phase 5: Live Coding Interview Practice (Python/Web/Data)

## 1. FastAPI Live Coding
**Problem:** Build a "Metadata API" in 30 minutes. 
- Requirement 1: An endpoint `/table/{table_name}` that returns the owner and row count from a mock dictionary.
- Requirement 2: Use Pydantic for the response schema.
- Requirement 3: Add a middleware that logs the time taken for each request.

**Solution:**
```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
import time

app = FastAPI()

TABLES = {
    "users": {"owner": "Growth", "rows": 1000000},
    "orders": {"owner": "Finance", "rows": 500000}
}

class TableMeta(BaseModel):
    owner: str
    rows: int

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(f"Time: {time.time() - start_time}")
    return response

@app.get("/table/{table_name}", response_model=TableMeta)
def get_table_meta(table_name: str):
    return TABLES.get(table_name, {"owner": "unknown", "rows": 0})
```

## 2. Django ORM Live Coding
**Problem:** You have a `Sensor` model and a `Reading` model. Write a query to find the average reading for a specific sensor in the last 24 hours.

**Solution:**
```python
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Models
class Sensor(models.Model):
    name = models.CharField(max_length=100)

class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_child=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

# The Solution Query
def get_avg_reading(sensor_id):
    yesterday = timezone.now() - timedelta(hours=24)
    return Reading.objects.filter(
        sensor_id=sensor_id, 
        timestamp__gte=yesterday
    ).aggregate(models.Avg('value'))
```

## 3. Data Cleaning (Python/Pandas)
**Problem:** You have a messy CSV where the `price` column has strings like `$1,200.50`. Clean it and convert to float.

**Solution:**
```python
import pandas as pd

def clean_price(price_str):
    if pd.isna(price_str):
        return 0.0
    # Solution: Remove currency symbols and commas using regex
    return float(str(price_str).replace('$', '').replace(',', ''))

df = pd.DataFrame({'price': ['$1,200.50', '$500', None]})
df['price_clean'] = df['price'].apply(clean_price)
```
