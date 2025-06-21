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
    video_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(video_path, "wb") as f:
        f.write(await file.read())

    extracted_count = extract_frames(video_path, output_dir="frames", interval=1)
    return {"message": "Frames extracted", "frames_count": extracted_count}

@app.post("/index-frames/")
async def index_frames():
    vectors = compute_all_histograms("frames")
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
