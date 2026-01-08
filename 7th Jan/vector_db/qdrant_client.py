import os
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from embeddings.ollama_embed import generate_embedding

QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = QdrantClient(url=QDRANT_URL)

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

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )

def store_document_chunks(doc_id, chunks, model):
    points = []

    for idx, chunk in enumerate(chunks):
        vector = generate_embedding(chunk)

        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "doc_id": doc_id,
                "chunk_index": idx,
                "content": chunk,
                "model": model,
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
