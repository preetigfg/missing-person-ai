from fastapi import FastAPI, UploadFile, File
import os
import shutil
import sqlite3
from scripts.face_search import search_face

app = FastAPI()

UPLOAD_DIR = "uploads"
DB_PATH = "database/missing_persons.db"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Missing Person AI Backend Running"}


@app.post("/search/")
async def search_person(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = search_face(file_path)

    if result["status"] == "success":

        top_match = result["matches"][0]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO search_history
            (searched_name, result, score)
            VALUES (?, ?, ?)
            """,
            (
                top_match["name"],
                "match",
                top_match["score"]
            )
        )

        conn.commit()
        conn.close()

    return result


@app.get("/history")
def get_history():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               searched_name,
               result,
               score
        FROM search_history
        ORDER BY id DESC
        """
    )

    history = cursor.fetchall()

    conn.close()

    return {
        "history": history
    }


@app.get("/dashboard")
def dashboard():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM persons"
    )

    total_persons = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM search_history"
    )

    total_searches = cursor.fetchone()[0]

    conn.close()

    return {
        "total_registered": total_persons,
        "total_searches": total_searches
    }