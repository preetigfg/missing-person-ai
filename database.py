import sqlite3

conn = sqlite3.connect("missing_persons.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    embedding TEXT NOT NULL
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

print("Database created successfully")