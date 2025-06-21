from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
from typing import List
import os
from utils.video_processing import extract_frames
from utils.feature_extraction import compute_histogram, compute_all_histograms
from utils.qdrant_client import client, COLLECTION, upload_vectors_to_qdrant

app = FastAPI()

class QueryImage(BaseModel):
    image_path: str

class QueryVector(BaseModel):
    vector: List[float] = Field(..., example=[0.0] * 512)

@app.get("/")
async def root():
    return {"message": "Welcome to the Video Feature Extraction and Retrieval API"}

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """Uploads a video, extracts frames, computes vectors, and indexes them in one go."""
    os.makedirs("temp", exist_ok=True)
    video_path = f"temp/{file.filename}"
    
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # 1. Extract frames
    frames_dir = "frames"
    extracted_count = extract_frames(video_path, output_dir=frames_dir, interval=1)
    if extracted_count == 0:
        return {"message": "No frames were extracted from the video."}

    # 2. Compute vectors and 3. Upload to Qdrant
    vectors = compute_all_histograms(frames_dir)
    upload_vectors_to_qdrant(vectors)

    # 4. Clean up temporary files
    try:
        os.remove(video_path)
        for frame_file in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, frame_file))
    except OSError as e:
        print(f"Error during cleanup: {e}")

    return {"message": f"{extracted_count} frames extracted and indexed successfully."}

@app.post("/index-frames/")
async def index_frames():
    """Manually index any frames that might exist on the filesystem."""
    vectors = compute_all_histograms("frames")
    if not vectors:
        return {"message": "No frames found to index."}
    upload_vectors_to_qdrant(vectors)
    return {"message": "Frames indexed successfully"}

@app.post("/get-vector/")
async def get_vector(item: QueryImage):
    """Computes and returns the feature vector for a given image."""
    vector = compute_histogram(item.image_path)
    return {"filename": item.image_path, "vector": vector.tolist()}

@app.post("/query-similar/")
async def query_similar(item: QueryVector):
    """Queries for similar frames using a provided feature vector."""
    hits = client.search(
        collection_name=COLLECTION,
        query_vector=item.vector,
        limit=10
    )
    results = [{"filename": h.payload["filename"], "score": h.score} for h in hits]
    return {"results": results}
