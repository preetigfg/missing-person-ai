import os
import json
import sqlite3
import cv2
from tqdm import tqdm
from collections import defaultdict
from insightface.app import FaceAnalysis

LFW_PATH = r"D:\dwonload\project\lfw_funneled"

DB_PATH = "database/missing_persons.db"

face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=-1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

person_images = defaultdict(list)

print("Scanning dataset...")

for person_name in os.listdir(LFW_PATH):

    person_folder = os.path.join(LFW_PATH, person_name)

    if not os.path.isdir(person_folder):
        continue

    images = [
        os.path.join(person_folder, img)
        for img in os.listdir(person_folder)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(images) >= 1:
        person_images[person_name] = images

print(f"Eligible identities: {len(person_images)}")

registered = 0
failed = 0

for person_name, images in tqdm(person_images.items()):

    image_path = images[0]

    img = cv2.imread(image_path)

    if img is None:
        failed += 1
        continue

    faces = face_app.get(img)

    if len(faces) == 0:
        failed += 1
        continue

    embedding = faces[0].embedding.tolist()

    cursor.execute(
        """
        INSERT INTO persons
        (name, image_path, embedding)
        VALUES (?, ?, ?)
        """,
        (
            person_name,
            image_path,
            json.dumps(embedding)
        )
    )

    registered += 1

conn.commit()
conn.close()

print("\nBulk registration completed.")

print("Registered:", registered)
print("Failed:", failed)