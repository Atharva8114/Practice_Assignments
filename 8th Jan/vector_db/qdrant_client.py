import os
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from embeddings.ollama_embed import generate_embedding



QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = QdrantClient(url=QDRANT_URL)

VECTOR_SIZE = 768  # nomic-embed-text embeddings size

# Create collection if it doesn't exist
try:
    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
except:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )


# ---------------------------
# Store a single query embedding
# ---------------------------
def store_query_embedding(query: str, vector: list[float], model: str):
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "query": query,
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])


# ---------------------------
# Store document chunks as points
# ---------------------------
def store_document_chunks(doc_id: str, chunks: list[str], model: str):
    points = []
    for idx, chunk in enumerate(chunks):
        vector = generate_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "doc_id": doc_id,
                "chunk_index": idx,
                "content": chunk,
                "model": model,
                "timestamp": datetime.utcnow().isoformat()
            }
        ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)


# ---------------------------
# Search for top-k similar chunks using HTTP API directly
# ---------------------------
def search_similar_chunks(query_vector: list[float], top_k: int = 5):
    """
    Returns top-k most similar document chunks from Qdrant
    """
    import requests
    
    # Use Qdrant REST API directly
    search_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
    
    payload = {
        "vector": query_vector,
        "limit": top_k,
        "with_payload": True,
        "filter": {
            "must": [
                {
                    "key": "doc_id",
                    "match": {
                        "except": [""]
                    }
                }
            ]
        }
    }
    
    response = requests.post(search_url, json=payload)
    response.raise_for_status()
    
    search_results = response.json()
    
    results = []
    for hit in search_results.get("result", []):
        results.append({
            "score": hit.get("score", 0),
            "content": hit.get("payload", {}).get("content", ""),
            "doc_id": hit.get("payload", {}).get("doc_id", ""),
            "chunk_index": hit.get("payload", {}).get("chunk_index", 0)
        })
    return results