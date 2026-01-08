# test_pipeline.py
import os
import pytest
from embeddings.ollama_embed import generate_embedding
from vector_db.qdrant_client import (
    store_query_embedding,
    store_document_chunks,
    search_similar_chunks,
    COLLECTION_NAME,
    client
)
import uuid

# Dummy data for testing
TEST_QUERY = "What is Artificial Intelligence?"
TEST_DOC_ID = "test_doc.pdf"
TEST_CHUNKS = [
    "Artificial Intelligence (AI) is a branch of computer science...",
    "Machine Learning is a subset of AI that allows computers to learn...",
    "Deep Learning is a type of Machine Learning inspired by neural networks...",
]

@pytest.mark.order(1)
def test_generate_embedding():
    vector = generate_embedding(TEST_QUERY)
    assert isinstance(vector, list)
    assert len(vector) > 0
    print("Embedding generated:", vector[:5], "...")  # show first 5 values

@pytest.mark.order(2)
def test_store_query_embedding():
    vector = generate_embedding(TEST_QUERY)
    store_query_embedding(TEST_QUERY, vector, model="nomic-embed-text")
    
    # Verify query is in collection (basic check using REST API)
    results = search_similar_chunks(vector, top_k=1)
    assert results[0]["score"] > 0
    print("Query stored and verified:", results[0])

@pytest.mark.order(3)
def test_store_document_chunks():
    store_document_chunks(TEST_DOC_ID, TEST_CHUNKS, model="nomic-embed-text")
    
    # Verify chunks stored
    vector = generate_embedding(TEST_CHUNKS[0])
    results = search_similar_chunks(vector, top_k=3)
    assert len(results) > 0
    print("Chunks stored and verified:")
    for res in results:
        print(res["chunk_index"], res["content"][:50], "...")

@pytest.mark.order(4)
def test_search_similar_chunks():
    # Pick a query related to stored chunks
    query = "Explain Deep Learning"
    query_vector = generate_embedding(query)
    
    results = search_similar_chunks(query_vector, top_k=5)
    
    assert len(results) > 0
    print(f"Top {len(results)} results for query '{query}':")
    for res in results:
        print(f"Score: {res['score']:.3f}, Chunk: {res['content'][:80]}...")

