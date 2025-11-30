from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database Setup
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
    conn.commit()
    conn.close()

init_db()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    item_id = c.lastrowid
    conn.close()
    return {"id": item_id, **item.dict()}

@app.get("/items/")
def read_items():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = [{"id": row[0], "name": row[1], "price": row[2]} for row in c.fetchall()]
    conn.close()
    return items
