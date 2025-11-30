import sqlite3
import os

DB_NAME = "reliability.db"

def setup_database():
    """Create a fresh database with a users table"""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table with constraints
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database {DB_NAME} created.")

if __name__ == "__main__":
    setup_database()
