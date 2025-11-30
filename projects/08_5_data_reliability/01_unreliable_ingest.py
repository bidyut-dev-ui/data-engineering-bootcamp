import sqlite3
import time

DB_NAME = "reliability.db"

def unreliable_ingest(users):
    """
    Ingests users but fails halfway.
    Does NOT use transactions properly.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("🚀 Starting unreliable ingest...")
    
    for i, user in enumerate(users):
        print(f"   Inserting {user['email']}...")
        
        # INSERT immediately (Auto-commit behavior in some drivers, 
        # though sqlite3 defaults to transactions, we simulate bad behavior by committing every row)
        cursor.execute("INSERT INTO users (id, email, name, balance) VALUES (?, ?, ?, ?)",
                       (user['id'], user['email'], user['name'], user['balance']))
        conn.commit() # <--- BAD PRACTICE: Committing every row
        
        # Simulate crash after 2nd record
        if i == 1:
            print("💥 CRASH! Process died unexpectedly.")
            conn.close()
            raise Exception("System Crash")
            
    conn.close()

if __name__ == "__main__":
    # Data to insert
    new_users = [
        {'id': 1, 'email': 'alice@example.com', 'name': 'Alice', 'balance': 100.0},
        {'id': 2, 'email': 'bob@example.com', 'name': 'Bob', 'balance': 200.0},
        {'id': 3, 'email': 'charlie@example.com', 'name': 'Charlie', 'balance': 300.0}
    ]
    
    try:
        unreliable_ingest(new_users)
    except Exception as e:
        print(f"   (Error caught: {e})")
        
    # Verify state
    conn = sqlite3.connect(DB_NAME)
    count = conn.cursor().execute("SELECT COUNT(*) FROM users").fetchone()[0]
    print(f"\n📊 Result: {count} users in database.")
    print("❌ PROBLEM: We have partial data! Alice and Bob are in, Charlie is missing.")
    print("   If we re-run this, Alice and Bob will cause 'UNIQUE constraint failed' errors.")
    conn.close()
