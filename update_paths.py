import sqlite3

OLD_PATH = r"D:\dwonload\project\lfw_funneled"

NEW_PATH = r"D:\dwonload\project\lfw_missing_person_dataset"

conn = sqlite3.connect("database/missing_persons.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE persons
SET image_path = REPLACE(
    image_path,
    ?,
    ?
)
""", (OLD_PATH, NEW_PATH))

conn.commit()

print("Rows updated:", conn.total_changes)

conn.close()

print("Image paths updated successfully!")