import os
import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

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
