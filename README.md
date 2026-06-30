# AI-Based Missing Person Identification System

An AI-powered face recognition system designed to identify missing persons by comparing uploaded face images with registered images stored in the database.

The system uses **Computer Vision**, **Face Recognition**, and **Machine Learning** techniques to automate the identification process, reducing manual effort and improving search speed.

---

##  Features

* Register missing person images in database
* Detect faces from uploaded images
* Extract facial embeddings using AI model
* Compare uploaded face with stored records
* Return top matching results with similarity score
* Dashboard for system statistics
* Search history tracking

---

## Tech Stack

### Programming Language

* Python

### Frontend

* Streamlit

### Backend

* FastAPI

### Database

* SQLite

### AI / ML Libraries

* OpenCV
* InsightFace
* Scikit-learn

### Dataset

* LFW (Labeled Faces in the Wild)

---

## Project Workflow

Register Images
↓
Extract Face Embeddings
↓
Store Embeddings in Database
↓
Upload New Image
↓
Detect Face
↓
Generate Embedding
↓
Compare Using Cosine Similarity
↓
Return Best Matches

---

## Project Structure

```bash
Missing_Person_AI/
│
├── app.py
├── main.py
├── bulk_register_lfw.py
├── test_search.py
├── update_paths.py
│
├── database/
│   └── missing_persons.db
│
├── scripts/
│   └── face_search.py
│
├── uploads/
│
└── lfw_funneled/
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-link>
cd Missing_Person_AI
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
.\venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install fastapi streamlit opencv-python insightface scikit-learn numpy pandas uvicorn
```

---

## Run Project

### Step 1: Register Dataset

```bash
python bulk_register_lfw.py
```

This script loads dataset images, extracts face embeddings, and stores them in database.

---

### Step 2: Start Backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

### Step 3: Start Frontend

```bash
streamlit run app.py
```

---

## API Endpoints

### Home

```bash
/
```

Returns API status.

---

### Search Face

```bash
/search/
```

Uploads image and returns best matching results.

---

### Dashboard

```bash
/dashboard
```

Returns:

* total registered persons
* total searches

---

### Search History

```bash
/history
```

Returns previous search records.

---

## AI Model Details

### Model Used

* InsightFace `buffalo_l`

### Similarity Metric

* Cosine Similarity

### Threshold

* 0.55

### Top Matches Returned

* Top 3 Matches

---

## How It Works

1. Dataset images are registered in database
2. Face embeddings are extracted using InsightFace
3. User uploads a new image
4. System detects face from uploaded image
5. New embedding is generated
6. Embedding is compared with stored embeddings
7. Similarity scores are calculated
8. Best matches are returned

---

## Why This Project?

Manual missing person identification is time-consuming and difficult for large databases.

This system automates identification using AI-powered face recognition, making search:

* faster
* scalable
* more efficient

---

## Future Improvements

* Real-time CCTV integration
* Cloud deployment
* Mobile app support
* GPU acceleration
* Large-scale vector search using FAISS

---

## Output

* Face Matching
* Similarity Scores
* Search History
* Dashboard Analytics

---

## 👩‍💻 Author

**Preeti Saini**
M.Tech Artificial Intelligence
NIT Jalandhar
