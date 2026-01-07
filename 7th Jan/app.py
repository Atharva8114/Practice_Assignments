from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import query  # import router

app = FastAPI(
    title="Ollama Vector API",
    description="Stores Ollama query embeddings in Qdrant",
    version="1.0.0"
)

# Include the router
app.include_router(query.router)
