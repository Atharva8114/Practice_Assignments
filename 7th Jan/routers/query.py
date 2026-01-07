from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from embeddings.ollama_embed import generate_embedding
from vector_db.qdrant_client import store_query_embedding

router = APIRouter()


class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    message: str


@router.post("/query", response_model=QueryResponse)
def store_query(request: QueryRequest):
    try:
        vector = generate_embedding(request.query)
        store_query_embedding(
            query=request.query,
            vector=vector,
            model="nomic-embed-text"
        )
        return {"message": "Query stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
