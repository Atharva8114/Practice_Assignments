from dotenv import load_dotenv
load_dotenv()

from embeddings.ollama_embed import generate_embedding
from vector_db.qdrant_client import store_query_embedding

query = "What is Ollama?"

vector = generate_embedding(query)
store_query_embedding(
    query=query,
    vector=vector,
    model="nomic-embed-text"
)

print("Query stored successfully")

