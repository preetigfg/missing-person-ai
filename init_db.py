import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/missing_persons.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    image_path TEXT,
    embedding TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    searched_name TEXT,
    result TEXT,
    score REAL
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")