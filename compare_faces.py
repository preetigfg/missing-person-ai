import cv2
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model
app = FaceAnalysis()
app.prepare(ctx_id=0)

# Load first image
img1 = cv2.imread("person1.jpg")
faces1 = app.get(img1)

# Load second image
img2 = cv2.imread("person2.jpg")
faces2 = app.get(img2)

# Check if face detected
if len(faces1) == 0 or len(faces2) == 0:
    print("Face not detected in one of the images")

else:
    # Extract embeddings
    embedding1 = faces1[0].embedding.reshape(1, -1)
    embedding2 = faces2[0].embedding.reshape(1, -1)

    # Compare similarity
    similarity = cosine_similarity(embedding1, embedding2)[0][0]

    print(f"Similarity Score: {similarity}")

    # Decision
    if similarity > 0.6:
        print("MATCH FOUND")
    else:
        print("NO MATCH")