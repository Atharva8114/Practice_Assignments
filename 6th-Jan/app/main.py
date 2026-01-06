from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="FastAPI Mongo CRUD")

app.include_router(router)
