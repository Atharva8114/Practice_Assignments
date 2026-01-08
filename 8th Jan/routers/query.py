from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from embeddings.ollama_embed import generate_embedding
from vector_db.qdrant_client import search_similar_chunks

router = APIRouter()


# Request model
class QueryRequest(BaseModel):
    query: str


# Response model
class QueryResponse(BaseModel):
    query: str
    results: list[dict]


# Endpoint to search top-5 relevant document chunks
@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    try:
        # Generate embedding for the query
        query_vector = generate_embedding(request.query)

        # Search in Qdrant for top 5 similar chunks
        results = search_similar_chunks(query_vector=query_vector, top_k=5)

        return {
            "query": request.query,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
