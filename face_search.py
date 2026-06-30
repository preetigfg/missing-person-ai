import sqlite3
import json
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis

DB_PATH = "database/missing_persons.db"

# Load InsightFace model
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=-1)   # CPU mode


def search_face(image_path, top_k=3):

    img = cv2.imread(image_path)

    if img is None:
        return {
            "status": "error",
            "message": "Image not found"
        }

    faces = face_app.get(img)

    if len(faces) == 0:
        return {
            "status": "error",
            "message": "No face detected"
        }

    query_embedding = faces[0].embedding.reshape(1, -1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, image_path, embedding
        FROM persons
    """)

    persons = cursor.fetchall()

    conn.close()

    matches = []

    for person in persons:

        person_id, name, registered_image_path, embedding_json = person

        embedding = np.array(
            json.loads(embedding_json)
        ).reshape(1, -1)

        score = cosine_similarity(
            query_embedding,
            embedding
        )[0][0]

        matches.append({
            "id": person_id,
            "name": name,
            "image_path": registered_image_path,
            "score": float(score)
        })

    # Sort by similarity score
    matches = sorted(
        matches,
        key=lambda x: x["score"],
        reverse=True
    )

    # Remove duplicate names
    unique_matches = []
    seen_names = set()

    for match in matches:

        if match["name"] not in seen_names:

            unique_matches.append(match)
            seen_names.add(match["name"])

        if len(unique_matches) == top_k:
            break

    top_matches = unique_matches

    # No matches found
    if len(top_matches) == 0:
        return {
            "status": "no_match",
            "matches": [],
            "score": 0
        }

    # Optional threshold
    MATCH_THRESHOLD = 0.55

    top_match = top_matches[0]

    if top_match["score"] < MATCH_THRESHOLD:

        return {
            "status": "no_match",
            "matches": [],
            "score": 0
        }

    return {
        "status": "match",
        "matches": top_matches
    }