from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import numpy as np
from config import QDRANT_HOST, QDRANT_API_KEY

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

COLLECTION = "video_frames"

def setup_qdrant(dim):
    if COLLECTION not in client.get_collections().collections:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def upload_vectors_to_qdrant(vectors):
    setup_qdrant(len(vectors[0][1]))
    points = []
    for i, (img_name, vector) in enumerate(vectors):
        points.append(PointStruct(id=i, vector=vector.tolist(), payload={"filename": img_name}))
    client.upsert(collection_name=COLLECTION, points=points)
