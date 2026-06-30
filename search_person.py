import cv2
import sqlite3
import json
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model
app = FaceAnalysis()
app.prepare(ctx_id=0)

# Input image
image_path = input("Enter image path: ")

img = cv2.imread(image_path)

if img is None:
    print("Image not found")
    exit()

# Detect face
faces = app.get(img)

if len(faces) == 0:
    print("No face detected")
    exit()

query_embedding = faces[0].embedding.reshape(1, -1)

# Connect database
conn = sqlite3.connect("missing_persons.db")
cursor = conn.cursor()

cursor.execute("SELECT name, embedding FROM persons")
records = cursor.fetchall()

best_name = None
best_score = -1

for name, embedding_json in records:
    embedding = np.array(json.loads(embedding_json)).reshape(1, -1)

    score = cosine_similarity(query_embedding, embedding)[0][0]

    if score > best_score:
        best_score = score
        best_name = name

conn.close()

print(f"\nBest Match: {best_name}")
print(f"Similarity Score: {best_score:.4f}")

if best_score > 0.6:
    print("MATCH FOUND")
else:
    print("NO MATCH")
    