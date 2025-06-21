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
    if not vectors:
        return {"message": "Could not compute feature vectors for the extracted frames."}
    upload_vectors_to_qdrant(vectors)

    # 4. Clean up temporary files
    try:
        os.remove(video_path)
        for frame_file in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, frame_file))
    except OSError as e:
        print(f"Error during cleanup: {e}")

    # 5. Return a sample vector for the user to test with
    sample_vector_data = {
        "filename": vectors[0][0],
        "vector": vectors[0][1].tolist()
    }

    return {
        "message": f"{extracted_count} frames extracted and indexed successfully.",
        "sample_query": sample_vector_data
    }

@app.post("/get-vector/")
async def get_vector(file: UploadFile = File(...)):
    """
    Accepts an image file upload and returns its computed feature vector.
    This is the recommended way to get a vector for querying.
    """
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    vector = compute_histogram(temp_path)

    try:
        os.remove(temp_path)
    except OSError as e:
        print(f"Error during cleanup: {e}")

    return {"filename": file.filename, "vector": vector.tolist()}

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
