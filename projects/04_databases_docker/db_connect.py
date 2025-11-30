import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Connection details from docker-compose.yml
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "de_db"

# Connection String
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def wait_for_db(engine):
    """Wait for the database to become available."""
    print("Waiting for database...")
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            break
        except OperationalError:
            print("Database not ready yet... retrying in 2s")
            time.sleep(2)

def main():
    print("=== Database Connection Tutorial ===")
    
    # 1. Create Engine
    engine = create_engine(DATABASE_URL)
    
    # 2. Wait for DB (since Docker might be starting up)
    wait_for_db(engine)
    
    # 3. Create a Table
    print("\nCreating table 'users'...")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                role VARCHAR(50)
            )
        """))
        conn.commit()
        print("Table created.")

    # 4. Insert Data
    print("\nInserting data...")
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (name, role) VALUES 
            ('Alice', 'Data Engineer'),
            ('Bob', 'Data Scientist'),
            ('Charlie', 'Manager')
        """))
        conn.commit()
        print("Data inserted.")

    # 5. Query Data
    print("\nQuerying data...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        for row in result:
            print(row)

if __name__ == "__main__":
    main()
