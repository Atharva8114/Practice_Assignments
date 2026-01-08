from fastapi import APIRouter, UploadFile, File
import os

from document_loader.text_loader import load_text_file
from document_loader.pdf_loader import load_pdf
from document_loader.chunker import chunk_text
from vector_db.qdrant_client import store_document_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = load_pdf(file_path)
    else:
        text = load_text_file(file_path)

    chunks = chunk_text(text)

    store_document_chunks(
        doc_id=file.filename,
        chunks=chunks,
        model="nomic-embed-text"
    )

    return {
        "document": file.filename,
        "chunks_stored": len(chunks)
    }
