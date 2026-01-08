from dotenv import load_dotenv
load_dotenv()

import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = QdrantClient(url=QDRANT_URL)

# Delete the old collection
try:
    client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Deleted collection: {COLLECTION_NAME}")
except:
    print(f"Collection {COLLECTION_NAME} doesn't exist")

# Create a fresh collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    )
)

print(f"Created fresh collection: {COLLECTION_NAME}")