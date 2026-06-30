import cv2
from insightface.app import FaceAnalysis

# Load face analysis model
app = FaceAnalysis()
app.prepare(ctx_id=0)

# Read image
img = cv2.imread("test.jpg")

# Detect faces
faces = app.get(img)

print(f"Number of faces detected: {len(faces)}")

# Print embedding size
if len(faces) > 0:
    embedding = faces[0].embedding
    print("Embedding vector size:", len(embedding))