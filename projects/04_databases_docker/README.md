# Week 5: Databases & Docker

**Goal**: Learn how to spin up a database using Docker and interact with it using Python (SQLAlchemy).

## Concepts Covered
1. **Docker Compose**: Defining services (Postgres) in a YAML file.
2. **SQLAlchemy**: The standard Python SQL toolkit.
3. **Database Interaction**: Connecting, Creating Tables, Inserting, and Querying.

## Instructions

### 1. Setup
Activate your environment:
```bash
cd ../04_databases_docker
source ../00_setup_and_refresher/venv/bin/activate
```

### 2. Start the Database
We use Docker Compose to start a Postgres container.
```bash
docker compose up -d
```
*Note: The first time you run this, it will download the Postgres image (approx 100MB).*

Check if it's running:
```bash
docker ps
```

### 3. Run the Tutorial
Run the Python script to connect to the database:
```bash
python db_connect.py
```
This script will:
1. Wait for the DB to be ready.
2. Create a `users` table.
3. Insert some dummy data.
4. Print the data to the console.

### 4. Cleanup
When you are done, stop the container to save resources:
```bash
docker compose down
```

## Homework / Challenge
Create `02_challenge.py`:
1. Create a new table called `sales` with columns: `id`, `product`, `amount`, `date`.
2. Insert 5 rows of sales data.
3. Write a query to calculate the **Total Sales Amount**.
