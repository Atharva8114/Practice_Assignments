from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from routers import query, documents


app = FastAPI(title="Ollama Vector API")


app.include_router(query.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"message": "API is running"}

