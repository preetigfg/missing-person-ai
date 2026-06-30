import cv2
import sqlite3
import json
from insightface.app import FaceAnalysis

# Load AI model
app = FaceAnalysis()
app.prepare(ctx_id=0)

# Person details
name = input("Enter person name: ")
image_path = input("Enter image path: ")

# Read image
img = cv2.imread(image_path)

if img is None:
    print("Image not found")
    exit()

# Detect face
faces = app.get(img)

if len(faces) == 0:
    print("No face detected")
    exit()

# Get embedding
embedding = faces[0].embedding.tolist()

# Save to database
conn = sqlite3.connect("missing_persons.db")
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO persons (name, image_path, embedding)
    VALUES (?, ?, ?)
    """,
    (
        name,
        image_path,
        json.dumps(embedding)
    )
)

conn.commit()
conn.close()

print(f"{name} registered successfully")