from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from document_loader.text_loader import load_text_file
from document_loader.pdf_loader import load_pdf
from document_loader.chunker import chunk_text
from vector_db.qdrant_client import store_document_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)

        # Read file content
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Load text based on file type
        if file.filename.endswith(".pdf"):
            text = load_pdf(file_path)
        else:
            text = load_text_file(file_path)

        # Check if text was extracted
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No text content found in document")

        # Chunk the text
        chunks = chunk_text(text, chunk_size=500, overlap=100)
        
        # Filter out empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="No valid chunks created from document")

        # Store chunks in vector database
        store_document_chunks(
            doc_id=file.filename,
            chunks=chunks,
            model="nomic-embed-text"
        )

        # Clean up temp file
        os.remove(file_path)

        return {
            "document": file.filename,
            "chunks_stored": len(chunks),
            "total_characters": len(text),
            "sample_chunk": chunks[0][:200] + "..." if len(chunks[0]) > 200 else chunks[0]
        }
    
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))