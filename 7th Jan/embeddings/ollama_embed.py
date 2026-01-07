import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("EMBED_MODEL")

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": MODEL_NAME,
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]
