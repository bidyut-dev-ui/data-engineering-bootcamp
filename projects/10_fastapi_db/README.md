# Week 14: Connecting FastAPI to Databases

**Goal**: Learn how to persist data by integrating FastAPI with databases, handle CRUD operations, and manage database connections properly.

## Scenario
Your API now needs to store data permanently. You'll learn to connect FastAPI to SQLite (for development) and understand patterns that apply to any SQL database (Postgres, MySQL, etc.).

## Concepts Covered
1. **Database Connections**: Creating and managing connections
2. **CRUD Operations**: Create, Read, Update, Delete
3. **SQL Injection Prevention**: Using parameterized queries
4. **Connection Pooling**: Efficient resource management
5. **Error Handling**: Database exceptions and HTTP status codes
6. **SQLite vs Postgres**: When to use each

## Structure
- `main.py`: Basic SQLite integration
- `02_sqlalchemy.py`: Using SQLAlchemy ORM (recommended for production)
- `database.py`: Database configuration and models
- `test.db`: SQLite database file (created automatically)

## Instructions

### 1. Setup
Activate your environment:
```bash
cd projects/10_fastapi_db
source ../00_setup_and_refresher/venv/bin/activate
pip install fastapi uvicorn sqlalchemy
```

### 2. Run Tutorial 1: Raw SQLite
Start the server:
```bash
uvicorn main:app --reload
```

**What Happens**:
- `test.db` file is created automatically
- `items` table is initialized
- API is ready at `http://localhost:8000`

### 3. Test CRUD Operations

#### Create an Item
Using Swagger UI (`http://localhost:8000/docs`):
1. Click `POST /items/`
2. Try it out with:
   ```json
   {
     "name": "Laptop",
     "price": 1299.99
   }
   ```

**Expected Output**:
```json
{
  "id": 1,
  "name": "Laptop",
  "price": 1299.99
}
```

#### Read All Items
```bash
curl http://localhost:8000/items/
```

**Expected Output**: Array of all items in the database.

#### Verify Database
You can inspect the SQLite database:
```bash
sqlite3 test.db "SELECT * FROM items;"
```

### 4. Run Tutorial 2: SQLAlchemy ORM
Stop the previous server (Ctrl+C) and run:
```bash
uvicorn 02_sqlalchemy:app --reload --port 8001
```

**What's Different**:
- Uses SQLAlchemy ORM instead of raw SQL
- Better type safety and validation
- Easier to switch databases (SQLite → Postgres)

Visit `http://localhost:8001/docs` and test the same operations.

### 5. Compare Approaches

**Raw SQL (`main.py`)**:
- ✅ Simple and direct
- ✅ Good for learning
- ❌ Prone to SQL injection if not careful
- ❌ Manual type conversion

**SQLAlchemy ORM (`02_sqlalchemy.py`)**:
- ✅ Type-safe
- ✅ Database-agnostic
- ✅ Automatic migrations (with Alembic)
- ✅ Relationship management
- ❌ Slight learning curve

## Homework / Challenge

### Challenge 1: Add Update and Delete
Modify `main.py`:
1. Add `PUT /items/{item_id}` to update an item
2. Add `DELETE /items/{item_id}` to delete an item
3. Return `404` if item not found

### Challenge 2: Add Relationships
Create `03_challenge.py`:
1. Create two tables: `categories` and `items`
2. Each item belongs to a category (foreign key)
3. Endpoints:
   - `POST /categories/` - Create category
   - `GET /categories/{id}/items` - Get all items in a category
   - `POST /items/` - Create item with category_id

### Challenge 3: Connect to Warehouse
Modify `02_sqlalchemy.py`:
1. Instead of SQLite, connect to the Postgres warehouse from Week 8
2. Query the `fact_sales` table
3. Create an endpoint `GET /sales/summary` that returns total sales by region

**Connection String**:
```python
DATABASE_URL = "postgresql://user:password@localhost:5434/warehouse_db"
```

## Expected Learning Outcomes
After completing this week, you should be able to:
- ✅ Connect FastAPI to a database
- ✅ Perform CRUD operations safely
- ✅ Choose between raw SQL and ORM
- ✅ Handle database errors gracefully
- ✅ Understand connection management

## Troubleshooting

**Issue**: `sqlite3.OperationalError: no such table`
- **Solution**: Delete `test.db` and restart the server. The `init_db()` function will recreate it.

**Issue**: Database locked
- **Solution**: Only one process can write to SQLite at a time. Close other connections or use Postgres for concurrent access.
